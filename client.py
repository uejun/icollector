# -*- coding: utf-8 -*-
"""This module provides image search http request clients.

    抽象SearchClientと各APIプロバイダーに対応する具象SearchClientを提供する.
    モジュールロード時にconfig.ymlを読み込み, 各SearchClientのクラスプロパティが
    セットされる. 読み込みが失敗した場合プロセスは終了する.

    Bing reference:
    https://www.microsoft.com/cognitive-services/en-us/bing-image-search-api
    https://msdn.microsoft.com/en-us/library/dn760791.aspx

    Google reference:
    https://developers.google.com/custom-search/json-api/v1/reference/cse/list
"""
from __future__ import print_function
from abc import ABCMeta
#from abc import abstractclassmethod # needed when supports python3 only.
from abc import abstractmethod
import logging
import math
import sys
import typing
from typing import List

import requests
import yaml

from domain import ImageInfo


# 下記はMetaクラスをpython2と3の両方に対応させるため. Lambdaが3に対応したら不要.
class abstractclassmethod(classmethod):

    __isabstractmethod__ = True

    def __init__(self, callable):
        callable.__isabstractmethod__ = True
        super(abstractclassmethod, self).__init__(callable)


class AbstractSearchClient():
    """provide search func and converter func.

    """
    # python2 対応. python3ではmetaclass=ABCMeta.
    __metaclass__ = ABCMeta

    provider_id = 0  # 検索APIのプロバイダー識別用
    base_url = ""
    base_header = {}
    base_query = {}
    count_per_req = 0
    keyword_query_key = ''

    def search(self, keyword, total, queries={}, headers={}):
        """Search image by http get method.

            Args:
                keyword: search keyword string.
                query: dictionary of optional queries.
                header: dictionary of optional headers.
            Return:
                List of ImageInfo returned by search api provider.

        """
        queries.update(self.base_query)
        headers.update(self.base_header)

        queries[self.keyword_query_key] = keyword

        # return list of ImageInfo
        return self._schedule_search(total, queries, headers)

    def _schedule_search(self, total, queries, headers):
        results = []
        for step in range(self._calc_steps(total)):
            count = self._calc_count(total)
            offset = step * count

            self._set_paging(queries, offset, count)

            step_result = self._request(queries, headers)
            results.extend(step_result)
        return results

    def _request(self, queries, headers):
        resp = requests.get(self.base_url,
                            params=queries,
                            headers=headers)
        if resp.status_code != 200:
            resp.raise_for_status()
        if resp.headers.get('content-length') in (0, None):
            raise SearchRequestError("invalid content-length")
        return self._convert(resp.json())

    def _calc_steps(self, total):
        # python2に対応するためfloat()とint()を使用
        return int(math.ceil(float(total) / self.count_per_req))

    def _calc_count(self, total):
        return self.count_per_req if total > self.count_per_req else total

    @abstractclassmethod
    def parse_config(cls, data):
        # type: (dict) -> None
        pass

    @abstractmethod
    def _set_paging(self, queries, offset, count):
        pass

    @abstractmethod
    def _convert(self, resp):
        # type: (dict) -> List[ImageInfo]
        pass


class BingSearchClient(AbstractSearchClient):

    @classmethod
    def parse_config(cls, data):
        # type: (dict) -> None
        bing = data['Bing']
        cls.provider_id = bing["provider_id"]
        cls.base_url = bing["base_url"]
        cls.count_per_req = bing['count_per_req']
        cls.keyword_query_key = 'q'
        cls.base_header = {
            'Ocp-Apim-Subscription-Key': bing["subscription_keys"][0]}

    def _set_paging(self, queries, offset, count):
        queries['offset'] = offset
        queries['count'] = count

    def _convert(self, resp):
        # type: (dict) -> List[ImageInfo]
        image_info_list = []
        for item in resp['value']:
            size_str = item['contentSize']
            byte_size = int(size_str.replace(' B', ''))
            info = ImageInfo(provider_id=self.provider_id,
                             url=item['contentUrl'],
                             width=item['width'],
                             height=item['height'],
                             byte_size=byte_size)
            image_info_list.append(info)
        return image_info_list


class GoogleSearchClient(AbstractSearchClient):

    @classmethod
    def parse_config(cls, data):
        # type: (dict) -> None
        google = data['Google']
        cls.provider_id = google["provider_id"]
        cls.base_url = google['base_url']
        cls.count_per_req = google['count_per_req']
        cls.keyword_query_key = 'q'
        cls.base_query = {"key": google['api_key'],
                          "cx": google['engine_id'],
                          "searchType": google['search_type']}

    def _set_paging(self, queries, offset, count):
        queries['start'] = offset + 1
        queries['num'] = count

    def _convert(self, resp):
        # type: (dict) -> List[ImageInfo]
        image_info_list = []
        for item in resp['items']:
            info = ImageInfo(provider_id=self.provider_id,
                             url=item['link'],
                             width=item['image']['width'],
                             height=item['image']['height'],
                             byte_size=item['image']['byteSize'])
            image_info_list.append(info)

        return image_info_list


class SearchRequestError(Exception):
    pass


try:
    with open("config.yml", 'r') as f:
        data = yaml.load(f)
        BingSearchClient.parse_config(data)
        GoogleSearchClient.parse_config(data)
except Exception as e:
    logging.error(e)
    sys.exit(1)

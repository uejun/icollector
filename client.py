"""This module provides image search http request clients.

    モジュールロード時にconfig.ymlを読み込む.
    読み込みが失敗した場合プロセスは終了する.

    Bing reference:
    https://www.microsoft.com/cognitive-services/en-us/bing-image-search-api
    https://msdn.microsoft.com/en-us/library/dn760791.aspx

    Google reference:
    https://developers.google.com/custom-search/json-api/v1/reference/cse/list
"""
from abc import ABCMeta
from abc import abstractclassmethod
from abc import abstractmethod
import enum
import math
import sys
from typing import List

import requests
import yaml

from domain import ImageInfo


class PROVIDER_ID(enum.Enum):
    """検索APIのプロパイダー識別用Enum."""
    BING = 1
    GOOGLE = 2


class AbstractSearchClient(metaclass=ABCMeta):
    """provide search func and converter func.

    """
    base_url = ""
    base_header = {}
    base_query = {}
    count_per_req = 0

    def __init__(self):
        pass

    def search(self, keyword, total, queries={}, headers={}) -> List[ImageInfo]:
        """Search image by http get method.

            Args:
                keyword: search keyword string.
                query: dictionary of optional queries.
                header: dictionary of optional headers.
            Return:
                List of ImageInfo returned by search api provider.

        """
        # set keyword to queries
        merged_queries = self._add_queries(keyword, total, queries)
        merged_headers = self._add_headers(headers)

        steps = self._calc_steps(total)

        image_info_list = []
        for _ in range(steps):
            resp = requests.get(self.base_url,
                                params=merged_queries,
                                headers=merged_headers)

            if resp.status_code != 200:
                resp.raise_for_status()

            if resp.headers.get('content-length') in (0, None):
                raise SearchRequestError("invalid content-length")

            results = self._convert(resp.json())
            image_info_list.extend(results)

        return image_info_list

    def _calc_steps(self, total):
        return math.ceil(total / self.count_per_req)

    @abstractclassmethod
    def parse_config(cls, data: dict):
        pass

    @abstractmethod
    def _add_queries(self, keyword, total, queries):
        pass

    def _calc_count(self, total):
        return self.count_per_req if total > self.count_per_req else total

    @abstractmethod
    def _add_headers(self, headers):
        all_headers = {}
        all_headers.update(self.base_header)
        all_headers.update(headers)
        return all_headers

    @abstractmethod
    def _convert(self, resp: dict) -> List[ImageInfo]:
        pass


class BingSearchClient(AbstractSearchClient):
    @classmethod
    def parse_config(cls, data: dict):
        bing = data['Bing']
        cls.base_url = bing["base_url"]
        cls.count_per_req = bing['count_per_req']
        cls.base_header = {
            'Ocp-Apim-Subscription-Key': bing["subscription_keys"][0]}

    def _add_queries(self, keyword, total, queries):
        all_queries = {}
        all_queries.update(self.base_query)
        all_queries['q'] = keyword
        all_queries['count'] = self._calc_count(total)
        all_queries.update(queries)
        return all_queries
    
    def _add_headers(self, headers):
        return super(BingSearchClient, self)._add_headers(headers)

    def _convert(self, resp: dict) -> List[ImageInfo]:
        image_info_list = []
        for item in resp['value']:
            info = ImageInfo(provider_id=PROVIDER_ID.BING,
                             url=item['contentUrl'],
                             width=item['width'],
                             height=item['height'],
                             byte_size=item['contentSize'])
            image_info_list.append(info)

        return image_info_list


class GoogleSearchClient(AbstractSearchClient):
    @classmethod
    def parse_config(cls, data: dict):
        google = data['Google']
        cls.base_url = google['base_url']
        cls.count_per_req = google['count_per_req']
        cls.base_query = {"key": google['api_key'],
                          "cx": google['engine_id'],
                          "searchType": google['search_type']}

    def _add_queries(self, keyword, total, queries):
        all_queries = {}
        all_queries.update(self.base_query)
        all_queries['q'] = keyword
        all_queries['num'] = self._calc_count(total)
        all_queries.update(queries)
        return all_queries
    
    def _add_headers(self, headers):
        return super(GoogleSearchClient, self)._add_headers(headers)

    def _convert(self, resp: dict) -> List[ImageInfo]:
        image_info_list = []
        for item in resp['items']:
            info = ImageInfo(provider_id=PROVIDER_ID.GOOGLE,
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
    print(e)
    sys.exit(1)


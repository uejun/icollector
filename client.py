"""This module provides image search http request clients.


"""
from typing import List

import requests

from config import Config
from domain import ImageInfo


class SearchClient:
    """provide search func and converter func.

    """
    def __init__(self, config: Config):
        self.config = config
        self.converter = config.converter

    def search(self, query={}, header={}) -> List[ImageInfo]:
        """Search image by http get method.

            Args:
                query: dictionary of queries.
                header: dictionary of headers.
            Return:
                List of ImageInfo returned by search api provider.

        """
        query.update(self.config.base_query)
        header.update(self.config.base_header)
        resp = requests.get(self.config.base_url, params=query, headers=header)

        if resp.status_code != 200:
            resp.raise_for_status()

        if resp.headers.get('content-length') in (0, None):
            raise SearchRequestError("invalid content-length")

        image_info_list = self.converter.convert(resp.json())

        return image_info_list


class SearchRequestError(Exception):
    pass


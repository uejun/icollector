# -*- coding: utf-8 -*-
import typing
from typing import List

from client import BingSearchClient
from client import GoogleSearchClient
from domain import ImageInfo

bing_client = BingSearchClient()
google_client = GoogleSearchClient()


def search(keyword, count, bing_queries=None, google_queries=None):
    # type: (str, int, dict, dict) -> List[ImageInfo]
    """複数のAPIプロバイダーをハンドリングする.

        検索は各クライントに委譲する.
        ToDo: MapReduce的に並列分散処理する.

        Args:
            keyword: 検索キーワード.
            count: 各APIクライントの検索件数.
            bing_queries: dict of Bing optional queries.
            google_queries: dict of Google optional queries.
        Return:
            List of ImageInfo.

    """
    if bing_queries is None:
        bing_queries = {}

    if google_queries is None:
        google_queries = {}

    image_info_list = []

    bing_images = bing_client.search(keyword, count, queries=bing_queries)
    google_images = google_client.search(keyword, count, queries=google_queries)

    image_info_list.extend(bing_images)
    image_info_list.extend(google_images)

    return image_info_list

"""SearchClientに与えるConfigを提供するモジュール.

    モジュールロード時にconfig.ymlを読み込む.
    読み込みが失敗した場合プロセスは終了する.

"""
from abc import ABCMeta
from abc import abstractmethod
import sys

import yaml

from provider import ResponseConverter
from provider import BingResponseConverter
from provider import GoogleResponseConverter


class Config(metaclass=ABCMeta):
    base_url = ""
    base_header = {}
    base_query = {}

    def __init__(self):
        self.converter = self._create_converter()

    @abstractmethod
    def _create_converter(self) -> ResponseConverter:
        pass

    @classmethod
    def parse(cls, data: dict):
        pass


class BingConfig(Config):
    def __init__(self):
        super(BingConfig, self).__init__()

    def _create_converter(self) -> ResponseConverter:
        return BingResponseConverter()

    @classmethod
    def parse(cls, data: dict):
        bing = data['Bing']
        auth_header = bing["auth_header"]
        subscription_keys = bing["subscription_keys"]
        header = {auth_header: subscription_keys[0]}

        cls.base_url = bing["base_url"]
        cls.base_header = header


class GoogleConfig(Config):
    def __init__(self):
        super(GoogleConfig, self).__init__()

    def _create_converter(self) -> ResponseConverter:
        return GoogleResponseConverter()

    @classmethod
    def parse(cls, data: dict):
        google = data['Google']
        api_key = google['api_key']
        engine_id = google['engine_id']
        search_type = google['search_type']
        base_query = {"key": api_key,
                      "cx": engine_id,
                      "searchType": search_type}

        cls.base_url = google['base_url']
        cls.base_query = base_query


try:
    with open("config.yml", 'r') as f:
        data = yaml.load(f)
        BingConfig.parse(data)
        GoogleConfig.parse(data)
except Exception as e:
    print(e)
    sys.exit(1)


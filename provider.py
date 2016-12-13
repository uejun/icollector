from abc import ABCMeta
from abc import abstractmethod
import enum
from typing import List

from domain import ImageInfo


class PROVIDER_ID(enum.Enum):
    """検索APIのプロパイダー識別用Enum."""
    BING = 1
    GOOGLE = 2


class ResponseConverter(metaclass=ABCMeta):
    @abstractmethod
    def convert(self, resp: dict) -> List[ImageInfo]:
        pass


class BingResponseConverter(ResponseConverter):
    def __init__(self):
        pass

    def convert(self, resp: dict) -> List[ImageInfo]:
        image_info_list = []
        for item in resp['value']:
            info = ImageInfo(provider_id=PROVIDER_ID.BING,
                             url=item['contentUrl'],
                             width=item['width'],
                             height=item['height'],
                             byte_size=item['contentSize'])
            image_info_list.append(info)

        return image_info_list


class GoogleResponseConverter(ResponseConverter):
    def __init__(self):
        pass

    def convert(self, resp: dict) -> List[ImageInfo]:
        image_info_list = []
        for item in resp['items']:
            info = ImageInfo(provider_id=PROVIDER_ID.GOOGLE,
                             url=item['link'],
                             width=item['image']['width'],
                             height=item['image']['height'],
                             byte_size=item['image']['byteSize'])
            image_info_list.append(info)

        return image_info_list
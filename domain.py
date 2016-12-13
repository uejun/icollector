#!/usr/bin/env python
# -*- coding: utf-8 -*-


class ImageInfo:
    """Image情報保持クラス"""

    def __init__(self, provider_id, url, width, height, byte_size):
        self.provider_id = provider_id
        self.url = url
        self.width = width
        self.height = height
        self.byte_size = byte_size

    def __str__(self):
        image_str = """
        url:{}
        width:{}
        height:{}
        byteSize:{}
        """.format(self.url, self.width, self.height, self.byte_size)
        return image_str

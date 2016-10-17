#!/usr/bin/env python
# -*- coding: utf-8 -*-


class Image:
    """Image情報保持クラス"""

    def __init__(self, integratedId, url, width, height, contentSize):
        self.integratedId = integratedId
        self.url = url
        self.width = width
        self.height = height
        self.contentSize = contentSize

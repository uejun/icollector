"""This module provides domain model."""


class ImageInfo:
    """Image情報保持クラス.
    """

    def __init__(self, provider_id, url, width, height, byte_size):
        self.provider_id = provider_id
        self.url = url.replace('\n', '').replace(' ', '')
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

    def dump_LTSV(self):
        text = "provider_id:{}\t" \
               "url:{}\t" \
               "width:{}\t" \
               "height:{}\t" \
               "byte_size:{}".format(self.provider_id,
                                       self.url,
                                       self.width,
                                       self.height,
                                       self.byte_size)
        return text

    def to_dict(self):
        return self.__dict__

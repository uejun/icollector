import urllib2
import sys
import json
import BingImageClient
import GCSImageClient

from json import JSONEncoder


class MyEncoder(JSONEncoder):

    def default(self, o):
        return o.__dict__


def main():
    keyword = sys.argv[1]
    bingImgs = BingImageClient.find(keyword)
    GCSImgs = GCSImageClient.find(keyword)
    imgs = bingImgs + GCSImgs

    print(MyEncoder().encode(imgs))

if __name__ == "__main__":
    main()

#!/usr/bin/env python
# -*- coding: utf-8 -*-

import urllib2
import sys
import argparse
import json
import BingImageClient
import GCSImageClient

from json import JSONEncoder

DEFAULT_OFFSET = 0
DEFAULT_COUNT = 10
DEFAULT_MKT = 'ja-JP'

class MyEncoder(JSONEncoder):

    def default(self, o):
        return o.__dict__

def findImages(keyword, offset, count, mkt):

    # keyword = args.keyword

    # クライアントの数でcountを等分
    img_clients = [BingImageClient]
    count = count / len(img_clients)
    offset = offset / len(img_clients)
    mod = count % len(img_clients)

    # あまりの部分は取得件数を１増やす
    tmp_imgs = []
    for i, client in enumerate(img_clients):
        ccount = count
        oofset = offset
        if (mod > 0):
            ccount = count + 1
            ooffset = offset + 1
            mod -= 1

        tmp_imgs.append(client.find(keyword, offset, count, mkt))

    # オフセット・カウントがずれないように取得した画像を各クライアント順番に並び替え
    # ex. tmp_imgs = AAABBCC (A, B, C: A, B, CのAPIから取得した画像)
    #     imgs = ABCABCA
    imgs = []
    for i in range(count + 1):
        for i in range(len(img_clients)):
            if (len(tmp_imgs[i]) == 0):
                continue
            imgs.append(tmp_imgs[i].pop())

    print(MyEncoder().encode(imgs))
    return MyEncoder().encode(imgs)

def main():
    """cli用画像検索エントリーポイント"""
    parser = argparse.ArgumentParser(description='Search Image from external api')
    parser.add_argument('keyword', type=str, help='search keyword')
    parser.add_argument('--offset', type=int, default=DEFAULT_OFFSET)
    parser.add_argument('--count', type=int, default=DEFAULT_COUNT)
    parser.add_argument('--mkt', type=str, default=DEFAULT_MKT)
    args = parser.parse_args()
    return findImages(args.keyword, args.offset, args.count, args.mkt)

def lambda_handler(event, context):
    """lambda用検画像検索エントリーポイント"""
    keyword = str(event['keyword'])
    offset = int(event['offset']) if('offset' in event) else DEFAULT_OFFSET
    count = int(event['count']) if('count' in event) else DEFAULT_COUNT
    mkt = str(event['mkt']) if('mkt' in event) else DEFAULT_MKT

    return findImages(keyword, offset, count, mkt)

if __name__ == "__main__":
    # main()
    lambda_handler({'keyword': 'face', 'offset': 1, 'count': 2, 'mkt': 'ja-JP'}, {})

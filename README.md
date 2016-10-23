# PPAP

複数の画像取得APIラッパー

## Using API
* [Bing Search API](https://www.microsoft.com/cognitive-services)
* [Google Custom Search API](https://developers.google.com/custom-search/json-api/v1/using_rest?hl=ja)
* ~~[Flickr API](https://www.flickr.com/services/api/flickr.photos.search.html)~~
* ~~[Instagram](https://www.instagram.com/developer/endpoints/media/)~~

## Usage

```
python main.py -h
usage: main.py [-h] [--offset OFFSET] [--count COUNT] [--mkt MKT] SEARCH_WORD

Search Image from external api

positional arguments:
  keyword          search keyword

optional arguments:
  -h, --help       show this help message and exit
  --offset OFFSET
  --count COUNT
  --mkt MKT
$ python main.py face --offset 3 --count 10 --mkt ja-JP
[{"url": "https://www.bing.com/cr?IG=0B65A8CA221A445E8FABF43F2DBE904A&CID=0160AB6957E868AF1B3CA2DE56FA69BA&rd=1&h=OtaxxPAfkwavqKL0wQoWgF2SJdGQZ3ZJf6NRdN7YkbI&v=1&r=https%3a%2f%2fm2hair.files.wordpress.com%2f2014%2f07%2flong-square-face.jpg&p=DevEx,5062.1", "width": 550, "contentSize": "62114 B", "integratedId": 1, "height": 550}, {"url": "http://www.bing.com/cr?IG=0B65A8CA221A445E8FABF43F2DBE904A&CID=0160AB6957E868AF1B3CA2DE56FA69BA&rd=1&h=E1ClITPvYYp6u0i-Fi-e0DHlnXw8UhQsSJMYG7PImQo&v=1&r=http%3a%2f%2fupload.wikimedia.org%2fwikipedia%2fcommons%2fd%2fde%2fTom-Limoncelli-face-hires.jpg&p=DevEx,5056.1", "width": 2094, "contentSize": "1194273 B", "integratedId": 1, "height": 2518}, {"url": "http://www.bing.com/cr?IG=0B65A8CA221A445E8FABF43F2DBE904A&CID=0160AB6957E868AF1B3CA2DE56FA69BA&rd=1&h=U3DN2YUp5TMwU7UFOm7FPwlPzp35HjdGGylIcAVfPv0&v=1&r=http%3a%2f%2fimg.mota.ru%2fupload%2fwallpapers%2f2011%2f06%2f01%2f09%2f05%2f25877%2fmota_ru_1060110-1920x1080.jpg&p=DevEx,5050.1", "width": 1920, "contentSize": "112406 B", "integratedId": 1, "height": 1080}, {"url": "https://www.bing.com/cr?IG=0B65A8CA221A445E8FABF43F2DBE904A&CID=0160AB6957E868AF1B3CA2DE56FA69BA&rd=1&h=QQEL6938RCrjUkfMESjHoM0uw1p9B8GQwE2bIDw-cnw&v=1&r=https%3a%2f%2fwww.dermisa.com%2fwordpress%2fwp-content%2fuploads%2f2012%2f03%2fWomanTouchFace.png&p=DevEx,5044.1", "width": 1408, "contentSize": "2224233 B", "integratedId": 1, "height": 1636}, {"url": "http://www.bing.com/cr?IG=0B65A8CA221A445E8FABF43F2DBE904A&CID=0160AB6957E868AF1B3CA2DE56FA69BA&rd=1&h=yPI8XUO6JI0Y_0U1BAZqfrkO--1_mEyL_AB-P0VAbxU&v=1&r=http%3a%2f%2fko-te.com%2fen%2fwp-content%2fuploads%2f2013%2f03%2fSkincare-Natural-face-lift-mask.jpg&p=DevEx,5038.1", "width": 1280, "contentSize": "353627 B", "integratedId": 1, "height": 828}, {"url": "http://www.bing.com/cr?IG=0B65A8CA221A445E8FABF43F2DBE904A&CID=0160AB6957E868AF1B3CA2DE56FA69BA&rd=1&h=3If0M1JT0IHK3TxxmF8R3uSWmy9gXsrf5WNgsf3rfCw&v=1&r=http%3a%2f%2fefdreams.com%2fdata_images%2fdreams%2fface%2fface-03.jpg&p=DevEx,5032.1", "width": 864, "contentSize": "111542 B", "integratedId": 1, "height": 960}, {"url": "http://www.bing.com/cr?IG=0B65A8CA221A445E8FABF43F2DBE904A&CID=0160AB6957E868AF1B3CA2DE56FA69BA&rd=1&h=96QvMooThgyRhJeHTXwfcsKzMlmpORnzIghO3AK8Jkc&v=1&r=http%3a%2f%2fwww.incrediblethings.com%2fwp-content%2fuploads%2fresized%2f72c89ead877fcf7059ca23df2aebcb2a_1_c_595x0.jpg&p=DevEx,5026.1", "width": 595, "contentSize": "192220 B", "integratedId": 1, "height": 683}, {"url": "http://www.bing.com/cr?IG=0B65A8CA221A445E8FABF43F2DBE904A&CID=0160AB6957E868AF1B3CA2DE56FA69BA&rd=1&h=Hkp8r6kzRtEoMwl9fTqjct7dWiI30skzKWX04w7Mc0k&v=1&r=http%3a%2f%2fwww.sephora.com%2fcontentimages%2fcategories%2fmakeup%2fCONTOURING%2f030515%2fanimations%2fround%2fround_01_before.jpg&p=DevEx,5020.1", "width": 338, "contentSize": "34647 B", "integratedId": 1, "height": 396}, {"url": "http://www.bing.com/cr?IG=0B65A8CA221A445E8FABF43F2DBE904A&CID=0160AB6957E868AF1B3CA2DE56FA69BA&rd=1&h=0R5AOuUjaxdqdw3wRCJImp8UWsTJIErNMf0wzBYATg4&v=1&r=http%3a%2f%2fyummymummybeauty.com%2fwp-content%2fuploads%2f2012%2f01%2fbeauty-face1.jpg&p=DevEx,5014.1", "width": 1414, "contentSize": "1906157 B", "integratedId": 1, "height": 2121}, {"url": "http://www.bing.com/cr?IG=0B65A8CA221A445E8FABF43F2DBE904A&CID=0160AB6957E868AF1B3CA2DE56FA69BA&rd=1&h=f_u_p_hY_tBTw5LB3iFp_n-fcnKg_PwEkELGAMhnc0U&v=1&r=http%3a%2f%2fdreamatico.com%2fdata_images%2fface%2fface-3.jpg&p=DevEx,5008.1", "width": 1200, "contentSize": "111836 B", "integratedId": 1, "height": 1200}]

```

## TODO
* API Gateway
* メタ情報の取得
* Bing以外の画像APIの対応

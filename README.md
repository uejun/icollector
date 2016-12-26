<p align="center">
    <img src="https://www.dropbox.com/s/nmo71xslwn3slm5/icollector-oruche.png?dl=1" alt="icollector!"/>
</p>

# icollector

Image Search API Wrapper

## Using API
* [Bing Search API](https://www.microsoft.com/cognitive-services)
* [Google Custom Search API](https://developers.google.com/custom-search/json-api/v1/using_rest?hl=ja)
* ~~[Flickr API](https://www.flickr.com/services/api/flickr.photos.search.html)~~
* ~~[Instagram](https://www.instagram.com/developer/endpoints/media/)~~

## Usage Overview

icollector has 6 way to use (zappa, cli, docker(web), web, aws_lambda, package).  

### First Settings

1. You need to copy a configuration file and edit it.  

```
$ cp config_sample.yml config.yml

# Edit them.
$ vi config.yml
```

2. Install packages.  
If you want to use zappa, docker or aws_lambda, you need to use python2.7 and virtualenv.

```
$ pip install -r requirement.txt
```

### The Way1: Use Zappa

Firstly, edit zappa_settings.json for your aws environment configuration.  
And run.

```
$ cp zappa_settings_sample.json zappa_settings.json
# Edit this.
$ vi zappa_settings.json 
$ zappa deploy dev
```
Done! How Cool is that?

Then, web api gets running.

```
    HealthCheck
        
        [GET] http://localhost:9000/ping

    Search.

        [GET] http://localhost:9000/search?keyword=anything&count=10

```

If you want to specify other optional queries, you add them with provider's annotation (e.g. bing_) like below.  
See 
- [Bing image search api reference](https://msdn.microsoft.com/en-us/library/dn760791.aspx)
- [Google custom search api refrence](https://developers.google.com/custom-search/json-api/v1/reference/cse/list)

```
?bing_mkt=ja-JP&google_imgSize=large

```

This returns JSON response.

```
# Example.
$ python icollector.py web
 * Running on http://127.0.0.1:5000/ (Press CTRL+C to quit)
  
$ curl http://127.0.0.1:5000/search?keyword=banana&count=1
[{"provider_id": 1, "height": 679, "byte_size": "46802 B", "url": "http://www.bing.com/cr?IG=7BDAA3D220564349A71398666C320946&CID=0ACF10B1D6806FD83C1D195AD7926E9F&rd=1&h=JE9jlpJMuqdCiBHIIKUMm7ffA-AuWi-d3g7FnYFHMoo&v=1&r=http%3a%2f%2fwww.hangthebankers.com%2fwp-content%2fuploads%2f2012%2f08%2fBanana-1024x679.jpg&p=DevEx,5008.1", "width": 1024}, {"provider_id": 2, "height": 2000, "byte_size": 1559778, "url": "https://upload.wikimedia.org/wikipedia/commons/4/44/Bananas_white_background_DS.jpg", "width": 3000}]

```

### The Way2: Use Cli Subcommand

```
$ python icollector.py cli -h
Usage: icollector.py cli [OPTIONS] KEYWORD

  Run cli search.

  KEYWORD(positional arg): word which you want to search.

  You can specify --bing and --google option like below.

  --bing "mkt=ja-JP, color=Gray" --google "safe=high, imgType=news"

Options:
  -c, --count INTEGER  Count by each provider.
  -b, --bing TEXT      Bing search optional queries
  -g, --google TEXT    Google search optional queries
  -o, --output TEXT    Output file name
  -h, --help           Show this message and exit.
 ```
This results' format is LTSV.
'-c' option specifies the count of each provider requests.
So Total counts are the multiplied number of providers (i.e so far 2).

Example.
```
$ python icollector.py cli banana -c 1
provider_id:1	url:http://www.bing.com/cr?IG=C0019F0B674E4A9ABD344FA6EDB2B279&CID=1E206F3198246F3A3DFD66DA99366E71&rd=1&h=JE9jlpJMuqdCiBHIIKUMm7ffA-AuWi-d3g7FnYFHMoo&v=1&r=http%3a%2f%2fwww.hangthebankers.com%2fwp-content%2fuploads%2f2012%2f08%2fBanana-1024x679.jpg&p=DevEx,5008.1	width:1024	height:679	byte_size:46802 B

provider_id:2	url:https://upload.wikimedia.org/wikipedia/commons/4/44/Bananas_white_background_DS.jpg	width:3000	height:2000	byte_size:1559778
```

#### Confirm help

```
$ python icollector.py --help

Usage: icollector.py [OPTIONS] COMMAND [ARGS]...

Options:
  --help  Show this message and exit.

Commands:
  cli  cli entry point.
```

### The Way3: Use Docker

Usage of rest api is same as zappa mode above.  

```
$ docker build -t icollector .
$ docker run -it --rm -p 5000:5000 icollector
```

### The Way4: Use Web api without docker.

You can launch wab api without docker.   

```
$ export FLASK_APP=inteface.py
$ flask run --host=0.0.0.0
#Or  
$ python -m interface.py --host=0.0.0.0
```
Usage of rest api is same as docker mode above.  


### The Way5: Use AWS Lambda manually.
Specify "aws_lambda" in interface.py as lambda function.
Their query keys are same as docker mode above.

### The Way6: Use as python package.

```
$ git submodule add https://github.com/Oruche/icollector.git
```
then,  

```
import icollector

resp = icollector.search.search(keyword, count, bing_queries, google_queries)
```



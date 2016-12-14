"""This module provides search application interface.

    Provided Interface
        - CLI
        - AWS Lambda Function
        - Web API
"""
import json

import click

from search import search
import util

DEFAULT_COUNT = 10


@click.group()
def api():
    pass


CONTEXT_SETTINGS = dict(help_option_names=['-h', '--help'])


@api.command(context_settings=CONTEXT_SETTINGS)
@click.argument('keyword')
@click.option('--count', '-c', default=DEFAULT_COUNT, type=int, help='Count by each provider.')
@click.option('--bing', '-b', default='', help='Bing search optional queries')
@click.option('--google', '-g', default='', help='Google search optional queries')
@click.option('--output', '-o', default='stdoutput', help='Output file name')
def cli(keyword, count, bing, google, output):
    """Run cli search.

        KEYWORD(positional arg): word which you want to search.

        You can specify --bing and --google option like below.

        --bing "mkt=ja-JP, color=Gray"
        --google "safe=high, imgType=news"

    """
    # convert to dict of queries.
    bing_optional_queries = util.parse_str_queries(bing)
    google_optional_queries = util.parse_str_queries(google)

    results = search(keyword,
                     count,
                     bing_optional_queries,
                     google_optional_queries)

    if output == 'stdoutput':
        for image_info in results:
            print(image_info.dump_LTSV())
    else:
        with open(output, 'w') as f:
            for image_info in results:
                f.write(image_info.dump_LTSV())


def aws_lambda(event, context):
    """Aws lambda entry point."""
    keyword = str(event['keyword'])
    count = int(event['count']) if('count' in event) else DEFAULT_COUNT

    bing_optional_queries = util.extract(event, 'bing_')
    google_optional_queries = util.extract(event, 'google_')

    results = search(keyword,
                     count,
                     bing_optional_queries,
                     google_optional_queries)
    return results


@api.command(context_settings=CONTEXT_SETTINGS)
def web():
    """Launch web search api.

        This allows you to search by HTTP like below.

        [GET] http://localhost:5000/search?keyword=anything&count=10

        If you want to specify other optional queries,
        you add them with provider's annotation (e.g. bing_) like below.

        ?bing_mkt=ja-JP&google_imgSize=large

    """
    from flask import Flask
    from flask import request
    from flask import Response
    app = Flask(__name__)

    @app.route("/search")
    def handler():
        keyword = str(request.args.get('keyword'))
        if 'count' in request.args:
            count = int(request.args.get('count'))
        else:
            count = DEFAULT_COUNT

        bing_optional_queries = util.extract(request.args, 'bing_')
        google_optional_queries = util.extract(request.args, 'google_')

        infos = search(keyword,
                       count,
                       bing_optional_queries,
                       google_optional_queries)

        infos = [info.to_dict() for info in infos]
        for info in infos:
            print(info)
        return Response(json.dumps(infos), mimetype='application/json')

    app.run()




from client import BingSearchClient
from client import GoogleSearchClient

bing_client = BingSearchClient()
google_client = GoogleSearchClient()


def search(keyword, total, bing_queries={}, google_queries={}):

    images = []

    bing_images = bing_client.search(keyword, total, queries=bing_queries)
    google_imaes = google_client.search(keyword, total, queries=google_queries)

    images.extend(bing_images)
    images.extend(google_imaes)

    return images


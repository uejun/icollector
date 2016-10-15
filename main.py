import urllib2, sys
import BingImageClient

def main():
  imgs = BingImageClient.find('hoge')
  for img in imgs:
      print(str(img))
  # term = sys.argv[1]
  # location = sys.argv[2]
  # params = search_params(term, location)
  # response = get_restaurants(params)
  # restaurants_info = response["businesses"]
  # restaurant_names = []
  # for restaurant_info in restaurants_info:
  #   restaurant_name = restaurant_info["name"]
  #   print restaurant_name
  #
if __name__ == "__main__":
  main()

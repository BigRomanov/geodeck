# Readability API Wrapper

import urllib
from bs4 import BeautifulSoup
from readability import ParserClient
from bson.json_util import dumps
import utils

PARSER_TOKEN=""

def testSoup():
  html = urllib.urlopen(source).read()
  soup = BeautifulSoup(html)
  texts = soup.findAll(text=True)

  with open('%s/soup.txt' % OUTPUT_DIR, 'w', encoding="utf-8") as fp:
  	fp.write(texts) 

# TEST MAIN
if __name__ == "__main__":
  OUTPUT_DIR = "output"


  # Sample sources
  #source = "http://skift.com/2015/12/28/landmark-new-york-city-hotels-pledge-to-cut-greenhouse-gas-emissions/"
  #source = "http://www.aluxurytravelblog.com/2016/01/03/4-of-the-most-romantic-places-to-spend-valentines-day-in-central-america/"
  source = "http://www.vagrantsoftheworld.com/things-to-do-in-bulgaria/"

  parser_client = ParserClient(token=PARSER_TOKEN)
  parser_response = parser_client.get_article(source)
  article = parser_response.json()

  with open('%s/readability.json' % OUTPUT_DIR, 'w', encoding="utf-8") as fp:
      fp.write(dumps(article))


  print(article['title'])
  print(article['content'])

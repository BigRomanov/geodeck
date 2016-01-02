# Readability API Wrapper

from readability import ParserClient
from bson.json_util import dumps
import utils

PARSER_TOKEN=""

# TEST MAIN
if __name__ == "__main__":
  OUTPUT_DIR = "output"

  source = "http://skift.com/2015/12/28/landmark-new-york-city-hotels-pledge-to-cut-greenhouse-gas-emissions/"

  parser_client = ParserClient(token=PARSER_TOKEN)
  parser_response = parser_client.get_article(source)
  article = parser_response.json()

  with open('%s/readability.json' % OUTPUT_DIR, 'w', encoding="utf-8") as fp:
      fp.write(dumps(article))


  print(article['title'])
  print(article['content'])

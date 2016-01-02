# Readability API Wrapper
import readability
from readability import ParserClient
import utils

PARSER_TOKEN="69277572f6b7c2842f599c02912ab989f3693eae"

# TEST MAIN
if __name__ == "__main__":
  OUTPUT_DIR = "output"

  source = "http://skift.com/2015/12/28/landmark-new-york-city-hotels-pledge-to-cut-greenhouse-gas-emissions/"

  parser_client = ParserClient(PARSER_TOKEN)
  parser_response = parser_client.get_article(source)
  article = parser_response.json()

  with open('%s/readability.json' % OUTPUT_DIR, 'w', encoding="utf-8") as fp:
      fp.write(dumps(article))


  print(article['title'])
  print(article['content'])

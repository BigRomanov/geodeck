# Lateral text extarctor

import requests
from bson.json_util import dumps

KEY="1394a79363bb7622f9d99478731b645b"

API_BASE="https://api.lateral.io/"
OUTPUT_DIR = "output"


# TEST MAIN
if __name__ == "__main__":

	#source = "http://skift.com/2015/12/28/landmark-new-york-city-hotels-pledge-to-cut-greenhouse-gas-emissions/"
	#source = "http://www.aluxurytravelblog.com/2016/01/03/4-of-the-most-romantic-places-to-spend-valentines-day-in-central-america/"
	#source = "http://www.vagrantsoftheworld.com/things-to-do-in-bulgaria/"
	source = "http://www.bbc.com/travel/story/20150213-where-las-vegas-meets-pyongyang"

	url = "https://document-parser-api.lateral.io/"

	querystring = {"url":"%s" % source}

	headers = {
	  'subscription-key': KEY,
	  'content-type': "application/json"
	  }

	response = requests.request("GET", url, headers=headers, params=querystring)

	print(response)

	with open('%s/lateral.json' % OUTPUT_DIR, 'w', encoding="utf-8") as fp:
	  fp.write(dumps(response))


	print(response.text)
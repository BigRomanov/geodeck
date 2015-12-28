import sys
import json

if __name__ == "__main__":

  if len(sys.argv) != 2:
    print ("Invalid parameters")
    exit(1)


  filename = sys.argv[1]
  print ("Engine running on file %s" % filename)

  # Initialize mongodb connection and database
  #client = MongoClient()
  #db = client.geodeck
  #geonames = db.geonames

  words = []
  json_data=open(filename).read()
  data = json.loads(json_data)

  with open("webster_words.json", "w", encoding="utf-8") as outfile:
    outfile.write(json.dumps(list(data.keys())))

  print("DONE!!!")
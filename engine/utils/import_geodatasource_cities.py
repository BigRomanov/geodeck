import sys
import pymongo
import re
from itertools import islice

from pymongo import MongoClient

if __name__ == "__main__":

  if len(sys.argv) != 2:
    print ("Invalid parameters")
    exit(1)


  filename = sys.argv[1]
  print ("Engine running on file %s" % filename)

  # Initialize mongodb connection and database
  client = MongoClient()
  db = client.geodeck
  c = db.geodatasource_cities

  # Read full data file one by one and insert them into database
  with open(filename) as infile:
    for line in islice(infile, 1, None):
        location = line.split('\t')
        doc = {"name": str(location[1].strip()), "fips": location[0]}
        loc_id = c.insert_one(doc) .inserted_id      

  print("DONE!!!")

  


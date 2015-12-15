import sys
import pymongo
import re

from pymongo import MongoClient

# Build a geonames location from a geonames text file line
# The main 'geoname' table has the following fields :
# ---------------------------------------------------
# geonameid         : integer id of record in geonames database
# name              : name of geographical point (utf8) varchar(200)
# asciiname         : name of geographical point in plain ascii characters, varchar(200)
# alternatenames    : alternatenames, comma separated, ascii names automatically transliterated, convenience attribute from alternatename table, varchar(10000)
# latitude          : latitude in decimal degrees (wgs84)
# longitude         : longitude in decimal degrees (wgs84)
# feature class     : see http://www.geonames.org/export/codes.html, char(1)
# feature code      : see http://www.geonames.org/export/codes.html, varchar(10)
# country code      : ISO-3166 2-letter country code, 2 characters
# cc2               : alternate country codes, comma separated, ISO-3166 2-letter country code, 200 characters
# admin1 code       : fipscode (subject to change to iso code), see exceptions below, see file admin1Codes.txt for display names of this code; varchar(20)
# admin2 code       : code for the second administrative division, a county in the US, see file admin2Codes.txt; varchar(80) 
# admin3 code       : code for third level administrative division, varchar(20)
# admin4 code       : code for fourth level administrative division, varchar(20)
# population        : bigint (8 byte int) 
# elevation         : in meters, integer
# dem               : digital elevation model, srtm3 or gtopo30, average elevation of 3''x3'' (ca 90mx90m) or 30''x30'' (ca 900mx900m) area in meters, integer. srtm processed by cgiar/ciat.
# timezone          : the timezone id (see file timeZone.txt) varchar(40)
# modification date : date of last modification in yyyy-MM-dd format

def buildLocation(line):
  fields = line.split("\t")
  location = {
   "0" : fields[0], 
   "1" : fields[1], 
   "2" : fields[2], 
   "3" : fields[3], 
   "4" : fields[4], 
   "5" : fields[5], 
   "6" : fields[6], 
   "7" : fields[7], 
   "8" : fields[8], 
   "9" : fields[9], 
   "10" : fields[10], 
   "11" : fields[11], 
   "12" : fields[12], 
   "13" : fields[13], 
   "14" : fields[14], 
   "15" : fields[15], 
   "16" : fields[16], 
   "17" : fields[17], 
   "18" : fields[18], 
  }

  return location
  


if __name__ == "__main__":

  if len(sys.argv) != 2:
    print ("Invalid parameters")
    exit(1)


  filename = sys.argv[1]
  print ("Engine running on file %s" % filename)

  # Initialize mongodb connection and database
  client = MongoClient()
  db = client.geodeck
  geonames = db.geonames

  # Read full data file one by one and insert them into database
  with open(filename) as infile:
    for line in infile:
        location = buildLocation(line)
        loc_id = geonames.insert_one(location).inserted_id      
        print(loc_id)

  


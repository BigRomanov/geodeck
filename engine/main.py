######
# Python 3 version
# Main python file for tokenizing and analyzing tokes retrieved from a file supplied as a parameter

# Library imports
import sys
import nltk, re, pprint
import enchant
import pymongo
import operator
import json
from bson.json_util import dumps

import dpath

# Geodeck imports
import utils
from timer import Timer

# Partial imports
from collections import OrderedDict
from nltk.tokenize import sent_tokenize
from pymongo import MongoClient

OUTPUT_DIR = "output"

#Globals
g_english_words_webster = []
g_monogoClient = None
g_geonames = None


# Naive algorithms
def naive_extractEntities(text):
  # Naive approach
  entities = []
  for line in text:
    for word in line.split():
      if word[0].isupper():
        entities.append(word)
  return entities

def getTokensFromText(text):
  
  tokens = nltk.word_tokenize(text)  
  # Token filtering
  #tokens = text.split()

  # First level, strip webster words
  tokens = [tok.strip().strip(":,;.!@#$%^&*()") for tok in text.split() if tok[0].isupper() and not (tok.upper() in g_english_words_webster)]

  # Second level, filter with enchant
  tokens = [tok for tok in tokens if not g_enchantDict.check(tok.lower())]

  return tokens

def getSentences(text):
  # Split by sentences
  sentences = sent_tokenize(text)
  utils.writeListToFile("%s/sentences.txt" % OUTPUT_DIR, sentences)
  return sentences

def getSequences(sentence):
  # TODO: Improve this regex, or replace with code, to handle cases like: 
  # Grand Cathedral of Lalala
  return re.findall('([A-Z][a-z]+(?=\s[A-Z]*)(?:\s[A-Z][a-z]+)+)', sentence)

# NLTK
def nltk_extractEntities(text):
  tokens = nltk.word_tokenize(text)  
  return tokens

def checkLocation(token):
  pass

# All initialization only done ONCE
def init():
  global g_english_words_webster
  global g_monogoClient
  global g_db
  global g_enchantDict
  global g_geodatasource_cities
  global g_geodatasource_countries

  # Initialize MongoDB connection
  g_monogoClient = MongoClient()
  g_db = g_monogoClient.geodeck

  # TODO: Move all db initizlisations to one place
  #g_geonames.create_index([('1', pymongo.ASCENDING)])

  # Initialize enchant dictionary
  g_enchantDict = enchant.Dict("en_US")

  # Initialize set of english words
  
  with open('data/webster_words.json') as data_file:    
    file_data = json.load(data_file)
    g_english_words_webster = set(list(file_data))
    print("Webster dictionary initialized:" + str(len(g_english_words_webster)))

def resolve_geodatasource(db, ta, token):
    #Resolve using geodatasource 
  res = g_db.g_geodatasource_countries.find({'name': re.compile("^"+token[0]+"$", re.IGNORECASE) } )
  if (res.count() > 0):
    utils.addMetadata(ta, ["geodatasource", "precise"], "country", list(res))
  else:
    res = g_db.g_geodatasource_countries.find({'name': re.compile(".*"+token[0]+".*", re.IGNORECASE) } )
    if (res.count() > 0):
      utils.addMetadata(ta, ["geodatasource", "contains"], "country", list(res))


  res = g_db.g_geodatasource_cities.find({'name': re.compile("^"+token[0]+"$", re.IGNORECASE) } )
  if (res.count() > 0):
    utils.addMetadata(ta, ["geodatasource", "precise"], "city", list(res))
  else:
    res = g_db.g_geodatasource_cities.find({'name': re.compile(".*"+token[0]+".*", re.IGNORECASE) } )
    if (res.count() > 0):
      utils.addMetadata(ta, ["geodatasource", "contains"], "city", list(res))


def resolve_geonames(db, ta):
  # TODO: Verify ta is valid, has token, meta etc...
  token = ta["token"]
  print("Geonames::resolve: %s" % token)
  with Timer() as t:
    res = db.geonames.find({'1': re.compile("^"+token+"$", re.IGNORECASE) } )
    if res.count() > 0:
      utils.addMetadata(ta, [], "geonames", list(res))
    else:
      res = db.geonames.find({'1': re.compile(".*"+token+".*", re.IGNORECASE) } )
      if res.count() > 0:
        utils.addMetadata(ta, [], "geonames", list(res))
  print("Geonames, resolved: %s in %s" % (token, t.secs))
    

# MAIN
if __name__ == "__main__":

  if len(sys.argv) != 2:
    print ("Invalid parameters")
    exit(1)

  # Initialization
  filename = sys.argv[1]
  print ("Engine running on file %s" % filename)

  init()

  # Read the text (from file this time)
  text = utils.readTextFromFile(filename)

  # Tokenize into sentences
  sentences = getSentences(text)

  # Create dictionary which will hold the analysis result
  result = {"filename" : filename}
  sentence_results = []
  allTokens = []

  # Analyze each centence separately
  for  idx, sentence in enumerate(sentences):
    # Initialize metadata dictionary which will hold the result of the analysis
    meta = {"sentence" : sentence, "idx" : idx}
    sequences = getSequences(sentence)

    # Remove the sequences we have found (TODO: optimize this)

    for sequence in sequences:
      sentence = sentence.replace(sequence, "")

    tokens = getTokensFromText(sentence)

    tokens = sequences + tokens
    meta["tokens"] = tokens
    allTokens = allTokens + tokens

    sentence_results.append(meta)

  result["sentences"] = sentence_results

  # Measure token frequency
  token_freq=nltk.FreqDist(allTokens)
  sorted_tokens = OrderedDict(sorted(token_freq.items(), key=lambda t: t[1]))



  token_analysis = []

  for token in sorted_tokens.items():
    # Create a dictionary for analyzed token
    ta = {"token" : token[0], "freq" : token[1], "weight" : token[1] / len(sorted_tokens), "meta" : {}}
    
    # Resolvers
    # ######################################################
    resolve_geonames(g_db, ta)
    #resolve_geodatasource(g_db, ta, token)

    # ######################################################

    # Check in which senteces appears (TODO)

    # Check if a names of a city or country


    token_analysis.append(ta)
  
  result["tokens"] = token_analysis

  with open('%s/result.json' % OUTPUT_DIR, 'w', encoding="utf-8") as fp:
    fp.write(dumps(result))

  print("Analysis complete")
  
  

  

  
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

# Geodeck imports
import utils

# Partial imports
from collections import OrderedDict
from nltk.tokenize import sent_tokenize
from pymongo import MongoClient

OUTPUT_DIR = "output"

#Globals
g_english_words_webster = []
g_monogoClient = None
g_geonamesDB = None


# Naive algorithms
def naive_extractEntities(text):
  # Naive approach
  entities = []
  for line in text:
    for word in line.split():
      if word[0].isupper():
        entities.append(word)
  return entities

def getTokensFromFile(filename):
  text = utils.readTextFromFile(filename)

  entities = nltk_extractEntities(text)

  utils.writeListToFile('%s\\entities.txt' % OUTPUT_DIR, entities)

  # Read the text
  text = utils.readTextFromFile(filename)

  

  # Get english dictionary from the enchant file
  d = enchant.Dict("en_US")

  print("Dictionary tests")
  print(d.check("Amsterdam"))

  # Token filtering
  tokens = text.split()

  print("Start from %s tokens" % str(len(tokens)))

  # First level, strip webster words
  tokens = [tok.strip().strip(":,;.!@#$%^&*()") for tok in text.split() if tok[0].isupper() and not (tok.upper() in g_english_words_webster)]

  print("%s tokens, after first filter" % str(len(tokens)))

  # Second level, filter with enchant
  tokens = [tok for tok in tokens if not d.check(tok.lower())]

  print("%s tokens, after second filter" % str(len(tokens)))
  
  utils.writeListToFile('%s\\tokens.txt' % OUTPUT_DIR, tokens)

  return tokens

def getSentences(text):
  # Split by sentences
  sentences = sent_tokenize(text)
  utils.writeListToFile("%s\\sentences.txt" % OUTPUT_DIR, sentences)
  return sentences

def getSequences(sentence):
  # ([A-Z][a-z]+(?=\s[A-Z])(?:\s[A-Z][a-z]+)+)
  return re.findall('([A-Z][a-z]+(?=\s[A-Z])(?:\s[A-Z][a-z]+)+)', sentence)



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
  global g_geonamesDB

  g_monogoClient = MongoClient()
  db = g_monogoClient.geodeck
  g_geonamesDB = db.geonames

  # Initialize set of english words
  with open('data\\webster_words.json') as data_file:    
    file_data = json.load(data_file)
    g_english_words_webster = set(list(file_data))
    print("Webster dictionary initialized:" + str(len(g_english_words_webster)))

  
# MAIN
if __name__ == "__main__":

  if len(sys.argv) != 2:
    print ("Invalid parameters")
    exit(1)

  # Initialization
  filename = sys.argv[1]
  print ("Engine running on file %s" % filename)

  init()

  text = utils.readTextFromFile(filename)

  sentences = getSentences(text)

  sequences = []
  for sentence in sentences:
    sequences.append(getSequences(sentence))

  utils.writeListToFile('%s\\sequences.txt' % OUTPUT_DIR, sequences)

  sys.exit(0)

  tokens = getTokensFromFile(filename)

  print("Got %s tokens" % len(tokens))

  # Measure token frequency
  distances = []
  token_freq=nltk.FreqDist(tokens)

  sorted_token_freq = OrderedDict(sorted(token_freq.items(), key=lambda t: t[1]))
  utils.writeDictToFile("%s\\distances.txt" % OUTPUT_DIR, sorted_token_freq)

  # Connect to the geonames db
  

  # for tok in tokens:
  #   print(tok)
  #   res = geonames.find({'2': re.compile(".*"+tok+".*", re.IGNORECASE)})
  #   for doc in res:
  #     print(doc)
  #   print("----------------------")

  print("Analysis complete")
  
  

  

  
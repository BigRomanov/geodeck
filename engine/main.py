######
# Python 3 version
# Main python file for tokenizing and analyzing tokes retrieved from a file supplied as a parameter

import sys
import nltk, re, pprint
import enchant
#import pymongo

from nltk.tokenize import sent_tokenize

# Utility functions
def readLinesFromFile(filename):
  with open(filename, encoding="utf8") as f:
    content = f.readlines()
    return content

def readTextFromFile(filename):
  with open(filename, "r", encoding="utf8") as f:
    return f.read()

def writeListToFile(filename, thelist):
  with open(filename, "w", encoding="utf-8") as thefile:
    for item in thelist:
      thefile.write(str(item) + "\n")

def writeDictToFile(filename, thedict):
  with open(filename, "w", encoding="utf-8") as thefile:
    for k,v in thedict.items():
      thefile.write(str(k)+':'+str(v) + "\n")

# Naive algorithms
def naive_extractEntities(text):
  # Naive approach
  entities = []
  for line in text:
    for word in line.split():
      if word[0].isupper():
        entities.append(word)
  return entities


# NLTK
def nltk_extractEntities(text):
  tokens = nltk.word_tokenize(text)  
  return tokens

  
# MAIN
if __name__ == "__main__":

  if len(sys.argv) != 2:
    print ("Invalid parameters")
    exit(1)

  # Initialization
  filename = sys.argv[1]
  print ("Engine running on file %s" % filename)


  text = readTextFromFile(filename)

  #pprint.pprint(content)

  entities = nltk_extractEntities(text)

  writeListToFile('entities.txt', entities)

  # Read the text
  text = readTextFromFile(filename)

  # Split by sentences
  sentences = sent_tokenize(text)
  writeListToFile("sentences.txt", sentences)

  # Tokens
  d = enchant.Dict("en_US")

  # Take only tokens which start with capital letter and are not in the english dictionary
  tokens = [tok.strip().strip(":,;.") for tok in text.split() if tok[0].isupper() and not d.check(tok)]
  writeListToFile('tokens.txt', tokens)
  #print(tokens[:100])

  # Measure token frequency
  distances = []
  Freq_dist_nltk=nltk.FreqDist(tokens)
  writeDictToFile("distances.txt", Freq_dist_nltk)
  

  

  
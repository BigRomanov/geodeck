import sys
import nltk, re, pprint
import codecs

def readLinesFromFile(filename):
  with open(filename, encoding="utf8") as f:
    content = f.readlines()
    return content

def readTextFromFile(filename):
  with open(filename, encoding="utf8") as f:
    return f.read()

def writeEntitiesToFile(filenane, entitylist):
  with open(filename, "w", "utf-8") as thefile:
    for item in entitylist:
      thefile.write(item)

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

if __name__ == "__main__":

  if len(sys.argv) != 2:
    print ("Invalid parameters")
    exit(1)


  filename = sys.argv[1]
  print ("Engine running on file %s" % filename)

  text = readTextFromFile(filename)

  #pprint.pprint(content)

  entities = nltk_extractEntities(text)

  writeEntitiesToFile('entities.txt', entities)


  
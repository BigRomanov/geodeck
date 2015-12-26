######
# Python 3 version
# Main python file for tokenizing and analyzing tokes retrieved from a file supplied as a parameter

import sys
import nltk
import enchant

from nltk.tokenize import sent_tokenize

# Utility functions
def readTextFromFile(filename):
  with open(filename, "r", encoding="utf-8") as f:
    content = f.read()
    return content

  
# MAIN
if __name__ == "__main__":

  if len(sys.argv) != 2:
    print ("Invalid parameters")
    exit(1)

  # Initialization
  filename = sys.argv[1]
  print ("Engine running on file %s" % filename)

  # Read the text
  text = readTextFromFile(filename)

  # Split by sentences
  #sentences = sent_tokenize(text)
  #print(sentences)

  # Tokens
  d = enchant.Dict("en_US")

  # Take only tokens which start with capital letter and are not in the english dictionary
  tokens = [tok.strip().strip(":") for tok in text.split() if tok[0].isupper() and not d.check(tok)]
  #print(tokens[:100])

  # Measure token frequency
  Freq_dist_nltk=nltk.FreqDist(tokens)
  for k,v in Freq_dist_nltk.items():
    print(str(k)+':'+str(v))

  

  
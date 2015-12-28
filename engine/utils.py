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

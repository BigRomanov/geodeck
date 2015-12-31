from exceptions import InvalidTokenFormat

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

# Path, is the list of 
def addMetadata(token, path, name, value):
  if not "meta" in token:
    raise InvalidTokenFormat("No meta in token")
    
  d = token["meta"]
  for p in path:
    d.setdefault(p, {})
    d = d[p]

  d[name] = value


# MAIN
if __name__ == "__main__":
  def testAddMetadata():
    test = {"meta": {}}
    addMetadata(test, ["a", "b", "c"], "name", "value")
    print(test)

  testAddMetadata()

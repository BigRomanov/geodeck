import sys


def readContentFromFile(filename):
  with open(filename, encoding="utf8") as f:
    content = f.readlines()
    return content
  

if __name__ == "__main__":

  if len(sys.argv) != 2:
    print ("Invalid parameters")
    exit(1)


  filename = sys.argv[1]
  print ("Engine running on file %s" % filename)

  content = readContentFromFile(filename)

  for line in content:
    print(line)


  
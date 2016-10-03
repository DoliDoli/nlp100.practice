import codecs
import re

fin = codecs.open('questions-words.txt', 'r', 'utf_8')

if __name__ == "__main__":

  for line in fin: #読み込み
    string = re.split(" ",line[:-1])
    if string[0] == ":":
      if string[1] == "family":
        family = True
      else:
        family = False
    if family == True:
      print(line[:-1])

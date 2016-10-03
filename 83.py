import codecs
import re
import collections

fin = codecs.open('82.txt', 'r', 'utf_8')
wordlist = []
lowercase = [chr(i) for i in range(97,97+26)]
uppercase = [chr(i) for i in range(65,65+26)]
wcase = lowercase + uppercase

if __name__ == "__main__":
  n = 0
  for line in fin:
    wordlist =re.split("\t",line[:-1])
    if wordlist[1] == "":
      continue
    if wordlist[0][0] in wcase and wordlist[1][0] in wcase:
      filename = "dir83/" + wordlist[0][0] + wordlist[1][0] + ".txt"
      fout = codecs.open(filename, 'a', 'utf_8')
      fout.writelines(line)
      print(n)
      n += 1

import codecs
import re
import numpy as np
import copy

def getallvec(): #全ベクトル読み込み
  npxdict = {}
  fin = codecs.open('90vec.txt', 'r', 'utf_8')
  for line in fin: #読み込み
    string = re.split(" ",line[:-1])
    a = [float(x) for x in string[1:301] ]
    npxdict[string[0]] = copy.deepcopy(np.array(a))
  return npxdict

if __name__ == "__main__":

  worddict = getallvec()

  # 96c.txt = 以前作成した国名リスト
  fin = codecs.open('96c.txt', 'r', 'utf_8')
  for line in fin: #読み込み
    country = line[:-1]
    if country in worddict:
      npa = worddict[country]
      print(country,end=" ")
      for y in npa:
        print(y,end=" ")
      print("")

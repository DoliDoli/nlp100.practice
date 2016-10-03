## ここら辺「適用する」って意味がよく分かってない

import codecs
import re
import numpy as np
import copy

def cos_sim(x, y): #コサイン類似度計算
    return np.dot(x, y) / (np.linalg.norm(x) * np.linalg.norm(y))

def getallvec(): #全ベクトル読み込み
  a = []
  npxdict = {}
  fin = codecs.open('85logvec.txt', 'r', 'utf_8')
  for line in fin: #読み込み
    string1 = re.split(" ",line[:-1])
    a = [float(x) for x in string1[1:301] ]
    npxdict[string1[0]] = copy.deepcopy(np.array(a))
  return npxdict

if __name__ == "__main__":

  worddict = getallvec()

  n = 0
  fset = codecs.open('set2.tab', 'r', 'utf_8')
  for line in fset: #読み込み
    if n == 0: #タイトル行を飛ばす
      n += 1
      continue
    string = re.split("\t",line[:-2]) 
    if not string[0] in worddict:
      print(string[0]," not exist.")
      continue
    else:
      npa = worddict[string[0]]
    if not string[1] in worddict:
      print(string[1]," not exist.")
      continue
    else:
      npb = worddict[string[1]]
    print(string[1],string[0],end=" ")
    print("{0:f}".format(cos_sim(npa,npb)))
    n += 1

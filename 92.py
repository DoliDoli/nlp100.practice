import codecs
import re
import numpy as np
import copy

def cos_sim(x, y): #コサイン類似度計算
    return np.dot(x, y) / (np.linalg.norm(x) * np.linalg.norm(y))

def getallvec(): #全ベクトル読み込み
  vecdict = {}
  fin = codecs.open('85logvec.txt', 'r', 'utf_8')
  for line in fin: #読み込み
    string1 = re.split(" ",line[:-1])
    a = [float(x) for x in string1[1:301] ]
    vecdict[string1[0]] = copy.deepcopy(np.array(a))
  return vecdict

def getsim(v,worddict): #類似度計算
  string = ""
  cos_sim1 = 0
  for k,v1 in worddict.items():
    npe = v1
    cos_sim2=cos_sim(v,npe)
    if cos_sim2 > cos_sim1: #類似度が大きいものに取り替え
      cos_sim1 = cos_sim2
      string = k
  print(string,end=" ")
  print("{0:f}".format(cos_sim1))

if __name__ == "__main__":

  worddict = getallvec()

  f91 = codecs.open('91.txt', 'r', 'utf_8')
  for line in f91: #読み込み
    string = re.split(" ",line[:-1])  

    if not string[1] in worddict:
      print(string[1]," not exist.")
      continue
    else:
      npa = worddict[string[1]]

    if not string[0] in worddict:
      print(string[0]," not exist.")
      continue
    else:
      npb = worddict[string[0]]

    if not string[2] in worddict:
      print(string[2]," not exist.")
      continue
    else:
      npc = worddict[string[2]]
      
    npd = npa - npb + npc
    print(string[1],"-",string[0],"+",string[2],end=" ")
    getsim(npd,worddict)

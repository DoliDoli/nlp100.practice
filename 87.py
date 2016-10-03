## 単語のコサイン類似度による意味判定

import codecs
import re
import numpy as np

fin = codecs.open('85vec.txt', 'r', 'utf_8')
a = []
b = []

if __name__ == "__main__":

　## aに"UnitedStates"の300次元ベクトルを入れる
  for line in fin: #読み込み
    string1 = re.split(" ",line[:-1])
    if string1[0] == "United_States":
      print(len(string1))
      for x in string1[1:301]:
        a.append(float(x))
      break
　## bに"U.S"の300次元ベクトルを入れる
  fin = codecs.open('85vec.txt', 'r', 'utf_8')
  for line in fin: #読み込み
    string2 = re.split(" ",line[:-1])
    if string2[0] == "U.S":
      print(len(string2))
      for x in string2[1:301]:
        b.append(float(x))
      break

  npa = np.array(a)
  npb = np.array(b)
  ## コサイン距離を求めている
  ## np.dot →　ベクトルの内積
  ## np.linalg.norm() →　ベクトルの長さ 
  cos_sim = np.dot(npa, npb) / ( np.linalg.norm(npa) * np.linalg.norm(npb) )
  print(cos_sim)

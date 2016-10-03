

import codecs
import re
import numpy as np

fin = codecs.open('85vec.txt', 'r', 'utf_8')

def cos_sim(x, y):
    return np.dot(x, y) / (np.linalg.norm(x) * np.linalg.norm(y))

# 引数の文字列の単語ベクトルの値を取得する関数
def getvec(word):
  a = []
  fin = codecs.open('85vec.txt', 'r', 'utf_8')
  for line in fin: #読み込み
    string1 = re.split(" ",line[:-1])
    if string1[0] == word:
      for x in string1[1:301]:
        a.append(float(x))
      npx = np.array(a)
      break
  return npx

if __name__ == "__main__":

　# ベクトルの値を加減
  npa = getvec("Spain")
  npb = getvec("Madrid")
  npc = getvec("Athens")
  npd = npa - npb + npc

　# npdとコサイン類似度の高い単語を、計算して検索
  b=[]
  fin = codecs.open('85vec.txt', 'r', 'utf_8')
  for line in fin: #読み込み
    string2 = re.split(" ",line[:-1])
    for x in string2[1:301]:
      b.append(float(x))
    npb = np.array(b)
    print(string2[0],end=" ")
    print("{0:f}".format(cos_sim(npd,npb)))
    b = []

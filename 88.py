## Englandのベクトルと、一通りのベクトルのコサイン類似度を算出
## 後々Unixコマンドで「nan」を取り除いて、値の大きい順にソート
## 後は87と同じ

import codecs
import re
import numpy as np

fin = codecs.open('85vec.txt', 'r', 'utf_8')
a = []
b = []

def cos_sim(x, y):
    return np.dot(x, y) / (np.linalg.norm(x) * np.linalg.norm(y))

if __name__ == "__main__":

  for line in fin: #読み込み
    string1 = re.split(" ",line[:-1])
    if string1[0] == "England":
      print(len(string1))
      for x in string1[1:301]:
        a.append(float(x))
      npa = np.array(a)
      break

  fin = codecs.open('85vec.txt', 'r', 'utf_8')
  for line in fin: #読み込み
    string2 = re.split(" ",line[:-1])
    for x in string2[1:301]:
      b.append(float(x))
    npb = np.array(b)
    print(string2[0],end=" ")
    print("{0:f}".format(cos_sim(npa,npb)))
    b = []

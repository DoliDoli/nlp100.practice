import codecs
import re
import copy
import numpy as np
# 素性名、素性値のペアが入ったdictを渡すと、疎行列に変換する
from sklearn.feature_extraction import DictVectorizer
# 次元圧縮（主成分分析に近い）
from sklearn.decomposition import TruncatedSVD
# 岩波DSは特異値分解している



fin = codecs.open('8584.txt', 'r', 'utf_8')
fout = codecs.open('85vec.txt', 'w', 'utf_8')
contextdic = {}
worddic = {}
keylist = []
vectorlist=[]

if __name__ == "__main__":
  for line in fin: #読み込み
    string = re.split("\t",line[:-1])
    context=string[1]
    value = string[2]
    contextdic[context[:-1]]=float(value[1:]) #二重辞書化
    if string[0] in worddic:
      worddic[string[0]].update(contextdic)
    else:
      worddic[string[0]]=contextdic
    contextdic={}

  n=0
  for k,v in worddic.items(): #リスト化
    keylist.append(k)
    vectorlist.append(v)
    print("vlist:",n)
    n += 1

  vec = DictVectorizer(sparse=True)
  array_vectors=vec.fit_transform(vectorlist)
  tsvd = TruncatedSVD(n_components=300)
  word_pca = tsvd.fit_transform(array_vectors)

  n=0
  while n < len(keylist):
    fout.write(keylist[n])
    fout.write(" ")
    for m in word_pca[n]:
      precision = 6
      m = str(np.round(m, precision))
      fout.write(m)
      fout.write(" ")
    n += 1
    fout.write("\n")

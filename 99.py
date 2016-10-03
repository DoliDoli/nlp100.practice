# そもそもt-SNEがよく分からない問題

import codecs
import re
import copy
import numpy as np
from sklearn.manifold import TSNE
from matplotlib import pyplot as plt

def getallvec(): #全ベクトル読み込み
  namelist = []
  npxlist = [] 
  fin = codecs.open('96.txt', 'r', 'utf_8')
  for line in fin: #読み込み
    string = re.split(" ",line[:-1])
    a = [float(x) for x in string[1:301] ]
    namelist.append(string[0])
    npxlist.append(copy.deepcopy(np.array(a)))
  npxarray = np.array(npxlist)
  return namelist,npxarray

if __name__ == "__main__":

  namelist,npxarray = getallvec()
#t-SNE
  model = TSNE(n_components=2)
  tsne_result = model.fit_transform(npxarray)
#表示
  plt.plot(tsne_result[:,0], tsne_result[:,1], ".")
  plt.show()

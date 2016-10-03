## ward方による階層型クラスタリングは scipy.cluster.hierarchyを使用
## デンドログラムも書いてくれる

import codecs
import re
import copy
import numpy as np
import scipy
from matplotlib.pyplot import show
from scipy.cluster.hierarchy import ward, dendrogram

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
# Ward法で階層クラスタリング
# numpy配列を入力とする
  result_w = scipy.cluster.hierarchy.ward(npxarray)
#描画
  dendrogram(result_w)
  show()

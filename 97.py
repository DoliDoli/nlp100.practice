## k-meansはscikit-learn内に存在
## k-meansを使用するためにはnumpyのarrayにする必要有り

import codecs
import re
import copy
import numpy as np
from sklearn.cluster import KMeans

def getallvec(): #全ベクトル読み込み
  namelist = []
  npxlist = [] 
  fin = codecs.open('96.txt', 'r', 'utf_8')
  for line in fin: #読み込み
    string = re.split(" ",line[:-1])
    
    a = [float(x) for x in string[1:301] ]
    
    # 単語リスト
    namelist.append(string[0])
    # 各ベクトルを配列の1要素としてappendしていく
    npxlist.append(copy.deepcopy(np.array(a)))
    
  npxarray = np.array(npxlist)
  return namelist,npxarray

if __name__ == "__main__":

  namelist,npxarray = getallvec()
　#k-meansクラスタリング
  kmeans_model = KMeans(n_clusters=5, random_state=10).fit(npxarray)
  labels = kmeans_model.labels_
  n=0
  for label in labels:
    print(label, namelist[n]) 
    n += 1

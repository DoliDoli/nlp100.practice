import codecs
import re

f94 = codecs.open('9490set2.txt', 'r', 'utf_8')
fset = codecs.open('set2.tab', 'r', 'utf_8')
list1 = []
list2 = []

if __name__ == "__main__":

  n=0
  for line in f94: #94データ読み込み
    string = re.split(" ",line[:-1]) 
    if len(string) > 4:
      list1.append([n,string[0],string[3],string[4]])
    else:
      list1.append([n,""])
    n += 1

  n = 0
  for line in fset: #set読み込み
    if n ==0:
      n += 1
      continue
    string = re.split("\t",line[:-2]) 
    list1[n-1].append(string[2])
    n += 1
 
  for x in list1: #欠損値削除
    if not x[1] == "":
      list2.append(x)
#並べ替え（cos類似度）
  list1_2 = sorted(list2, key=lambda sim: sim[3], reverse=True)
#順位設定(1から)
  n=1
  for x in list1_2:
    list1_2[n-1].append(n)
    n += 1

#並べ替え（人間判定類似度）
  list1_3 = sorted(list1_2, key=lambda sim: sim[4], reverse=True)
#順位設定（1から）
  n=1
  for x in list1_3:
    list1_3[n-1].append(n)
    n += 1

#スピアマン相関係数計算
  num = len(list1_3)

  dis=0
  for x in list1_3:
    dis += (int(x[5])-int(x[6]))**2

  spearman = 1 - ( 6 * dis / ( num * (num**2 - 1) ))

  print(spearman)

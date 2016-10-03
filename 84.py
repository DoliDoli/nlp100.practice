import codecs
import re
import collections
import math

#f(t,c)の出現分布
flc10 = codecs.open('aalc10.txt', 'r', 'utf_8')
#単語tの出現回数
ftc = codecs.open('aatc.txt', 'r', 'utf_8')
# 文脈語cの出現分布
fcc = codecs.open('aacc.txt', 'r', 'utf_8')

wordlist = []
tdic = collections.defaultdict(int)
cdic = collections.defaultdict(int)

# aa.txtの行数
N = 701279

if __name__ == "__main__":

　# 単語の辞書作成
  for line in ftc:
    string =re.split(" ",line[:-1])  
    tdic[string[1]]=int(string[0])

　#　文脈後の辞書作成
  for line in fcc:
    string =re.split(" ",line[:-1])  
    cdic[string[1]]=int(string[0])
　# 単語文脈行列の計算
  for line in flc10:
    string =re.split(" ",line[:-1])  
    wordlist =re.split("\t",string[1])   
    Xtc = math.log(N) + math.log(int(string[0])) - math.log ( tdic[wordlist[0]] ) - math.log( cdic[wordlist[1]] )
    if Xtc < 0:
       Xtc = 0
    print(string[1],"\t",Xtc)

import codecs
import re

f85vec = codecs.open('9285vec.txt', 'r', 'utf_8')
f91 = codecs.open('91.txt', 'r', 'utf_8')
list1 = []
list2 = []
list3 = []

if __name__ == "__main__":

  for line in f91: #読み込み
    string = re.split(" ",line[:-1])
    list1.append(string[3])

  for line in f85vec: #読み込み
    string = re.split(" ",line[:-1])  
    if len(string) > 5:
      list2.append(string[5])
    else:
      list2.append("")

  n = 0
  x = 0
  while n < len(list1):
    list3.append([list1[n],list2[n]])
    if list1[n] == list2[n]:
      x += 1
    n += 1

  print(x)
  print(x/len(list1))

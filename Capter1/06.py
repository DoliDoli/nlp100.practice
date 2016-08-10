word1="paraparaparadise"
word2="paragraph"

#set 重複のない要素を持つ順序なしのコレクションオブジェクト　リストから重複する値を除いたり、集合演算を行うために使用します
X=set([word1[i:i+2] for i in range(len(word1)-1)])
Y=set([word2[i:i+2] for i in range(len(word2)-1)])

print("X="+str(X))
print("Y="+str(Y))
print ("和集合:"+str(X|Y))
print ("差集合:"+str(X-Y))
print ("積集合:"+str(X&Y))
if 'se' in X:
    print( "'se'はXに含まれるよ" )
if 'se' in Y:
    print( "'se'はYに含まれるよ" )

#これも出力結果の順番がまちまちだが、大丈夫なのだろうか
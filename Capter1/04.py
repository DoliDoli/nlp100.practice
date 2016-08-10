s = "Hi He Lied Because Boron Could Not Oxidize Fluorine. New Nations Might Also Sign Peace Security Clause. Arthur King Can."

#.を消す
s = s.replace(".","")
#単語分割
words = s.split(" ")
words_index = {}

#enumurate ＝　ループ時にインデックスつきで要素を得ることができる
for i, word in enumerate(words):
    n = i + 1
    if n in [1, 5, 6, 7, 8, 9, 15, 16, 19]:
        #index番号のwordから1文字取り出す
        words_index[word[:1]] = n
    else:
        words_index[word[:2]] = n

print(words_index)


sentence ="Hi He Lied Because Boron Could Not Oxidize Fluorine. New Nations Might Also Sign Peace Security Clause. Arthur King Can."

#単語に分解
words=[word.strip(".,") for word in sentence.split()]

#先頭の1文字(または2文字)と、その単語のインデックスを対応付ける辞書を作成
link={}
for i,v in enumerate(words,1):
    length=1 if i in [1,5,6,7,8,9,15,16,19] else 2
    link.update({v[:length]:i})
print(link)


#実行するたびに出力結果が変わるが、これは大丈夫なのだろうか？
import sys,random,itertools

sentence="I couldn't believe that I could actually understand what I was reading : the phenomenal power of the human mind."

#文を単語に分解
words=[word.strip(".,") for word in sentence.split()]

#enumurate ＝　ループ時にインデックスつきで要素を得ることができる
for idx,word in enumerate(words):
    ret=""
    L=len(word)
    #4文字以下はなにもしない
    if 4<L:
        #最初は確定
        ret+=word[0]
        #並べ替えパターンを全てリストに
        #iter tols = ループ実行のためのイテレータ
        perm=list(itertools.permutations(list(word[1:L-1]),L-2))
        #乱数生成
        rnd=random.randint(0,len(perm)-1)
        #並びのなかからランダムにピック
        ret+="".join(perm[rnd])
        #最後も確定
        ret+=word[L-1]
        words[idx]=ret
print(words)
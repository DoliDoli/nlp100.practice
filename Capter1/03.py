#re =正規表現を扱えるようになるライブラリ
import re

s = "Now I need a drink, alcoholic of course, after the heavy lectures involving quantum mechanics."

#[.,]を抜いた正規表現化する
pat = re.compile('[.,]')
#re.sub(pattern, repl, string, count=0, flags=0)
#patternのマッチをreplで置き換える
#for 変数　in オブジェクト　　シーケンス型のオブジェクトから要素を順に変数に代入する
print([len(pat.sub('', word)) for word in s.split()])
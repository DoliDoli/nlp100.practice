import numpy as np
import matplotlib.pyplot as plt
from matplotlib.font_manager import FontProperties

import ngram

import sys
import io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

def tabbed_str_to_dict(tabbed_str: str) -> dict:
    """
    例えば「次第に   シダイニ    次第に   副詞-一般   」のようなタブ区切りで形態素を表す文字列をDict型に変換する.
    :param tabbed_str タブ区切りで形態素を表す文字列
    :return Dict型で表された形態素
    """
    elements = tabbed_str.split()
    if 0 < len(elements) < 4:
        return {'surface': elements[0], 'base': '', 'pos': '', 'pos1': ''}
    else:
        return {'surface': elements[0], 'base': elements[1], 'pos': elements[2], 'pos1': elements[3]}

with open('neko.txt.mecab', encoding='utf-8') as file_wrapper:
    morphemes = [tabbed_str_to_dict(line) for line in file_wrapper]

#frecuencyを取得する
def get_frequency(words: list) -> dict:
    """
    単語のリストを受け取って、単語をキーとして、頻度をバリューとする辞書を返す.
    :param words 単語のリスト
    :return dict 単語をキーとして、頻度をバリューとする辞書
    """
    frequency = {}
    for word in words:
        if frequency.get(word):
            frequency[word] += 1
        else:
            frequency[word] = 1

    return frequency


frequency = get_frequency([morpheme['surface'] for morpheme in morphemes])
frequency = [(k, v) for k, v in sorted(frequency.items(), key=lambda x: x[1], reverse=True)]

#新規
#グラフフォーマット
fig = plt.figure(figsize=(20, 6))

# 37. 出現頻度が高い10語とその出現頻度をグラフ（例えば棒グラフなど）で表示せよ．
words = [f[0] for f in frequency[0:10]]
  #np.arrange　引数の数だけデータを生成
x_pos = np.arange(len(words))
fp = FontProperties(fname=r'C:\Windows\Fonts\msgothic.ttc', size=14)

ax1 = fig.add_subplot(131)
  #各単語の出現回数をプロットするためのもの
  #bar = 棒グラフ
ax1.bar(x_pos, [f[1] for f in frequency[0:10]], align='center', alpha=0.4)
ax1.set_xticks(x_pos)
ax1.set_xticklabels(words, fontproperties=fp)
ax1.set_ylabel('Frequency')
ax1.set_title('Top 10 frequent words')

# 38. 単語の出現頻度のヒストグラム（横軸に出現頻度，縦軸に出現頻度をとる単語の種類数を棒グラフで表したもの）を描け．
freq = list(dict(frequency).values())
freq.sort(reverse=True)

ax2 = fig.add_subplot(132)
  #hist = ヒストグラム
ax2.hist(freq, bins=50, range=(0, 50))
ax2.set_title('Histogram of word count')
ax2.set_xlabel('Word count')
ax2.set_ylabel('Frequency')

# 39. 単語の出現頻度順位を横軸，その出現頻度を縦軸として，両対数グラフをプロットせよ．
rank = list(range(1, len(freq) + 1))

ax3 = fig.add_subplot(133)
ax3.plot(freq, rank)
ax3.set_xlabel('Rank')
ax3.set_ylabel('Frequency')
ax3.set_title('Zipf low')
ax3.set_xscale('log')
ax3.set_yscale('log')

fig.savefig('morphological_analysis.png')
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


#新規
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

# ソート　frequencyのitemsをソート対象とする　
#key=lambda x: x[1] タプル2つ目でソートする　
#lambdaは無名関数 xが引数でx[1]が戻り値
frequency = [(k, v) for k, v in sorted(frequency.items(), key=lambda x: x[1], reverse=True)]

# 結果の確認
print(frequency[0:20])
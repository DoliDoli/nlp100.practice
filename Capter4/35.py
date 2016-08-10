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

def morphemes_to_noun_array(morphemes: list) -> list:
    """
    辞書型で表された形態素のリストを句点もしくは名詞以外の形態素で区切ってグルーピングし、リスト化する.
    :param morphemes 辞書型で表された形態素のリスト
    :return 名詞の連接のリスト
    """
    nouns_list = []
    nouns = []

    for morpheme in morphemes:
        #ここの条件、何を指定しているのか
        if morpheme['pos1'].find('名詞') >= 0:
            nouns.append(morpheme)
        #ここの条件、何を指定しているのか
        elif (morpheme['pos1'] == '記号-句点') | (morpheme['pos1'].find('名詞') < 0):
            nouns_list.append(nouns)
            nouns = []

    return [nouns for nouns in nouns_list if len(nouns) > 1]


noun_array = [''.join([noun['surface'] for noun in nouns]) for nouns in morphemes_to_noun_array(morphemes)]

# 結果の確認
print(noun_array[::100])
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

#以下追加#
def ngramed_list(lst: list, n: int = 3) -> list:
    """
    listをNグラム化する.
    :param lst Nグラム化対象のリスト
    :param n N (デフォルトは N = 3)
    :return Nグラム化済みのリスト
    """
    index = ngram.NGram(N=n)
    return [term for term in index.ngrams(lst)]

def is_noun_no_noun(words: list) -> bool:
    """
    3つの単語から成るリストが「名詞-の-名詞」という構成になっているかを判定する.
    :param words 3つの単語から成るリスト
    :return bool (True:「名詞-の-名詞」という構成になっている / False:「名詞-の-名詞」という構成になっていない)
    """
    return (type(words) == list) and (len(words) == 3) and \
           (words[0]['pos1'].find('名詞') == 0) and \
           (words[1]['surface'] == 'の') and \
           (words[2]['pos1'].find('名詞') == 0)

# 「名詞-の-名詞」を含むNグラムのみを抽出
noun_no_noun = [ngrams for ngrams in ngramed_list(morphemes) if is_noun_no_noun(ngrams)]

# 表層を取り出して結合する
noun_no_noun = [''.join([word['surface'] for word in ngram]) for ngram in noun_no_noun]

# 結果の確認
print(noun_no_noun[::100])
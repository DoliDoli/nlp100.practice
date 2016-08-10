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

verbs_surface = [morpheme['surface'] for morpheme in morphemes if morpheme['pos1'].find('動詞') == 0]
verbs_base = [morpheme['base'] for morpheme in morphemes if morpheme['pos1'].find('動詞') == 0]
nouns_suru = [morpheme['surface'] for morpheme in morphemes if morpheme['pos1'] == '名詞-サ変接続']

# 結果の確認
print(verbs_surface[::100])
print(verbs_base[::100])
print(nouns_suru[::100])
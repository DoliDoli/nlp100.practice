import MeCab
import ngram
import numpy as np

def make_analyzed_file(input_file_name: str, output_file_name: str) -> None:
    """
    プレーンな日本語の文章ファイルを形態素解析してファイルに保存する.
    :param input_file_name プレーンな日本語の文章ファイル名
    :param output_file_name 形態素解析済みの文章ファイル名
    """
    _m = MeCab.Tagger("-Ochasen")
    with open(input_file_name, encoding='utf-8') as input_file:
        with open(output_file_name, mode='w', encoding='utf-8') as output_file:
            output_file.write(_m.parse(input_file.read()))

make_analyzed_file('neko.txt', 'neko.txt.mecab')

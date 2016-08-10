import pydotplus
import subprocess


class Morph:
    """
    1つの形態素を表すクラス
    """
    def __init__(self, surface, base, pos, pos1):
        """
        メンバ変数として表層形（surface），基本形（base），品詞（pos），品詞細分類1（pos1）を持つ.
        """
        self.surface = surface
        self.base = base
        self.pos = pos
        self.pos1 = pos1

    def is_end_of_sentence(self) -> bool: return self.pos1 == '句点'

    def __str__(self) -> str: return 'surface: {}, base: {}, pos: {}, pos1: {}'.format(self.surface, self.base, self.pos, self.pos1)


class Chunk:
    def __init__(self, morphs: list, dst: str, srcs: str) -> None:
        """
        形態素（Morphオブジェクト）のリスト（morphs），係り先文節インデックス番号（dst），係り元文節インデックス番号のリスト（srcs）をメンバ変数に持つ
        """
        self.morphs = morphs
        self.dst = int(dst.strip("D"))
        self.srcs = int(srcs)

    def __str__(self) -> str:
        return 'srcs: {}, dst: {}, morphs: ({})'.format(self.srcs, self.dst, ' / '.join([str(_morph) for _morph in self.morphs]))

def make_chunk_list(analyzed_file_name: str) -> list:
    """
    係り受け解析済みの文章ファイルを読み込んで、各文をChunkオブジェクトのリストとして表現する
    :param analyzed_file_name 係り受け解析済みの文章ファイル名
    :return list 一つの文章をChunkオブジェクトのリストとして表現したもののリスト
    """
    sentences = []
    sentence = []
    _chunk = None
    with open(analyzed_file_name, encoding='utf-8') as input_file:
        for line in input_file:
            line_list = line.split()
            if line_list[0] == '*':
                if _chunk is not None:
                    sentence.append(_chunk)
                _chunk = Chunk(morphs=[], dst=line_list[2], srcs=line_list[1])
            elif line_list[0] == 'EOS':  # End of sentence
                if _chunk is not None:
                    sentence.append(_chunk)
                if len(sentence) > 0:
                    sentences.append(sentence)
                _chunk = None
                sentence = []
            else:
                line_list = line_list[0].split(',') + line_list[1].split(',')
                # この時点でline_listはこんな感じ
                # ['始め', '名詞', '副詞可能', '*', '*', '*', '*', '始め', 'ハジメ', 'ハジメ']
                _morph = Morph(surface=line_list[0], base=line_list[7], pos=line_list[1], pos1=line_list[2])
                _chunk.morphs.append(_morph)

    return sentences


chunked_sentences = make_chunk_list('neko.txt.cabocha')

# 3文目の形態素列を表示
for chunk in chunked_sentences[2]:
    print(str(chunk))
# 問題文の意味がなぞ

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
    def join_morphs(self) -> str:
        return ''.join([_morph.surface for _morph in self.morphs if _morph.pos != '記号'])

    def has_noun(self) -> bool:
        return any([_morph.pos == '名詞' for _morph in self.morphs])
    def has_verb(self) -> bool:
        return any([_morph.pos == '動詞' for _morph in self.morphs])
    
    def has_sahen_connection_noun_plus_wo(self) -> bool:
        """
        「サ変接続名詞+を（助詞）」を含むかどうかを返す.
        """
        for idx, _morph in enumerate(self.morphs):
            if _morph.pos == '名詞' and _morph.pos1 == 'サ変接続' and len(self.morphs[idx:]) > 1 and \
                            self.morphs[idx + 1].pos == '助詞' and self.morphs[idx + 1].base == 'を':
                return True

        return False

    #新規#
    def first_verb(self) -> Morph:
        return [_morph for _morph in self.morphs if _morph.pos == '動詞'][0]

    def has_particle(self) -> bool:
        return any([_morph.pos == '助詞' for _morph in self.morphs])

    def last_particle(self) -> list:
        return [_morph for _morph in self.morphs if _morph.pos == '助詞'][-1]
    #以上#

    def replace_noun(self, alt: str) -> None:
        """
        名詞の表象を置換する.
        """
        for _morph in self.morphs:
            if _morph.pos == '名詞':
                _morph.surface = alt
    
    def pair(self, sentence: list) -> str:
        return self.join_morphs() + '\t' + sentence[self.dst].join_morphs()
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


def path_to_root(_chunk: Chunk, _sentence: list) -> list:
    """
    引数として与えられた文節(`_chunk`)がrootの場合は、その文節を返します.
    引数として与えられた文節(`_chunk`)がrootでない場合は、その文節とその文節が係っている文節からrootまでのパスをlistとして返します.
    :param _chunk rootへの起点となる文節
    :param _sentence 分析対象の文章
    :return list _chunkからrootまでのパス
    """
    if _chunk.dst == -1:
        return [_chunk]
    else:
        return [_chunk] + path_to_root(_sentence[_chunk.dst], _sentence)

def join_chunks_by_arrow(_chunks: list) -> str:
    return ' -> '.join([c.join_morphs() for c in _chunks])

def noun_pairs(_sentence: list):
    """
    引数として渡された文章が持つ全ての名詞節から作ることができる全てのペアのリストを返す.
    """
    from itertools import combinations
    _noun_chunks = [_chunk for _chunk in _sentence if _chunk.has_noun()]
    return list(combinations(_noun_chunks, 2))


def common_chunk(path_i: list, path_j: list) -> Chunk:
    """
    文節iと文節jから構文木の根に至る経路上で共通の文節kで交わる場合、文節kを返す.
    """
    _chunk_k = None
    path_i = list(reversed(path_i))
    path_j = list(reversed(path_j))
    for idx, (c_i, c_j) in enumerate(zip(path_i, path_j)):
        if c_i.srcs != c_j.srcs:
            _chunk_k = path_i[idx - 1]
            break

    return _chunk_k

for sentence in chunked_sentences:
    # 名詞句ペアのリスト
    n_pairs = noun_pairs(sentence)
    if len(n_pairs) == 0:
        continue

    for n_pair in n_pairs:
        chunk_i, chunk_j = n_pair

        # 文節iとjに含まれる名詞句はそれぞれ，XとYに置換する
        chunk_i.replace_noun('X')
        chunk_j.replace_noun('Y')

        # 文節iとjからrootへのパス(Chunk型のlist)
        path_chunk_i_to_root = path_to_root(chunk_i, sentence)
        path_chunk_j_to_root = path_to_root(chunk_j, sentence)

        if chunk_j in path_chunk_i_to_root:
            # 文節iから構文木の根に至る経路上に文節jが存在する場合

            # 文節jの文節iから構文木の根に至る経路上におけるインデックス
            idx_j = path_chunk_i_to_root.index(chunk_j)

            # 文節iから文節jのパスを表示
            print(join_chunks_by_arrow(path_chunk_i_to_root[0: idx_j + 1]))
        else:
            # 上記以外で，文節iと文節jから構文木の根に至る経路上で共通の文節kで交わる場合

            # 文節kを取得
            chunk_k = common_chunk(path_chunk_i_to_root, path_chunk_j_to_root)
            if chunk_k is None:
                continue

            # 文節kの文節iから構文木の根に至る経路上におけるインデックス
            idx_k_i = path_chunk_i_to_root.index(chunk_k)

            # 文節kの文節jから構文木の根に至る経路上におけるインデックス
            idx_k_j = path_chunk_j_to_root.index(chunk_k)

            # 文節iから文節kに至る直前のパスと文節jから文節kに至る直前までのパス，文節kの内容を"|"で連結して表示
            print(' | '.join([join_chunks_by_arrow(path_chunk_i_to_root[0: idx_k_i]),
                              join_chunks_by_arrow(path_chunk_j_to_root[0: idx_k_j]),
                              chunk_k.join_morphs()]))
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


# 最初10文だけ出力して動作確認
for sentence in chunked_sentences[0:10]:
    for chunk in sentence:
        if chunk.has_noun():
            print(join_chunks_by_arrow(path_to_root(chunk, sentence)))
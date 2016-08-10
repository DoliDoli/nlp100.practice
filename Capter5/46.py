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

def is_valid_chunk(_chunk, sentence):
    #.dstとは？
    return _chunk.join_morphs() != '' and _chunk.dst > -1 and sentence[_chunk.dst].join_morphs() != ''

def sentence_to_dot(idx: int, sentence: list) -> str:
    head = "digraph sentence{} ".format(idx)
    body_head = "{ graph [rankdir = LR]; "
    body_list = ['"{}"->"{}"; '.format(*chunk_pair.split()) for chunk_pair in sentence]

    return head + body_head + ''.join(body_list) + '}'


def sentences_to_dots(sentences: list) -> list:
    _dots = []
    for idx, sentence in enumerate(sentences):
        _dots.append(sentence_to_dot(idx, sentence))
    return _dots


def save_graph(dot: str, file_name: str) -> None:
    g = pydotplus.graph_from_dot_data(dot)
    g.write_jpeg(file_name, prog='dot')

paired_sentences = [[chunk.pair(sentence) for chunk in sentence if is_valid_chunk(chunk, sentence)] for sentence in chunked_sentences if len(sentence) > 1]

#新規#
def sorted_double_list(key_list: list, value_list: list) -> tuple:
    """
    2つのリストを引数に取り、一方のリストをキー、もう一方のリストを値としてdict化しキーでソートしてから、元通りに2つのリストに分解してタプルとして返す.
    :param key_list ソートするときのキーとなるリスト
    :param value_list keyに従ってソートされるリスト
    :return key_listでソート済みの2つのリストのタプル
    """
    double_list = list(zip(key_list, value_list))
    double_list = dict(double_list)
    double_list = sorted(double_list.items())
    return [pair[0] for pair in double_list], [pair[1] for pair in double_list]


def case_frame_patterns(_chunked_sentences: list) -> list:
    """
    動詞の格フレームのパターン(動詞と助詞の組み合わせ)のリストを返します.
    :param _chunked_sentences チャンク化された形態素を文章ごとにリスト化したもののリスト
    :return 格のパターン(例えば['する', ['て', 'は'], ['泣いて', 'いた事だけは']])のリスト
    """
    _case_frame_patterns = []
    for sentence in _chunked_sentences:
        for _chunk in sentence:
            if not _chunk.has_verb():
                continue

            clauses = [c.join_morphs() for c in sentence if c.dst == _chunk.srcs and c.has_particle()]
            particles = [c.last_particle().base for c in sentence if c.dst == _chunk.srcs and c.has_particle()]

            if len(particles) > 0:
                _case_frame_patterns.append([_chunk.first_verb().base, *sorted_double_list(particles, clauses)])

    return _case_frame_patterns


def save_case_frame_patterns(_case_frame_patterns: list, file_name: str) -> None:
    """
    動詞の格のパターン(動詞と助詞の組み合わせ)のリストをファイルに保存します.
    :param _case_frame_patterns 格フレーム(例えば['する', ['て', 'は'], ['泣いて', 'いた事だけは']])のリスト
    :param file_name 保存先のファイル名
    """
    with open(file_name, mode='w', encoding='utf-8') as output_file:
        for case in _case_frame_patterns:
            output_file.write('{}\t{}\t{}\n'.format(case[0], ' '.join(case[1]), ' '.join(case[2])))


save_case_frame_patterns(case_frame_patterns(chunked_sentences), 'case_frame_patterns.txt')
#ここまで#
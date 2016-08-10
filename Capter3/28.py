#!/usr/bin/env python
# -*- coding: utf-8 -*-

from extract_from_json import extract_from_json

import sys
import io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

import re

def remove_markup(str):
    #強調
    str = re.sub(r"'{2,5}", r"", str)
    #　内部リンク
    str = re.sub(r"\[{2}([^|\]]+?\|)*(.+?)\]{2}", r"\2", str)
    # 言語を指定した標記
    str = re.sub(r"\{{2}.+?\|.+?\|(.+?)\}{2}", r"\1 ", str)
    # コメント
    str = re.sub(r"<.*?>", r"", str)
    # 外部リンク
    str = re.sub(r"\[.*?\]", r"", str)
    return str

temp_dict = {}
lines = extract_from_json(u"イギリス").split("\n")

for line in lines:
    temp_line = re.search("^\|(.*?)\s=\s(.*)", line)
    if temp_line is not None:
        temp_dict[temp_line.group(1)] = remove_markup(temp_line.group(2))

for k, v in sorted(temp_dict.items(), key=lambda x: x[0]):
    print(k, v)

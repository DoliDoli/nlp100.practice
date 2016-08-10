#!/usr/bin/env python
# -*- coding: utf-8 -*-


from extract_from_json import extract_from_json

import sys
import io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

import re

#\n = ラインフィード
lines = extract_from_json(u"イギリス").split("\n")

for line in lines:
    file_line = re.search(u"(File|ファイル):(.*?)\|", line)
    if file_line is not None:
        #インデックスで　グループを参照する
        print(file_line.group(2))
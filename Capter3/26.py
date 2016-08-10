#!/usr/bin/env python
# -*- coding: utf-8 -*-

from extract_from_json import extract_from_json

import sys
import io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

import re

temp_dict = {}
lines = re.split(r"\n[\|}]", extract_from_json(u"イギリス"))

for line in lines:
    temp_line = re.search("^(.*?)\s=\s(.*)", line, re.S)
    if temp_line is not None:
        #re.subは正規表現にマッチしてくれる箇所を置換してくれる
        #２個以上、5以下の'を""にかえてくれる
        temp_dict[temp_line.group(1)] = re.sub(r"'{2,5}", r"", temp_line.group(2))

# 25.py と同様 Python3 参照
for k, v in sorted(temp_dict.items(), key=lambda x: x[1]):
    print(k, v)
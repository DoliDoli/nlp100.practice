#!/usr/bin/env python
# -*- coding: utf-8 -*-
# 22.py

import re
from extract_from_json import extract_from_json

import sys
import io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

lines = extract_from_json(u"イギリス").split("\n")

for line in lines:
    #下記が正規表現
    category_line = re.search("^\[\[Category:(.*?)(|\|.*)\]\]$", line)
    if category_line is not None:
        print(category_line.group(1))

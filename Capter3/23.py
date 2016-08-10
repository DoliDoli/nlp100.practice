#!/usr/bin/env python
# -*- coding: utf-8 -*-
# 23.py

import re
from extract_from_json import extract_from_json

import sys
import io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

lines = extract_from_json(u"イギリス").split("\n")

for line in lines:
#下記が正規表現
    section_line = re.search("^(=+)\s*(.*?)\s*(=+)$", line)
    if section_line is not None:
        print(section_line.group(2), len(section_line.group(1)) - 1)

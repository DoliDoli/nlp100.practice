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
        temp_dict[temp_line.group(1)] = temp_line.group(2)

# What?
for k, v in sorted(temp_dict.items(), key=lambda x: x[1]):
    print(k, v)
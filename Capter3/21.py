#!/usr/bin/python
# -*- coding: utf-8 -*-

from extract_from_json import extract_from_json

import sys
import io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

lines = extract_from_json(u"イギリス").split("\n")

for line in lines:
    if "Category" in line:
        print(line)
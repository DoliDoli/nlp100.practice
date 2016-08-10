#!/usr/bin/python
# -*- coding: utf-8 -*-

import json

import sys
import io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

#with構文を使うとcloseの呼び出しが不要です
with open("jawiki-country.json", encoding="utf-8") as f:
    article_json = f.readline()
    while article_json:
        article_dict = json.loads(article_json)
        #u = unicode文字列を作成
        #utf-8で書かれている場合はこれ
        if article_dict["title"] == u"イギリス":    
            print(article_dict["text"])
        article_json = f.readline()
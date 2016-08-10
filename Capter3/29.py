#!/usr/bin/env python
# -*- coding: utf-8 -*-

from extract_from_json import extract_from_json

import sys
import io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

import re
import requests

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

url = "https://en.wikipedia.org/w/api.php"
payload = {"action": "query",
           "titles": "File:{}".format(temp_dict[u"国旗画像"]),
           "prop": "imageinfo",
           "format": "json",
           "iiprop": "url"}

#requestsを用いたAPIの呼び出し
json_data = requests.get(url, params=payload).json()

#ここが良く分からない
def json_search(json_data):
    ret_dict = {}
    for k, v in json_data.items():
        if isinstance(v, list):
            for e in v:
                ret_dict.update(json_search(e))
        elif isinstance(v, dict):
            ret_dict.update(json_search(v))
        else:
            ret_dict[k] = v
    return ret_dict
    
print(json_search(json_data)["url"])


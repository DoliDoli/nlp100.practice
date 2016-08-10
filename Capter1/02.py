#!/usr/bin/env python3
# -*- coding: utf-8 -*-

s1="パトカー"
s2="タクシー"
s3=""
#zip関数　＝複数の引数を同時にループできる
#char 文字1文字の型
for char1, char2 in zip(s1, s2):
    s3 = s3 + char1 + char2

print(s3)
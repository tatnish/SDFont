#!/usr/bin/env python3
# coding: utf-8
# 
# This script outputs set of characters used by font_to_py.py
# Usage:
# python3 jisx0208.py > chars.txt 
# python3 font_to_py.py -k chars.txt <input ttf font name> <output.py>
# 
# Go visit: https://github.com/tatnish/micropython-font-to-py 
# for more detail converter info.
# 
# Note: JIS0208.TXT is available at:
#   http://unicode.org/Public/MAPPINGS/OBSOLETE/EASTASIA/JIS/JIS0208.TXT

jisx0208=[]
unicode=[]

with open("JIS0208.TXT", "r") as f:
    for line in f:
        if (not line[0] == "#"):
            _, jis, uni, __ = line.strip().split("\t")
            jisx0208.append(int(jis,16))
            unicode.append(int(uni,16))

# ASCII
for i in range(0x20,0x7F):
  print(chr(i),end="")

# Half-width kana
for i in range(0xFF61,0xFF9D):
  print(chr(i),end="")

# JIS X 0208
for i in jisx0208:
   print(chr(unicode[jisx0208.index(i)]), end="")


#!/usr/bin/env python
# -*- encoding: utf-8 -*-

import re
import os


def valueString(dic: dict, key: str):
    if key in dic:
        value = dic[key]
        if value != None and len(str(value)) > 0:
            return value
    return None


# path = os.path.abspath(".")
# path = os.path.join(path, "download/诸天至尊.txt")
# print(path)

# content = ""

# with open(path, 'rb') as f:
#     content = f.read().decode('utf-8')

# content = content.replace("正文_", "")
# replace_str = ""
# print(len(content))
# # dot1 = "…+"
# # content = re.sub(dot1, "...", content)
# # print(re.findall(dot1, content))

# pat = "[….晚安]*诸天至尊最新章节就来笔趣阁网址：Www.BiQuYun.Com"
# content = re.sub(pat, replace_str, content)
# print(len(re.findall(pat, content)))

# with open(path, 'wb') as f:
#     f.write(content.encode('utf-8'))

from qiqu.model import GMBookInfo

book = GMBookInfo()
book.url = "www.baiud.com"
book.des = "sadf"

# chapter = GMBookChapter(
# url="http://www.biquyun.com/20_20197/10054989.html")

# for name, value in vars(book).items():
#     print(name + " === " + value)


def eal_name(name: str):
    new_name = name
    if "_" in new_name:
        if new_name[0] == "_":
            index = 0
            for ele in new_name:
                if ele != "_":
                    break
                index += 1
            new_name = new_name[index:len(new_name)]
    return new_name


print(eal_name("_asdfas"))

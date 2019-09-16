#!/usr/bin/env python
# -*- encoding: utf-8 -*-

# import re

# list = "零一二三四五六七八九"
# unit = "十百千万"

# def replaceTitle(title_old):

#     title_new = ""
#     title_new_list = []
#     title_old_list = []

#     # 过滤掉高位为零的状况
#     for o in title_old:
#         if int(o) == 0 and len(title_old_list) == 0:
#             continue
#         title_old_list.append(o)

#     i = 0
#     for o in reversed(title_old_list):
#         str_2 = list[int(o)]
#         if (i - 1 >= len(unit)):
#             # 越界处理
#             return title_old
#         elif (i > 0) and str_2 != "零":
#             # 拼接单位 个位不拼接  其他位数字为0 不拼接
#             str_2 += unit[i - 1]

#         if i != 0 or (i == 0 and int(o) != 0):
#             title_new_list.append(str_2)
#         i += 1

#     # 拼接正确章节
#     last_str = ""
#     for o in reversed(title_new_list):
#         if (last_str == o and o == "零"):
#             continue
#         title_new += o
#         last_str = o

#     return title_new

# content = ""
# path = GMString.downloadTempFilePath("download", "很纯很暧昧", ".txt")
# print(path)
# with open(path, 'rb') as f:
#     content = f.read().decode('utf-8')

# pat = re.compile(r"[0-9]\d*")
# results = re.findall(pat, content)
# replace_results = {}

# for title_old in results:
#     replace_results[title_old] = replaceTitle(title_old)

# replace_key = []
# for key in replace_results.keys():
#     if key in replace_key:
#         continue
#     print(key + "    " + replace_results[key])

#     content = content.replace(key, "第" + replace_results[key] + "章")
#     replace_key.append(key)

# with open(path, 'wb') as f:
#     f.write(content.encode('utf-8'))

# from tkinter import *
# from tkinter import ttk


def test(*value):
    print(value)


class GMModels(object):
    list_xx: [] = None
    name = "123"

    def __getattribute__(self, name):
        # print("sadf")
        # if name == "list_xx":
        #     print("222")

        return super().__getattribute__(name)


if __name__ == "__main__":
    # # re_ret = re.search("第.+?章", "第1a123123章 望气第1a1231222223章 望气")
    # # print(re_ret)

    # mo = GMModels()
    # mo.name = "xxx"
    # mo.list_xx = ["as", "22"]
    # # print(mo.list_xx)

    # for (key, value) in vars(mo).items():
    #     print(key, "-----", value)

    # # top = Tk()
    # # btn = Button(top, text="几十个按钮")
    # # btn.pack()

    # sss = ttk.OptionMenu(top, StringVar())
    # sss.pack()
    # value222 = ("1", "2", "3")
    # print(*value222)
    # sss.set_menu("", *value222)

    # top.mainloop()

    stringss = ["s"]
    if stringss:
        print("sfd")
    else:
        print("22")

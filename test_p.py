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

# def test(*value):
#     print(value)

# class GMModels(object):
#     list_xx: [] = None
#     name = "123"

#     def __getattribute__(self, name):
#         # print("sadf")
#         # if name == "list_xx":
#         #     print("222")

#         return super().__getattribute__(name)

# from tkinter.constants import *

# def action(index):
#     print(str(index))

# import threading
# import time
# import queue

# def product(bq):
#     str_tuple = ("Python", "Kotlin", "Swift")
#     for i in range(99999):
#         print(threading.current_thread().name + "生产者准备生产元组元素！")
#         # 尝试放入元素，如果队列已满，则线程被阻塞
#         bq.put(str_tuple[i % 3])
#         print(threading.current_thread().name \
#             + "生产者生产元组元素完成！")

# def consume(bq):
#     while True:
#         time.sleep(15)
#         # 尝试取出元素，如果队列已空，则线程被阻塞
#         t = bq.get()
#         # print(threading.current_thread().name + "消费者准备消费元组元素！")

#         # print(threading.current_thread().name \
#         #     + "消费者消费[ %s ]元素完成！" % t)

# # 创建一个容量为1的Queue
# bq = queue.Queue(maxsize=1)
# # 启动3个生产者线程
# threading.Thread(target=product, args=(bq, )).start()
# threading.Thread(target=product, args=(bq, )).start()
# threading.Thread(target=product, args=(bq, )).start()
# # 启动一个消费者线程
# threading.Thread(target=consume, args=(bq, )).start()

# ssl._create_default_https_context = ssl._create_unverified_context()

# # h = urllib3.PoolManager(cert_reqs='CERT_REQUIRED', ca_certs=certifi.where())

# # os.path.abspath("certs.pem")
# h = urllib3.PoolManager()

# b = "http://www.baidu.com"
# b = "https://www.biquge.cm"
# rs = h.request('GET', b)

# print("typepepeepep = = ")
# print(rs.data.decode('GBK'))
# print("typepepeepep = = ")


class A:
    __lis_xx = ["1"]

    def prints(self):
        print("sadf")
        return
        print("123222")

        print("123")


if __name__ == "__main__":
    A().prints()

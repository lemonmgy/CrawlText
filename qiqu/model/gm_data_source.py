#!/usr/bin/env python
# -*- encoding: utf-8 -*-

from ..tool.gm_tools import GMKey


class GMDataSource(object):
    __data_list = []
    __data_dic = {}

    def append(self, ele, key):
        if ele in self.__data_list:
            return

        if not key or key in self.__data_dic:
            key = GMKey.key(key, len(self.__data_list))

        self.__data_list.append(ele)
        self.__data_dic[key] = ele

    def pop(self, ele=None, index=None, key=None):
        if not ele:
            if index and index >= 0 and index < len(self.__data_list):
                ele = self.__data_list[index]

        if not ele:
            if key and key in self.__data_dic:
                ele = self.__data_dic[key]
        self.__remove_obj(ele)

    def __remove_obj(self, ele=None):
        if ele:
            self.__data_list.remove(ele)
            re_key = None
            for key, value in self.__data_dic.items():
                if value == ele:
                    re_key = key
            if re_key:
                del self.__data_dic[re_key]
                # self.__data_dic.pop()

    def dataList(self):
        return self.__data_list

    def dataDic(self):
        return self.__data_dic


if __name__ == "__main__":

    data = GMDataSource()
    data.append("a", "2")
    data.append("b", "3")
    data.append("x", "4")
    data.append("v", "4")
    print(data.dataList())
    print(data.dataDic())

    # dicss = {"a": "2", "b": "3"}
    # if "a" in dicss:
    #     print("123123123z")
    # for key, value in dicss.items():
    #     print(key, value)
    # del dicss["b"]
    # print(dicss.pop("a", ["s"]))
    # print(dicss)

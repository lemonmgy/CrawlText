#!/usr/bin/env python
# -*- encoding: utf-8 -*-


class GMDataSource():
    __data_list: list
    __data_dict: dict

    def dataList(self):
        return self.__data_list

    def dataDict(self):
        return self.__data_dict

    def __init__(self, *args, **kwargs):
        self.__data_list = []
        self.__data_dict = {}
        super().__init__(*args, **kwargs)

    def add(self, key, value):
        if not key or not value:
            return
        self.__data_list.append(value)
        self.__data_dict[key] = value

    def pop(self, key):
        if not key:
            return
        value = None
        if key in self.__data_dict:
            value = self.__data_dict[key]
            del self.__data_dict[key]
        if value and value in self.__data_list:
            self.__data_list.remove(value)

    def clear(self):
        self.__data_list.clear()
        self.__data_dict.clear()

    def value(self, key):
        if key not in self.__data_dict:
            return None
        return self.__data_dict[key]

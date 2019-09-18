#!/usr/bin/env python
# -*- encoding: utf-8 -*-

import json


def gm_isinstance(obj, t):
    """ 判断主要归类到四种大类型 (str) (dict)
    (list, tuple, set) (int, float, bool, complex) """

    gm_lists = (list, tuple, set)
    gm_numbers = (str, int, float, bool, complex)

    if t == dict:
        return isinstance(obj, dict)
    elif (t in gm_lists):
        return isinstance(obj, gm_lists)
    elif (t in gm_numbers):
        return isinstance(obj, gm_numbers)


class GMJson(object):
    string: str = None
    json: dict = None
    model = None

    @staticmethod
    def loads(s: str):
        return json.loads(s)

    @staticmethod
    def dumps(obj, key: str = None):
        gm_json = GMJson()
        try:
            gm_json.model = obj
            gm_json.string = gm_json.any_to_json_str(obj)
            if gm_json.string:
                gm_json.json = json.loads(gm_json.string)
        except BaseException:
            print(
                "json转化失败  -------  \n object- %s  \n string- %s \n json - %s"
                % (gm_json.model, gm_json.string, gm_json.json))
            gm_json.model = None
            gm_json.string = None
            gm_json.json = None
        else:
            print("json转化成功")
        return gm_json

    # 传入一个对象转化为json字符串
    def any_to_json_str(self, obj, key: str = None):
        if not obj:
            return ""
        elif gm_isinstance(obj, str):
            return self.__to_json_string(obj)
        elif gm_isinstance(obj, list):
            return self.__list_to_json(obj)
        elif gm_isinstance(obj, dict):
            return self.__dict_to_json(obj)
        else:
            return self.__obj_to_json_str(obj, key)

    def __obj_to_json_str(self, obj, key: str = None):
        ret_str = ""
        for name_key, value in vars(obj).items():
            name = self.deal_name(name_key)
            pre = ""
            if len(ret_str) != 0:
                pre = ","
            if not value:
                value = ""

            if gm_isinstance(value, str):
                ret_str += pre + self.__to_json_string(
                    name) + ":" + self.__to_json_string(value)
            elif gm_isinstance(value, list):
                ret_str += pre + self.__to_json_string(name) + ":"
                ret_str += self.__list_to_json(value)
            elif gm_isinstance(value, dict):
                ret_str += pre + self.__to_json_string(name) + ":"
                ret_str += self.__dict_to_json(value)
            else:
                obj_str = self.any_to_json_str(value, name)
                if len(obj_str) != 0:
                    obj_str = obj_str[1:len(obj_str) - 1]
                    ret_str += pre + obj_str

        ret_str = "{" + ret_str + "}"

        if key:
            if len(key) != 0 and len(ret_str) != 0:
                return "{%s:%s}" % (self.__to_json_string(key), ret_str)
        return ret_str

    def __list_to_json(self, o_list):
        ret_str = ""
        for obj in o_list:
            pre = ","
            if len(ret_str) == 0:
                pre = "["
            ret_str += pre + self.any_to_json_str(obj)
        return "[]" if (len(ret_str) == 0) else (ret_str + "]")

    def __dict_to_json(self, dic: dict):
        ret_str = ""
        pre = ""
        for key, value in dic.items():
            if len(ret_str) != 0:
                pre = ","
            ret_str += pre + self.__to_json_string(key) + ":"
            ret_str += self.any_to_json_str(value)

        ret_str = "{" + ret_str + "}"
        return ret_str

    # 将key value转化为json字符
    def __to_json_string(self, content):
        def deal_character(content):
            return str(content).replace("\"", "”")

        return "\"" + deal_character(content) + "\""

    def deal_name(self, name):
        new_name_key = name
        if "_" in new_name_key:
            if new_name_key[0] == "_":
                index = 0
                for ele in new_name_key:
                    if ele != "_":
                        break
                    index += 1
                new_name_key = new_name_key[index:len(new_name_key)]
        return new_name_key

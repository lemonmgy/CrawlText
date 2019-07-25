#!/usr/bin/env python
# -*- coding: utf-8 -*-

import re
import json


def rapidly_generated_dict(value):
    pass


# 多处替换文本
def replace(content: str, rep: [], be_rep):
    for a in rep:
        content = content.replace(a, be_rep)
    return content


# 转json
def to_json_string(content):
    return "\"" + str(content) + "\""


def obj_to_json(obj, key: str = None):
    if obj == None:
        return ""
    elif isinstance(obj, str) == True:
        return obj
    elif isinstance(obj, list) == True:
        return list_to_json(obj)
    elif isinstance(obj, dict) == True:
        return dict_to_json(obj)
    else:
        ret_str = ""
        for name, value in vars(obj).items():
            pre = ""
            if len(ret_str) != 0:
                pre = ","
            if value == None:
                value = ""

            if isinstance(value, str):
                ret_str += pre + to_json_string(name) + ":" + to_json_string(
                    value)
            elif isinstance(value, list):
                ret_str += pre + to_json_string(name) + ":"
                ret_str += list_to_json(value)
            elif isinstance(value, dict):
                ret_str += pre + to_json_string(name) + ":"
                ret_str += dict_to_json(value)
            else:
                obj_str = obj_to_json(value, name)
                if len(obj_str) != 0:
                    obj_str = obj_str[1:len(obj_str) - 1]
                    ret_str += pre + obj_str

        ret_str = "{" + ret_str + "}"

        if key != None:
            if len(key) != 0 and len(ret_str) != 0:
                return "{%s:%s}" % (to_json_string(key), ret_str)
        return ret_str


def list_to_json(o_list):
    ret_str = ""
    for obj in o_list:
        pre = ","
        if len(ret_str) == 0:
            pre = "["
        ret_str += pre + obj_to_json(obj)
    return "[]" if (len(ret_str) == 0) else (ret_str + "]")


def dict_to_json(dic: dict):
    ret_str = ""
    pre = ""
    for key, value in dic.items():
        if len(ret_str) != 0:
            pre = ","
        ret_str += pre + to_json_string(key) + ":"
        if isinstance(value, str):
            ret_str += to_json_string(value)
        elif isinstance(value, list):
            ret_str += list_to_json(value)
        elif isinstance(value, dict):
            ret_str += dict_to_json(value)
        else:
            ret_str += obj_to_json(value)

    ret_str = "{" + ret_str + "}"

    return ret_str


# 可以数组，或者字符串
def remove_tag(content, tags):
    ret = str(content)
    if isinstance(tags, str):
        ret = ret.replace('<%s>' % str(tags), "")
        ret = ret.replace('</%s>' % str(tags), "")
    elif isinstance(tags, list) == True:
        for tag in tags:
            ret = ret.replace('<%s>' % tag, "")
            ret = ret.replace('</%s>' % tag, "")
    return ret


def remove_escape_character(content, include_garbage_character: bool = False):
    ret = str(content)
    pat = re.compile(r"&#.+?;")
    search_ret = re.findall(pat, ret)
    if search_ret != None:
        for b in search_ret:
            ret = ret.replace(b, "")
    if include_garbage_character == True:
        ret = remove_garbage_character(content)

    return ret


def remove_garbage_character(content: str):
    char_sys = ['\n', '<br>']
    # for s in char_sys:
    #     content = replace(content,
    #                       re.compile(r'%s+' % (s)).findall(content), s)
    return replace(content, char_sys + ["　", " ", "\xa0"], "")

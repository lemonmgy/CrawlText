#!/usr/bin/env python
# -*- encoding: utf-8 -*-


def valueString(dic: dict, key: str):
    if key in dic:
        value = dic[key]
        if value != None and len(str(value)) > 0:
            return value
    return None


ss: tuple = (3, 4)
print(len(ss))
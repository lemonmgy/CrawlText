#!/usr/bin/env python
# -*- encoding: utf-8 -*-

if __name__ == "__main__":
    ret = {"2": "s", "0": "s"}


class GMValue(object):
    @classmethod
    def valueList(cls, oData: dict, key_str: str):
        return cls.value(oData, key_str, list)

    @classmethod
    def valueDict(cls, oData: dict, key_str: str, value_type=str):
        return cls.value(oData, key_str, dict)

    @classmethod
    def valueStirng(cls, oData: dict, key_str: str, value_type=str):
        return cls.value(oData, key_str, str)

    @classmethod
    def value(cls, oData: dict, key_str: str, value_type=None):
        # 处理结果类型
        if value_type:
            if not isinstance(value_type, type):
                value_type = type(value_type)

        # 是否有有效值
        def is_valid_value(v_value, v_type):
            return v_value and isinstance(v_value, v_type) and len(v_value) > 0

        # 处理值  类型 处理，
        def deal_ret_value(v_ret, v_type: type = None):
            if v_type and not isinstance(v_ret, v_type):
                v_ret = v_type()
            return v_ret

        def obtainValue(dic: dict, key: str):
            if isinstance(key, str) and key in dic:
                return dic[key]
            else:
                return None

        # 判断是否为有效值
        if not is_valid_value(oData, dict) or not is_valid_value(key_str, str):
            return deal_ret_value(None)

        ret_list = []

        def getValue(dic: dict, key: str):
            key_list = key
            if "," in key:
                key_list = key.split(",")
                for k in key_list:
                    getValue(dic, k)
            elif ":" in key:
                sub_key = key.split(":", 1)
                first_key = sub_key[0]
                getValue(deal_ret_value(obtainValue(dic, first_key), dict),
                         sub_key[-1])
            else:
                ret_list.append(
                    deal_ret_value(obtainValue(dic, key), value_type))

        getValue(oData, key_str)
        if len(ret_list) == 0:
            return deal_ret_value(None, value_type)
        elif len(ret_list) == 1:
            return ret_list[0]
        else:
            return ret_list


if __name__ == "__main__":
    l = list()
    l.append("s")
    if l:
        print("if")
    else:
        print("else")

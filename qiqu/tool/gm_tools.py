#!/usr/bin/env python
# -*- coding: utf-8 -*-

import re


class GMTools(object):
    @classmethod
    def key(self, data, defaultKey: str, addkey: str = None):
        """
        将 数组、元组的元素 or 字典的key 处理为唯一值，
        默认key  addkey后面追加的key
        """
        def __key(data, defaultKey, addkey):
            if defaultKey in data:
                defaultKey = ("" if len(defaultKey) == 0 else
                              (defaultKey + "_")) + addkey
                return __key(data, defaultKey, addkey)
            else:
                return defaultKey

        # 判断data是否满足条件
        if not isinstance(data, list) and not isinstance(
                data, tuple) and not isinstance(data, dict):
            return defaultKey

        if not isinstance(addkey, str) or len(addkey) == 0:
            addkey = "0"
        return __key(data, defaultKey, addkey)

    @classmethod
    def multiple_replace(self, content: str, rep=None, re_str: str = None):
        """多处替换文本"""
        if not rep or not isinstance(re_str, str):
            return content
        if isinstance(rep, str):
            content = content.replace(rep, re_str)
        elif isinstance(rep, (list, tuple, set)):
            for a in rep:
                content = content.replace(a, re_str)

        return content

    @classmethod
    def remove_tag(self, content, tags):
        """
        移除闭合标签 可以数组，或者字符串
        """
        ret = str(content)
        if isinstance(tags, str):
            ret = ret.replace('<%s>' % str(tags), "")
            ret = ret.replace('</%s>' % str(tags), "")
        elif isinstance(tags, list):
            for tag in tags:
                ret = ret.replace('<%s>' % tag, "")
                ret = ret.replace('</%s>' % tag, "")
        return ret

    @classmethod
    def remove_escape_character(self,
                                content,
                                include_garbage_character: bool = False):
        """移除html符号  """
        ret = str(content)
        pat = re.compile(r"&#.+?;")
        search_ret = re.findall(pat, ret)
        if not search_ret:
            for b in search_ret:
                ret = ret.replace(b, "")
        if include_garbage_character:
            ret = self.remove_garbage_character(content)
        return ret

    @classmethod
    def remove_garbage_character(self, content: str):
        """移除空格换行等符号"""
        char_sys = ['\n', '<br>']
        # for s in char_sys:
        #     content = replace(content,
        #                       re.compile(r'%s+' % (s)).findall(content), s)
        return self.multiple_replace(content, char_sys + ["　", " ", "\xa0"],
                                     "")


if __name__ == "__main__":
    string_ss = "asndfk123d123d323"
    print(GMTools.multiple_replace(string_ss, ["123", "a"], ""))

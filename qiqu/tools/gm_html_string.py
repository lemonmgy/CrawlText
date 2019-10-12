#!/usr/bin/env python
# -*- encoding: utf-8 -*-

import re


class GMHtmlString():
    @classmethod
    def remove_tag(self, content):
        """
        移除闭合标签 可以数组，或者字符串
        """
        ret = str(content)
        pat = re.compile('<[^\u4e00-\u9fa5]*?>|<|>')
        return re.sub(pat, "", ret)

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
        char_sys = ['\n', '<br>'] + ["　", " ", "\xa0"]
        for s in char_sys:
            # content = replace(content,
            # re.compile(r'%s+' % (s)).findall(content), s)
            content = content.replace(s, "")
        return content

    @classmethod
    def conversion_title(cls, ostr: str = ""):
        if not ostr:
            return ""

        dic = {
            "0": "零",
            "1": "一",
            "2": "二",
            "3": "三",
            "4": "四",
            "5": "五",
            "6": "六",
            "7": "七",
            "8": "八",
            "9": "九"
        }
        uni_list = ["", "十", "百", "千", "万", "十万", "百万", "千万", "亿"]

        li = list(ostr)
        li.reverse()
        uni = 0
        ret_str = []
        for x in li:
            if x not in dic:
                ret_str.append(x)
                continue

            if "章" not in ret_str:
                ret_str.append("章")
            o_x = dic[x]

            if len(ret_str) == 0 and o_x == "零":
                o_x = ""

            if len(o_x):
                if o_x != "零":
                    o_x += uni_list[uni]
                ret_str.append(o_x)
            uni += 1
        ret_str.reverse()
        ret_str = "".join(ret_str)
        if "第" not in ret_str:
            ret_str = "第" + ret_str
        return ret_str

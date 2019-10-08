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
        pat = re.compile('<.*?>')
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

#!/usr/bin/env python
# -*- coding: utf-8 -*-

import re


class GMBookChapter(object):
    book_name = ""
    title = ""  # 最新标题
    # url = ""  # 最新文章地址
    pre_url = ""  # 前一个文章地址
    suf_url = ""  # 后一个文章地址
    date = ""  # 章节日期
    content = ""
    chapter_id = ""

    def __init__(self, *args, **kwargs):
        if "url" in kwargs:
            self.url = kwargs["url"]
        super().__init__()

    @property
    def url(self):
        return self._url

    @url.setter
    def url(self, value):
        if not isinstance(value, str):
            raise TypeError('Expected a string')

        self._url = value

        chapter_id = ""
        ret = re.search("[0-9]+.html", value)

        if isinstance(ret, re.Match):
            chapter_id = ret.group()
        else:
            value_splist = value.split("/")
            chapter_id = value_splist[-1] if len(value_splist) != 0 else ""
        self.chapter_id = chapter_id.replace(".html", "")

    @url.deleter
    def url(self):
        raise AttributeError("Can't delete attribute")


class GMBookInfo(object):
    name = ""  # 书名
    book_id = ""  # 书籍类型
    img = ""  # 图片
    author = ""  # 作者
    des = ""  # 描述
    book_type = ""  # 书籍类型
    new_chapter: GMBookChapter
    chapter_list: []

    def __init__(self, url=""):
        pass

    @property
    def url(self):
        return self._url

    @url.setter
    def url(self, value):
        if not isinstance(value, str):
            raise TypeError('Expected a string')
        self._url = value
        ret_search = re.search("[0-9]+_[0-9]+", value)
        if ret_search:
            self.book_id = ret_search.group()
        if len(self.book_id) > 1:
            self.book_id = value.split(".com/")[-1].replace("/", "")

    @url.deleter
    def url(self):
        raise AttributeError("Can't delete attribute")


class GMModuleBook(object):
    book_category_des = ""
    top_book: GMBookInfo
    book_list: []


class GMResponse(object):
    url = ""
    status = ""
    data = ""


if __name__ == "__main__":
    book = GMBookInfo()
    book.url = "www.baiud.com"
    # chapter = GMBookChapter(
    # url="http://www.biquyun.com/20_20197/10054989.html")
    print(book.url)

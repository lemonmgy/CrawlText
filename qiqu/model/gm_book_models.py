#!/usr/bin/env python
# -*- coding: utf-8 -*-

import re

from ..tools import GMNovelHttp


class GMBookChapter(object):
    chapter_url = ""
    book_id = ""
    chapter_id = ""
    chapter_title = ""  # 最新标题
    date = ""  # 章节日期
    content = ""

    def url_with_chapter_id(self, value: str, host: str = None):
        """
        通过连接中获取 chapter_id
        """
        if not value or not isinstance(value, str):
            return
        if not value.startswith('http'):
            value = GMNovelHttp.append_bqg_host(value)
        self.chapter_url = value

        # https://www.biquge.cm/7/7760/6549010.html
        ret_search = re.search(r'[0-9]+/[0-9]+/[0-9]+.html', value)
        if ret_search:
            id_list = ret_search.group().split("/")
            self.chapter_id = id_list[-1]
            self.chapter_id.replace(".html", "")

            del id_list[-1]
            self.book_id = "/".join(id_list)

        ret_search = re.search(r'[0-9]+.html', value)
        if ret_search:
            self.chapter_id = ret_search.group().replace(".html", "")


class GMBookInfo(object):
    book_url = ""
    book_id = ""  # 书籍类型
    book_name = ""  # 书名
    author = ""  # 作者
    img = ""  # 图片
    des = ""  # 描述
    book_type = ""  # 书籍类型
    new_chapter: GMBookChapter
    chapter_list: []

    def url_with_book_id(self, value: str):
        """
        通过连接中获取 book_id
        """

        if not isinstance(value, str):
            return
        self.book_url = value
        if ".html" in value:
            # https://www.biquge.cm/7/7760/6549010.html
            ret_search = re.search(r'[0-9]+/[0-9]+/[0-9]+.html', value)
            if ret_search:
                id_list = ret_search.group().split("/")
                del id_list[-1]
                self.book_id = "/".join(id_list)
        else:
            # https://www.biquge.cm/7/7760/
            ret_search = re.search(r'[0-9]+/[0-9]+', value)
            if ret_search:
                id_list = ret_search.group().split("/")
                self.book_id = "/".join(id_list)


class GMModuleBook(object):
    book_category_des = ""
    top_book: GMBookInfo
    book_list: []

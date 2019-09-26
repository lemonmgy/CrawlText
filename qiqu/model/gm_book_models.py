#!/usr/bin/env python
# -*- coding: utf-8 -*-

import re
from gmhelper import GMHTTP


class GMBookChapter(object):
    chapter_url = ""
    book_id = ""
    chapter_id = ""
    chapter_title = ""  # 最新标题
    date = ""  # 章节日期
    content = ""

    def url_with_chapter_id(self, chapter_url: str, host: str = None):
        """
        通过连接中获取 chapter_id
        """
        if not chapter_url or not isinstance(chapter_url, str):
            return

        def regular_chapter_id(value):
            ret_search = re.search(r'[0-9]+.html', value)
            chapter_id = None
            if ret_search:
                chapter_id = ret_search.group().replace(".html", "")
            return chapter_id

        def regular_book_id(value, ishost=False):
            # https://www.biquge.cm/7/7760/6549010.html
            if ishost:
                ret_search = re.search(r'm/[0-9]+/[0-9]+', value)
                if ret_search:
                    id_list = ret_search.group().split("/")
                    del id_list[0]
                    return "/".join(id_list)
            else:
                ret_search = re.search(r'[0-9]+/[0-9]+/[0-9]+.html', value)
                if ret_search:
                    id_list = ret_search.group().split("/")
                    del id_list[-1]
                    return "/".join(id_list)

            return None

        self.chapter_id = regular_chapter_id(chapter_url)

        if chapter_url.startswith('http'):
            self.book_id = regular_book_id(chapter_url)
            self.chapter_url = chapter_url
        elif chapter_url and host:
            url_book_id = regular_book_id(chapter_url)
            host_book_id = regular_book_id(host, True)
            if self.chapter_id and host_book_id:
                # https://www.biquge.cm/7/7760 7/7760/6549010.html
                self.book_id = host_book_id
                self.chapter_url = GMHTTP.appen_url(
                    [host, self.chapter_id + '.html'])
            elif url_book_id and not host_book_id:
                self.book_id = url_book_id
                self.chapter_url = GMHTTP.appen_url([host, chapter_url])


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

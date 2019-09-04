#!/usr/bin/env python
# -*- coding: utf-8 -*-


class GMBookChapter(object):
    book_name = ""
    title = ""  # 最新标题
    url = ""  # 最新文章地址
    pre_url = ""  # 前一个文章地址
    suf_url = ""  # 后一个文章地址
    date = ""  # 章节日期
    content = ""


class GMBookInfo(object):
    name = ""  # 书名
    url = ""  # 地址
    book_id = ""  # 书籍类型
    img = ""  # 图片
    author = ""  # 作者
    des = ""  # 描述
    book_type = ""  # 书籍类型
    new_chapter: GMBookChapter
    chapter_list: []


class GMModuleBook(object):
    book_category_des = ""
    top_book: GMBookInfo
    book_list: []


class GMResponse(object):
    url = ""
    status = ""
    data = ""


class GMDownloadRequest:
    url = ""
    book_id = ""

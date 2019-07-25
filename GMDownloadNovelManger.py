#!/usr/bin/env python
# -*- coding: utf-8 -*-

import GMCrawlWebDataManger
from GMCrawlWebModels import GMBookChapter
import GMDocumentManger
import threading

from multiprocessing import Process


def download_novel_list_style(url: str = "", book_id: str = "", callback=None):
    # 线程
    t = threading.Thread(
        target=download_novel_with_list_style,
        kwargs={
            "url": url,
            "book_id": book_id,
            "callback": callback
        },
        name="download_novel_list_style")
    t.start()


def download_novel_with_list_style(url: str = "",
                                   book_id: str = "",
                                   callback=None):

    ret = GMCrawlWebDataManger.getNovelListData(url, book_id)
    if ret == None:
        print("获取小说信息失败！！！")
    else:
        json_dic = ret[-1]
        if json_dic != None:
            chapter_list = json_dic['chapter_list']
            book_name = json_dic['name']
            chapter_title = ""
            chapter_content = ""
            for ele_book_info in chapter_list:
                chapter_title = ele_book_info["title"]
                chapter_info = GMCrawlWebDataManger.getNovelContentData(
                    ele_book_info["url"])

                if chapter_info != None:
                    chapter_info_dic = chapter_info[-1]
                    chapter_title = chapter_info_dic["title"]
                    chapter_content = chapter_info_dic["content"]
                    if book_name == None or len(book_name) == 0:
                        book_name = chapter_info_dic["book_name"]

                path = GMDocumentManger.downloadFilePath(
                    'download', book_name, '.txt')
                if path == None:
                    print("书名有问题!")
                    if callback != None:
                        callback(code=201, book_url=url)
                    return
                GMDocumentManger.appendContent(
                    path, (chapter_title + "\n" + chapter_content))
                print(chapter_title)
                if callback != None:
                    callback(chapter_info[0])

            if callback != None:
                callback(code=200, book_url=url)

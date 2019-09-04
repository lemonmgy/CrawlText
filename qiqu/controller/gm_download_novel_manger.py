#!/usr/bin/env python
# -*- coding: utf-8 -*-

import threading
from multiprocessing import Process

from .gm_crawl_web_data_manger import GMCrawlWebDataManger
from .gm_document_manger import GMDocumentManger
from ..model import GMBookChapter, GMDownloadRequest


class GMDownloadNovelManger(object):
    __download_map = []

    __state = {}

    def __new__(cls, *args, **kwargs):
        ob = super(GMDownloadNovelManger, cls).__new__(cls, *args, **kwargs)
        ob.__dict__ = cls.__state
        return ob

    @classmethod
    def add_download_novel(self,
                           request: GMDownloadRequest = None,
                           callback=None):
        manger = GMDownloadNovelManger()
        if len(manger.__download_map) >= 3:
            print("下载数量达到最大")
            return
        task = GMDownloadNovelTask()
        manger.__download_map.append(task)
        task.start_download(request, callback)


# dmanger = GMDownloadNovelManger()


class GMDownloadNovelTask(object):
    def start_download(self, request: GMDownloadRequest = None, callback=None):
        # 线程
        t = threading.Thread(
            target=self.download_novel_with_list_style,
            kwargs={
                "request": request,
                "callback": callback
            },
            name="download_novel_list_style")
        t.start()

    def download_novel_with_list_style(self,
                                       request: GMDownloadRequest = None,
                                       callback=None):
        url = request.url
        book_id = request.book_id
        # 或取消说首页内容
        ret = GMCrawlWebDataManger.getNovelListData(url, book_id)

        json_dic = {}
        if ret != None and len(ret) == 3:
            json_dic = ret[-1]

        if json_dic == None or len(json_dic) == 0:
            print("获取小说信息失败！！！")
        else:
            chapter_list = json_dic['chapter_list']
            book_name = json_dic['name']
            path = ""

            # 章节列表
            for ele_book_info in chapter_list:
                chapter_title = ele_book_info["title"]
                # 获取章节内容
                chapter_info = GMCrawlWebDataManger.getNovelContentData(
                    ele_book_info["url"])

                if chapter_info == None or len(chapter_info) != 3:
                    print(chapter_title + "——下载失败，获取html出错")
                else:
                    chapter_info_dic = chapter_info[-1]
                    # chapter_title = chapter_info_dic["title"]
                    chapter_content = chapter_info_dic["content"]

                    # 创建路径
                    if len(path) <= 0:
                        if book_name == None or len(book_name) == 0:
                            book_name = chapter_info_dic["book_name"]

                        # 获取路径
                        path = GMDocumentManger.downloadFilePath(
                            'qiqu/0_download', book_name, '.txt')
                        if path == None:
                            print("获取" + book_name + "路径失败!")
                            if callback != None:
                                callback(code=201, book_url=url)
                            return

                    # 追加内容到文本中
                    GMDocumentManger.appendContent(
                        path, (chapter_title + "\n" + chapter_content))
                    print(chapter_title + "——下载完成")

                # 向上层跑出结果
                if callback != None:
                    callback(chapter_info[0])

            if callback != None:
                callback(code=200, book_url=url)

#!/usr/bin/env python
# -*- coding: utf-8 -*-

import threading, os, shutil
from multiprocessing import Process

from .gm_crawl_web_data_manger import GMCrawlWebDataManger
from .gm_document_manger import GMDocumentManger
from ..model import GMBookChapter
from ..model import GMDownloadStatus, GMDownloadRequest, GMDownloadCallback


class GMDownloadNovelManger(object):
    __max_count = 3
    __download_map = {}
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
        task_id = self.task_id(request)

        if task_id in self.__download_map:
            # 任务列表中存在
            GMDownloadCallback.callback(GMDownloadStatus.download_exist,
                                        "正在下载中。。。", None, callback)
        elif len(manger.__download_map) >= manger.__max_count:
            # 任务达到最大数
            GMDownloadCallback.callback(GMDownloadStatus.download_max,
                                        "下载数量达到最大！", None, callback)
        else:
            # 开始任务
            task = GMDownloadNovelTask()
            manger.__download_map[task_id] = task
            task.start_download(request, callback)

    @classmethod
    def task_id(self, request: GMDownloadRequest):
        task_id = ""
        if request.book_id != None and len(request.book_id):
            task_id = request.book_id
        if request.url != None and len(request.url):
            task_id = request.url
        return "00_00" if len(task_id) == 0 else task_id


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

    def download_new_book(self, path, book_id, book_name):
        file_name = self.__download_info_file_name(book_id, book_name)
        info_path = GMDocumentManger.downloadTempFilePath(file_name, '.txt')
        if os.path.exists(info_path):
            os.remove(info_path)

    def __download_info_file_name(self, book_id, book_name):
        return book_name + "_" + book_id + ""

    def download_novel_with_list_style(self,
                                       request: GMDownloadRequest = None,
                                       callback=None):
        def dealcallback(
                code: GMDownloadStatus = GMDownloadStatus.error_unknown,
                msg: str = "",
                data=None):
            if code != GMDownloadStatus.success_book and data != None:
                pass
            GMDownloadCallback.callback(code, msg, data, callback)

        url = request.url
        book_id = request.book_id
        # 或取消说首页内容
        ret = GMCrawlWebDataManger.getNovelListData(url, book_id)

        book_dic = {}
        if ret != None and len(ret) == 3:
            book_dic = ret[-1]

        if book_dic == None or len(book_dic) == 0:
            msg = "获取小说信息失败！！！"
            print(msg)
            dealcallback(GMDownloadStatus.error_path, msg)
        else:
            chapter_list = book_dic['chapter_list']
            chapter_no_download_list: list = chapter_list

            book_name = book_dic['name']
            path = ""
            path_info = ""

            chapter_list = chapter_list[1:10]

            # 章节列表
            for ele_chapter_info in chapter_list:
                chapter_title = ele_chapter_info["title"]
                # 获取章节内容
                chapter_info = GMCrawlWebDataManger.getNovelContentData(
                    ele_chapter_info["url"])

                if chapter_info == None or len(chapter_info) != 3:
                    print(chapter_title + "——下载失败，获取html出错")
                else:
                    chapter_info_dic = chapter_info[-1]
                    # chapter_title = chapter_info_dic["title"]
                    chapter_content = chapter_info_dic["content"]

                    if book_name == None or len(book_name) == 0:
                        book_name = chapter_info_dic["book_name"]

                    # 创建路径
                    if len(path) <= 0:
                        # 获取路径
                        path = GMDocumentManger.downloadTempFilePath(
                            book_name, '.txt')
                        if not os.path.exists(path):
                            GMDocumentManger.replaceContent(path, "")
                        if not os.path.exists(path):
                            dealcallback(GMDownloadStatus.error_path,
                                         "获取" + book_name + "路径失败!")
                            return

                    if len(path_info) <= 0:
                        path_info = GMDocumentManger.downloadTempFilePath(
                            self.__download_info_file_name(book_id, book_name),
                            "txt")

                    # 追加内容到文本中
                    GMDocumentManger.appendContent(
                        path, (chapter_title + "\n" + chapter_content))
                    # 描述文件更替
                    chapter_no_download_list.remove(ele_chapter_info)
                    GMDocumentManger.replaceContent(path_info,
                                                    chapter_no_download_list)

                    print(chapter_title + "——下载完成")

                # 向上层跑出结果
                dealcallback(GMDownloadStatus.success_chapter,
                             "获取 " + chapter_title + " 成功", ele_chapter_info)

            # 下载完成
            dealcallback(GMDownloadStatus.success_book,
                         "获取 " + chapter_title + " 成功", book_dic)
            # 下载完成移动为指导download文件夹下
            shutil.move(path, GMDocumentManger.downloadFilePath())
            # 删除记录文件
            os.remove(path_info)

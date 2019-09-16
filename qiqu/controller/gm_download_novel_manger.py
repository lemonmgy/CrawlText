#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import threading
import shutil
import re
# from multiprocessing import Process

from .gm_crawl_web_data_manger import GMCrawlWebDataManger
from ..tool import GMFileManger, GMPath, GMJson, GMKey
from ..model import GMBookChapter, GMBookInfo
from ..model import GMDownloadStatus, GMDownloadResponse
from ..model import GMDownloadRequest

from gmhelper import GMValue


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
        # 创建任务唯一key
        if not request.request_id:
            request.request_id = request.book_id
        request.request_id = GMKey.key(self.__download_map, request.request_id)

        manger = GMDownloadNovelManger()
        print("len(manger.__download_map) = " +
              str(len(manger.__download_map)))
        response = GMDownloadResponse(request, callback)
        if not request or not request.request_id:
            response.call(GMDownloadStatus.download_error, "任务id出错")
        elif request.request_id in self.__download_map:
            # 任务列表中存在
            response.call(GMDownloadStatus.download_error, "正在下载中。。。")
        elif len(manger.__download_map) >= manger.__max_count:
            # 任务达到最大数
            response.call(GMDownloadStatus.download_error, "下载数量达到最大！")
        else:
            # 开始任务
            task = GMDownloadNovelTask(manger.callback_manager)
            manger.__download_map[request.request_id] = task
            task.start_download(request, callback)

    def callback_manager(self, response: GMDownloadResponse):
        if response.code != GMDownloadStatus.downloading_chapter:
            if response.request and response.request.request_id:
                del self.__download_map[response.request.request_id]
        response.call()


class GMDownloadNovelTask(object):
    response_data: dict
    response: GMDownloadResponse = None
    callback_manager = None

    def __init__(self, callback_manager=None, *args, **kwargs):
        self.callback_manager = callback_manager
        super().__init__(*args, **kwargs)

    def start_download(self, request: GMDownloadRequest = None, callback=None):
        """
        开始下载任务
        """
        self.response_data = {}
        self.response = GMDownloadResponse(request, callback)
        t = threading.Thread(
            target=self.__download_novel_with_list_style,
            kwargs={"request": request},
            name="__download_novel_with_list_style" + request.request_id)
        t.start()

    def download_new_book(self, path, book_id, book_name):
        file_name = self.__download_info_file_name(book_id, book_name)
        info_path = GMPath.downloadTempFilePath(file_name, '.txt')
        if os.path.exists(info_path):
            os.remove(info_path)

    def __callback(self,
                   code=GMDownloadStatus.download_error,
                   msg: str = None,
                   progress: str = None):
        self.response_data["progress"] = progress
        if self.callback_manager:
            self.response.code = code
            self.response.msg = msg
            self.response.data = self.response_data
            self.callback_manager(self.response)
        else:
            self.response.call(code, msg, self.response_data)

    def __download_info_file_name(self, book_id, book_name):
        return book_name + "_" + book_id + ""

    def __download_novel_with_list_style(self,
                                         request: GMDownloadRequest = None):
        url = request.url
        book_id = request.book_id

        self.response_data["name"] = GMValue.valueStirng(request.extra, "name")

        # 开始下载章节
        self.__callback(GMDownloadStatus.downloading_chapter, "获取小说信息...")

        # 或取消说首页内容
        gmJsonModel: GMJson = GMCrawlWebDataManger.getNovelListData(
            url, book_id)
        bookModel: GMBookInfo = None

        if gmJsonModel and gmJsonModel.model:
            bookModel: GMBookInfo = gmJsonModel.model

        if not bookModel or not isinstance(
                bookModel, GMBookInfo) or not bookModel.chapter_list:
            self.__callback(GMDownloadStatus.download_error, "获取小说信息失败！！！")
        else:
            self.response_data["name"] = bookModel.name
            self.response_data["author"] = bookModel.author
            self.response_data["url"] = bookModel.url
            self.response_data["book_id"] = bookModel.book_id

            index = 0
            all_count = len(bookModel.chapter_list)

            book_name = bookModel.name
            path = ""
            path_info = ""

            #swarning test code
            # chapter_list = chapter_list[1:6]
            self.__callback(GMDownloadStatus.downloading_chapter, "开始下载...")

            for ele_chapter in bookModel.chapter_list:  # 章节列表

                # 获取章节内容
                chapter_data = GMCrawlWebDataManger.getNovelContentData(
                    ele_chapter.url, book_id, ele_chapter.chapter_id)
                chapterModel: GMBookChapter = chapter_data.model
                chapter_title = ele_chapter.title
                if not chapter_title:
                    chapter_title = chapterModel.title

                if not chapterModel:
                    print(chapter_title + "——下载失败，获取html出错")
                else:
                    if not book_name:
                        book_name = chapterModel.book_name

                    # 创建路径
                    if len(path) <= 0:
                        path = GMPath.downloadTempFilePath(book_name, '.txt')
                        path_info = GMPath.downloadTempFilePath(
                            self.__download_info_file_name(book_id, book_name),
                            "txt")
                        if os.path.exists(path) and os.path.exists(path_info):
                            # 两个文件都存在，继续下载内容 未完成
                            pass
                        elif not os.path.exists(path) or not os.path.exists(
                                path_info):
                            # 有一个不存在，都删除了重新下载
                            if os.path.exists(path):
                                os.remove(path)
                            if os.path.exists(path_info):
                                os.remove(path_info)

                    # 追加内容到文本中
                    GMFileManger.appendContent(
                        path, (chapter_title + "\n" + chapterModel.content))
                    # 描述文件更替 待开启
                    # GMFileManger.replaceContent(path_info,
                    # chapter_no_download_list)

                # 向上层跑出结果
                re_ret = re.search("第.+?章", chapter_title)
                if re_ret:
                    chapter_title = re_ret.group()
                progress = "-".join(
                    [book_name, chapter_title,
                     str(index),
                     str(all_count)])
                # 处理打印文案
                print(index)
                self.__callback(
                    GMDownloadStatus.downloading_chapter,
                    chapter_title + "——下载完成 url：" + ele_chapter.url, progress)
                index += 1

            # 下载完成
            # 删除记录文件
            if os.path.exists(path_info):
                os.remove(path_info)

                # 下载完成移动为指导download文件夹下
                down_file_path = GMPath.downloadFilePath(book_name, '.txt')

                if os.path.exists(down_file_path):
                    os.remove(down_file_path)

                if os.path.exists(path):
                    shutil.move(path, GMPath.downloadFilePath())
                else:
                    print("下载文件不存在 移动到对应位置 失败")

                print("下载完成， 移动到对应位置 成功")

            self.__callback(GMDownloadStatus.download_success,
                            book_name + "全书下载完成")

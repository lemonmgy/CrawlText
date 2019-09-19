#!/usr/bin/env python
# -*- coding: utf-8 -*-

import re
import os
import shutil

from .gm_biquge_request import GMBiqugeRequest

from ..tools import GMDownloadCache

from ..model import GMBookChapter, GMBookInfo
from ..model import GMDownloadStatus, GMDownloadResponse
from ..model import GMDownloadRequest

from gmhelper import GMValue, GMJson, GMFileManager
from gmhelper import GMThreading


class GMDownloadNovelManager(object):
    __max_count = 3
    __download_map = {}
    __state = {}

    def __new__(cls, *args, **kwargs):
        ob = super(GMDownloadNovelManager, cls).__new__(cls, *args, **kwargs)
        ob.__dict__ = cls.__state
        return ob

    @classmethod
    def add_download_novel(self, request: GMDownloadRequest = None):
        # 创建任务唯一key
        manger = GMDownloadNovelManager()

        msg = None
        if not request or not request.book_url:
            msg = "任务id出错"
        elif request.book_url in self.__download_map:
            # 任务列表中存在
            msg = "正在下载中。。。"
        elif len(manger.__download_map) >= manger.__max_count:
            # 任务达到最大数
            msg = "下载数量达到最大！"

        if msg:
            request.call(GMDownloadStatus.error, msg)
        else:
            # 开始任务
            manger.__download_map[
                request.book_url] = GMDownloadNovelTask.start(
                    request, manger.callback_manager)

    def callback_manager(self, response: GMDownloadResponse):
        if response and response.book_url\
           and response.code != GMDownloadStatus.downloading:
            del self.__download_map[response.book_url]


class GMDownloadNovelTask(object):
    manager_callback = None
    request: GMDownloadRequest = None
    response_data: dict = None

    @classmethod
    def start(cls, request: GMDownloadRequest = None, manager_callback=None):
        """
        开始下载任务
        """
        task = GMDownloadNovelTask()
        task.manager_callback = manager_callback
        task.request = request
        task.response_data = {}
        GMThreading.start(task.__download_novel_with_list_style,
                          "download_" + request.book_url,
                          request=request)
        return task

    def __callback(self, code=GMDownloadStatus.error, msg: str = ""):
        response = GMDownloadResponse(self.request.book_url, code, msg,
                                      self.response_data)
        if self.manager_callback:
            self.manager_callback(response)
        self.request.call(response)

    def __download_novel_with_list_style(self,
                                         request: GMDownloadRequest = None):
        key = request.book_url

        book_name = GMValue.valueStirng(request.extra, "name")
        last_chapter_id = GMValue.valueStirng(request.extra, "chapter_id")

        self.response_data["name"] = book_name

        # 开始下载章节
        self.__callback(GMDownloadStatus.downloading, book_name + "_获取信息中...")
        # 描述文件更替 待开启
        if not GMDownloadCache.is_exists(key):
            GMDownloadCache.save(key, "", book_name)

        # 或取消说首页内容
        gmJsonModel: GMJson = GMBiqugeRequest.getNovelListData(
            request.book_url)
        bookModel: GMBookInfo = None

        if gmJsonModel and gmJsonModel.model:
            bookModel: GMBookInfo = gmJsonModel.model

        if not bookModel or not isinstance(
                bookModel, GMBookInfo) or not bookModel.chapter_list:
            self.__callback(GMDownloadStatus.error, book_name + "_获取信息失败！！！")
        else:
            self.response_data["book_url"] = request.book_url
            self.response_data["name"] = bookModel.name

            self.__callback(GMDownloadStatus.downloading,
                            book_name + "_开始下载...")

            path = ""
            book_name = bookModel.name
            chapter_list = list(bookModel.chapter_list)
            index = 0
            all_count = len(bookModel.chapter_list)
            is_exists_id = False
            last_chapter_id_index = 0
            if last_chapter_id:

                for ele_chapter in chapter_list:  # 章节列表
                    if last_chapter_id == ele_chapter.chapter_id:
                        is_exists_id = True
                        break
                    last_chapter_id_index += 1

                if is_exists_id:
                    if last_chapter_id_index + 1 < len(bookModel.chapter_list):
                        chapter_list = chapter_list[(
                            last_chapter_id_index +
                            1):len(bookModel.chapter_list)]
                    else:
                        is_exists_id = False

            for ele_chapter in chapter_list:  # 章节列表

                # 获取章节内容
                chapter_data = GMBiqugeRequest.getNovelContentData(
                    ele_chapter.chapter_url)
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
                        path = GMFileManager.downloadTempFilePath(
                            book_name, '.txt')
                        if last_chapter_id and not is_exists_id\
                           and os.path.exists(path):
                            os.remove(path)

                    # 追加内容到文本中
                    GMFileManager.appendContent(
                        path, (chapter_title + "\n" + chapterModel.content))
                    # 描述文件更替 待开启
                    GMDownloadCache.save(key, ele_chapter.chapter_id,
                                         book_name)

                # 向上层跑出结果
                re_ret = re.search("第.+?章", chapter_title)
                if re_ret:
                    chapter_title = re_ret.group()
                progress = "_".join([
                    book_name, chapter_title,
                    str(index + last_chapter_id_index)
                ])
                progress += "/" + str(all_count)
                # 处理打印文案
                self.__callback(GMDownloadStatus.downloading, progress)
                index += 1

            # 下载完成
            # 下载完成移动为指导download文件夹下
            down_file_path = GMFileManager.downloadFilePath(book_name, '.txt')

            if os.path.exists(down_file_path):
                os.remove(down_file_path)

            if os.path.exists(path):
                shutil.move(path, GMFileManager.downloadFilePath())
            else:
                print("下载文件不存在 移动到对应位置 失败")

            print("下载完成， 移动到对应位置 成功")
            # 移除缓存文件
            GMDownloadCache.remove(key)

            self.__callback(GMDownloadStatus.success, book_name + "全书下载完成")

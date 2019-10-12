#!/usr/bin/env python
# -*- coding: utf-8 -*-

import re
import os
import shutil

from .gm_biquge_request import GMBiqugeRequest

from ..tools import GMDownloadCache

from ..model import GMBookChapter, GMBookInfo

from gmhelper import GMValue, GMJson, GMFileManager
from gmhelper import GMThreading

from enum import Enum

from ..tools import GMHtmlString


class GMDownloadStatus(Enum):
    suspend = 101
    delete = 101
    success = 200
    downloading = 201
    error = 503


class GMDownloadRequest(object):
    url = ""
    name = ""

    def __init__(self, url: str, name: str, *args, **kwargs):
        self.url = url
        self.name = name
        super().__init__(*args, **kwargs)


class GMDownloadResponse(object):
    code: GMDownloadStatus = GMDownloadStatus.suspend
    msg: str = ""
    url = ""
    name = ""

    def __init__(self,
                 code: GMDownloadStatus = GMDownloadStatus.suspend,
                 msg: str = "",
                 url="",
                 name="",
                 *args,
                 **kwargs):
        self.code = code
        self.msg = msg
        self.url = url
        self.name = name
        super().__init__(*args, **kwargs)


class GMDownloadNovelManager(object):
    __max_count = 3
    __downloading_count = 0
    __all_tasks = {}
    __notifys = set()

    __state = {}

    def __new__(cls, *args, **kwargs):
        ob: GMDownloadNovelManager = super(GMDownloadNovelManager,
                                           cls).__new__(cls, *args, **kwargs)
        ob.__dict__ = cls.__state
        ob.__init_download_tasks()
        return ob

    def __init_download_tasks(self):

        if not self.__all_tasks:
            data = GMDownloadCache.all_list_info()
            if not data:
                return
            for e in data:
                url = GMValue.valueStirng(e, GMDownloadCache.url_key)
                name = GMValue.valueStirng(e, GMDownloadCache.name_key)
                msg = GMValue.valueStirng(e, GMDownloadCache.msg_key)

                response = GMDownloadResponse(GMDownloadStatus.suspend, msg,
                                              url, name)
                if url and name:
                    self.__all_tasks[url] = GMDownloadNovelTask(
                        None, self.__manager_callback, response)

    def __counter(self, type):
        if type == "add":
            self.__downloading_count += 1
            if self.__downloading_count > self.__downloading_count:
                self.__downloading_count = self.__downloading_count
        elif type == "sub":
            self.__downloading_count -= 1
            if self.__downloading_count < 0:
                self.__downloading_count = 0
        print("__counter：", self.__downloading_count)

    def __manager_callback(self, response: GMDownloadResponse):
        if not response:
            return
        if response.url and response.code != GMDownloadStatus.downloading:
            self.__counter("sub")
        if len(self.__notifys) and response.url in self.__all_tasks.keys():
            for callback in self.__notifys:
                callback(response)

    @staticmethod
    def tasks():
        return list(GMDownloadNovelManager().__all_tasks.values())

    # 添加监听方法
    @staticmethod
    def add_notify(notify):
        GMDownloadNovelManager.__deal_notify(notify, "add")

    @staticmethod
    def del_notify(notify):
        GMDownloadNovelManager.__deal_notify(notify, "del")

    @staticmethod
    def __deal_notify(notify, t=""):
        m = GMDownloadNovelManager()
        if t == "add":
            if notify and notify not in m.__notifys:
                m.__notifys.add(notify)
        elif t == "del":
            if notify and notify in m.__notifys:
                m.__notifys.remove(notify)

    def __add_task(self, request: GMDownloadRequest):
        # 开始任务
        task = GMDownloadNovelTask(request, self.__manager_callback)
        self.__all_tasks[request.url] = task
        return task

    def __start_task(self, task):
        if self.__downloading_count >= self.__max_count:
            self.__manager_callback(
                GMDownloadResponse(GMDownloadStatus.error, "下载数量达到最大！",
                                   task.response.url, task.response.name))
        else:
            self.__counter("add")
            task.start()

    @staticmethod
    def add(request: GMDownloadRequest):
        m = GMDownloadNovelManager()
        msg = None
        if not request or not request.url or not request.name:
            msg = "任务id出错"
        elif request.url in m.__all_tasks.keys():
            msg = "已加入到下载列表中..."

        if msg:
            m.__manager_callback(
                GMDownloadResponse(GMDownloadStatus.error, msg, request.url,
                                   request.name))
        else:
            task = m.__add_task(request)
            m.__start_task(task)

    @classmethod
    def task_with_request(cls, request):
        m = GMDownloadNovelManager()
        if request.url and request.url in m.__all_tasks:
            return m.__all_tasks[request.url]
        return None

    @classmethod
    def recovery(cls, request: GMDownloadRequest):
        task = cls.task_with_request(request)
        if task:
            if task.state != GMDownloadStatus.downloading:
                m = GMDownloadNovelManager()
                m.__start_task(task)
        else:
            GMDownloadNovelManager().add(request)

    @classmethod
    def suspend(cls, request: GMDownloadRequest):
        task = cls.task_with_request(request)
        if task and task.state == GMDownloadStatus.downloading:
            task.state = GMDownloadStatus.suspend
            task.manager_callback = None

            m = GMDownloadNovelManager()
            request.name = task.response.name
            request.url = task.response.url
            task = m.__add_task(task.response)
            task.state = GMDownloadStatus.suspend
            task.is_cancel()

    @classmethod
    def delete(cls, request: GMDownloadRequest):
        task = cls.task_with_request(request)
        if task:
            task.state = GMDownloadStatus.delete
            name = request.name
            if not name:
                info = GMDownloadCache.info(request.url)
                name = GMValue.valueStirng(info, GMDownloadCache.name_key)
            if name:
                path = GMFileManager.downloadTempFilePath(name, '.txt')
                if os.path.exists(path):
                    os.remove(path)

            del GMDownloadNovelManager().__all_tasks[request.url]
            GMDownloadCache.remove(request.url)


class GMDownloadNovelTask(object):
    manager_callback = None
    response: GMDownloadResponse = None
    state = GMDownloadStatus.suspend
    download_takss = None

    def __init__(self,
                 request: GMDownloadRequest = None,
                 callback=None,
                 response=None,
                 *args,
                 **kwargs):

        self.manager_callback = callback
        if request and not response:
            self.response = GMDownloadResponse(url=request.url,
                                               name=request.name)
        elif response:
            self.response = response

        if response and not response.url and request and request.url:
            self.response.url = request.url
        self.download_takss = {}
        super().__init__(*args, **kwargs)

    def start(self):
        if self.response.code == GMDownloadStatus.downloading:
            return
        self.response.code = GMDownloadStatus.downloading
        self.state = GMDownloadStatus.downloading
        """ 开始下载任务 """
        GMThreading.start("download_" + self.response.url,
                          self.__download_novel_info)
        return self

    # 回调
    def callback(self, code=GMDownloadStatus.error, msg: str = "", c_name=""):
        self.response.code = code
        if not c_name:
            c_name = self.response.name
        self.response.msg = c_name + " " + msg
        print("msg：", self.response.msg)
        if self.manager_callback:
            self.manager_callback(self.response)

    # 是否取消下载
    def is_cancel(self):
        if self.state == GMDownloadStatus.suspend:
            self.callback(GMDownloadStatus.suspend, "暂停下载...")
        elif self.state == GMDownloadStatus.delete:
            self.callback(GMDownloadStatus.suspend, "")
        return self.state != GMDownloadStatus.downloading

    def __download_novel_info(self):
        # 开始下载章节
        self.callback(GMDownloadStatus.downloading, "获取信息中...")
        book_url = self.response.url

        # 获取小说首页内容
        if self.is_cancel():
            return
        gmJsonModel: GMJson = GMBiqugeRequest.getNovelListData(book_url)
        if self.is_cancel():
            return

        # 获取model
        bookModel: GMBookInfo = None
        if gmJsonModel and gmJsonModel.model:
            bookModel: GMBookInfo = gmJsonModel.model
        if not bookModel or\
           not isinstance(bookModel, GMBookInfo) or\
           not bookModel.chapter_list:
            self.callback(GMDownloadStatus.error, "获取信息失败！！！")
        else:
            count = 10
            self.callback(GMDownloadStatus.downloading, "开始下载...")
            li = list(bookModel.chapter_list)
            co = int(len(li) / count)
            if not GMDownloadCache.info(book_url):
                GMDownloadCache.save(book_url, self.response.name)

            threads = []
            for x in range(count):
                maxindex = (x + 1) * co
                if x == (count - 1):
                    maxindex = len(li)
                download_list = li[x * co:maxindex]

                if x != 1:
                    continue
                g = GMThreading.start("download_" + self.response.name + "_" +
                                      str(x),
                                      self.__mulit_download_novel,
                                      file_index=str(x),
                                      download_list=download_list)
                threads.append(g)
            for t in threads:
                t.thread.join()
            print("完成")

            if self.state == GMDownloadStatus.downloading:
                # 读取内容
                content = ""
                for t in threads:
                    temp_path = GMDownloadCache.download_temp_path(
                        self.response.name, t.re_kwargs["file_index"])

                    if not os.path.exists(temp_path):
                        continue
                    # os.remove(temp_path)
                    content_temp = GMFileManager.readContent(temp_path)
                    content += (("" if (len(content) == 0) else "\r\r") +
                                content_temp)

                # 获取下载路径
                down_file_path = GMFileManager.downloadFilePath(
                    self.response.name, '.txt')
                # 下载文件夹存在文件先删除
                if os.path.exists(down_file_path):
                    os.remove(down_file_path)
                GMFileManager.createContent(down_file_path, content)
                # 移除缓存文件
                GMDownloadCache.remove(book_url)

                self.callback(GMDownloadStatus.success, "下载完成")

    def mulit_save(self, index: str, chapter_id="", complete=""):
        GMDownloadCache.mulit_save(self.response.name, index, chapter_id,
                                   complete)

    def __mulit_download_novel(self, file_index, download_list):
        # 缓存书本信息  描述文件更替 待开启 
        cache_info = GMDownloadCache.mulit_info(self.response.name, file_index)
        if GMValue.valueStirng(cache_info,
                               GMDownloadCache.complete_key) == "1":
            return
        last_chapter_id = GMValue.valueStirng(cache_info, "chapter_id")
        if not cache_info:
            self.mulit_save(file_index)

        temp_path = GMDownloadCache.download_temp_path(self.response.name,
                                                       file_index)
        chapter_list = list(download_list)
        index = 1
        all_count = len(download_list)
        is_exists_id = False
        last_chapter_id_index = 0
        if last_chapter_id:
            for ele_chapter in chapter_list:  # 章节列表
                last_chapter_id_index += 1
                if last_chapter_id == ele_chapter.chapter_id:
                    is_exists_id = True
                    break
            if is_exists_id:
                if last_chapter_id_index < len(download_list):
                    chapter_list = chapter_list[(
                        last_chapter_id_index):len(download_list)]
                else:
                    is_exists_id = False
            else:
                last_chapter_id_index = 0

        if os.path.exists(temp_path) and\
           ((last_chapter_id and not is_exists_id) or not last_chapter_id):
            os.remove(temp_path)

        max_index = len(chapter_list)
        for ele_chapter in chapter_list:  # 章节列表
            if self.is_cancel():
                break

            # 获取章节内容
            chapter_data = GMBiqugeRequest.getNovelContentData(
                ele_chapter.chapter_url)

            if self.is_cancel():
                break

            chapterModel: GMBookChapter = chapter_data.model
            chapter_title = GMHtmlString.conversion_title(ele_chapter.title)

            if chapterModel:
                if not chapter_title:
                    chapter_title = chapterModel.title
                # 追加内容到文本中
                GMFileManager.appendContent(
                    temp_path, (chapter_title + "\n" + chapterModel.content))
                # 描述文件更替 待开启
                # GMDownloadCache.save(book_url, book_name,
                #                      ele_chapter.chapter_id)
                complete = "0" if index < max_index else "1"
                self.mulit_save(file_index, ele_chapter.chapter_id, complete)
            else:
                print(chapter_title + "——下载失败，获取html出错")

            # 向上层跑出结果
            re_ret = re.search("第.+?章", chapter_title)
            if re_ret:
                chapter_title = re_ret.group()
            pros = str(index + last_chapter_id_index) + "/" + str(all_count)
            # 处理打印文案
            self.callback(GMDownloadStatus.downloading,
                          chapter_title + " " + pros,
                          c_name=self.response.name + "_" + str(file_index))
            index += 1

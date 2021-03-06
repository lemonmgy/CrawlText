#!/usr/bin/env python
# -*- coding: utf-8 -*-

import re
import os
import shutil
import threading
from enum import Enum

from .gm_biquge_request import GMBiqugeRequest

from ..tools import GMHtmlString

from ..model import GMBookChapter, GMBookInfo

from gmhelper import GMValue, GMJson
from gmhelper import GMThreading, GMFileManager


class GMDownloadStatus(Enum):
    start = 1
    downloading = 3
    wait = 5
    suspend = 7
    delete = 9
    complete = 11
    error = 13


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
    __max_count = 1
    __downloading_task = {}
    __all_tasks = {}
    __notifys = set()

    __state = {}

    def __new__(cls, *args, **kwargs):
        ob: GMDownloadNovelManager = super(GMDownloadNovelManager,
                                           cls).__new__(cls, *args, **kwargs)
        ob.__dict__ = cls.__state
        ob.__init_download_tasks()
        return ob

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

    m_lock = threading.RLock()

    def __manager_callback(self, response: GMDownloadResponse):

        if not response:
            return
        if response.url and response.code != GMDownloadStatus.downloading:
            self.__del_counter(response.url)
        if len(self.__notifys) and response.url in self.__all_tasks.keys():
            if response.code == GMDownloadStatus.complete:
                GMDownloadCache.save(response.url, response.name,
                                     response.code)
                self.delete(GMDownloadRequest(response.url, response.name),
                            False)
                self.__start_wait_task()
            for callback in self.__notifys:
                callback(response)
        else:
            self.delete(GMDownloadRequest(response.url, response.name), True)
            self.__start_wait_task()

    def __start_wait_task(self):
        for t in self.__all_tasks.values():
            if t.state == GMDownloadStatus.wait:
                self.__start_task(t)
                break

    # 处理任务
    def __init_download_tasks(self):

        if not self.__all_tasks:
            data = GMDownloadCache.all_list_info()
            if not data:
                return
            for e in data:
                url = GMValue.valueStirng(e, GMDownloadCache.url_key)
                name = GMValue.valueStirng(e, GMDownloadCache.name_key)
                msg = GMValue.valueStirng(e, GMDownloadCache.msg_key)

                if url and name:
                    response = GMDownloadResponse(GMDownloadStatus.suspend,
                                                  msg, url, name)
                    self.__all_tasks[url] = GMDownloadNovelTask(
                        None, self.__manager_callback, response)

    def __add_counter(self, task):
        go = False
        self.m_lock.acquire()
        if len(self.__downloading_task.keys()) < self.__max_count:
            self.__downloading_task[task.response.url] = task
            print("__counter：", len(self.__downloading_task.keys()))
            go = True
        self.m_lock.release()
        return go

    def __del_counter(self, url):
        go = False
        self.m_lock.acquire()
        if url in self.__downloading_task.keys():
            del self.__downloading_task[url]
            print("__counter：", len(self.__downloading_task.keys()))
            go = True
        self.m_lock.release()
        return go

    def __add_task(self, request: GMDownloadRequest):
        # 开始任务
        task = GMDownloadNovelTask(request, self.__manager_callback)
        self.__all_tasks[request.url] = task
        return task

    def __start_task(self, task):
        if self.__add_counter(task):
            task.state = GMDownloadStatus.start
            task.start()
            return True
        else:
            task.state = GMDownloadStatus.wait
            self.__manager_callback(
                GMDownloadResponse(GMDownloadStatus.wait,
                                   task.response.name + " 等待下载...",
                                   task.response.url, task.response.name))
            return False

    @staticmethod
    def tasks():
        return list(GMDownloadNovelManager().__all_tasks.values())

    @classmethod
    def task_with_request(cls, request):
        m = GMDownloadNovelManager()
        if request.url and request.url in m.__all_tasks:
            return m.__all_tasks[request.url]
        return None

    @staticmethod
    def add(request: GMDownloadRequest):
        if not GMBiqugeRequest.is_url(request.url):  # 本地
            return
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
            GMDownloadCache.save(request.url, request.name)
            task = m.__add_task(request)
            m.__start_task(task)

    @classmethod
    def recovery(cls, request: GMDownloadRequest):
        if not GMBiqugeRequest.is_url(request.url):  # 本地
            return
        task = cls.task_with_request(request)
        m = GMDownloadNovelManager()
        if task:
            if task.state != GMDownloadStatus.downloading:
                # vs = list(m.__downloading_task.values())
                # if len(vs) > 0:
                #     t = vs[0]
                #     cls.suspend(
                #         GMDownloadRequest(t.response.url, t.response.name))
                m.__start_task(task)
        else:
            m.add(request)

    @classmethod
    def suspend(cls, request: GMDownloadRequest):
        if not GMBiqugeRequest.is_url(request.url):  # 本地
            return
        task = cls.task_with_request(request)
        if task and (task.state == GMDownloadStatus.downloading
                     or task.state == GMDownloadStatus.wait):
            task.state = GMDownloadStatus.suspend
            task.manager_callback = None

            m = GMDownloadNovelManager()
            request.name = task.response.name
            request.url = task.response.url
            task = m.__add_task(task.response)
            task.state = GMDownloadStatus.suspend
            task.is_cancel()
            m.__start_wait_task()

    @classmethod
    def delete(cls, request: GMDownloadRequest, clear_cache_info=True):
        if not request.url:
            return
        task = cls.task_with_request(request)

        if not task:
            return

        m = GMDownloadNovelManager()
        task.state = GMDownloadStatus.delete
        m.__del_counter(request.url)

        # 处理下载文件
        name = request.name
        if not name and request.url:
            info = GMDownloadCache.info(request.url)
            name = GMValue.valueStirng(info, GMDownloadCache.name_key)
        if name:
            # 删除中间文件
            path = GMFileManager.download_temp_path(name)
            if os.path.exists(path):
                if os.path.isdir(path):
                    shutil.rmtree(path)
                else:
                    os.remove(path)

        if clear_cache_info:
            del m.__all_tasks[request.url]
            GMDownloadCache.remove(request.url)
            if name:
                if ".txt" not in name:
                    name += ".txt"
                path = GMFileManager.download_path(name, False)
                if os.path.exists(path):
                    os.remove(path)

        m.__start_wait_task()


class GMDownloadNovelTask(object):
    __thread_count = 5
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
        info = GMDownloadCache.info(self.response.url)
        code = GMValue.value(info, GMDownloadCache.complete_key)
        if code == GMDownloadStatus.complete:
            self.callback(GMDownloadStatus.complete, "下载完成")
            return
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
            self.callback(GMDownloadStatus.suspend, "已暂停...")
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
            count = self.__thread_count
            self.callback(GMDownloadStatus.downloading, "开始下载...")
            li = list(bookModel.chapter_list)
            co = int(len(li) / count)

            threads = []
            for x in range(count):
                maxindex = (x + 1) * co
                if x == (count - 1):
                    maxindex = len(li)
                download_list = li[x * co:maxindex]

                # if x != 1:
                #     continue
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
                    content_temp = GMFileManager.read_content(temp_path)
                    content += (("" if (len(content) == 0) else "\r\r") +
                                content_temp)

                # 获取下载路径
                down_file_path = GMFileManager.download_path(
                    self.response.name + '.txt')
                # 下载文件夹存在文件先删除
                if os.path.exists(down_file_path):
                    os.remove(down_file_path)
                GMFileManager.write_content(down_file_path, content, True)
                self.callback(GMDownloadStatus.complete, "下载完成")

    def mulit_save(self, index: str, chapter_id="", complete=""):
        GMDownloadCache.mulit_save(self.response.name, index, chapter_id,
                                   complete)

    def __mulit_download_novel(self, file_index, download_list):
        # 缓存书本信息  描述文件更替 待开启
        cache_info = GMDownloadCache.mulit_info(self.response.name, file_index)
        if GMValue.valueStirng(cache_info,
                               GMDownloadCache.mulit_complete_key) == "1":
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
                GMFileManager.write_content(
                    temp_path, (chapter_title + "\n" + chapterModel.content))
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


class GMDownloadCache():

    __download_file_path = GMFileManager.download_temp_path(
        '.download_info.json')
    url_key = "book_url"
    name_key = "book_name"
    author_key = "book_author"
    msg_key = "msg_key"
    complete_key = "complete_key"

    @classmethod
    def save(cls,
             book_url: str,
             name: str,
             status: GMDownloadStatus = GMDownloadStatus.suspend):
        if not book_url or not name:
            return
        if not status or status != GMDownloadStatus.complete:
            msg = " 已暂停"
        else:
            msg = " 已完成"


        #warning unfinished code --- 需要完成状态
        cache_dict = dict(GMDownloadCache.__read_info())
        cache_dict[book_url] = {
            cls.url_key: book_url,
            cls.name_key: name,
            cls.msg_key: name + msg,
            cls.complete_key: status
        }
        GMDownloadCache.__write_info(cache_dict)

    @classmethod
    def remove(cls, book_url: str = None):
        if not book_url:
            return
        cache_dict = dict(GMDownloadCache.__read_info())

        if book_url in cache_dict.keys():
            del cache_dict[book_url]
        GMDownloadCache.__write_info(cache_dict)

    @classmethod
    def all_list_info(cls):
        cache_dict = dict(GMDownloadCache.__read_info())
        if cache_dict:
            return cache_dict.values()
        return None

    @classmethod
    def info(cls, book_url):
        if book_url:
            cache_dict = GMDownloadCache.__read_info()
            if book_url in list(cache_dict.keys()):
                return cache_dict[book_url]
        return None

    @classmethod
    def __read_info(cls):
        info_path = GMDownloadCache.__download_file_path
        content = GMFileManager.read_content(info_path)

        cache_dict: dict = None
        if content:
            try:
                cache_dict = GMJson.loads(content)
            finally:
                pass

        if not cache_dict:
            cache_dict = {}

        return cache_dict

    @classmethod
    def __write_info(cls, cache_dict):
        info_path = GMDownloadCache.__download_file_path
        GMFileManager.write_content(info_path, cache_dict, True)

    mulit_name_key = "book_name"
    mulit_chapter_id_key = "chapter_id"
    mulit_msg_key = "msg_key"
    mulit_complete_key = "complete_key"

    @classmethod
    def mulit_save(cls,
                   name: str,
                   index: str,
                   chapter_id: str = "",
                   complete=""):

        if not name:
            return
        if not chapter_id:
            chapter_id = ""

        cache_dict = {
            cls.mulit_name_key: name,
            cls.mulit_chapter_id_key: chapter_id,
            cls.mulit_msg_key: name + " 已暂停...",
            cls.mulit_complete_key: complete
        }
        info_path = cls.download_temp_info_path(name, index)
        GMFileManager.write_content(info_path, cache_dict, True)

    @classmethod
    def mulit_info(cls, name: str, index: str):
        if not name:
            return None

        info_path = cls.download_temp_info_path(name, index)
        content = GMFileManager.read_content(info_path)

        cache_dict: dict = None
        if content:
            try:
                cache_dict = GMJson.loads(content)
            finally:
                pass
        return cache_dict

    @classmethod
    def download_temp_info_path(cls, name: str, index: str):
        return GMFileManager.download_temp_path(name + "/" +
                                                ('.download_info_' + index) +
                                                ".json")

    @classmethod
    def download_temp_path(cls, name: str, index: str):
        return GMFileManager.download_temp_path(name + "/" + index + ".txt")

#!/usr/bin/env python
# -*- encoding: utf-8 -*-

import tkinter as tk
import tkinter.messagebox as tkMessage
import tkinter.constants as tk_cons
from tkinter import ttk

from ..model import GMDataSource
from .gm_list_box import GMListbox, GMListboxMenuModel, GMListboxListModel

from gmhelper import GMThreading

from ..controller import GMDownloadNovelManager, GMDownloadStatus
from ..controller import GMDownloadRequest, GMDownloadResponse


class GMDownloadFrame(tk.Frame):
    __novel_chapter_gm_list_box: GMListbox = None
    __downloading_dataSource: GMDataSource = None
    __selected_model: GMListboxListModel = None

    def destroy(self):
        GMDownloadNovelManager.del_notify(self.downlaod_click_callback)

    @classmethod
    def show(cls, window):
        down_frame = GMDownloadFrame(window)
        down_frame.pack(fill=tk_cons.BOTH, expand=tk_cons.YES)
        down_frame.create_subFrame()
        down_frame.get_download_cache_data()
        return down_frame

    def create_subFrame(self):
        GMDownloadNovelManager.add_notify(self.downlaod_click_callback)

        self.__downloading_dataSource = GMDataSource()
        self.__search_ret_data = GMListboxMenuModel()

        self.menu_model = GMListboxMenuModel()
        self.menu_model.list_datas = self.__downloading_dataSource.dataList()

        op_back = tk.Frame(self)
        op_back.pack(fill=tk_cons.X)

        suspended_btn = ttk.Button(op_back,
                                   text="暂停",
                                   command=self.suspend_click)
        suspended_btn.pack(side=tk_cons.LEFT)

        start_btn = ttk.Button(op_back, text="开始", command=self.start_click)
        start_btn.pack(side=tk_cons.LEFT)

        delete_btn = ttk.Button(op_back, text="删除", command=self.delete_click)
        delete_btn.pack(side=tk_cons.RIGHT)

        self.__novel_chapter_gm_list_box = GMListbox(self,
                                                     self.item_click_callback)
        self.__novel_chapter_gm_list_box.pack(fill=tk_cons.BOTH,
                                              expand=tk_cons.YES)

        self.__novel_chapter_gm_list_box.update_list_contetns(
            [self.menu_model])

    def request_with_selected_model(self):
        if self.__selected_model:
            response: GMDownloadResponse = self.__selected_model.data
            if isinstance(response, GMDownloadResponse):
                return GMDownloadRequest(response.url, response.name)
        return None

    def delete_click(self):
        request = self.request_with_selected_model()
        if not request:
            return
        GMDownloadNovelManager.delete(request)
        self.__downloading_dataSource.pop(request.url)
        self.__novel_chapter_gm_list_box.update_current_option_menu()

    def suspend_click(self):
        request = self.request_with_selected_model()
        if not request:
            return
        GMDownloadNovelManager.suspend(request)

    def start_click(self):
        request = self.request_with_selected_model()
        if not request:
            return
        GMDownloadNovelManager.recovery(request)

    def item_click_callback(self, model):
        self.__selected_model = model

    def get_download_cache_data(self):
        def update_download_cache_data():
            task_list = GMDownloadNovelManager.tasks()
            if not task_list:
                return
            for task in task_list:
                self.update_downloading_view(task.response)

        GMThreading.start("dowload_cache_data", update_download_cache_data)

    # 下载回调
    def downlaod_click_callback(self, response: GMDownloadResponse):
        if response.code != GMDownloadStatus.error:
            self.update_downloading_view(response)
        else:
            # 错误
            tkMessage.showerror("提示", response.msg)

    menu_model = None

    def update_downloading_view(self, response: GMDownloadResponse):
        # 章节下载成功
        # 找出任务列表中 的showmodel
        # 列表中下载的model
        book_url = response.url
        if not book_url and response.msg:
            return
        model = self.__downloading_dataSource.value(book_url)
        if not model:
            model = GMListboxListModel()
            self.__downloading_dataSource.add(book_url, model)

        # 刷新数据列表中model的数据
        model.title = response.msg
        model.data = response
        if not self.menu_model:
            return
        self.__novel_chapter_gm_list_box.update_current_option_menu()


class GMDownloadToplevel(tk.Toplevel):
    download_frame: GMDownloadFrame = None

    def __init__(self, master=None, cnf={}, **kw):
        super().__init__(master=master, cnf={}, **kw)
        self.protocol("WM_DELETE_WINDOW", self.withdraw)
        self.title("下载列表")
        self.download_frame = GMDownloadFrame.show(self)
        self.geometry('320x240')

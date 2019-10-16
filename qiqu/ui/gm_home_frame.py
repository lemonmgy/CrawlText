#!/usr/bin/env python
# -*- coding: utf-8 -*-

import tkinter as tk
import tkinter.messagebox as tkMessage
import tkinter.constants as tk_cons

from .gm_list_box import GMListbox, GMListboxListStyle
from .gm_list_box import GMListboxMenuModel, GMListboxListModel

from ..model import GMModuleBook, GMBookInfo

from ..controller import GMBiqugeRequest
from ..controller import GMDownloadNovelManager, GMDownloadRequest

from gmhelper import GMValue, GMThreading

defalut_text = "绝世邪神"


class GMHomeFrame(tk.Frame):

    # 搜索内容
    __serach_text_content: tk.StringVar
    __serach_btn_content: tk.StringVar
    __search_ret_data: GMListboxMenuModel = None

    # 分类小说
    __week_gm_list_box: GMListbox
    __home_data: list = None

    # 选中的书籍
    __selected_book: GMBookInfo = None

    @classmethod
    def show(cls, window):
        home = GMHomeFrame(window)
        home.pack(fill=tk_cons.BOTH, expand=tk_cons.YES)

        home.create_subView()
        home.__get_home_data()
        return home

    def create_subView(self):
        self.__home_data = []
        self.__search_ret_data = GMListboxMenuModel(menu_title="搜索结果")

        search_frame = tk.Frame(self)
        search_frame.pack(fill=tk_cons.X)

        self.__serach_text_content = tk.StringVar()
        self.__serach_text_content.set((defalut_text))
        serach_entry = tk.Entry(search_frame,
                                textvariable=self.__serach_text_content)
        serach_entry.pack(side=tk_cons.LEFT,
                          fill=tk_cons.X,
                          expand=tk_cons.YES)

        self.__serach_btn_content = tk.StringVar()
        self.__serach_btn_content.set(("搜索"))
        search_btn = tk.Button(search_frame,
                               command=self.start_search_text_cation,
                               textvariable=self.__serach_btn_content,
                               width=8)
        search_btn.pack(side=tk_cons.RIGHT)

        self.__week_gm_list_box = GMListbox(
            self, self.hot_item_click_callback,
            GMListboxListStyle.menu_title).pack(fill=tk_cons.BOTH,
                                                expand=tk_cons.YES)
        down_load_btn = tk.Button(self,
                                  text="加入到下载列表",
                                  command=self.downlaod_click)
        down_load_btn.pack(ipadx=30)

    # 获取数据
    def __get_home_data(self):
        def update_home_data():
            data = GMBiqugeRequest.getHomePageData()
            data_json = data.model
            if not data_json:
                tkMessage.showerror("获取数据失败")
                return
            show_list = []

            def add_module_books(module: GMModuleBook):
                if len(module.book_list) <= 0:
                    return None
                menu_model = GMListboxMenuModel()
                menu_model.menu_title = module.book_category_des
                for book in module.book_list:
                    list_model = GMListboxListModel()
                    list_model.title = book.name if len(
                        book.author) <= 0 else book.name + "_" + book.author
                    list_model.data = book
                    menu_model.list_datas.append(list_model)
                show_list.append(menu_model)

            week_new_module = GMValue.value(data_json,
                                            "week_module,new_module")
            for ele in week_new_module:
                add_module_books(ele)

            hot_list = GMValue.valueList(data_json, "hot_content")
            if len(hot_list) > 0:
                hot_module = GMModuleBook()
                hot_module.book_category_des = "热门小说"
                hot_module.book_list = hot_list
                add_module_books(hot_module)

            self.__home_data = show_list
            self.__update_main_list()

        GMThreading.start("request_home_data", update_home_data)

    def __update_main_list(self, index=None):
        self.__week_gm_list_box.update_list_contetns(self.__home_data, index)

    # 事件处理
    # 搜索按钮点击事件
    def start_search_text_cation(self):
        content = self.__serach_text_content.get()
        self.__search_ret_data.list_datas.clear()
        GMThreading.start("search", self.search_text_request, content=content)

    def search_text_request(self, content=None):
        if self.__serach_btn_content.get() == "搜索中.":
            tkMessage.showerror("提示", "正在搜索中，请稍后再试")
            return
        if not content:
            self.__update_main_list()
            return

        self.__serach_btn_content.set(("搜索中."))
        book_list = GMBiqugeRequest.searchNovelData(content).model
        self.__serach_btn_content.set(("搜索"))
        if not book_list:
            tkMessage.showerror("提示", "暂无搜索结果")
        else:
            for book in book_list:
                list_model = GMListboxListModel()
                list_model.title = book.name if not book.author else (
                    book.name + "_" + book.author)
                list_model.data = book
                self.__search_ret_data.list_datas.append(list_model)
            if self.__search_ret_data not in self.__home_data:
                self.__home_data.append(self.__search_ret_data)

            self.__update_main_list(
                self.__home_data.index(self.__search_ret_data))

    # item点击回调
    def hot_item_click_callback(self, showModel: GMListboxListModel):
        if showModel:
            book = showModel.data
            if isinstance(book, GMBookInfo):
                self.__selected_book = book
                print("selected_book %s = %s" % (book.name, book.book_url))
                return
        print("selected_book = None")
        self.__selected_book = None

    # 下载按钮点击事件
    def downlaod_click(self):
        if not self.__selected_book:
            tkMessage.showerror("提示", "未选中书籍")
            return

        book_url: str = self.__selected_book.book_url
        name: str = self.__selected_book.name
        request = GMDownloadRequest(book_url, name)
        GMDownloadNovelManager.add(request)

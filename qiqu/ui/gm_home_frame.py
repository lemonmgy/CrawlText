#!/usr/bin/env python
# -*- coding: utf-8 -*-

import tkinter as tk
import tkinter.messagebox as tkMessage
import tkinter.constants as tk_cons

from .gm_list_box import GMListbox
from ..model import GMModuleBook, GMBookInfo
from ..model import GMDownloadRequest, GMDownloadResponse, GMDownloadStatus
from ..model import GMDataSource, GMListboxMenuModel, GMListboxListModel
from ..controller import GMCrawlWebDataManger, GMDownloadNovelManger
from gmhelper import GMValue
from ..tool import GMThreading


class GMHomeFrame(tk.Frame):
    # 搜索内容
    __serach_text_content: tk.StringVar
    __serach_btn_content: tk.StringVar
    # 本周热门小说
    __week_gm_list_box: GMListbox

    __novel_chapter_gm_list_box: GMListbox = None
    # 选中的书籍
    __selected_book: GMBookInfo = None

    __search_ret_data: GMListboxMenuModel = None
    __home_data: list = None
    __downloading_dataSource: GMDataSource = None

    @classmethod
    def run(cls):
        main_window = tk.Tk()
        print(main_window.geometry())
        print(main_window.winfo_screenwidth(),
              main_window.winfo_screenheight())
        # main_window.geometry("380x500+0+0")
        # main_window.title("小说首页")
        # main_window.iconbitmap("")
        GMHomeFrame.show(main_window)
        main_window.mainloop()

    def tesetClick(self, om):
        print("sadf", om)

    @classmethod
    def show(cls, window):
        home = GMHomeFrame(window)
        home.pack(fill=tk_cons.X)

        home.create_subView()
        home.__get_home_data()
        # home.__get_download_cache_data()

    def create_subView(self):
        self.__home_data = []
        self.__downloading_dataSource = GMDataSource()
        self.__search_ret_data = GMListboxMenuModel()
        self.__search_ret_data.menu_title = "搜索结果"

        # 创建视图
        self.__create_novel_view()
        self.__create_download_view()

    # 创建小说view
    def __create_novel_view(self):
        search_frame = tk.Frame(self)
        search_frame.pack(fill=tk_cons.X)

        self.__serach_text_content = tk.StringVar()
        self.__serach_text_content.set(("诸天至尊"))
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
            self, self.hot_item_click_callback).pack(fill=tk_cons.X)

    # 下载列表
    def __create_download_view(self):
        down_load_btn = tk.Button(self,
                                  text="开始下载",
                                  command=self.downlaod_click)
        down_load_btn.pack(ipadx=30)
        self.__novel_chapter_gm_list_box = GMListbox(self).pack(
            fill=tk_cons.X, expand=tk_cons.YES).setTopTitle("下载列表")

    def __get_download_cache_data(self):
        all_info = GMCrawlWebDataManger.get_download_cache_data()
        if not all_info:
            return
        for ele_dic in all_info:
            self.__start_download(None, GMValue.value(ele_dic, "book_id"),
                                  GMValue.value(ele_dic, "name"),
                                  GMValue.value(ele_dic, "chapter_id"))

    # 获取数据
    def __get_home_data(self):
        data = GMCrawlWebDataManger.getHomePageData()
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
                menu_model.list_box_datas.append(list_model)
            show_list.append(menu_model)

        week_new_module = GMValue.value(data_json, "week_module,new_module")
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

        self.__get_download_cache_data()

    def __update_main_list(self, index=None):
        self.__week_gm_list_box.update_list_contetns(self.__home_data, index)

    # 事件处理
    # 搜索按钮点击事件
    def start_search_text_cation(self):
        content = self.__serach_text_content.get()
        self.__search_ret_data.list_box_datas.clear()
        GMThreading.start(self.search_text_request, "search", content=content)

    def search_text_request(self, content=None):
        if self.__serach_btn_content.get() == "搜索中.":
            tkMessage.showerror("提示", "正在搜索中，请稍后再试")
            return
        if not content:
            self.__update_main_list()
            return

        self.__serach_btn_content.set(("搜索中."))
        book_list = GMCrawlWebDataManger.searchNovelData(content).model
        self.__serach_btn_content.set(("搜索"))
        if not book_list:
            tkMessage.showerror("提示", "暂无搜索结果")
        else:
            for book in book_list:
                list_model = GMListboxListModel()
                list_model.title = book.name if not book.author else (
                    book.name + "_" + book.author)
                list_model.data = book
                self.__search_ret_data.list_box_datas.append(list_model)
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
                print("%s = %s" % (book.name, book.url))
                return
        print("__selected_book = None")
        self.__selected_book = None

    # 下载按钮点击事件
    def downlaod_click(self):
        if not self.__selected_book:
            tkMessage.showerror("提示", "未选中书籍")
            return
        self.__start_download(self.__selected_book.url,
                              self.__selected_book.book_id,
                              self.__selected_book.name)

    def __start_download(self,
                         url: str = None,
                         book_id: str = None,
                         name: str = None,
                         chapter_id: str = None):

        request = GMDownloadRequest()
        request.url = url
        request.book_id = book_id
        request.extra = {}
        if chapter_id:
            request.extra["chapter_id"] = chapter_id
        if name:
            request.extra["name"] = name

        GMDownloadNovelManger.add_download_novel(request,
                                                 self.downlaod_click_callback)

    # 下载回调
    def downlaod_click_callback(self, response: GMDownloadResponse):
        if response.code == GMDownloadStatus.download_success:
            # 书籍下载完成
            request_id: str = response.request.request_id
            self.__downloading_dataSource.pop(key=request_id)
            self.__novel_chapter_gm_list_box.update_list_contetns(None)
            tkMessage.showinfo("提示", response.msg)

        elif response.code == GMDownloadStatus.downloading_chapter:
            data: dict = response.data
            if not isinstance(data, dict):
                # tkMessage.showerror("类型错误")
                print("类型错误")
                return

            print(data)

            # 章节下载成功
            # 找出任务列表中 的showmodel
            # 列表中下载的model
            request_id: str = response.request.request_id
            current_list_model: GMListboxListModel = GMValue.value(
                self.__downloading_dataSource.dataDic(), request_id)

            # current_list_model == none 时创建创建并将showmodel添加到下载列表
            if not current_list_model:
                current_list_model = GMListboxListModel()
                self.__downloading_dataSource.append(current_list_model,
                                                     request_id)
            # 刷新数据列表中model的数据
            current_list_model.title = response.msg
            current_list_model.data = data

            menu_model = GMListboxMenuModel(
                self.__downloading_dataSource.dataList())
            self.__novel_chapter_gm_list_box.update_list_contetns([menu_model])
        else:
            # 错误
            tkMessage.showerror("提示", response.msg)


if __name__ == "__main__":
    GMHomeFrame.run()

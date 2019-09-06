#!/usr/bin/env python
# -*- coding: utf-8 -*-

import tkinter as tk
import tkinter.messagebox as tkMessage
import threading

from .gm_list_box import GMListbox
from ..model import GMModuleBook, GMBookInfo, GMBookChapter, GMDownloadRequest, GMDownloadResponse, GMDownloadStatus
from ..controller.gm_crawl_web_data_manger import GMCrawlWebDataManger
from ..controller.gm_download_novel_manger import GMDownloadNovelManger


class GMHomeFrame(tk.Frame):
    # 总视图
    window: tk.Tk
    # 搜索内容
    __serach_text_content: tk.StringVar
    # 下载文案
    __download_btn_content: tk.StringVar
    # 本周热门小说
    __week_gm_list_box: GMListbox

    __novel_chapter_gm_list_box: GMListbox = None
    # 选中的书籍
    __selected_book: GMBookInfo = None

    __downloading_list: []

    @classmethod
    def run(cls):
        main_window = tk.Tk()
        gm_home_frame = GMHomeFrame(main_window)
        gm_home_frame.pack()
        main_window.mainloop()

    @staticmethod
    def run2():
        GMHomeFrame.run()

    def __init__(self, master=None, **kw):
        self.window = master
        self.__create_search_view()
        self.__create_novel_view()
        self.__downloading_list = []

        self.__download_btn_content = tk.StringVar()
        self.__download_btn_content.set("下载")
        down_load_btn = tk.Button(
            self.window,
            command=self.downlaod_click,
            textvariable=self.__download_btn_content)
        down_load_btn.pack()

        self.getdata()
        return super().__init__(master=master, **kw)

    # 搜索视图
    def __create_search_view(self):
        search_frame = tk.Frame(self.window)
        search_frame.pack()
        self.__serach_text_content = tk.StringVar()
        self.__serach_text_content.set(("诸天至尊"))
        serach_entry = tk.Entry(
            search_frame, textvariable=self.__serach_text_content)
        serach_entry.pack(side="left")

        search_btn = tk.Button(
            search_frame, text="搜索", command=self.start_search_text_cation)
        search_btn.pack()

    # 创建小说view
    def __create_novel_view(self):
        self.__week_gm_list_box = GMListbox(self.window,
                                            self.hot_item_click_callback)
        self.__week_gm_list_box.pack()

    # 获取数据
    def getdata(self):
        data = GMCrawlWebDataManger.getHomePageData()
        data_json = data[0]
        week_module: GMModuleBook = data_json["week_module"]
        self.__week_gm_list_box.update_list_contetns(
            week_module.book_list, week_module.book_category_des)

    # 事件处理
    # 搜索按钮点击事件
    def start_search_text_cation(self):
        content = self.__serach_text_content.get()
        if len(content) == 0:
            return
        book_list = GMCrawlWebDataManger.searchNovelData(content)[0]
        if len(book_list) > 0:
            self.__week_gm_list_box.update_list_contetns(book_list)
        else:
            tkMessage.showerror("提示", "搜索结果有误，稍后重试！")

    # item点击回调
    def hot_item_click_callback(self, book: GMBookInfo):
        print("%s = %s" % (book.name, book.url))

        # data = GMCrawlWebDataManger.getNovelListData(book.url)
        # book: GMBookInfo = data[0]
        self.__selected_book = book

        if self.__selected_book in self.__downloading_list:
            self.__download_btn_content.set("下载中。。。")

        if self.__novel_chapter_gm_list_box == None:
            self.__novel_chapter_gm_list_box = GMListbox(self.window)
            self.__novel_chapter_gm_list_box.back_frame.pack()

        self.__novel_chapter_gm_list_box.update_list_contetns(
            [], book.name + "_" + book.author)

    # 下载按钮点击事件
    def downlaod_click(self):
        if self.__selected_book == None:
            tkMessage.showerror("提示", "未选中书籍")
            return
        # if self.__selected_book in self.__downloading_list:
        #     return
        # self.__downloading_list.append(self.__selected_book)
        # self.__download_btn_content.set("下载中。。。")

        request = GMDownloadRequest()
        request.url = self.__selected_book.url
        request.book_id = self.__selected_book.book_id
        GMDownloadNovelManger.add_download_novel(request,
                                                 self.downlaod_click_callback)

    # 下载回调
    def downlaod_click_callback(self, response: GMDownloadResponse):
        if response.code == GMDownloadStatus.success_book:
            self.__download_btn_content.set("下载完成")
            remove_list = []
            for ele in self.__downloading_list:
                if ele.book_id == response.data["book_id"]:
                    remove_list.append(ele)
            for obj in remove_list:
                self.__downloading_list.remove(obj)
            # return
        elif response.code == GMDownloadStatus.success_chapter:
            chapters = []
            chapters.extend(
                self.__novel_chapter_gm_list_box.gm_list_box_books_data)
            last_chapter = GMBookChapter()
            last_chapter.title = response.data["title"]
            chapters.append(last_chapter)
            self.__novel_chapter_gm_list_box.update_list_contetns(chapters)
        else:
            tkMessage.showerror("提示", response.msg)

        # chapters = []
        # chapters.extend(
        #     self.__novel_chapter_gm_list_box.gm_list_box_books_data)
        # last_chapter = GMBookChapter()
        # last_chapter.title = chapter.title
        # chapters.append(last_chapter)
        # self.__novel_chapter_gm_list_box.update_list_contetns(chapters)


if __name__ == "__main__":
    GMHomeFrame.run2()

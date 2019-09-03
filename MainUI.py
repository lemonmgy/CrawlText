#!/usr/bin/env python
# -*- coding: utf-8 -*-

import tkinter as tk
import tkinter.messagebox as tkMessage
import GMCrawlWebDataManger
from GMCrawlWebModels import GMModuleBook, GMBookInfo, GMBookChapter
from GMListbox import GMListbox
import GMDownloadNovelManger
import threading


class GMHomeFrame(tk.Frame):
    window: tk.Tk
    __serach_text_content: tk.StringVar
    __week_list_box: GMListbox
    __novel_chapter_list_box: GMListbox = None
    __selected_book: GMBookInfo = None
    __down_load_btn_content: tk.StringVar
    __downloading_list: []

    def downlaod_click_calback(self, chapter=None, code=0, book_url=""):
        if code == 200:
            self.__down_load_btn_content.set("下载完成")
            remove_list = []
            for ele in self.__downloading_list:
                if ele.url == book_url:
                    remove_list.append(ele)
            for obj in remove_list:
                self.__downloading_list.remove(obj)
            return

        chapters = []
        chapters.extend(self.__novel_chapter_list_box.list_box_books_data)
        last_chapter = GMBookChapter()
        last_chapter.title = chapter.title
        chapters.append(last_chapter)
        self.__novel_chapter_list_box.update_list_contetns(chapters)

    def downlaod_click(self):

        if self.__selected_book != None:
            if self.__selected_book in self.__downloading_list:
                return
            self.__downloading_list.append(self.__selected_book)
            self.__down_load_btn_content.set("下载中。。。")
            GMDownloadNovelManger.download_novel_list_style(
                self.__selected_book.url, callback=self.downlaod_click_calback)

    def __init__(self, master=None, **kw):
        self.window = master
        self.__create_search_view()
        self.__create_novel_view()
        self.__downloading_list = []

        self.__down_load_btn_content = tk.StringVar()
        self.__down_load_btn_content.set("下载")
        down_load_btn = tk.Button(
            self.window,
            command=self.downlaod_click,
            textvariable=self.__down_load_btn_content)
        down_load_btn.pack()

        self.getdata()
        return super().__init__(master=master, **kw)

    def start_search_text(self):
        content = self.__serach_text_content.get()
        if len(content) == 0:
            return
        book_list = GMCrawlWebDataManger.searchNovelData(content)[0]
        self.__week_list_box.update_list_contetns(book_list)
        # if self.__novel_chapter_list_box != None:
        #     self.__novel_chapter_list_box.back_frame.destroy()
        #     self.__novel_chapter_list_box = None

    def __create_search_view(self):
        search_frame = tk.Frame(self.window)
        search_frame.pack()
        self.__serach_text_content = tk.StringVar()
        self.__serach_text_content.set(("诸天至尊"))
        serach_entry = tk.Entry(
            search_frame, textvariable=self.__serach_text_content)
        serach_entry.pack(side="left")

        search_btn = tk.Button(
            search_frame, text="搜索", command=self.start_search_text)
        search_btn.pack()

    def hot_item_click_callback(self, book: GMBookInfo):
        print("%s = %s" % (book.name, book.url))

        # data = GMCrawlWebDataManger.getNovelListData(book.url)
        # book: GMBookInfo = data[0]
        self.__selected_book = book

        if self.__selected_book in self.__downloading_list:
            self.__down_load_btn_content.set("下载中。。。")

        if self.__novel_chapter_list_box == None:
            self.__novel_chapter_list_box = GMListbox(self.window)
            self.__novel_chapter_list_box.back_frame.pack()

        self.__novel_chapter_list_box.update_list_contetns(
            [], book.name + "_" + book.author)

    def __create_novel_view(self):
        self.__week_list_box = GMListbox(self.window,
                                         self.hot_item_click_callback)
        self.__week_list_box.pack()

    def getdata(self):
        data = GMCrawlWebDataManger.getHomePageData()
        data_json = data[0]
        week_module: GMModuleBook = data_json["week_module"]
        self.__week_list_box.update_list_contetns(
            week_module.book_list, week_module.book_category_des)


main_window = tk.Tk()
home_frame = GMHomeFrame(main_window)
home_frame.pack()

main_window.mainloop()

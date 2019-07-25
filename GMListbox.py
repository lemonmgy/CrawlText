#!/usr/bin/env python
# -*- coding: utf-8 -*-

import tkinter as tk
from GMCrawlWebModels import GMBookInfo, GMBookChapter


class GMListbox(object):

    back_frame: tk.Frame
    list_title: tk.Label
    list_title_contents: tk.StringVar
    list_box: tk.Listbox
    list_box_contents: tk.StringVar
    list_box_books_data = []
    item_click_callback: object

    def pack(self, side=""):
        if len(side) == 0:
            self.back_frame.pack()
        else:
            self.back_frame.pack(side=side)

    def item_click(self, event):
        contents_str: str = self.list_box_contents.get()
        contents_list = contents_str.split(',')
        if len(self.list_box_books_data) == len(contents_list):
            index = self.list_box.curselection()[0]
            book = self.list_box_books_data[index]
            if self.item_click_callback != None:
                self.item_click_callback(book)

    def __init__(self, master=None, item_click_callback=None, **kw):
        self.item_click_callback = item_click_callback
        self.list_box_contents = tk.StringVar()
        self.list_title_contents = tk.StringVar()
        self.list_box_books_data = []

        self.back_frame = tk.Frame(master)

        self.list_title = tk.Label(
            self.back_frame, textvariable=self.list_title_contents)
        self.list_title.pack()

        self.list_box = tk.Listbox(
            self.back_frame, listvariable=self.list_box_contents)
        self.list_box.pack()
        self.list_box.bind("<ButtonRelease-1>", self.item_click)

        return super().__init__(**kw)

    def update_list_contetns(self, list_data=[], title=""):
        del self.list_box_books_data[0:len(self.list_box_books_data)]
        self.list_box_books_data.extend(list_data)
        contents = []
        if len(self.list_box_books_data):
            if isinstance(self.list_box_books_data[0], GMBookInfo):
                for obj in self.list_box_books_data:
                    contents.append(obj.name)
            elif isinstance(self.list_box_books_data[0], GMBookChapter):
                for obj in self.list_box_books_data:
                    contents.append(obj.title)

        self.list_box_contents.set(contents)
        if len(title) > 0:
            self.list_title_contents.set(title)

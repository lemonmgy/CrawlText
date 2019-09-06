#!/usr/bin/env python
# -*- coding: utf-8 -*-

import tkinter as tk
from ..model import GMBookInfo, GMBookChapter


class GMListbox(object):

    back_frame: tk.Frame
    list_title: tk.Label
    list_title_contents: tk.StringVar
    gm_list_box: tk.Listbox
    gm_list_box_contents: tk.StringVar
    gm_list_box_books_data = []
    item_click_callback: object

    def pack(self, side=""):
        if len(side) == 0:
            self.back_frame.pack()
        else:
            self.back_frame.pack(side=side)

    def item_click(self, event):
        # contents_str: str = self.gm_list_box_contents.get()
        # contents_list = contents_str.split(',')
        index = self.gm_list_box.curselection()
        if len(index) < 0:
            return
        index = index[0]
        if index < 0 or index > len(self.gm_list_box_books_data):
            return
        book = self.gm_list_box_books_data[index]
        if self.item_click_callback != None:
            self.item_click_callback(book)

    def __init__(self, master=None, item_click_callback=None, **kw):
        self.item_click_callback = item_click_callback
        self.gm_list_box_contents = tk.StringVar()
        self.list_title_contents = tk.StringVar()
        self.gm_list_box_books_data = []

        self.back_frame = tk.Frame(master)

        self.list_title = tk.Label(
            self.back_frame, textvariable=self.list_title_contents)
        self.list_title.pack()

        self.gm_list_box = tk.Listbox(
            self.back_frame, listvariable=self.gm_list_box_contents)
        self.gm_list_box.pack()
        self.gm_list_box.bind("<ButtonRelease-1>", self.item_click)

        return super().__init__(**kw)

    def update_list_contetns(self, list_data=[], title=""):
        del self.gm_list_box_books_data[0:len(self.gm_list_box_books_data)]
        self.gm_list_box_books_data.extend(list_data)
        contents = []
        if len(self.gm_list_box_books_data) > 0:
            if isinstance(self.gm_list_box_books_data[0], GMBookInfo):
                for obj in self.gm_list_box_books_data:
                    name = obj.name
                    if len(obj.author) > 0:
                        name = obj.name + "_" + obj.author
                    contents.append(name)
            elif isinstance(self.gm_list_box_books_data[0], GMBookChapter):
                for obj in self.gm_list_box_books_data:
                    contents.append(obj.title)

        self.gm_list_box_contents.set(contents)
        if len(title) > 0:
            self.list_title_contents.set(title)
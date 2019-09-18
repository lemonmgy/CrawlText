#!/usr/bin/env python
# -*- coding: utf-8 -*-

import tkinter as tk
# from tkinter.constants import *
from tkinter import ttk
from ..tool import GMTools
import tkinter.constants as tk_cons
from ..model import GMListboxMenuModel


class GMListbox(object):
    # 背景frame
    back_frame: tk.Frame
    top_title_view: tk.Frame

    # 顶部选项条

    top_label_title: tk.Label
    top_label_title_stringVar: tk.StringVar

    is_no_menu = False
    top_menu_title: ttk.OptionMenu
    top_menu_title_stringVar: tk.StringVar
    # 底部列表
    gm_list_box: tk.Listbox
    gm_list_box_contents: tk.StringVar
    # 数据源
    gm_list_box_books_data: [GMListboxMenuModel]
    # 列表点击事件回调
    item_click_callback = None
    selected_model: GMListboxMenuModel = None

    def pack(self, cnf={}, **kw):
        """Pack a widget in the parent widget. Use as options:
        after=widget - pack it after you have packed widget
        anchor=NSEW (or subset) - position widget according to
                                  given direction
        before=widget - pack it before you will pack widget
        expand=bool - expand widget if parent size grows
        fill=NONE or X or Y or BOTH - fill widget if widget grows
        in=master - use master to contain this widget
        in_=master - see 'in' option description
        ipadx=amount - add internal padding in x direction
        ipady=amount - add internal padding in y direction
        padx=amount - add padding in x direction
        pady=amount - add padding in y direction
        side=TOP or BOTTOM or LEFT or RIGHT -  where to add this widget.
        """
        if 'padx' not in kw:
            # print(kw['padx'])
            kw['padx'] = '20'
        self.back_frame.pack(cnf=cnf, **kw)
        return self

    def select_item_change(self):
        index = self.gm_list_box.curselection()
        book = None
        if len(index) > 0:
            index = index[0]
            if index >= 0 and index < len(self.selected_model.list_box_datas):
                book = self.selected_model.list_box_datas[index]
        if self.item_click_callback:
            self.item_click_callback(book)

        print("indexindex === " + str(index))

    def item_click(self, event):
        self.select_item_change()

    def menu_item_click(self, menu):
        for menu_model in self.gm_list_box_books_data:
            if menu_model.menu_title == menu:
                self.__update_selected_model(menu_model)
                return
        self.select_item_change()

    def __init__(self, master=None, item_click_callback=None, *args, **kwargs):
        self.item_click_callback = item_click_callback
        self.gm_list_box_contents = tk.StringVar()
        self.top_menu_title_stringVar = tk.StringVar()
        self.top_label_title_stringVar = tk.StringVar()
        self.gm_list_box_books_data = []

        self.back_frame = tk.Frame(master)

        self.top_title_view = tk.Frame(self.back_frame, height=25)
        self.top_title_view.pack()

        self.top_label_title = tk.Label(
            self.top_title_view, textvariable=self.top_label_title_stringVar)

        self.top_menu_title = ttk.OptionMenu(self.top_title_view,
                                             self.top_menu_title_stringVar,
                                             command=self.menu_item_click)

        self.gm_list_box = tk.Listbox(self.back_frame,
                                      listvariable=self.gm_list_box_contents)
        self.gm_list_box.pack(fill=tk_cons.X)
        self.gm_list_box.bind("<ButtonRelease-1>", self.item_click)
        super().__init__(*args, **kwargs)

    def setTopTitle(self, title):
        self.top_label_title.pack_forget()
        self.top_label_title.pack()
        self.top_label_title_stringVar.set(title)
        self.is_no_menu = True
        return self

    def update_list_contetns(self,
                             list_data: [GMListboxMenuModel],
                             defalut_index=None):
        if not list_data:
            list_data = []
        if not self.is_no_menu:
            old_count = len(self.gm_list_box_books_data)
            new_count = len(list_data)
            if old_count == 0 and new_count != 0:
                self.top_menu_title.pack()
            elif old_count != 0 and new_count == 0:
                self.top_menu_title.pack_forget()

        self.gm_list_box_books_data.clear()
        self.gm_list_box_books_data.extend(list_data)
        self.selected_model = None

        if defalut_index and defalut_index >= 0 and defalut_index < len(
                self.gm_list_box_books_data):
            select_model = self.gm_list_box_books_data[defalut_index]
        elif len(self.gm_list_box_books_data) > 0:
            select_model = self.gm_list_box_books_data[0]
        else:
            select_model = None

        if not self.is_no_menu:
            menu_titles = []
            for menuModel in self.gm_list_box_books_data:
                menuModel.menu_title = GMTools.key(menu_titles,
                                                   menuModel.menu_title)
                menu_titles.append(menuModel.menu_title)
            self.top_menu_title.set_menu(None, *menu_titles)

        self.__update_selected_model(select_model)

    def __update_selected_model(self, selectedModel=None):
        print(selectedModel)
        self.selected_model = selectedModel
        if self.selected_model:
            if not self.is_no_menu:
                top_title = self.selected_model.menu_title if len(
                    self.selected_model.menu_title) > 0 else "未设置标题"
                self.top_menu_title_stringVar.set(top_title)

            title_list = []
            for menuModel in self.selected_model.list_box_datas:
                title_list.append(menuModel.title)
            self.gm_list_box_contents.set(title_list)
        else:
            self.top_menu_title_stringVar.set("暂无数据")
            self.gm_list_box_contents.set([])

        self.select_item_change()

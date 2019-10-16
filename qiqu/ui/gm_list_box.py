#!/usr/bin/env python
# -*- coding: utf-8 -*-

import tkinter as tk
from tkinter import ttk
import tkinter.constants as tk_cons

from enum import Enum


# 列表中展示数据模型
class GMListboxListModel(object):
    # 展示的标题
    title: str = ""
    # 原来的数据源
    data = None


# 选项数据源
class GMListboxMenuModel(object):
    # 选项标题
    menu_title = ""
    # 列表展示的数据源 GMListboxListModel
    list_datas: list = None

    def __init__(self, data: list = None, menu_title="", *args, **kwargs):
        self.list_datas = []
        self.menu_title = menu_title
        if data:
            self.list_datas.extend(data)
        super().__init__(*args, **kwargs)


class GMWidgetHelper(object):
    widget: tk.Widget = None
    is_packed = False

    def __init__(self, widget=None, *args):
        self.widget = widget
        super(GMWidgetHelper, self).__init__(*args)

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
        self.widget.pack(cnf=cnf, **kw)
        self.is_packed = True

    def pack_forget(self, cnf={}, **kw):
        self.widget.pack_forget(cnf=cnf, **kw)
        self.is_packed = False


class GMListboxListStyle(Enum):
    no_title = 0
    title = 1
    menu_title = 2


class GMListbox(object):

    style: GMListboxListStyle = GMListboxListStyle.no_title

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

        if 'padx' not in kw:
            # print(kw['padx'])
            kw['padx'] = '20'
        self.back_frame.pack(cnf=cnf, **kw)
        return self

    def select_item_change(self):
        if not self.selected_model or not self.item_click_callback:
            return
        index = self.gm_list_box.curselection()
        book = None
        if len(index) > 0:
            index = index[0]
            if index >= 0 and index < len(self.selected_model.list_datas):
                book = self.selected_model.list_datas[index]

        self.item_click_callback(book)

    def item_click(self, event):
        self.select_item_change()

    def menu_item_click(self, menu):
        for menu_model in self.gm_list_box_books_data:
            if menu_model.menu_title == menu:
                self.__update_selected_model(menu_model)
                return
        self.select_item_change()

    def __init_data(self):
        self.gm_list_box_contents = tk.StringVar()
        self.top_menu_title_stringVar = tk.StringVar()
        self.top_label_title_stringVar = tk.StringVar()
        self.gm_list_box_books_data = []

    def __init__(self,
                 master=None,
                 item_click_callback=None,
                 style=GMListboxListStyle.no_title,
                 *args,
                 **kwargs):
        self.item_click_callback = item_click_callback
        self.__init_data()

        self.back_frame = tk.Frame(master)

        self.top_title_view = tk.Frame(self.back_frame, height=25)

        self.top_label_title = tk.Label(
            self.top_title_view, textvariable=self.top_label_title_stringVar)

        self.top_menu_title = ttk.OptionMenu(self.top_title_view,
                                             self.top_menu_title_stringVar,
                                             command=self.menu_item_click)

        self.gm_list_box = tk.Listbox(self.back_frame,
                                      listvariable=self.gm_list_box_contents)
        self.gm_list_box.bind("<ButtonRelease-1>", self.item_click)
        self.set_style(style)
        self.show_loading()
        super().__init__(*args, **kwargs)

    def set_style(self, style):
        self.style = style
        if style == GMListboxListStyle.title:
            self.top_title_view.pack_forget()
            self.top_title_view.pack(fill=tk_cons.X)
            self.top_label_title.pack_forget()
            self.top_label_title.pack()
        elif style == GMListboxListStyle.menu_title:
            self.top_title_view.pack_forget()
            self.top_title_view.pack(fill=tk_cons.X)
            self.top_menu_title.pack_forget()
            self.top_menu_title.pack(side=tk_cons.LEFT)
        else:
            self.top_title_view.pack_forget()
            self.top_menu_title.pack_forget()

        self.gm_list_box.pack_forget()
        self.gm_list_box.pack(fill=tk_cons.BOTH, expand=tk_cons.YES)
        self.back_frame.update()

    loading = None

    def show_loading(self):
        self.top_label_title.pack_forget()
        self.top_menu_title.pack_forget()
        self.hide_loading()
        self.loading = tk.Label(self.gm_list_box,
                                text="加载中...",
                                font=("", "10"),
                                fg='blue')

        self.loading.place(x=0, y=0, relwidth=1, relheight=1)

    def hide_loading(self):
        if self.loading:
            self.loading.destroy()
            self.loading = None

    def setTopTitle(self, title):
        self.top_label_title_stringVar.set(title)
        return self

    def update_list_contetns(self,
                             list_data: [GMListboxMenuModel],
                             defalut_index=None):
        self.hide_loading()
        if not list_data or not isinstance(list_data, list):
            list_data = []
        if self.style == GMListboxListStyle.menu_title:
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

        if self.style == GMListboxListStyle.menu_title:
            menu_titles = []
            for menuModel in self.gm_list_box_books_data:
                menuModel.menu_title = self.menu_title_key(
                    menu_titles, menuModel.menu_title)
                menu_titles.append(menuModel.menu_title)
            self.top_menu_title.set_menu(None, *menu_titles)
            self.top_menu_title.update()

        self.__update_selected_model(select_model)

    def menu_title_key(self, data, defaultKey: str, addkey: str = None):
        """
        将 数组、元组的元素 or 字典的key 处理为唯一值，
        默认key  addkey后面追加的key
        """
        def __key(data, defaultKey, addkey):
            if defaultKey in data:
                defaultKey = ("" if len(defaultKey) == 0 else
                              (defaultKey + "_")) + addkey
                return __key(data, defaultKey, addkey)
            else:
                return defaultKey

        # 判断data是否满足条件
        if not isinstance(data, list) and not isinstance(
                data, tuple) and not isinstance(data, dict):
            return defaultKey

        if not isinstance(addkey, str) or len(addkey) == 0:
            addkey = "0"
        return __key(data, defaultKey, addkey)

    def update_current_option_menu(self):
        self.__update_selected_model(self.selected_model)

    def __update_selected_model(self, selectedModel=None):
        self.selected_model = selectedModel
        if self.selected_model:
            if self.style == GMListboxListStyle.menu_title:
                top_title = self.selected_model.menu_title if len(
                    self.selected_model.menu_title) > 0 else "未设置标题"
                self.top_menu_title_stringVar.set(top_title)

            title_list = []
            for menuModel in self.selected_model.list_datas:
                title_list.append(menuModel.title)
            self.gm_list_box_contents.set(title_list)
        else:
            self.top_menu_title_stringVar.set("暂无数据")
            self.gm_list_box_contents.set([])

        self.gm_list_box.update()

        self.select_item_change()

#!/usr/bin/env python
# -*- encoding: utf-8 -*-


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
    list_box_datas: list = None

    def __init__(self, data: list = None, *args, **kwargs):
        self.list_box_datas = []
        if data:
            self.list_box_datas.extend(data)
        super().__init__(*args, **kwargs)

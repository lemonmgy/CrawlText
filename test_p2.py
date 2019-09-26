#!/usr/bin/env python
# -*- encoding: utf-8 -*-


class GMDownloadNovelManager(object):
    max_count = 3
    downloading_count = 0
    all_tasks = {}
    __notifys = set()

    __state = {}

    # def __new__(cls, *args, **kwargs):
    #     ob = super(GMDownloadNovelManager, cls).__new__(cls, *args, **kwargs)
    #     ob.__dict__ = cls.__state
    #     print(ob.__dict__)
    #     return ob

    def __init__(self, *args, **kwargs):
        self.__dict__ = GMDownloadNovelManager.__state
        print(self.__dict__)
        super().__init__(*args, **kwargs)


if __name__ == "__main__":
    # GMDownloadNovelManager().all_tasks["2"] = "33"
    # print(GMDownloadNovelManager().all_tasks)

    # GMDownloadNovelManager.all_tasks = {}
    # GMDownloadNovelManager.all_tasks["2xx"] = "33"
    # GMDownloadNovelManager().all_tasks["x"] = "x"
    # print(GMDownloadNovelManager().all_tasks)
    # print(GMDownloadNovelManager.all_tasks)
    # GMDownloadNovelManager().all_tasks = {}
    # GMDownloadNovelManager().max_count = 2
    print(GMDownloadNovelManager.max_count)

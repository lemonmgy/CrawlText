#!/usr/bin/env python
# -*- encoding: utf-8 -*-

# from gmhelper import GMJson, GMFileManager

from gmhelper import GMJson, GMFileManager

info_dict_key = "__info_dict_key"
info_list_key = "__info_list_key"


class GMDownloadCache():
    @staticmethod
    def all_list_info():

        cache_dict = GMDownloadCache.read_info()
        info_list: list = cache_dict[info_list_key]
        info_dict: dict = cache_dict[info_dict_key]

        ret = []
        keys = list(info_dict.keys())
        need_save = False
        for book_id in list(info_list):
            if book_id not in keys:
                need_save = True
                info_list.remove(book_id)
            else:
                ret.append(info_dict[book_id])

        for book_id in keys:
            if book_id not in info_list:
                need_save = True
                info_list.append(book_id)
                ret.append(info_dict[book_id])
        if need_save:
            GMDownloadCache.write_info(cache_dict)
        return ret

    @staticmethod
    def is_exists(book_id):
        cache_dict = GMDownloadCache.read_info()
        info_dict: dict = cache_dict[info_dict_key]
        return book_id in list(info_dict.keys())

    @staticmethod
    def read_info():
        info_path = GMFileManager.downloadTempFilePath('download_info.txt')
        content = GMFileManager.readContent(info_path)

        cache_dict: dict = None
        if content:
            try:
                cache_dict = GMJson.loads(content)
            finally:
                pass

        if not cache_dict:
            cache_dict = {}

        keys = list(cache_dict.keys())
        if info_dict_key not in keys:
            cache_dict[info_dict_key] = {}

        if info_list_key not in keys:
            cache_dict[info_list_key] = []

        return cache_dict

    @staticmethod
    def write_info(cache_dict):
        info_path = GMFileManager.downloadTempFilePath('download_info.txt')
        GMFileManager.replaceContent(info_path, cache_dict)

    @staticmethod
    def save(book_id: str, chapter_id: str, name: str):
        if not book_id or not name:
            return
        if not chapter_id:
            chapter_id = ""

        cache_dict = GMDownloadCache.read_info()
        info_list: list = cache_dict[info_list_key]

        if book_id not in info_list:
            info_list.append(book_id)

        info_dict: dict = cache_dict[info_dict_key]
        info_dict[book_id] = {
            "book_id": book_id,
            "name": name,
            "chapter_id": chapter_id
        }
        GMDownloadCache.write_info(cache_dict)

    @staticmethod
    def remove(book_id: str = None):
        if not book_id:
            return
        cache_dict = GMDownloadCache.read_info()
        info_list: list = cache_dict[info_list_key]
        if book_id in info_list:
            info_list.remove(book_id)

        info_dict: dict = cache_dict[info_dict_key]
        if book_id in info_dict:
            del info_dict[book_id]
        GMDownloadCache.write_info(cache_dict)

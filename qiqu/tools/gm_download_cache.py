#!/usr/bin/env python
# -*- encoding: utf-8 -*-

# from gmhelper import GMJson, GMFileManager

from gmhelper import GMJson, GMFileManager


class GMDownloadCache():

    __download_file_path = GMFileManager.downloadTempFilePath(
        '.download_info.json')
    url_key = "book_url"
    name_key = "book_name"
    author_key = "book_author"
    msg_key = "msg_key"

    @classmethod
    def save(cls, book_url: str, name: str, author: str = ""):
        if not book_url or not name:
            return
        if not author:
            author = ""

        cache_dict = dict(GMDownloadCache.__read_info())
        cache_dict[book_url] = {
            cls.url_key: book_url,
            cls.name_key: name,
            cls.msg_key: name + "_已暂停..."
        }
        GMDownloadCache.__write_info(cache_dict)

    @classmethod
    def remove(cls, book_url: str = None):
        if not book_url:
            return
        cache_dict = dict(GMDownloadCache.__read_info())

        if book_url in cache_dict.keys():
            del cache_dict[book_url]
        GMDownloadCache.__write_info(cache_dict)

    @classmethod
    def all_list_info(cls):
        cache_dict = dict(GMDownloadCache.__read_info())
        if cache_dict:
            return cache_dict.values()
        return None

    @classmethod
    def info(cls, book_url):
        if book_url:
            cache_dict = GMDownloadCache.__read_info()
            if book_url in list(cache_dict.keys()):
                return cache_dict[book_url]
        return None

    @classmethod
    def __read_info(cls):
        info_path = GMDownloadCache.__download_file_path
        content = GMFileManager.readContent(info_path)

        cache_dict: dict = None
        if content:
            try:
                cache_dict = GMJson.loads(content)
            finally:
                pass

        if not cache_dict:
            cache_dict = {}

        return cache_dict

    @classmethod
    def __write_info(cls, cache_dict):
        info_path = GMDownloadCache.__download_file_path
        GMFileManager.createContent(info_path, cache_dict)

    mulit_name_key = "book_name"
    mulit_chapter_id_key = "chapter_id"
    mulit_msg_key = "msg_key"
    mulit_complete_key = "complete_key"

    @classmethod
    def mulit_save(cls,
                   name: str,
                   index: str,
                   chapter_id: str = "",
                   complete=""):

        if not name:
            return
        if not chapter_id:
            chapter_id = ""

        cache_dict = {
            cls.mulit_name_key: name,
            cls.mulit_chapter_id_key: chapter_id,
            cls.mulit_msg_key: name + " 已暂停...",
            cls.mulit_complete_key: complete
        }
        info_path = cls.download_temp_info_path(name, index)
        GMFileManager.createContent(info_path, cache_dict)

    @classmethod
    def mulit_info(cls, name: str, index: str):
        if not name:
            return None

        info_path = cls.download_temp_info_path(name, index)
        content = GMFileManager.readContent(info_path)

        cache_dict: dict = None
        if content:
            try:
                cache_dict = GMJson.loads(content)
            finally:
                pass
        return cache_dict

    @classmethod
    def download_temp_info_path(cls, name: str, index: str):
        return GMFileManager.downloadTempFilePath(
            name + "/" + ('.download_info_' + index), ".json")

    @classmethod
    def download_temp_path(cls, name: str, index: str):
        return GMFileManager.downloadTempFilePath(name + "/" + index, ".txt")


if __name__ == "__main__":
    print("")

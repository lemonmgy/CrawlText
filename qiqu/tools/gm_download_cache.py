#!/usr/bin/env python
# -*- encoding: utf-8 -*-

# from gmhelper import GMJson, GMFileManager

from gmhelper import GMJson, GMFileManager

info_dict_key = "__info_dict_key"
info_list_key = "__info_list_key"


class GMDownloadCache():
    url_key = "book_url"
    name_key = "book_name"
    chapter_id_key = "chapter_id"
    msg_key = "msg_key"

    __download_file_path = GMFileManager.downloadTempFilePath(
        'download_info.json')

    @classmethod
    def save(cls, book_url: str, name: str, chapter_id: str = ""):
        if not book_url or not name:
            return
        if not chapter_id:
            chapter_id = ""

        cache_dict = GMDownloadCache.__read_info()
        info_list: list = cache_dict[info_list_key]

        if book_url not in info_list:
            info_list.append(book_url)

        info_dict: dict = cache_dict[info_dict_key]
        info_dict[book_url] = {
            cls.url_key: book_url,
            cls.name_key: name,
            cls.chapter_id_key: chapter_id,
            cls.msg_key: name + "_已暂停..."
        }
        GMDownloadCache.__write_info(cache_dict)

    @classmethod
    def remove(cls, book_url: str = None):
        if not book_url:
            return
        cache_dict = GMDownloadCache.__read_info()
        info_list: list = cache_dict[info_list_key]
        if book_url in info_list:
            info_list.remove(book_url)

        info_dict: dict = cache_dict[info_dict_key]
        if book_url in info_dict:
            del info_dict[book_url]
        GMDownloadCache.__write_info(cache_dict)

    @classmethod
    def all_list_info(cls):

        cache_dict = GMDownloadCache.__read_info()
        info_list: list = cache_dict[info_list_key]
        info_dict: dict = cache_dict[info_dict_key]

        ret = []
        keys = list(info_dict.keys())
        need_save = False
        for book_url in info_list:
            if book_url not in keys:
                need_save = True
                info_list.remove(book_url)
            else:
                ret.append(info_dict[book_url])

        for book_url in keys:
            if book_url not in info_list:
                need_save = True
                info_list.append(book_url)
                ret.append(info_dict[book_url])
        if need_save:
            GMDownloadCache.__write_info(cache_dict)
        return ret

    @classmethod
    def info(cls, book_url):
        if book_url:
            cache_dict = GMDownloadCache.__read_info()
            info_dict: dict = cache_dict[info_dict_key]
            if book_url in list(info_dict.keys()):
                return info_dict[book_url]
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

        keys = list(cache_dict.keys())
        if info_dict_key not in keys:
            cache_dict[info_dict_key] = {}

        if info_list_key not in keys:
            cache_dict[info_list_key] = []

        return cache_dict

    @classmethod
    def __write_info(cls, cache_dict):
        info_path = GMDownloadCache.__download_file_path
        GMFileManager.replaceContent(info_path, cache_dict)


if __name__ == "__main__":
    print("")

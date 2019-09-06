#!/usr/bin/env python
# -*- encoding: utf-8 -*-

from enum import Enum


class GMDownloadStatus(Enum):
    success_chapter = 200
    success_book = 201
    download_max = 300
    download_exist = 300
    error_path = 502
    error_book_info = 503
    error_unknown = 503


def download_novel_with_list_style():
    def dealcallback(code: GMDownloadStatus = GMDownloadStatus.error_unknown,
                     msg: str = "",
                     data=None):
        if code != GMDownloadStatus.success_book and data != None:
            print("sadfasdf")

    print("1")
    dealcallback(GMDownloadStatus.error_path)


if __name__ == "__main__":
    print(GMDownloadStatus.error_unknown != GMDownloadStatus.error_book_info)
    download_novel_with_list_style()


class GMDownloadRequest(object):
    url: str = ""
    book_id: str = ""


class GMDownloadResponse(object):
    code: GMDownloadStatus = GMDownloadStatus.error_unknown
    msg: str = ""
    data = None


class GMDownloadCallback(object):
    @staticmethod
    def callback(code: GMDownloadStatus = GMDownloadStatus.error_unknown,
                 msg: str = "",
                 data=None,
                 callback=None):
        print("msg：" + msg)
        if callback != None:
            response = GMDownloadResponse()
            response.code = code
            response.msg = msg
            response.data = data
            callback(response)

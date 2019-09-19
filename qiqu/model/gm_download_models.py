#!/usr/bin/env python
# -*- encoding: utf-8 -*-

from enum import Enum


class GMDownloadStatus(Enum):
    suspend = 101
    success = 200
    downloading = 201
    error = 503


class GMDownloadResponse(object):
    book_url: str = ""
    code: GMDownloadStatus = GMDownloadStatus.suspend
    msg: str = ""
    data: dict = None

    def __init__(self,
                 book_url: str,
                 code: GMDownloadStatus = GMDownloadStatus.suspend,
                 msg: str = "",
                 data: dict = None,
                 *args,
                 **kwargs):
        self.book_url = book_url
        self.code = code
        self.msg = msg
        self.data = data

        super().__init__(*args, **kwargs)


class GMDownloadRequest(object):
    book_url: str = ""
    extra: dict
    call_back = None

    def call(self, response):
        print("msg：", response.msg)
        if self.call_back:
            self.call_back(response)

    def __init__(self,
                 book_url: str,
                 extra=None,
                 call_back=None,
                 *args,
                 **kwargs):
        self.book_url = book_url
        self.extra = extra
        self.call_back = call_back
        super().__init__(*args, **kwargs)

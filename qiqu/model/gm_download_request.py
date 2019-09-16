#!/usr/bin/env python
# -*- encoding: utf-8 -*-

from enum import Enum


class GMDownloadStatus(Enum):
    download_success = 200
    downloading_chapter = 201
    download_error = 503


class GMDownloadRequest(object):
    url: str = ""
    book_id: str = ""
    extra: dict

    @property
    def request_id(self):
        if not self._request_id:
            task_id = None
            if self.book_id:
                task_id = self.book_id
            elif self.url:
                task_id = self.url
            self._request_id = task_id if task_id else None
        return self._request_id

    @request_id.setter
    def request_id(self, value):
        self._request_id = value

    @request_id.deleter
    def request_id(self):
        raise AttributeError("request_id can`t delete attr")

    def __init__(self, request_id=None, *args, **kwargs):
        self._request_id = request_id
        super().__init__(*args, **kwargs)


if __name__ == "__main__":
    resq = GMDownloadRequest()
    resq.book_id = "2"
    resq.url = "http:/ww"
    resq.request_id = 3234
    print(resq.request_id)


class GMDownloadResponse(object):
    code: GMDownloadStatus = GMDownloadStatus.download_error
    msg: str = ""
    data = None

    request = None
    __call_back = None

    def __init__(self, request=None, call_back=None, *args, **kwargs):
        if not request:
            request = GMDownloadRequest()
        self.request = request
        if call_back:
            self.__call_back = call_back

        super().__init__(*args, **kwargs)

    def call(self, code: GMDownloadStatus = None, msg: str = None, data=None):
        if msg:
            print("msg：" + msg)
        elif self.msg:
            print("msg：" + self.msg)
        else:
            print("msg: nonono")
        if self.__call_back:
            if code:
                self.code = code
            if not self.code:
                self.code = GMDownloadStatus.download_error
            if msg:
                self.msg = msg
            if data:
                self.data = data
            self.__call_back(self)

#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os, shutil


class GMDocumentManger(object):
    @staticmethod
    def readContent(path):
        if os.path.exists(path):
            with open(path, 'rb') as f:
                return f.read().decode('utf-8')
        return ""

    @staticmethod
    def replaceContent(path, content):
        if not isinstance(content, str):
            content = str(content)
        if content != None:
            with open(path, 'wb') as f:
                f.write(content.encode('utf-8'))

    @staticmethod
    def appendContent(path, content):
        reCotnent = GMDocumentManger.readContent(path)
        reCotnent += (("" if (len(reCotnent) == 0) else "\r\r") + content)
        GMDocumentManger.replaceContent(path, reCotnent)

    @staticmethod
    def downloadFilePath(fileName: str = "", extension=""):
        return GMDocumentManger.getFilePath('download', fileName, extension)

    @staticmethod
    def downloadTempFilePath(fileName: str = "", extension=""):
        return GMDocumentManger.getFilePath('download/temp', fileName,
                                            extension)

    @staticmethod
    def getFilePath(folder, fileName: str = "", extension=""):
        if folder == None or len(folder) == 0:
            return None
        abspath = os.path.abspath(".")
        downloadPath = os.path.join(abspath, folder)

        if not os.path.exists(downloadPath):
            os.mkdir(downloadPath)

        if fileName == None or len(fileName) == 0:
            return downloadPath

        if len(extension) > 0:
            extension = ("" if ("." in extension) else ".") + extension

        return os.path.join(downloadPath, fileName + extension)


if __name__ == "__main__":
    path = GMDocumentManger.downloadFilePath("22")
    GMDocumentManger.replaceContent(path, "")
    # if not os.path.exists(path):
    #     msg = "获取"
    #     print(msg)
    print("asdasd")
    # print(GMDocumentManger.downloadTempFilePath("haha", "text"))
    # print(GMDocumentManger.downloadFilePath())
    # shutil.move(
    #     GMDocumentManger.downloadTempFilePath("haha", "txt"),
    #     GMDocumentManger.downloadFilePath())
    # path = GMDocumentManger.downloadFilePath("haha", ".txt")
    # print(path)
    # print(os.path.exists(path))
    # GMDocumentManger.replaceContent(path, str({"3": "2xxx"}))

    # dic_str = GMDocumentManger.readContent(path)
    # print(dic_str)
    # print(type(dic_str))
    # dic_str = eval(dic_str)
    # print(dic_str)
    # print(dic_str["3"])
#!/usr/bin/env python
# -*- encoding: utf-8 -*-

import os
import json
from .gm_json import GMJson


class GMFileManger(object):
    """管理内容写入到本地的管理类"""
    @staticmethod
    def downloadFilePath(fileName: str = "", extension=""):
        return GMFileManger.getFilePath('download', fileName, extension)

    @staticmethod
    def downloadTempFilePath(fileName: str = "", extension=""):
        return GMFileManger.getFilePath('download/temp', fileName, extension)

    @staticmethod
    def getFilePath(folder, fileName: str = "", extension=""):
        # if len(fileName) == 0:
        #     fileName = "/"
        #     extension = ""
        abspath = os.path.abspath(".")
        folder_paths = folder.split("/")

        n_path = abspath
        for n in folder_paths:
            if "." not in n:
                n_path = os.path.join(n_path, n)
                if not os.path.exists(n_path):
                    os.mkdir(n_path)

        if folder and len(folder) > 0:
            downloadPath = os.path.join(abspath, folder)

        if not os.path.exists(downloadPath):
            os.mkdir(downloadPath)

        if not fileName or len(fileName) == 0:
            return downloadPath + "/"

        if len(extension) > 0:
            extension = ("" if ("." in extension) else ".") + extension
        return os.path.join(downloadPath, fileName + extension)

    @staticmethod
    def readContent(path):
        """
        读取文件内容
        """
        if os.path.exists(path):
            with open(path, 'rb') as f:
                return f.read().decode('utf-8')
        return ""

    @staticmethod
    def replaceContent(path, content):
        """
        覆盖（新建）文件内容
        """
        if isinstance(content, (list, tuple, dict)):
            new_content = None
            try:
                new_content = json.dumps(content)
            except BaseException:
                pass
            else:
                content = new_content
        elif not isinstance(content, str):

            new_content = None
            try:
                new_content = GMJson.dumps(content)
            except BaseException:
                pass
            else:
                content = new_content
        if content:
            with open(path, 'wb') as f:
                f.write(content.encode('utf-8'))

    @staticmethod
    def appendContent(path, content):
        """
        追加文件内容
        """
        reCotnent = GMFileManger.readContent(path)
        reCotnent += (("" if (len(reCotnent) == 0) else "\r\r") + content)
        GMFileManger.replaceContent(path, reCotnent)

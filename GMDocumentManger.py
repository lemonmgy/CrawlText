#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os


def appendContent(path, content):
    reCotnent = ""
    if os.path.exists(path):
        with open(path, 'rb') as f:
            reCotnent = f.read().decode('utf-8')
    if len(reCotnent) == 0:
        reCotnent = content
    else:
        reCotnent = reCotnent + "\r\r" + content

    with open(path, 'wb') as f:
        f.write(reCotnent.encode('utf-8'))


def downloadFilePath(folder, fileName: str, extension):
    if fileName == None or len(fileName) == 0:
        return None
    abspath = os.path.abspath(".")
    downloadPath = os.path.join(abspath, folder)
    if os.path.exists(downloadPath) == False:
        os.mkdir(downloadPath)

    return os.path.join(downloadPath, fileName + extension)

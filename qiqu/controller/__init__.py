#!/usr/bin/env python
# -*- encoding: utf-8 -*-

from .gm_biquge_request import GMBiqugeRequest
from .gm_download_novel_manager import GMDownloadNovelManager, GMDownloadCache
from .gm_download_novel_manager import GMDownloadRequest, GMDownloadResponse
from .gm_download_novel_manager import GMDownloadStatus

if __name__ == "__main__":
    GMBiqugeRequest()
    GMDownloadNovelManager()
    GMDownloadRequest("", "")
    GMDownloadResponse()
    GMDownloadCache()
    print(GMDownloadStatus.delete)

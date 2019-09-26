#!/usr/bin/env python
# -*- encoding: utf-8 -*-

from .gm_biquge_request import GMBiqugeRequest
from .gm_download_novel_manager import GMDownloadNovelManager, GMDownloadStatus
from .gm_download_novel_manager import GMDownloadRequest, GMDownloadResponse

if __name__ == "__main__":
    GMBiqugeRequest()
    GMDownloadNovelManager()
    GMDownloadRequest("", "")
    GMDownloadResponse()
    print(GMDownloadStatus.delete)

#!/usr/bin/env python
# -*- encoding: utf-8 -*-

from .gm_download_cache import GMDownloadCache
from .gm_html_string import GMHtmlString
from .gm_novel_http import GMNovelHttp

if __name__ == "__main__":
    GMDownloadCache()
    GMHtmlString()
    GMNovelHttp()

#!/usr/bin/env python
# -*- encoding: utf-8 -*-

from gmhelper import GMHTTP


class GMNovelHttp():
    bqg_host = "https://www.biquge.cm"
    bqg_search_url = bqg_host + "/modules/article/sou.php"

    @classmethod
    def requestBQYHTML(self, url, params=None, log: bool = True):
        response = GMHTTP.get(url, params, fields_encoding="gb2312", log=log)
        try:
            response.data = response.data.decode('GBK')
        finally:
            if len(response.data) == 0:
                print("出错的链接" + url + "      status = " + str(response.status))
            # print("response.data ==== " + response.data)
            return response

    @classmethod
    def append_bqg_host(cls, urls=None):
        if not urls:
            return urls

        if isinstance(urls, str):
            urls = [urls]
        if not isinstance(urls, (list, tuple, set)):
            return urls

        return GMHTTP.appen_url([GMNovelHttp.bqg_host] + urls)

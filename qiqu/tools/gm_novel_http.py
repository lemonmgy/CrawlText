#!/usr/bin/env python
# -*- encoding: utf-8 -*-

from gmhelper import GMHTTP


class GMNovelHttp(GMHTTP):
    bqg_host = "https://www.biquge.cm"
    bqg_search_url = bqg_host + "/modules/article/sou.php"

    @classmethod
    def requestBQYHTML(cls, url, params=None, log=True):
        response = cls.request(url, params, fields_encoding="gb2312", log=log)
        try:
            # response.data = response.data.decode('GBK', "replace")
            response.data = response.data.decode('GBK', "ignore")
        except IOError as e:
            print(e)
            print("内容有问题：" + url)
        finally:
            if len(response.data) == 0:
                print("出错的链接：" + url + "      status = " +
                      str(response.status))
            # print("response.data ==== " + response.data)
            return response


# 4985288

# https://www.biquge.cm/5/5750/3358967.html    status = start
# https://www.biquge.cm/5/5750/3358967.html    status = 200
# encoding error : input conversion failed due to input error, bytes 0xAD 0xA1 0xAD 0xA1
# encoding error : input conversion failed due to input error, bytes 0xAD 0xA1 0xAD 0xA1
# encoding error : input conversion failed due to input error, bytes 0xAD 0xA1 0xAD 0xA1
# I/O error : encoder error

    @classmethod
    def append_bqg_host(cls, urls=None):
        if not urls:
            return urls

        if isinstance(urls, str):
            urls = [urls]
        if not isinstance(urls, (list, tuple, set)):
            return urls

        return GMHTTP.appen_url([GMNovelHttp.bqg_host] + urls)

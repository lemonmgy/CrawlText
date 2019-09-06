#!/usr/bin/env python
# -*- coding: utf-8 -*-

# import os
# import certifi

import urllib3
from urllib import parse
from ..model import GMResponse


class GMHTTP(object):
    @classmethod
    def appen_url(self, pre_url: str = "", last_url: str = ""):
        if last_url.startswith('/'):
            last_url = last_url.lstrip('/')
        if pre_url.endswith('/') == False:
            pre_url = pre_url + '/'
        return pre_url + last_url

    @classmethod
    def get_header(self, cookie, user_agent):
        return {'Cookie': cookie, 'User-Agent': user_agent}

    @classmethod
    def appen_bqy_host(self, urls: str = ""):
        return self.appen_url(GMHTTP.bqy_host, urls)

    @classmethod
    def default_bqy_header(self):
        return GMHTTP.get_header(
            '__jsluid=a87f8c0b2f2754d4c0141e24162de96f; __cfduid=deea3a0da494f89c8bc097a1c2f3f434f1546590946; __jsl_clearance=1546864195.542|0|u9Ao5aXiIuvxPoeCUTK%2FKpUVhXg%3D',
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36'
        )

    @classmethod
    def get(self, url, fields=None, headers=None, fields_encoding=None):

        # http = urllib3.PoolManager(
        #     cert_file='/path/to/your/client_cert.pem',
        #     cert_reqs='CERT_REQUIRED',
        #     ca_certs=certifi.where())
        new_fields = fields
        if fields != None and fields_encoding != None:
            paramsStr = parse.urlencode(fields, encoding=fields_encoding)
            url = url + "?" + paramsStr
            new_fields = None

        http = urllib3.PoolManager()
        response = http.request('GET', url, new_fields, headers)

        gm_r = GMResponse()
        gm_r.url = url
        gm_r.data = response.data
        gm_r.status = response.status
        print(gm_r.url + "      status = " + str(gm_r.status))

        return gm_r

    bqy_host = "http://www.biquyun.com"
    bqy_search_url = "/modules/article/soshu.php"

    @classmethod
    def requestBQYHTML(self, url, params=None):
        response = GMHTTP.get(url, params, fields_encoding="gb2312")
        try:
            response.data = response.data.decode('GBK')
        finally:
            if len(response.data) == 0:
                print("出错的链接" + url + "      status = " + str(response.status))
            # print("response.data ==== " + response.data)
            return response
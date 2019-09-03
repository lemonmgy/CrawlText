#!/usr/bin/env python
# -*- coding: utf-8 -*-

# import os
# import certifi

import urllib3
from urllib import parse
from GMCrawlWebModels import GMResponse

bqy_host = "http://www.biquyun.com"
bqy_search_url = "/modules/article/soshu.php"


def appen_bqy_host(url: str = ""):
    return appen_url(bqy_host, url)


def default_bqy_header():
    return get_header(
        '__jsluid=a87f8c0b2f2754d4c0141e24162de96f; __cfduid=deea3a0da494f89c8bc097a1c2f3f434f1546590946; __jsl_clearance=1546864195.542|0|u9Ao5aXiIuvxPoeCUTK%2FKpUVhXg%3D',
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36'
    )


def requestBQYHTML(url, params=None):

    if params != None:
        paramsStr = parse.urlencode(params, encoding='gb2312')
        url = url + "?" + paramsStr

        # http = urllib3.PoolManager(
        #     cert_file='/path/to/your/client_cert.pem',
        #     cert_reqs='CERT_REQUIRED',
        #     ca_certs=certifi.where())
    http = urllib3.PoolManager()
    request = http.request("GET", url)
    print(url + "      status = " + str(request.status))
    response = GMResponse()
    response.request_url = url
    try:
        response.content = request.data.decode('GBK')
    finally:
        if len(response.content) == 0:
            print("出错的链接" + url + "      status = " + str(request.status))
        print("response.content ==== " + response.content)
        return response


def request_original_data(url):
    http = urllib3.PoolManager()
    requeset = http.request('GET', url=url)
    return requeset.data


def appen_url(pre_url: str = "", last_url: str = ""):
    if last_url.startswith('/'):
        last_url = last_url.lstrip('/')

    if pre_url.endswith('/') == False:
        pre_url = pre_url + '/'

    return pre_url + last_url


def get_header(cookie, user_agent):
    return {'Cookie': cookie, 'User-Agent': user_agent}

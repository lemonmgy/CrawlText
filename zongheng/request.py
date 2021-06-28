#!/usr/bin/env python
# -*- encoding: utf-8 -*-

import re
from gmhelper import GMHTTP
from gmhelper import GMJson


class GMZHHttp(GMHTTP):
    host = "https://m.zongheng.com/"

    @classmethod
    def get(cls, url, params=None, log=True):
        if "http" not in url:
            request_url = GMZHHttp.host + url
        headers = {
            'Cookie':
            "ZHID=97069241B6C575815E0018E4200B41ED; ver=2018; zhffr=www.google.com; zh_visitTime=1609234497960; v_user=https%3A%2F%2Fwww.google.com%2F%7Chttp%3A%2F%2Fwww.zongheng.com%2F%7C35710195; sajssdk_2015_cross_new_user=1; sensorsdata2015jssdkcross=%7B%22distinct_id%22%3A%22176add9c20b510-01db102ff3b0a2-6d112d7c-1024000-176add9c20ca17%22%2C%22%24device_id%22%3A%22176add9c20b510-01db102ff3b0a2-6d112d7c-1024000-176add9c20ca17%22%2C%22props%22%3A%7B%22%24latest_traffic_source_type%22%3A%22%E8%87%AA%E7%84%B6%E6%90%9C%E7%B4%A2%E6%B5%81%E9%87%8F%22%2C%22%24latest_referrer%22%3A%22https%3A%2F%2Fwww.google.com%2F%22%2C%22%24latest_referrer_host%22%3A%22www.google.com%22%2C%22%24latest_search_keyword%22%3A%22%E6%9C%AA%E5%8F%96%E5%88%B0%E5%80%BC%22%7D%7D; Hm_lvt_c202865d524849216eea846069349eb9=1609234498; Hm_up_c202865d524849216eea846069349eb9=%7B%22uid_%22%3A%7B%22value%22%3A%2297069241B6C575815E0018E4200B41ED%22%2C%22scope%22%3A1%7D%7D; Hm_lpvt_c202865d524849216eea846069349eb9=1609234512; platform=H5; Hm_lpvt_08a75cda7645e41f2d08825a3a78199b=1609238042; Hm_lvt_08a75cda7645e41f2d08825a3a78199b=1609238042; zhVisitTime=1609238038511; zhUserType=0; fingerprint=GrzXUq8CjFmZhFjYmB2Z1609238038820; zhUserType=0",
            'User-Agent':
            "Mozilla/5.0 (iPhone; CPU iPhone OS 13_2_3 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.0.3 Mobile/15E148 Safari/604.1",
            'Accept-Language':
            "zh-CN,zh;q=0.9",
            "Accept-Encoding":
            "gzip, deflate, br",
            "Accept":
            "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9"
        }
        # fields_encoding="gb2312",
        response = cls.request(request_url, params, headers=headers, log=log)
        print(response.data)
        return response

    @classmethod
    def list(cls, bookId=0, page=0):
        params = {
            "h5": "1",
            "bookId": bookId,
            "pageNum": page,
            "pageSize": "20",
            "chapterId": "0",
            "callback": "jsonp5",
            "asc": "0"
        }
        response = cls.get('h5/ajax/chapter/list', params)
        json = response.data
        matchObj = re.match(r'jsonp\d\(', json, re.M | re.I)
        if matchObj:
            json = json.replace(matchObj.group(), "")
            json = json[:-1]
        else:
            print("No match!!")
        json = GMJson.loads(json)
        # json.chapterlist chapters
        # matchObj = re.search( r'dogs', line, re.M|re.I)
        # if matchObj:
        #   print("search --> matchObj.group() : ", matchObj.group())
        # else:
        #   print("No match!!")
        # json = json[7:]
        # json = json[:-1]
        # print(json)


if __name__ == "__main__":
    GMZHHttp.get('http://book.zongheng.com/showchapter/1073902.html')
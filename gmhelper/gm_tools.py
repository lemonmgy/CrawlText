#!/usr/bin/env python
# -*- coding: utf-8 -*-

import threading
import datetime
import urllib3
import certifi
from urllib import parse
import os
import json

import io
from PIL import Image


def gm_isinstance(obj, t):
    """ 判断主要归类到四种大类型 (str) (dict)
    (list, tuple, set) (int, float, bool, complex) """

    gm_lists = (list, tuple, set)
    gm_numbers = (str, int, float, bool, complex)

    if t == dict:
        return isinstance(obj, dict)
    elif (t in gm_lists):
        return isinstance(obj, gm_lists)
    elif (t in gm_numbers):
        return isinstance(obj, gm_numbers)


class GMJson(object):
    """
    对象转json
    """
    string: str = None
    json: dict = None
    model = None

    @staticmethod
    def loads(s: str):
        return json.loads(s)

    @staticmethod
    def dumps(obj, key: str = None):
        gm_json = GMJson()
        try:
            gm_json.model = obj
            gm_json.string = gm_json.any_to_json_str(obj)
            if gm_json.string:
                gm_json.json = json.loads(gm_json.string)
        except BaseException:
            print(
                "json转化失败  -------  \n object- %s  \n string- %s \n json - %s"
                % (gm_json.model, gm_json.string, gm_json.json))
            gm_json.model = None
            gm_json.string = None
            gm_json.json = None
        else:
            pass
        return gm_json

    # 传入一个对象转化为json字符串
    def any_to_json_str(self, obj, key: str = None):
        if not obj:
            return ""
        elif gm_isinstance(obj, str):
            return self.__to_json_string(obj)
        elif gm_isinstance(obj, list):
            return self.__list_to_json(obj)
        elif gm_isinstance(obj, dict):
            return self.__dict_to_json(obj)
        else:
            return self.__obj_to_json_str(obj, key)

    def __obj_to_json_str(self, obj, key: str = None):
        ret_str = ""
        for name_key, value in vars(obj).items():
            name = self.deal_name(name_key)
            pre = ""
            if len(ret_str) != 0:
                pre = ","
            if not value:
                value = ""

            if gm_isinstance(value, str):
                ret_str += pre + self.__to_json_string(
                    name) + ":" + self.__to_json_string(value)
            elif gm_isinstance(value, list):
                ret_str += pre + self.__to_json_string(name) + ":"
                ret_str += self.__list_to_json(value)
            elif gm_isinstance(value, dict):
                ret_str += pre + self.__to_json_string(name) + ":"
                ret_str += self.__dict_to_json(value)
            else:
                obj_str = self.any_to_json_str(value, name)
                if len(obj_str) != 0:
                    obj_str = obj_str[1:len(obj_str) - 1]
                    ret_str += pre + obj_str

        ret_str = "{" + ret_str + "}"

        if key:
            if len(key) != 0 and len(ret_str) != 0:
                return "{%s:%s}" % (self.__to_json_string(key), ret_str)
        return ret_str

    def __list_to_json(self, o_list):
        ret_str = ""
        for obj in o_list:
            pre = ","
            if len(ret_str) == 0:
                pre = "["
            ret_str += pre + self.any_to_json_str(obj)
        return "[]" if (len(ret_str) == 0) else (ret_str + "]")

    def __dict_to_json(self, dic: dict):
        ret_str = ""
        pre = ""
        for key, value in dic.items():
            if len(ret_str) != 0:
                pre = ","
            ret_str += pre + self.__to_json_string(key) + ":"
            ret_str += self.any_to_json_str(value)

        ret_str = "{" + ret_str + "}"
        return ret_str

    # 将key value转化为json字符
    def __to_json_string(self, content):
        def deal_character(content):
            ret = str(content)
            p = {"\"": "”", "\\": ""}
            for (key, vlaue) in p.items():
                ret = ret.replace(key, vlaue)
            return ret

        return "\"" + deal_character(content) + "\""

    def deal_name(self, name):
        new_name_key = name
        if "_" in new_name_key:
            if new_name_key[0] == "_":
                index = 0
                for ele in new_name_key:
                    if ele != "_":
                        break
                    index += 1
                new_name_key = new_name_key[index:len(new_name_key)]
        return new_name_key


class GMResponse(object):
    url = ""
    status = ""
    data = ""
    o_response = None


class GMHTTP(object):
    """
    基本HTTP请求
    """
    @classmethod
    def appen_url(cls, urls: list = None):
        if not list:
            return None
        url = ""
        for e in urls:
            if not e.endswith('/') and e != urls[-1]:
                e += '/'
            if e.startswith('/'):
                e = e.lstrip('/')
            url += e
        return url

    @classmethod
    def get_header(cls, cookie, user_agent):
        return {'Cookie': cookie, 'User-Agent': user_agent}

    @classmethod
    def default_bqy_header(cls):
        return GMHTTP.get_header(
            '__jsluid=a87f8c0b2f2754d4c0141e24162de96f; \
             __cfduid=deea3a0da494f89c8bc097a1c2f3f434f1546590946; \
             __jsl_clearance=1546864195.542\
             |0|u9Ao5aXiIuvxPoeCUTK%2FKpUVhXg%3D',
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_2) \
             AppleWebKit/537.36 (KHTML, like Gecko) \
            Chrome/71.0.3578.98 Safari/537.36')

    @classmethod
    def get(cls,
            url,
            fields=None,
            headers=None,
            fields_encoding=None,
            log=True):

        # http = urllib3.PoolManager(
        #     cert_file='/path/to/your/client_cert.pem',
        #     cert_reqs='CERT_REQUIRED',
        #     ca_certs=certifi.where())
        new_fields = fields
        if fields and fields_encoding:
            paramsStr = parse.urlencode(fields, encoding=fields_encoding)
            url = url + "?" + paramsStr
            new_fields = None

        http = urllib3.PoolManager()
        http = urllib3.PoolManager(cert_reqs='CERT_REQUIRED',
                                   ca_certs=certifi.where())
        if log:
            print(url + "    status = start")
        response = http.request('GET', url, new_fields, headers)

        gm_r = GMResponse()
        gm_r.url = url
        gm_r.data = response.data
        gm_r.status = response.status
        gm_r.o_response = response
        if log:
            print(url + "    status = " + str(gm_r.status))
        return gm_r


class GMImage(object):
    """
    获取image 的类
    """
    @staticmethod
    def request_network_image(img_url):
        img_url = "https://www.biquyun.com/\
          files/article/image/14/14055/14055s.jpg"

        data_stream = GMHTTP.get(img_url).data
        data_stream = io.BytesIO(data_stream)
        pil_image = Image.open(data_stream)
        return pil_image


class GMThreading():
    thread = None
    re_kwargs = None
    """
    创建线程
    """
    @staticmethod
    def start(name: str, target, **kwargs):
        if not name:
            name = str(datetime.datetime.now())
        name = "threading_" + name

        t = threading.Thread(target=target, kwargs=kwargs, name=name)
        t.start()
        g = GMThreading()
        if kwargs:
            g.re_kwargs = dict(kwargs)
        g.thread = t
        return g

    @staticmethod
    def print_current_threading():
        print("current_threading：", threading.currentThread())


class GMFileManager(object):
    """管理内容写入到本地的管理类"""
    @staticmethod
    def downloadFilePath(fileName: str = "", extension=""):
        return GMFileManager.getFilePath('download', fileName, extension)

    @staticmethod
    def downloadTempFilePath(fileName: str = "", extension=""):
        folder_path = 'download/.temp'
        t_l = fileName.split("/")
        if len(t_l) > 1:
            fileName = t_l[-1]
            del t_l[-1]
            folder_path += "/" + "/".join(t_l)

        return GMFileManager.getFilePath(folder_path, fileName, extension)

    file_lock = threading.RLock()

    @staticmethod
    def getFilePath(folder, fileName: str = "", extension=""):
        GMFileManager.file_lock.acquire()
        # if len(fileName) == 0:
        #     fileName = "/"
        #     extension = ""
        abspath = os.path.abspath(".")
        folder_paths = folder.split("/")

        n_path = abspath
        for n in folder_paths:
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
        GMFileManager.file_lock.release()

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
    def createContent(path, content):
        """
        覆盖（新建）文件内容
        """
        if isinstance(content, (list, tuple, dict)):
            new_content = None
            try:
                new_content = json.dumps(content, ensure_ascii=False)
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
        reCotnent = GMFileManager.readContent(path)
        reCotnent += (("" if (len(reCotnent) == 0) else "\r\r") + content)
        GMFileManager.createContent(path, reCotnent)

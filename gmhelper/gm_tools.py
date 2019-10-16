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

from enum import Enum


class GMJson(object):
    """
    对象转json
    """
    string: str = None
    json: dict = None
    model = None

    def __gm_isinstance(self, obj, t):
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
        else:
            return isinstance(obj, t)

    @staticmethod
    def loads(s: str):
        """ 字符串转json """
        return json.loads(s)

    @staticmethod
    def dumps(obj, key: str = None):
        """ 对象转GMJson对象 """
        gm_json = GMJson()
        try:
            gm_json.model = obj
            gm_json.string = gm_json.__any_to_json_str(obj)
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
    def __any_to_json_str(self, obj, key: str = None):
        if not obj:
            return self.__to_json_string("")
        elif self.__gm_isinstance(obj, str):
            return self.__to_json_string(obj)
        elif self.__gm_isinstance(obj, list):
            return self.__list_to_json(obj)
        elif self.__gm_isinstance(obj, dict):
            return self.__dict_to_json(obj)
        elif self.__gm_isinstance(obj, Enum):
            return self.__to_json_string("")
        else:
            return self.__obj_to_json_str(obj, key)

    # 对象转string
    def __obj_to_json_str(self, obj, key: str = None):
        ret_str = ""
        for name_key, value in vars(obj).items():
            name = self.__deal_property_key(name_key)
            pre = ""
            if len(ret_str) != 0:
                pre = ","
            if not value:
                value = ""

            if self.__gm_isinstance(value, str):
                ret_str += pre + self.__to_json_string(
                    name) + ":" + self.__to_json_string(value)
            elif self.__gm_isinstance(value, list):
                ret_str += pre + self.__to_json_string(name) + ":"
                ret_str += self.__list_to_json(value)
            elif self.__gm_isinstance(value, dict):
                ret_str += pre + self.__to_json_string(name) + ":"
                ret_str += self.__dict_to_json(value)
            else:
                obj_str = self.__any_to_json_str(value, name)
                if len(obj_str) != 0:
                    obj_str = obj_str[1:len(obj_str) - 1]
                    ret_str += pre + obj_str

        ret_str = "{" + ret_str + "}"

        if key:
            if len(key) != 0 and len(ret_str) != 0:
                return "{%s:%s}" % (self.__to_json_string(key), ret_str)
        return ret_str

    # 列表转json
    def __list_to_json(self, o_list):
        ret_str = ""
        for obj in o_list:
            pre = ","
            if len(ret_str) == 0:
                pre = "["
            ret_str += pre + self.__any_to_json_str(obj)
        return "[]" if (len(ret_str) == 0) else (ret_str + "]")

    # 字典转json
    def __dict_to_json(self, dic: dict):
        ret_str = ""
        pre = ""
        for key, value in dic.items():
            if len(ret_str) != 0:
                pre = ","
            ret_str += pre + self.__to_json_string(key) + ":"
            ret_str += self.__any_to_json_str(value)

        ret_str = "{" + ret_str + "}"
        return ret_str

    # 将key value转化为json字符
    def __to_json_string(self, content):
        def deal_character(content):
            if not content:
                return ""
            ret = str(content)
            p = {"\"": "”", "\\": ""}
            for (key, vlaue) in p.items():
                ret = ret.replace(key, vlaue)
            return ret

        return "\"" + deal_character(content) + "\""

    # 处理对象属性 __key 这种形式
    def __deal_property_key(self, name):
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


class GMHTTPResponse(object):
    """
    http请求响应
    """
    url = ""
    status = ""
    data = ""
    o_response = None


class GMHTTP(object):
    """
    基本HTTP请求
    """
    @classmethod
    def is_url(cls, url: str = ""):
        return url.startswith("http")

    @classmethod
    def appen_url(cls, urls: list = None):
        """
        拼接字符串
        """
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
        if not cls.is_url(url):  # 本地
            gm_r = GMHTTPResponse()
            gm_r.url = url
            return gm_r
        """
        http get 请求
        """
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

        gm_r = GMHTTPResponse()
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
    """ 封装线程 """

    thread = None
    re_kwargs = None

    @staticmethod
    def start(name: str, target, **kwargs):
        """ 开启线程 """
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


class GMListdirMode(Enum):
    files = 1  # 所有文件
    dirs = 2  # 所有文件夹
    all = 3  # 所有文件和文件夹


class GMFileManager(object):
    """ 管理内容写入到本地的管理类 """
    @classmethod
    def read_content(cls, path):
        """ 读取文件内容 """
        if os.path.exists(path):
            with open(path, 'rb') as f:
                return f.read().decode('utf-8')
        return ""

    @classmethod
    def write_content(cls, path, content, overwrite=False, r=True):
        """  追加文件内容 overwrite : 是否覆盖文件 r : 代表追加内容是否换行 """

        # if isinstance(content, (list, tuple, dict)):
        #     new_content = ""
        #     try:
        #         new_content = json.dumps(content, ensure_ascii=False)
        #     except BaseException:
        #         new_content = ""
        #     else:
        #         content = new_content
        if not isinstance(content, str):

            new_content = ""
            try:
                new_content = GMJson.dumps(content).string
            except BaseException:
                new_content = ""
            else:
                content = new_content

        if not overwrite:
            reCotnent = cls.read_content(path)
            if r and len(reCotnent) > 0:
                reCotnent += ("\r\r" + content)
            else:
                reCotnent += content
            content = reCotnent

        if not os.path.exists(path):
            cls.create_file(path)
        with open(path, 'wb') as f:
            f.write(content.encode('utf-8'))

    @classmethod
    def download_path(cls, path: str = "", isc=True):
        folder_path = 'download'
        path = os.path.join(folder_path, path)
        path = cls.file_path(path)
        if isc:
            cls.create_file(path)
        return path

    @classmethod
    def download_temp_path(cls, path: str = "", isc=True):
        folder_path = 'download/.temp'
        path = os.path.join(folder_path, path)
        path = cls.file_path(path)
        if isc:
            cls.create_file(path)
        return path

    @classmethod
    def file_path(cls, add_path: str = ""):
        abspath = os.path.abspath(".")
        return os.path.join(abspath, add_path)

    file_lock = threading.RLock()

    @classmethod
    def create_file(cls, path: str = ""):
        def makedirs(p):
            if not os.path.exists(p):
                os.makedirs(p)

        cls.file_lock.acquire()
        if path[-1] == "/":
            makedirs(path)
        else:
            p = os.path.split(path)
            makedirs(p[0])
            if not os.path.exists(path):
                open(path, 'wb')
        cls.file_lock.release()

    @classmethod
    def list_files(cls, path: str, extension="", isabs=False):
        p_li = cls.list_dirs(path, GMListdirMode.files)

        if not p_li:
            return []

        ret = []
        if extension:
            for f in p_li:
                if os.path.splitext(f)[-1] == extension\
                   or os.path.splitext(f)[-1] == ("."+extension):
                    ret.append(f)
        else:
            ret.extend(p_li)

        # 获取相对路径
        if not isabs:
            temp_ret = []
            for f in ret:
                temp_ret.append(os.path.basename(f))
            ret = temp_ret

        return ret

    @classmethod
    def list_dirs(cls,
                  path: str,
                  mode: GMListdirMode = GMListdirMode.all,
                  recursion=False):
        """
        获取目录文件  path： 路径 mode：模式（文件，文件夹，文件和文件夹）recursion：是否递归子文件夹
        """
        file_paths = []
        if not recursion:

            for p in os.listdir(path):
                f_path = os.path.join(path, p)
                if mode == GMListdirMode.all:
                    file_paths.append(f_path)
                elif mode == GMListdirMode.files and os.path.isfile(f_path):
                    file_paths.append(f_path)
                elif mode == GMListdirMode.dirs and os.path.isdir(f_path):
                    file_paths.append(f_path)
        else:

            def file_list_dir(subpath: str):
                for p in os.listdir(subpath):
                    f_path = os.path.join(subpath, p)
                    if mode == GMListdirMode.files:
                        if os.path.isfile(f_path):
                            file_paths.append(f_path)
                        elif os.path.isdir(f_path):
                            file_list_dir(f_path)
                    elif mode == GMListdirMode.dirs:
                        if os.path.isdir(f_path):
                            file_paths.append(f_path)
                            file_list_dir(f_path)
                    elif mode == GMListdirMode.all:
                        if os.path.isfile(f_path):
                            file_paths.append(f_path)
                        elif os.path.isdir(f_path):
                            file_paths.append(f_path)
                            file_list_dir(f_path)

            file_list_dir(path)

        return file_paths


if __name__ == "__main__":
    print(os.path.splitext("鸟"))

#!/usr/bin/env python
# -*- coding: utf-8 -*-

import re
import json
import os


class GMKey(object):
    @staticmethod
    def key(data, defaultKey: str, addkey: str = None):
        """
        将 数组、元组的元素 or 字典的key 处理为唯一值，
        默认key  addkey后面追加的key
        """
        # 判断data是否满足条件
        if not isinstance(data, list) and not isinstance(
                data, tuple) and not isinstance(data, dict):
            return defaultKey

        if not isinstance(addkey, str) or len(addkey) == 0:
            addkey = "0"
        return GMKey.__key(data, defaultKey, addkey)

    @staticmethod
    def __key(data, defaultKey, addkey):

        if defaultKey in data:
            defaultKey = ("" if len(defaultKey) == 0 else
                          (defaultKey + "_")) + addkey
            return GMKey.__key(data, defaultKey, addkey)
        else:
            return defaultKey


class GMString(object):
    @classmethod
    def replace(self, content: str, rep: [], be_rep):
        """
        多处替换文本
        """
        for a in rep:
            content = content.replace(a, be_rep)
        return content

    @classmethod
    def remove_tag(self, content, tags):
        """
        移除闭合标签 可以数组，或者字符串
        """
        ret = str(content)
        if isinstance(tags, str):
            ret = ret.replace('<%s>' % str(tags), "")
            ret = ret.replace('</%s>' % str(tags), "")
        elif isinstance(tags, list):
            for tag in tags:
                ret = ret.replace('<%s>' % tag, "")
                ret = ret.replace('</%s>' % tag, "")
        return ret

    @classmethod
    def remove_escape_character(self,
                                content,
                                include_garbage_character: bool = False):
        """移除html符号  """
        ret = str(content)
        pat = re.compile(r"&#.+?;")
        search_ret = re.findall(pat, ret)
        if not search_ret:
            for b in search_ret:
                ret = ret.replace(b, "")
        if include_garbage_character:
            ret = self.remove_garbage_character(content)
        return ret

    @classmethod
    def remove_garbage_character(self, content: str):
        """移除空格换行等符号"""
        char_sys = ['\n', '<br>']
        # for s in char_sys:
        #     content = replace(content,
        #                       re.compile(r'%s+' % (s)).findall(content), s)
        return self.replace(content, char_sys + ["　", " ", "\xa0"], "")


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
            print("json转化成功")
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
            return str(content).replace("\"", "”")

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


class GMPath():
    """获取路径类"""

    @staticmethod
    def downloadFilePath(fileName: str = "", extension=""):
        return GMPath.getFilePath('download', fileName, extension)

    @staticmethod
    def downloadTempFilePath(fileName: str = "", extension=""):
        return GMPath.getFilePath('download/temp', fileName, extension)

    @staticmethod
    def getFilePath(folder, fileName: str = "", extension=""):
        # if len(fileName) == 0:
        #     fileName = "/"
        #     extension = ""
        abspath = os.path.abspath(".")
        folder_paths = folder.split("/")

        n_path = abspath
        for n in folder_paths:
            if "." not in n:
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
        return os.path.join(downloadPath, fileName + extension)


class GMFileManger(object):
    """管理内容写入到本地的管理类"""

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
    def replaceContent(path, content):
        if isinstance(content, (list, tuple, dict)):
            new_content = None
            try:
                new_content = json.dumps(content)
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
        reCotnent = GMFileManger.readContent(path)
        reCotnent += (("" if (len(reCotnent) == 0) else "\r\r") + content)
        GMFileManger.replaceContent(path, reCotnent)


info_dict_key = "__info_dict_key"
info_list_key = "__info_list_key"


class GMDownloadCache():
    @staticmethod
    def all_list_info():

        cache_dict = GMDownloadCache.read_info()
        info_list: list = cache_dict[info_list_key]
        info_dict: dict = cache_dict[info_dict_key]

        ret = []
        keys = list(info_dict.keys())
        need_save = False
        for book_id in list(info_list):
            if book_id not in keys:
                need_save = True
                info_list.remove(book_id)
            else:
                ret.append(info_dict[book_id])

        for book_id in keys:
            if book_id not in info_list:
                need_save = True
                info_list.append(book_id)
                ret.append(info_dict[book_id])
        if need_save:
            GMDownloadCache.write_info(cache_dict)
        return ret

    @staticmethod
    def is_exists(book_id):
        cache_dict = GMDownloadCache.read_info()
        info_dict: dict = cache_dict[info_dict_key]
        return book_id in list(info_dict.keys())

    @staticmethod
    def read_info():
        info_path = GMPath.downloadTempFilePath('download_info.txt')
        content = GMFileManger.readContent(info_path)

        cache_dict: dict = None
        if content:
            try:
                cache_dict = GMJson.loads(content)
            finally:
                pass

        if not cache_dict:
            cache_dict = {}

        keys = list(cache_dict.keys())
        if info_dict_key not in keys:
            cache_dict[info_dict_key] = {}

        if info_list_key not in keys:
            cache_dict[info_list_key] = []

        return cache_dict

    @staticmethod
    def write_info(cache_dict):
        info_path = GMPath.downloadTempFilePath('download_info.txt')
        GMFileManger.replaceContent(info_path, cache_dict)

    @staticmethod
    def save(book_id: str, chapter_id: str, name: str):
        if not book_id or not name:
            return
        if not chapter_id:
            chapter_id = ""

        cache_dict = GMDownloadCache.read_info()
        info_list: list = cache_dict[info_list_key]

        if book_id not in info_list:
            info_list.append(book_id)

        info_dict: dict = cache_dict[info_dict_key]
        info_dict[book_id] = {
            "book_id": book_id,
            "name": name,
            "chapter_id": chapter_id
        }
        GMDownloadCache.write_info(cache_dict)

    @staticmethod
    def remove(book_id: str = None):
        if not book_id:
            return
        cache_dict = GMDownloadCache.read_info()
        info_list: list = cache_dict[info_list_key]
        if book_id in info_list:
            info_list.remove(book_id)

        info_dict: dict = cache_dict[info_dict_key]
        if book_id in info_dict:
            del info_dict[book_id]
        GMDownloadCache.write_info(cache_dict)


if __name__ == "__main__":

    # index = 0
    # while index < 5:
    GMDownloadCache.save("123", "", "xxx")
    #     index += 1

    # print(GMDownloadCache.read_info())
    print(GMDownloadCache.all_list_info())

    # a = ["2", "3", "4"]
    # b = list()
    # b.extend(a)
    # print(a, b)
    # b.remove("2")
    # print(a, b)
    # g.json_string = 123

    # gx = GMJson()
    # gx.model = g

    # json_g = GMJson()
    # json_g.model = gx
    # print("json转化失败  -------  \n object- %s  \n string- %s \n json - %s" %
    #       (g, {
    #           "123": "2"
    #       }, ["s"]))

    # try:
    #     vars("123")
    # except BaseException:
    #     print("sadf")
    # else:
    #     print("pass")
    # s = 0
    # try:
    #     result = 20 / int(s)
    #     print('20除以%s的结果是: %g' % (s, result))
    # except ValueError:
    #     print('值错误，您必须输入数值')
    # except ArithmeticError:
    #     print('算术错误，您不能输入0')
    # else:
    #     print('没有出现异常')
    # print("程序继续运行")

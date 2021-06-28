#!/usr/bin/env python
# -*- coding: utf-8 -*-
from qiqu.ui.gm_window_frame import GMWindowFrame
# from gmhelper.gm_tools import GMHTTP
import re
import time  # 引入time模块
# from zongheng import GMZHHttp
from gmhelper import GMFileManager

# from qiqu import GMNovelHttp, GMBiqugeRequest


def replace_tag(content):
    # content = re.sub(r'(.|\n)*用户上传之内容开始(.|\n)*Bxwx.Org\n*《', "《", content)
    # content = re.sub(r'《 笔下(.|\n)*结束(.|\n)*', "end", content)
    content = re.sub(r'神印王座&神印王座', "", content)
    content = re.sub(r'注意：本章.*', "", content)
    content = re.sub(r'\s*\(下载小说到云轩阁.*', "", content)
    content = re.sub(r'\s*\(未完待续.*', "", content)
    content = re.sub(r'\s*\(未完待续.*', "", content)

    content = re.sub(r'第.*免费\)?', "", content)
    content = re.sub(r'\n-*\s*分节阅读[\s\d]*\n', "", content)
    content = re.sub(r'分节阅读[\s\d]*', "", content)

    # &lt;divstyle=&quot;display:none&quot;&gt;&lt;/div&gt;
    content = re.sub(r'([a-z]|\s)*(=|:)[a-z]*&[a-z]*;', "", content)
    content = re.sub(r'/[a-z]*&[a-z]*;', "", content)
    content = re.sub(r'[a-z]*:[a-z]*', "", content)
    content = re.sub(r'&[a-z]*;', "", content)
    content = re.sub(r'&[a-z]*', "", content)

    content = re.sub(r'<.*>?', "", content)
    content = re.sub(r'.*/>?', "", content)
    content = re.sub(r'\s*\[=*\s*=*\]?', "", content)
    content = re.sub(r'-*', "", content)
    content = re.sub(r'发布[\s|;]*', "", content)
    content = re.sub(r' *', "", content)

    return content


def crawl_text():
    path = "./download/极品家丁.txt"
    print("read")
    content = time.strftime(
        "%Y-%m-%d %H:%M:%S",
        time.localtime()) + GMFileManager.read_content(path)
    print("replace")
    content = replace_tag(content)
    print("write")
    GMFileManager.write_content(path, content, True)


if __name__ == "__main__":
    # crawl_text();
    # GMZHHttp.list()
    # GMBiqugeRequest.getNovelContentData(
    #     "https://www.biquge.cm/5/5750/3358135.html")
    GMWindowFrame.run()

#!/usr/bin/env python
# -*- coding: utf-8 -*-

# p = PyQuery(html)
# p("#nr .odd a"))  # 是查找id的标签  .是查找class 的标签  link 是查找link 标签 中间的空格表示里层

import GMRequest
import GMTools
from GMCrawlWebModels import GMBookInfo, GMModuleBook, GMBookChapter, GMResponse
from pyquery import PyQuery
import re
import json


# 原始数据， json字符串， json数据
def return_data_deal(o_data):

    json_ret = {}
    json_str = ""
    try:
        json_str = GMTools.obj_to_json(o_data)
        json_ret = json.loads(json_str)
    except:
        print("json转化失败")
    else:
        print("json转化成功")

    return o_data, json_str, json_ret

# 首页
def getHomePageData():
    respone = GMRequest.requestBQYHTML(GMRequest.bqy_host)

    # pat = re.compile(r"hotcontent\">")
    # ret = re.search(pat, )
    # #表示查询的id .为class .items()会是一个生成器
    p = PyQuery(respone.content)

    # <img src="https://www.biquyun.com/files/article/image/14/14055/14055s.jpg"/>
    # a.attr('src') 拿到 src对应的url

    # 热门小说
    list = p('#hotcontent .item').items()
    hot_content = []
    for item in list:
        book = GMBookInfo()
        # 书名
        img_item = item('.image img')
        book.name = img_item.attr('alt')
        book.img = img_item.attr('src')
        # 跳转链接
        book.url = item('.image a').attr('href')

        # 作者 <span>风凌天下</span>
        book.author = str(item('dl dt span').text())

        # <dd>药不成丹只是毒，人不成神终成灰。&#13;</dd>
        book.des = GMTools.remove_escape_character(
            str(item('dl dd').text()), True)

        hot_content.append(book)

    # 模块小说
    novelslist = p('#main .novelslist .content').items()
    novels_list = []
    for content in novelslist:
        module_book = GMModuleBook()
        module_book.book_list = []
        module_book.book_category_des = content('h2').text()
        novels_list.append(module_book)

        top = content('.top')
        top_book = GMBookInfo()
        top_book.img = top('.image img').attr('src')
        top_book.url = top('dl dt a').attr('href')
        top_book.name = top('dl dt a').text()
        top_book.des = top('dl dd').text()

        module_book.top_book = top_book

        ul_li = content('ul li').items()
        for li in ul_li:
            li_book = GMBookInfo()
            li_book.book_type = module_book.book_category_des
            li_book.url = li('a').attr('href')
            li_book.name = li('a').text()

            pat = re.compile(r'</a>.+?</li>')
            search_ret = re.search(pat, str(li))
            if search_ret != None:
                ret = GMTools.remove_tag(str(search_ret.group()), ['a', 'li'])
                li_book.author = GMTools.replace(ret, ["/", " "], "")

            module_book.book_list.append(li_book)

    # 最近更新小说
    newscontent = p('#newscontent')
    news_ul_li = newscontent('.l ul li').items()
    week_ul_li = newscontent('.r ul li').items()

    new_module = GMModuleBook()
    new_module.book_category_des = newscontent('.l h2').text()
    new_module.book_list = []

    for ele_li in news_ul_li:
        book = GMBookInfo()
        s2_a = ele_li('.s2 a')
        book.name = s2_a.text()
        book.url = s2_a.attr('href')
        book.book_type = ele_li('.s1').text()
        s3_a = ele_li('.s3 a')
        book.author = ele_li('.s4').text()

        book.new_chapter = GMBookChapter()
        book.new_chapter.title = s3_a.text()
        book.new_chapter.url = GMRequest.appen_bqy_host(s3_a.attr('href'))
        book.new_chapter.date = ele_li('.s5').text()

        new_module.book_list.append(book)

    # 本周热门小说
    week_module = GMModuleBook()
    week_module.book_category_des = newscontent('.r h2').text()
    week_module.book_list = []

    for ele_li in week_ul_li:
        book = GMBookInfo()
        book.name = ele_li('.s2 a').text()
        book.url = ele_li('.s2 a').attr('href')
        book.book_type = ele_li('.s1').text()
        book.author = ele_li('.s5').text()
        week_module.book_list.append(book)

    json_dic = {
        "hot_content": hot_content,
        "novels_list": novels_list,
        "new_module": new_module,
        "week_module": week_module
    }
    return return_data_deal(json_dic)


# 小说列表页面
def getNovelListData(url: str = "", book_id: str = ""):
    if url == None or len(url) == 0:
        if book_id == None or len(book_id) == 0:
            return None
        else:
            url = GMRequest.appen_bqy_host(book_id + "/")
    response = GMRequest.requestBQYHTML(url)
    p = PyQuery(response.content)
    book = GMBookInfo()
    box_con_sidebar = p('.box_con #sidebar')
    img = box_con_sidebar('img').attr('src')
    if img == None:
        img = box_con_sidebar('img').attr('onerror')
        pat = re.compile(r'/.*?.jpg')
        img = str(re.search(pat, img).group())
    book.img = GMRequest.appen_bqy_host(img)

    box_con_maininfo = p('.box_con #maininfo')
    book.des = box_con_maininfo('#intro p').text()

    info = box_con_maininfo('#info')
    book.name = info('h1').text()

    book.new_chapter = GMBookChapter()
    info_p = info('p').items()

    def book_info_split(info_content: str):
        if isinstance(info_content, str) == False:
            return info_content
        info_content = GMTools.remove_escape_character(info_content, True)
        content_split = info_content.split('：')
        return info_content if (len(content_split) <= 0) else content_split[-1]

    i = 0
    for ele_p in info_p:
        if i == 0:
            book.author = book_info_split(ele_p.text())
        elif i == 2:
            book.new_chapter.date = book_info_split(ele_p.text())
        elif i == 3:
            book.new_chapter.title = ele_p('a').text()
            book.new_chapter.url = GMRequest.appen_url(url,
                                                       ele_p('a').attr('href'))
        else:
            pass
        i += 1

    box_con_list_dl_dd = p('.box_con #list dl dd').items()
    chapter_list = []
    book.chapter_list = chapter_list
    for ele_dd in box_con_list_dl_dd:
        chapter = GMBookChapter()
        chapter.title = ele_dd('a').text()
        chapter.url = GMRequest.appen_url(url, ele_dd('a').attr('href'))
        chapter_list.append(chapter)

    return return_data_deal(book)


def getNovelContentData(url: str = "", book_id: str = "",
                        chapter_id: str = ""):

    if url == None or len(url) == 0:
        if book_id != None and chapter_id != None and len(book_id) > 0 and len(
                chapter_id) > 0:
            url = GMRequest.appen_bqy_host(book_id + "/" + chapter_id +
                                           ".html")
        else:
            return ""

    respone = GMRequest.requestBQYHTML(url)
    p = PyQuery(respone.content)
    box_con = p('.content_read .box_con')
    bookname = box_con('.bookname')

    chapter = GMBookChapter()
    chapter.url = url
    chapter.title = bookname('h1').text()
    bottem1 = bookname('.bottem1 a')

    pat = re.compile(r'/[0-9]*_[0-9]+/[0-9]+.html|/[0-9]*_[0-9]+/')
    chapter_urls = pat.findall(str(bottem1))
    if len(chapter_urls) >= 3:
        chapter.pre_url = GMRequest.appen_bqy_host(chapter_urls[0])
        chapter.suf_url = GMRequest.appen_bqy_host(chapter_urls[-1])

    book_content = box_con('div #content').text()
    chapter.content = GMTools.remove_escape_character(book_content, True)
    return return_data_deal(chapter)


def searchNovelData(name):
    # 请求搜索html https://www.biquyun.com/modules/article/soshu.php?searchkey=+%B4%D3%C1%E3%BF%AA%CA%BC
    respone = GMRequest.requestBQYHTML(
        GMRequest.appen_bqy_host('modules/article/soshu.php'),
        {"searchkey": name})
    # print(respone.content)
    # print(respone)
    print(
        "\n\n\n\n\n ------------------------------------------------------------------------------ \n\n\n\n\n\n"
    )

    book_list = deal_search_novel_result_page(respone)

    if len(book_list) <= 0:
        pat = re.compile(r'format=xhtml;.*?"/>')
        pat_ret = pat.findall(str(respone.content))
        if len(pat_ret) > 0:
            url = pat_ret[0]
            pat = re.compile(r'[0-9]+_[0-9]+')
            url = pat.findall(str(url))
            if len(url) > 0:
                book = GMBookInfo()
                book.name = name
                book.url = GMRequest.appen_bqy_host(url[0] + "/")
                book_list = [book]

    return return_data_deal(book_list)


def deal_search_novel_result_page(respone: GMResponse):
    p = PyQuery(respone.content)
    tbody = p('#main #content .grid #nr').items()

    def create_book(tds: list):
        tds = list(tds)
        book = GMBookInfo()
        book.name = tds[0]('a').text()
        book.url = tds[0]('a').attr('href')
        book.author = tds[2].text()
        book.new_chapter = GMBookChapter()
        book.new_chapter.url = GMRequest.appen_bqy_host(
            tds[1]('a').attr('href'))
        book.new_chapter.title = tds[1].text()
        book.new_chapter.date = tds[4].text()
        return book

    book_list = []

    for ele in tbody:
        tds = ele('td').items()
        book_list.append(create_book(tds))
    return book_list

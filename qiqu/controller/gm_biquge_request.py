#!/usr/bin/env python
# -*- coding: utf-8 -*-

# p = PyQuery(html)
# p("#nr .odd a"))  # 是查找id的标签  .是查找class 的标签  link 是查找link 标签 中间的空格表示里层

import re
from pyquery import PyQuery

from ..model import GMBookInfo, GMModuleBook, GMBookChapter

from gmhelper import GMResponse, GMJson
from ..tools import GMDownloadCache, GMHtmlString, GMNovelHttp


class GMBiqugeRequest():

    # 原始数据， json字符串， json数据
    @classmethod
    def return_data_deal(cls, o_data):
        return GMJson.dumps(o_data)

    # 小说网站首页
    @classmethod
    def getHomePageData(cls):
        response = GMNovelHttp.requestBQYHTML(GMNovelHttp.bqg_host)

        # pat = re.compile(r"hotcontent\">")
        # ret = re.search(pat, )
        # #表示查询的id .为class .items()会是一个生成器
        p = PyQuery(response.data)

        # <img src="https://www.biquyun.com
        # /files/article/image/14/14055/14055s.jpg"/>
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
            book.url_with_book_id(item('.image a').attr('href'))

            # 作者 <span>风凌天下</span>
            book.author = str(item('dl dt span').text())

            # <dd>药不成丹只是毒，人不成神终成灰。&#13;</dd>
            book.des = GMHtmlString.remove_escape_character(
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
            top_book.url_with_book_id(top('dl dt a').attr('href'))
            top_book.name = top('dl dt a').text()
            top_book.des = top('dl dd').text()

            module_book.top_book = top_book

            ul_li = content('ul li').items()
            for li in ul_li:
                li_book = GMBookInfo()
                li_book.book_type = module_book.book_category_des
                li_book.url_with_book_id(li('a').attr('href'))
                li_book.name = li('a').text()

                pat = re.compile(r'</a>.+?</li>')
                search_ret = re.search(pat, str(li))
                if not search_ret:
                    ret = GMHtmlString.remove_tag(str(search_ret.group()))
                    for e in ["/", " "]:
                        ret = ret.replace(e, "")
                    li_book.author = ret

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
            book.url_with_book_id(s2_a.attr('href'))
            book.book_type = ele_li('.s1').text()
            s3_a = ele_li('.s3 a')
            book.author = ele_li('.s4').text()

            book.new_chapter = GMBookChapter()
            book.new_chapter.title = s3_a.text()
            book.new_chapter.url_with_chapter_id(s3_a.attr('href'),
                                                 book.book_url)
            book.new_chapter.date = ele_li('.s5').text()

            new_module.book_list.append(book)

        # 本周热门小说
        week_module = GMModuleBook()
        week_module.book_category_des = newscontent('.r h2').text()
        week_module.book_list = []

        for ele_li in week_ul_li:
            book = GMBookInfo()
            book.name = ele_li('.s2 a').text()
            book.url_with_book_id(ele_li('.s2 a').attr('href'))
            book.book_type = ele_li('.s1').text()
            book.author = ele_li('.s5').text()
            week_module.book_list.append(book)

        json_dic = {
            "hot_content": hot_content,
            "novels_list": novels_list,
            "new_module": new_module,
            "week_module": week_module
        }
        return cls.return_data_deal(json_dic)

    # 小说列表页面
    @classmethod
    def getNovelListData(cls, book_url: str = ""):
        if not book_url:
            return GMJson
        response = GMNovelHttp.requestBQYHTML(book_url)
        p = PyQuery(response.data)
        book = GMBookInfo()
        book.url_with_book_id(book_url)
        box_con_sidebar = p('.box_con #sidebar')
        img = box_con_sidebar('img').attr('src')
        if not img:
            img = box_con_sidebar('img').attr('onerror')
            pat = re.compile(r'/.*?.jpg')
            img = str(re.search(pat, img).group())
        book.img = GMNovelHttp.append_bqg_host(img)

        box_con_maininfo = p('.box_con #maininfo')
        book.des = box_con_maininfo('#intro p').text()

        info = box_con_maininfo('#info')
        book.name = info('h1').text()

        book.new_chapter = GMBookChapter()
        info_p = info('p').items()

        def book_info_split(info_content: str):
            if not isinstance(info_content, str):
                return info_content
            info_content = GMHtmlString.remove_escape_character(
                info_content, True)
            content_split = info_content.split('：')
            return info_content if (
                len(content_split) <= 0) else content_split[-1]

        i = 0
        for ele_p in info_p:
            if i == 0:
                book.author = book_info_split(ele_p.text())
            elif i == 2:
                book.new_chapter.date = book_info_split(ele_p.text())
            elif i == 3:
                book.new_chapter.title = ele_p('a').text()
                book.new_chapter.url_with_chapter_id(
                    ele_p('a').attr('href'), book.book_url)
            else:
                pass
            i += 1

        box_con_list_dl_dd = p('.box_con #list dl dd').items()
        chapter_list = []
        book.chapter_list = chapter_list
        for ele_dd in box_con_list_dl_dd:
            chapter = GMBookChapter()
            chapter.title = ele_dd('a').text()
            c_url = ele_dd('a').attr('href')
            chapter.url_with_chapter_id(c_url, book.book_url)
            chapter_list.append(chapter)

        return cls.return_data_deal(book)

    @classmethod
    def getNovelContentData(cls, chapter_url):
        response = GMNovelHttp.requestBQYHTML(chapter_url)
        p = PyQuery(response.data)
        box_con = p('.content_read .box_con')
        bookname = box_con('.bookname')

        chapter = GMBookChapter()
        chapter.url_with_chapter_id(chapter_url)
        chapter.chapter_title = bookname('h1').text()

        book_content = box_con('div #content').text()
        chapter.content = GMHtmlString.remove_escape_character(
            book_content, True)
        return cls.return_data_deal(chapter)

    @classmethod
    def searchNovelData(cls, name):
        # 请求搜索html https://www.biquyun.com/# modules/article/soshu.php?
        # searchkey=+%B4%D3%C1%E3%BF%AA%CA%BC

        def multiple_search_result_data(response: GMResponse):
            p = PyQuery(response.data)
            tbody = p('#main #content .grid #nr').items()

            def create_book(tds: list):
                tds = list(tds)
                book = GMBookInfo()
                book.name = tds[0]('a').text()
                book.url_with_book_id(tds[0]('a').attr('href'))
                book.author = tds[2].text()
                book.new_chapter = GMBookChapter()
                book.new_chapter.url_with_chapter_id(tds[1]('a').attr('href'),
                                                     book.book_url)
                book.new_chapter.title = tds[1].text()
                book.new_chapter.date = tds[4].text()
                return book

            book_list = []

            for ele in tbody:
                tds = ele('td').items()
                book_list.append(create_book(tds))
            return book_list

        def a_search_result_data(response: GMResponse):
            # format=xhtml; url=https://m.biquge.cm/8/8453/
            pat = re.compile(r'format=xhtml;.*?"/>')
            pat1 = pat.findall(str(response.data))
            if pat1:
                pat2 = re.search(r'[0-9]+/[0-9]+', pat1[0])
                if pat2:
                    book = GMBookInfo()
                    book.name = name
                    book.url_with_book_id(
                        GMNovelHttp.append_bqg_host(str(pat2.group())))
                    p = PyQuery(response.data)
                    # p("#nr .odd a"))  # 是查找id的标签 \
                    # .是查找class 的标签  link 是查找link 标签 中间的空格表示里层
                    info = p('#maininfo #info')
                    au = re.compile(r'<p>作.*?者：.*?</p>').findall(str(info))
                    if au:
                        au = GMHtmlString.remove_tag(str(au[0]))
                        au = re.sub(re.compile('作.*?者：'), "", au)
                        au = GMHtmlString.remove_escape_character(au, True)
                        book.author = au
                    print(info)
                    return [book]
            return []

        response = GMNovelHttp.requestBQYHTML(GMNovelHttp.bqg_search_url,
                                              {"searchkey": name})
        book_list = multiple_search_result_data(response)

        if not book_list:
            book_list = a_search_result_data(response)
        if not book_list:
            book_list = []
        return cls.return_data_deal(book_list)

    @classmethod
    def get_download_cache_data(cls):
        all_info = GMDownloadCache.all_list_info()
        return all_info
        # if all_info:
        #     data_list = []
        #     for ele_dic in all_info:
        #         box_list_model = GMListboxListModel()
        #         box_list_model.title = GMValue.value(ele_dic,
        #                                              "name") + "_准备下载..."
        #         box_list_model.data = ele_dic
        #         data_list.append(box_list_model)

        #     menu_model = GMListboxMenuModel(data_list)
        #     return menu_model
        # return None

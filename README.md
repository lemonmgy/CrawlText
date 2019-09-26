# CrawlText

tkinter:

# print(main_window.geometry())
print(main_window.winfo_screenwidth(),
      main_window.winfo_screenheight())
print(main_window.winfo_screenmmwidth(),
      main_window.winfo_screenmmheight())
# main_window.geometry("380x500+0+0")
# main_window.title("小说首页")
# main_window.iconbitmap("")

destroy()  移除视图

Tk  attributes('-topmost', True)
窗口置顶


json:

json.loads()   字符串，二进制转json 
json.dumps()   json转字符串  




<!-- 单例 -->
    # __state = {}
    # def __new__(cls, *args, **kwargs):
    #     ob = super(GMDownloadNovelManager, cls).__new__(cls, *args, **kwargs)
    #     ob.__dict__ = cls.__state
    #     return ob
#!/usr/bin/env python
# -*- encoding: utf-8 -*-

import sched
import time
from datetime import datetime

# class GMSchdule(object):

#     # 初始化sched模块的scheduler类
#     # 第一个参数是一个可以返回时间戳的函数，第二参数可以在定时未到达之前阻塞
#     schedule = None

#     # 被周期性调度触发函数
#     def printTime(self, inc):
#         print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
#         self.schedule.enter(inc, 0, self.printTime, (inc, ))

#     # 默认参数60s
#     def main(self, inc=60):
#         # enter四个参数分别为：间隔事件,优先级（用于同时到达两个事件同时执行的顺序），被调度触发的函数
#         # 给该触发器函数的参数（tuple形式）
#         self.schdule = sched.scheduler(time.time, time.sleep)
#         self.schedule.enter(0, 0, self.printTime, (inc, ))
#         self.schedule.run()

# g = GMSchdule()
# g.main(5)


def conversion_title(ostr: str = ""):
    if not ostr:
        return ""

    dic = {
        "0": "零",
        "1": "一",
        "2": "二",
        "3": "三",
        "4": "四",
        "5": "五",
        "6": "六",
        "7": "七",
        "8": "八",
        "9": "九"
    }
    uni_list = ["", "十", "百", "千", "万", "十万", "百万", "千万", "亿"]

    li = list(ostr)
    li.reverse()
    uni = 0
    ret_str = []
    for x in li:
        if x not in dic:
            ret_str.append(x)
            continue

        if "章" not in ret_str:
            ret_str.append("章")
        o_x = dic[x]

        if len(ret_str) == 0 and o_x == "零":
            o_x = ""

        if len(o_x):
            if o_x != "零":
                o_x += uni_list[uni]
            ret_str.append(o_x)
        uni += 1
    ret_str.reverse()
    ret_str = "".join(ret_str)
    if "第" not in ret_str:
        ret_str = "第" + ret_str
    return ret_str


if __name__ == "__main__":
    strss = "123 找那个会"
    print("xxx".join(strss.split(" ")))

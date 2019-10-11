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

name = "哈哈哈2"
print(name.replace("2", "x"))

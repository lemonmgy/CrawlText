#!/usr/bin/env python
# -*- encoding: utf-8 -*-

import threading
import datetime


class GMThreading():
    @staticmethod
    def start(target, name: str, **kwargs):
        if not name:
            name = str(datetime.datetime.now())
        name = "threading_" + name
        t = threading.Thread(target=target, kwargs=kwargs, name=name)
        t.start()


if __name__ == "__main__":
    print(str(datetime.datetime.now()))

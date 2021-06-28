#!/usr/bin/env python
# -*- encoding: utf-8 -*-

from .gm_list_box import GMListbox
from .gm_home_frame import GMHomeFrame
from .gm_window_frame import GMWindowFrame
from .gm_download_frame import GMDownloadFrame, GMDownloadToplevel

if __name__ == "__main__":
    GMListbox()
    GMHomeFrame()
    GMWindowFrame()
    GMDownloadFrame()
    GMDownloadToplevel()

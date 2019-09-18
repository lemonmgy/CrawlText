#!/usr/bin/env python
# -*- coding: utf-8 -*-

import io
from PIL import Image
from .gm_http import GMHTTP


class GMImage(object):
    @staticmethod
    def request_network_image(img_url):
        img_url = "https://www.biquyun.com/\
          files/article/image/14/14055/14055s.jpg"

        data_stream = GMHTTP.get(img_url).data
        data_stream = io.BytesIO(data_stream)
        pil_image = Image.open(data_stream)
        return pil_image

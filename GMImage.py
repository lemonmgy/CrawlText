#!/usr/bin/env python
# -*- coding: utf-8 -*-

import io
import GMRequest
from PIL import Image


def request_network_image(img_url):
    img_url = "https://www.biquyun.com/files/article/image/14/14055/14055s.jpg"
    data_stream = GMRequest.request_original_data(img_url)
    data_stream = io.BytesIO(data_stream)
    pil_image = Image.open(data_stream)
    return pil_image


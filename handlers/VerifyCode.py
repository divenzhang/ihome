#!/usr/bin/python
# -*- coding:utf-8 -*-
"""
------------------------------------
  Author: ZFD
  Date  : 2017/12/27
  Time  : 9:38
------------------------------------
"""
from handlers.BaseHandlers import BaseHandler
from utils.captcha.captcha import Captcha
import constants
import logging
class ImageCodeHandlers(BaseHandler):
    def get(self,*args,**kwargs):
        code_id = self.get_argument("codeid")
        pre_code_id = self.get_argument("pcode")

        if pre_code_id:
            try:
               self.redis.delete("")
            except Exception as e:
                logging.error(e)
        # a=Captcha()
        name, text, image = Captcha().generate_captcha()
        try:
            self.redis.setex("image_code_%s" % code_id,constants.PIC_CODE_EXPIRES_SECONDS,text)
        except Exception as e:
            logging.error(e)
            # self.write("")
        self.set_header("Content-Type", "image/jpg")
        self.write(image)
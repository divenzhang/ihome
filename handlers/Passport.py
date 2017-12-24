#!/usr/bin python
# -*- coding:utf-8 -*-
"""
-------------------------------------------------
  File Name: Passport
  Author   : ZFD
  date     : 2017/12/21
-------------------------------------------------
"""
import logging
from .BaseHandlers import BaseHandler

class IndexHandler(BaseHandler):
    def get(self):
        logging.debug()
        self.write("hello")
        # pass
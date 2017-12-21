#!/usr/bin python
# -*- coding:utf-8 -*-
"""
-------------------------------------------------
  File Name: BaseHandlers
     Author: ZFD
       date: 2017/12/20
-------------------------------------------------
"""
import json
from tornado.web import RequestHandler,StaticFileHandler

class BaseHandler(RequestHandler):
    """"自定义基类"""
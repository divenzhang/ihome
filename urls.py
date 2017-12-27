#!/usr/bin python
# -*- coding:utf-8 -*-
"""
-------------------------------------------------
  File Name: urls
     Author: ZFD
       date: 2017/12/20
-------------------------------------------------
"""
from handlers import Passport,VerifyCode
urls = [
    (r"/", Passport.IndexHandler),
    (r"/api/imgcode", VerifyCode.ImageCodeHandlers),
]
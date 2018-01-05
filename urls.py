#!/usr/bin python
# -*- coding:utf-8 -*-
"""
-------------------------------------------------
  File Name: urls
  Author   : ZFD
  date     : 2017/12/20
-------------------------------------------------
"""

import os
from handlers import Passport,VerifyCode,House
from handlers.BaseHandlers import StaticFileHandler
urls = [
    (r"/api/piccode", VerifyCode.PicCodeHandler),
    (r"/api/smscode", VerifyCode.SMSCodeHandler),
    (r"/api/login", Passport.LoginHandler),
    (r"/api/logout", Passport.LogoutHandler),
    # (r"/api/logout", Passport.LogHandler),
    (r"/api/check_login", Passport.CheckLoginHandler), # 判断用户是否登录
    (r'^/api/house/index$', House.IndexHandler), # 首页
    (r"/api/register", Passport.RegisterHandler),
    (r"/(.*)", StaticFileHandler,
     dict(path=os.path.join(os.path.dirname(__file__), "html"), default_filename="index.html"))

]
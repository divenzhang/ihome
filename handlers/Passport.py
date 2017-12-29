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
from handlers.BaseHandlers import BaseHandler
from utils.response_code import RET
# class IndexHandler(BaseHandler):
#     def get(self):
#         # logging.debug()
#         self.write("hello")
        # pass
#   登录出来
class LoginHandler(BaseHandler):
    pass
# 退出登录
class LogoutHandler(BaseHandler):
    pass
# 检查是否登录
class CheckLoginHandler(BaseHandler):
    def get(self, *args, **kwargs):
        if self.get_current_user():
            """"存在session data已登录"""
            self.write({"errcode":RET.OK,"errmsg":"true", "data":{"name":self.session.data.get("name")}})
        else:
            self.write({"errcode":RET.SESSIONERR, "errmsg":"false"})


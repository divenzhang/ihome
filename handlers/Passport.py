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
import re
import config
import hashlib
from utils.session import Session
# class IndexHandler(BaseHandler):
#     def get(self):
#         # logging.debug()
#         self.write("hello")
        # pass
#   登录
class LoginHandler(BaseHandler):

    def post(self, *args, **kwargs):
        mobile = self.json_args.get('mobile')
        password = self.json_args.get('password')
        # 检查参数
        if not all([mobile,password]):
            return self.write(dict(errcode=RET.PARAMERR, errmsg="参数错误"))
        if not re.match(r"^1\d{10}$",mobile):
            return self.write(dict(errcode=RET.DATAERR,errmsg="手机号错误"))
#         检查密码是否正确
        res =self.db.get("select up_user_id,up_name,up_passwd from ih_user_profile where up_mobile=%(mobile)s",mobile=mobile)
        password = hashlib.sha256(password+config.passwd_hash_key).hexdigest()

        if res and res['up_password'] == password:
            # 生成session数据
            # 返回客户端
            try:
                self.session = Session(self)
                self.session.data['user_id'] = res['up_user_id']
                self.session.data['name'] = res['up_name']
                self.session.data['moblie'] = mobile
                self.session.save()
            except Exception as e :
                logging.error(e)
            return self.write(dict(errcode=RET.OK, errmsg="OK"))
        else:
            return self.write(dict(errcode=RET.DATAERR,errmsg="手机号或密码错误！"))



# 退出登录
class LogoutHandler(BaseHandler):
    def get(self, *args, **kwargs):
        sha1_test = hashlib.sha256()
        sha1_test.update("12345".encode("utf8"))
        self.write(sha1_test.hexdigest())
    # pass
# 检查是否登录
class CheckLoginHandler(BaseHandler):
    def get(self, *args, **kwargs):
        if self.get_current_user():
            """"存在session data已登录"""
            self.write({"errcode":RET.OK,"errmsg":"true", "data":{"name":self.session.data.get("name")}})
        else:
            self.write({"errcode":RET.SESSIONERR, "errmsg":"false"})

# 注册
class RegisterHandler(BaseHandler):
    def post(self, *args, **kwargs):
        mobile=self.json_args.get("mobile")
        sms_code = self.json_args.get("phonecode")
        password = self.json_args.get("password")

        if not all([mobile,sms_code,password]):
            return self.write(dict(errcode=RET.PARAMERR,errsg='参数不完整'))
        if not re.match(r"^1\d{10}$", mobile):
            return self.write(dict(errcode=RET.DATAERR, errmsg="手机号格式错误"))
        # 判断短信验证码是否真确
        # TODO 测试阶段短信验证先默认为2468
        if "2468" != sms_code:
            try:
                # real_sms_code = self.redis.get("sms_code_%s" % mobile)
                # 测试时，默认短信验证码为2468
                real_sms_code = 2468
            except Exception as e:
                logging.error(e)
                return self.write(dict(errcode=RET.DBERR, errmsg="查询验证码出错"))

            # 判断短信验证码是否过期
            if not real_sms_code:
                return self.write(dict(errcode=RET.NODATA, errmsg="验证码过期"))

            # 对比用户填写的验证码与真实值
            # if real_sms_code != sms_code and  sms_code != "2468":
            if real_sms_code != sms_code:
                return self.write(dict(errcode=RET.DATAERR, errmsg="验证码错误"))
            # 测试阶段暂时不用
            # try:
            #     self.redis.delete("sms_code_%s" % mobile)
            # except Exception as e:
            #     logging.error(e)

                # 保存数据，同时判断手机号是否存在，判断的依据是数据库中mobile字段的唯一约束
        passwd = hashlib.sha256(password.encode('latin1 ') + config.passwd_hash_key.encode('latin1')).hexdigest()
        sql = "insert into ih_user_profile(up_name, up_mobile, up_passwd) values(%(name)s, %(mobile)s, %(passwd)s);"
        try:
            user_id = self.db.execute(sql, name=mobile, mobile=mobile, passwd=passwd)
        except Exception as e:
            logging.error(e)
            return self.write(dict(errcode=RET.DATAEXIST, errmsg="手机号已存在"))

        # 用session记录用户的登录状态
        session = Session(self)
        session.data["user_id"] = user_id
        session.data["mobile"] = mobile
        session.data["name"] = mobile
        try:
            session.save()
        except Exception as e:
            logging.error(e)

        self.write(dict(errcode=RET.OK, errmsg="注册成功"))

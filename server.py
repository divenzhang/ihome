#!/usr/bin python
# -*- coding:utf-8 -*-
"""
-------------------------------------------------
  File Name: server
     Author: ZFD
       date: 2017/12/20
-------------------------------------------------
"""
import tornado.web
import tornado.ioloop
import tornado.options
import tornado.httpserver
from tornado.options import define,options
from tornado.web import RequestHandler

define("port",type=int,default=8080,help="run server on the given port 8080")

class IndexHandler(RequestHandler):
    def get(self):
        pass

def main():
    tornado.options.parse_command_line()
    app=tornado.web.Application(
        [(r"/", IndexHandler),],
    )
    http_server = tornado.httpserver.HTTPServer(app)
    http_server.listen(options.port)
    tornado.ioloop.IOLoop.current().start()

if __name__ == '__main__':
    main()
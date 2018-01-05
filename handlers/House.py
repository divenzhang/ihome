#!/usr/bin/python
# -*- coding:utf-8 -*-
"""
------------------------------------
  Author: ZFD
  Date  : 2017/12/28
  Time  : 15:47
------------------------------------
"""
import logging
import constants
from handlers.BaseHandlers import BaseHandler
from utils.response_code import RET
import json
class IndexHandler(BaseHandler):
    def get(self):
        try:
            ret = self.redis.get("home_page_data")
        except Exception as e:
            logging.error(e)
            ret = None
        if ret:
            json_houses = ret
        else:
            try:
                #数据库查询房源
                house_ret = self.db.query("select hi_house_id,hi_title,hi_order_count,hi_index_image_url from ih_house_info " \
                                          "order by hi_order_count desc limit %s;" % constants.HOME_PAGE_MAX_HOUSES)
            except Exception as e:
                logging.error(e)
                return  self.write({"errcode":RET.DBERR,"errmsg":"get data error"})
            if not house_ret:
                return self.write({"errcode":RET.NODATA,"errmsg":"no data"})
            houses = []
            for l in house_ret:
                if not l["hi_index_image_url"]:
                    continue
                house = {
                    "house_id": l["hi_house_id"],
                    "title": l["hi_title"],
                    "img_url": constants.QINIU_URL_PREFIX + l["hi_index_image_url"]
                }
                houses.append(house)
            json_houses = json.dumps(houses)
            try:
                self.redis.setex("home_page_data",constants.HOME_PAGE_DATA_REDIS_EXPIRE_SECOND,json_houses)
            except Exception as e:
                logging.error(e)

        # 返回首页城区数据
        try:
            ret = self.redis.get("area_info")
        except Exception as e:
            logging.error(e)
            ret = None
        if ret: #已存在数据
            json_areas = ret
        else:
            try:
                area_ret = self.db.query("select ai_area_id,ai_name from ih_area_info")
            except Exception as e:
                logging.error(e)
                area_ret =None
            areas = []
            if area_ret:
                for area in area_ret:
                    areas.append(dict(area_id=area["ai_area_id"], name=area["ai_name"]))
            json_areas = json.dumps(areas)
            try:
                self.redis.setex("area_info",constants.REDIS_AREA_INFO_EXPIRES_SECONDES,json_areas)
            except Exception as e:
                logging.error(e)
        resp = '{"errcode":"0","errmsg":"OK","houses":%s,"areas":%s}' %(json_houses,json_areas)
        self.write(resp)


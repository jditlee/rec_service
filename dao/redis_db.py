# -*- coding:utf-8 -*-
# author:凌陨心
# datetime:2023/5/19 10:09
# software: PyCharm
import redis

class Redis(object):
    def __init__(self):
        self.redis = redis.StrictRedis(host='127.0.0.1',
                                       port=6379,
                                       password='',
                                       decode_responses=True)
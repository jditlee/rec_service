# -*- coding:utf-8 -*-
# author:凌陨心
# datetime:2023/5/19 11:15
# software: PyCharm
from dao.redis_db import Redis


class PageUtils(object):
    def __init__(self):
        self._redis = Redis()

    def get_data_with_page(self, page, page_size):
        start = (page - 1) * page_size
        end = start + page_size
        data = self._redis.redis.zrevrange('rec_date_list',start,end)
        lst = list()
        for x in data:
            info = self._redis.redis.get("news_detail:"+x)
            lst.append(info)
        return lst

if __name__ == '__main__':
    page_info = PageUtils()
    print(page_info.get_data_with_page(101,4))
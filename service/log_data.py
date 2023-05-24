# -*- coding:utf-8 -*-
# author:凌陨心
# datetime:2023/5/24 11:03
# software: PyCharm
from dao.redis_db import Redis
from dao.mongo_db import MongoDB
import datetime
# from datetime import datetime
from utils.log import get_logger

logger = get_logger()


class LogData(object):
    def __init__(self):
        self._mongo = MongoDB(db='recommendation')
        self._redis = Redis()

    def insert_log(self, user_id, content_id, title, tables):
        try:
            col = self._mongo.db_recommendation[tables]
            info = {}
            info['user_id'] = user_id
            info['content_id'] = content_id
            info['title'] = title
            info['date'] = datetime.datetime.utcnow()
            col.insert_one(info)
            logger.info(f'{info}')
            return True
        except Exception as e:
            logger.error(f'插入日志异常:{e}')
            return False
    def modify_article_detail(self, key, ops):
        try:
            info = self._redis.redis.get(key)
            info = eval(info)
            info[ops] += 1
            self._redis.redis.set(key, str(info))
            info.pop('describe')
            logger.info(f'更新redis:{info}')
            return True
        except Exception as e:
            logger.error(f'更新redis error:{e}')
            return False

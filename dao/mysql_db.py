# -*- coding:utf-8 -*-
# author:凌陨心
# datetime:2023/5/23 17:23
# software: PyCharm
from sqlalchemy import create_engine
from sqlalchemy.orm import  sessionmaker

class Mysql(object):
    def __init__(self,user='root',pwd='123456',ip='localhost',port='3306',db='rec'):
        self.engine = create_engine(f'mysql+pymysql://{user}:{pwd}@{ip}:{port}/{db}')
        self._DBSession = sessionmaker(bind=self.engine)
# -*- coding:utf-8 -*-
# author:凌陨心
# datetime:2023/5/23 17:28
# software: PyCharm
from sqlalchemy import Column, String, Integer
from sqlalchemy.ext.declarative import declarative_base
from dao.mysql_db import Mysql

Base = declarative_base()


class User(Base):
    __tablename__ = 'user'

    id = Column(Integer(), primary_key=True, autoincrement=True)
    user_name = Column(String(20))
    pwd = Column(String(500))
    nick = Column(String(20))
    gender = Column(String(10))
    age = Column(String(2))
    city = Column(String(50))

    def __init__(self):
        mysql = Mysql()
        engine = mysql.engine
        Base.metadata.create_all(engine)

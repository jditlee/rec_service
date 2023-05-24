# -*- coding:utf-8 -*-
# author:凌陨心
# datetime:2023/5/24 11:16
# software: PyCharm
import logging

def get_logger():
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

    logger = logging.getLogger(__name__)
    return logger
# -*- coding: utf-8 -*-
'''
Created on 2016-11-16 16:25
---------
@summary: 操作oracle数据库
---------
@author: Boris
'''
import sys
sys.path.append('../')
import init
import pymysql
import utils.tools as tools
from utils.log import log

IP        = tools.get_conf_value('config.conf', 'mysql', 'ip')
PORT      = int(tools.get_conf_value('config.conf', 'mysql', 'port'))
DB        = tools.get_conf_value('config.conf', 'mysql', 'db')
USER_NAME = tools.get_conf_value('config.conf', 'mysql', 'user_name')
USER_PASS = tools.get_conf_value('config.conf', 'mysql', 'user_pass')

class Singleton(object):
    def __new__(cls, *args, **kwargs):
        if not hasattr(cls,'_inst'):
            cls._inst=super(Singleton,cls).__new__(cls, *args, **kwargs)

        return cls._inst


class MysqlDB(Singleton):
    def __init__(self, ip = IP, port = PORT, db = DB, user_name = USER_NAME, user_pass = USER_PASS):
        super(MySQL, self).__init__()

        if not hasattr(self,'_db'):
            try:
                self.conn = pymysql.connect(host = ip, port = port, user = user_name, passwd = user_pass, db = db, charset = 'utf8')
                self.cursor = self.conn.cursor()
            except Exception as e:
                raise
            else:
                log.debug('连接到数据库 %s'%db)

    def find(self, sql, fetch_one = False):
        result = []
        if fetch_one:
            result =  self.cursor.execute(sql).fetchone()
        else:
            result =  self.cursor.execute(sql).fetchall()

        return result

    def add(self, sql):
        try:
            self.cursor.execute(sql)
            insert_id = self.cursor.lastrowid
            self.conn.commit()
        except:
            return False
        else:
            return insert_id

    def update(self, sql):
        try:
            self.cursor.execute(sql)
            self.conn.commit()
        except:
            return False
        else:
            return True

    def delete(self, sql):
        try:
            self.cursor.execute(sql)
            self.conn.commit()
        except:
            return False
        else:
            return True

    def set_unique_key(self, table, key):
        try:
            sql = 'alter table %s add unique (%s)'%(table, key)
            self.cursor.execute(sql)
            self.conn.commit()

        except:
            log.error("%s表中%s有重复的数据, 请先去重" % (table, key))

    def close(self):
        self.cursor.close()
        self.conn.close()
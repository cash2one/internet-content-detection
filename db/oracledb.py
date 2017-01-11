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
import cx_Oracle
import utils.tools as tools
from utils.log import log

IP        = tools.get_conf_value('config.conf', 'oracledb', 'ip')
PORT      = int(tools.get_conf_value('config.conf', 'oracledb', 'port'))
DB        = tools.get_conf_value('config.conf', 'oracledb', 'db')
USER_NAME = tools.get_conf_value('config.conf', 'oracledb', 'user_name')
USER_PASS = tools.get_conf_value('config.conf', 'oracledb', 'user_pass')

class Singleton(object):
    def __new__(cls, *args, **kwargs):
        if not hasattr(cls,'_inst'):
            cls._inst=super(Singleton,cls).__new__(cls, *args, **kwargs)

        return cls._inst


class OracleDB(Singleton):
    def __init__(self, ip = IP, port = PORT, db = DB, user_name = USER_NAME, user_pass = USER_PASS):
        super(OracleDB, self).__init__()

        if not hasattr(self,'_db'):
            try:
                self.conn = cx_Oracle.connect(user_name, user_pass, '%s:%d/%s'%(ip, port, db))
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

    def set_unique_key(self, table, key): #TODO
        try:
            sql = 'alter table %s add unique (%s)'%(table, key)
            self.cursor.execute(sql)
            self.conn.commit()

        except:
            log.error("%s表中%s有重复的数据, 请先去重" % (table, key))

    def close(self):
        self.cursor.close()
        self.conn.close()

# db = OracleDB()
# sql =  'select t.* from TAB_IVMS_TASK_KEYWORD t where t.task_id in (select task_id from TAB_IVMS_TASK_INFO where task_status = 501)'
# result = db.find(sql)
# for x in result:
#     print(x)


# 12468 MainThread 2017-01-10 17:59:48 oracledb.py __init__ [line:41] DEBUG 连接到数据库 orcl
# (2, 1, '颐和园', '郝蕾', '景点')
# (1, 1, '色戒', '汤唯,梁朝伟', '苍井空')
# [Finished in 0.9s]
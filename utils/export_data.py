# -*- coding: utf-8 -*-
'''
Created on 2017-01-11 15:41
---------
@summary: mongo 导数据 到oracle 或 mysql
---------
@author: Boris
'''
import sys
sys.path.append('..')
import init

from db.mongodb import MongoDB
from db.oracledb import OracleDB
from db.mysqldb import MysqlDB
from utils.log import log
import utils.tools as tools
import os
os.environ['nls_lang'] = 'AMERICAN_AMERICA.AL32UTF8'   # 插入数据时编码错误 加上这句解决 设置客户端编码

class ExportData():
    def __init__(self, source_table, aim_table, key_map, unique_key = None):
        '''
        @summary: 初始化
        ---------
        @param source_table: 源table
        @param aim_table:    目标table
        @param key_map:      目标table 和 源table 的键的映射
        eg: key_map = {
            'aim_key1' : 'str_source_key2',          # 目标键 = 源键对应的值         类型为str
            'aim_key2' : 'int_source_key3',          # 目标键 = 源键对应的值         类型为int
            'aim_key3' : 'date_source_key4',         # 目标键 = 源键对应的值         类型为date
            'aim_key4' : 'vint_id',                  # 目标键 = 值                   类型为int
            'aim_key5' : 'vstr_name',                # 目标键 = 值                   类型为str
            'aim_key6' : 'sint_select id from xxx'   # 目标键 = 值为sql 查询出的结果 类型为int
            'aim_key7' : 'sstr_select name from xxx' # 目标键 = 值为sql 查询出的结果 类型为str
        }

        @param unique_key:    唯一的key 目标数据库根据该key去重
        ---------
        @result:
        '''

        super(ExportData, self).__init__()

        self._source_table = source_table
        self._aim_table = aim_table
        self._key_map = key_map
        self._unique_key = unique_key

        self._mongodb = MongoDB()

        self._is_oracle = False
        self._export_count = 0


    def export_to_oracle(self):
        self._aim_db = OracleDB()
        self._is_oracle = True
        self.__export()

    def export_to_mysql(self):
        self._aim_db = MysqlDB()
        self.__export()

    # @tools.run_safe_model(__name__)
    def __export(self):
        if self._unique_key:
            self._aim_db.set_unique_key(self._aim_table, self._unique_key)

        aim_keys = tuple(self._key_map.keys())
        source_keys = tuple(self._key_map.values())

        # 取源key值 对应的type 和 key （源key包含type 和 key 信息）
        keys = []
        value_types = []
        for source_key in source_keys:
            temp_var = source_key.split('_', 1)
            value_types.append(temp_var[0])
            keys.append(temp_var[1])

        datas = self._mongodb.find(self._source_table, {'read_status':0})
        for data in datas:
            sql = 'insert into ' + self._aim_table + " (" + ', '.join(aim_keys) + ") values ("
            values = []
            for i in range(len(keys)):
                if value_types[i] == 'str':
                    values.append(data[keys[i]].replace("'", "''"))  # 将单引号替换成两个单引号 否者sql语句语法出错
                    sql += "'%s', "

                elif value_types[i] == 'int':
                    values.append(data[keys[i]])
                    if isinstance(data[keys[i]], int):
                        sql += '%d, '
                    else:
                        sql += '%s, '

                elif value_types[i] == 'date':
                    values.append(data[keys[i]])
                    if self._is_oracle:
                        sql += "to_date('%s','yyyy-mm-dd hh24:mi:ss'), "
                    else:
                        sql += "'%s', "

                elif value_types[i] == 'vint':
                     values.append(keys[i])
                     sql += '%s, '

                elif value_types[i] == 'vstr':
                     values.append(keys[i])
                     sql += "'%s', "

                elif value_types[i] == 'sint':
                    value = self._oracledb.find(keys[i], fetch_one = True)
                    values.append(value)
                    sql += '%d, '

                elif value_types[i] == 'sstr':
                    value = self._oracledb.find(keys[i], fetch_one = True)
                    values.append(value)
                    sql += "'%s', "

                else:
                    log.error('%s不符合key_map规定格式'%value_types[i])
                    return

            sql = sql[:-2] + ")"
            sql = sql%tuple(values)

            log.debug(sql)
            if self._aim_db.add(sql):
                self._export_count += 1
                self._mongodb.update(self._source_table, data, {'read_status':1})

        # self._aim_db.close()
        log.debug('共导出%d条数据'%self._export_count)

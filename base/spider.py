# -*- coding: utf-8 -*-
'''
Created on 2017-01-09 10:38
---------
@summary: 组装parser、 parser_control 和 collector
---------
@author: Boris
'''

import sys
sys.path.append('../')
from db.mongodb import MongoDB
import utils.tools as tools
from base.parser_control import PaserControl
from base.collector import Collector
import threading

class Spider(threading.Thread):
    def __init__(self, tab_urls, tab_site, tab_content, parser_count = None, search_keyword1 = [], search_keyword2 = [], search_keyword3 = [], begin_callback = None, end_callback = None):
        '''
        @summary:
        ---------
        @param tab_urls: url表名
        @param tab_site: 网站表名
        @param parser_count: parser 的线程数，为空时以配置文件为准
        @param search_keyword1: 搜索关键字（列表）全部包含
        @param search_keyword2: 搜索关键字（列表）至少包含一个
        @param search_keyword3: 搜索关键字（列表）一个都不能包含
        @param begin_callback:  爬虫开始的回调
        @param end_callback:    爬虫结束的回调
        ---------
        @result:
        '''
        super(Spider, self).__init__()

        self._db = MongoDB()
        self._db.set_unique_key(tab_urls, 'url')
        self._db.set_unique_key(tab_site, 'site_id')
        self._db.set_unique_key(tab_content, 'url')

        self._collector = Collector(tab_urls)
        self._parsers = []

        self._search_keyword1 = search_keyword1
        self._search_keyword2 = search_keyword2
        self._search_keyword3 = search_keyword3

        self._begin_callback = begin_callback
        self._end_callabck = end_callback

        self._parser_count = int(tools.get_conf_value('config.conf', 'parser', 'parser_count')) if not parser_count else parser_count
        self._spider_site_name = tools.get_conf_value('config.conf', "spider_site", "spider_site_name").split(',')
        self._except_site_name = tools.get_conf_value('config.conf', "spider_site", "except_site_name").split(',')

    def add_parser(self, parser):
        if self._spider_site_name[0] == 'all':
            for except_site_name in self._except_site_name:
                if parser.NAME != except_site_name.strip():
                    self._parsers.append(parser)
        else:
            for spider_site_name in self._spider_site_name:
                if parser.NAME == spider_site_name.strip():
                    self._parsers.append(parser)

    def run(self):
        self.__start()

    def __start(self):
        if self._begin_callback:
            self._begin_callback()

        if not self._parsers:
            if self._end_callabck:
                self._end_callabck()
            return

        # 启动collector
        self._collector.add_finished_callback(self._end_callabck)
        self._collector.start()
        # 启动parser 的add site 和 add root
        for parser in self._parsers:
            threading.Thread(target = parser.add_site_info).start()
            threading.Thread(target = parser.add_root_url, args = (self._search_keyword1, self._search_keyword2, self._search_keyword3)).start()
        # 启动parser control
        while self._parser_count:
            parser_control = PaserControl(self._collector)

            for parser in self._parsers:
                parser_control.add_parser(parser)

            parser_control.start()
            self._parser_count -= 1

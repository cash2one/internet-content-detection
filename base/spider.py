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
import init
from db.mongodb import MongoDB
from utils.log import log
import utils.tools as tools
from base.parser_control import PaserControl
from base.collector import Collector
import threading

class Spider():
    def __init__(self, tab_urls, tab_site):
        self._db = MongoDB()
        self._db.set_unique_key(tab_urls, 'url')
        self._db.set_unique_key(tab_site, 'site_id')

        self._collector = Collector(tab_urls)
        self._parsers = []

        self._parser_count = int(tools.get_conf_value('config.conf', 'parser', 'parser_count'))
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

    def start(self):
        if not self._parsers:
            return

        # 启动collector
        self._collector.start()
        # 启动parser 的add site 和 add root
        for parser in self._parsers:
            threading.Thread(target = parser.add_site_info).start()
            threading.Thread(target = parser.add_root_url).start()
        # 启动parser control
        while self._parser_count:
            parser_control = PaserControl(self._collector)

            for parser in self._parsers:
                parser_control.add_parser(parser)

            parser_control.start()
            self._parser_count -= 1

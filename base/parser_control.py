# -*- coding: utf-8 -*-
'''
Created on 2017-01-03 16:06
---------
@summary: paser 控制类
---------
@author: Boris
'''
import utils.tools as tools
import base.constance as Constance
import base.base_parser as base_parser
from utils.log import log
import threading
import time

class  PaserControl(threading.Thread):
    def __init__(self, collector, tab_urls):
        super(PaserControl, self).__init__()
        self._parsers = []
        self._collector = collector
        self._urlCount = int(tools.get_conf_value('config.conf', "parser", "url_count"))
        self._interval = int(tools.get_conf_value('config.conf', "parser", "sleep_time"))

        self._tab_urls = tab_urls

    def run(self):
        while True:
            try:
                urls = self._collector.get_urls(self._urlCount)
                log.debug("取到的url大小 %d"%len(urls))

                # 判断是否结束
                if self._collector.is_finished():
                    break

                for url in urls:
                    for parser in self._parsers:
                        if parser.SITE_ID == url['site_id']:
                            try:
                                parser.parser(url)
                            except Exception as e:
                                log.error(parser.NAME + " parser -- " + str(e))
                                print(self._tab_urls)
                                print(url['url'])
                                base_parser.update_url(self._tab_urls, url['url'], Constance.EXCEPTION)
                            break

                time.sleep(self._interval)
            except Exception as e:
                log.debug(e)

    def add_parser(self, parser):
        self._parsers.append(parser)
import sys
sys.path.append('../')
import init
from utils.log import log
from base.spider import Spider
import utils.tools as tools
from utils.export_data import ExportData
import time

# 需配置
from live_app.parsers import *
def main():
    search_keyword1 = []
    search_keyword2 = []
    search_keyword3 = []

    def begin_callback():
        log.info('\n********** VA begin **********')

    def end_callback():
        # 更新关键词状态 做完
        log.info('\n********** VA end **********')

    # 配置spider
    spider = Spider(tab_urls = 'LiveApp_urls', tab_site = 'LiveApp_site_info', tab_content = 'LiveApp_anchor_info',
                    parser_count = 1, begin_callback = begin_callback, end_callback = end_callback,
                    search_keyword1 = search_keyword1, search_keyword2 = search_keyword2, search_keyword3 = search_keyword3)

    # 添加parser
    spider.add_parser(inke_parser)

    spider.start()

if __name__ == '__main__':
    main()
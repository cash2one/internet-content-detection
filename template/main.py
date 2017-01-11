import sys
sys.path.append('../')
import init
from utils.log import log
from base.spider import Spider

# 需配置
from template.parsers import *
def main():
    search_keyword1 = ['hi']
    search_keyword2 = ['hello']
    search_keyword3 = ['hello, hi']
    task_id = 1

    def begin_callback():
        log.info('\n********** template begin **********')

    def end_callback():
        print(task_id)
        log.info('\n********** template end **********')

    # 配置spider
    # spider = Spider(tab_urls = 'template_urls', tab_site = 'template_site_info', begin_callback = begin_callback, end_callback = end_callback)
    spider = Spider(tab_urls = 'template_urls', tab_site = 'template_site_info', begin_callback = begin_callback, end_callback = end_callback, search_keyword1 = search_keyword1, search_keyword2 = search_keyword2, search_keyword3 = search_keyword3)

    # 添加parser
    spider.add_parser(xxx_parser)
    spider.add_parser(yyy_parser)

    spider.start()

if __name__ == '__main__':
    main()

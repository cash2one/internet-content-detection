import sys
sys.path.append('../')
import init
from utils.log import log
from base.spider import Spider
import utils.tools as tools
import time

# 需配置
from template.parsers import *
def main():

    search_task_sleep_time = int(tools.get_conf_value('config.conf', 'task', 'search_task_sleep_time'))
    while True:
        # if do_task:
        #     continue
        # 查任务
        search_keyword1 = ['hi']
        search_keyword2 = ['hello']
        search_keyword3 = ['hello, hi']
        task_id = 1

        def begin_callback():
            log.info('\n********** template begin **********')
            # 更新任务状态 正在做

        def end_callback():
            log.info('\n********** template end **********')

            # 更新任务状态 做完

            # 导出数据

        # 配置spider
        # spider = Spider(tab_urls = 'template_urls', tab_site = 'template_site_info', tab_content = '', parser_count = 1, begin_callback = begin_callback, end_callback = end_callback)
        spider = Spider(tab_urls = 'template_urls', tab_site = 'template_site_info', tab_content = 'template_content_info', parser_count = 1, begin_callback = begin_callback, end_callback = end_callback, search_keyword1 = search_keyword1, search_keyword2 = search_keyword2, search_keyword3 = search_keyword3)

        # 添加parser
        spider.add_parser(xxx_parser)
        spider.add_parser(yyy_parser)

        spider.start()

        # time.sleep(search_task_sleep_time)
        break

if __name__ == '__main__':
    main()

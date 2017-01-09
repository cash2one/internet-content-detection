import sys
sys.path.append('../')
import init
from utils.log import log
from base.spider import Spider

# 需配置
from template.parsers import *
def main():
    log.info('\n********** template begin **********')

    # 配置spider
    spider = Spider(tab_urls = 'template_urls', tab_site = 'template_site_info')

    # 添加parser
    spider.add_parser(xxx_parser)
    spider.add_parser(yyy_parser)

    spider.start()

if __name__ == '__main__':
    main()

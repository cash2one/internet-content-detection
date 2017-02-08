import sys
sys.path.append('../../')

import init
import base.base_parser as base_parser
import utils.tools as tools
from utils.log import log

SITE_ID = 2
NAME = '百度'

@tools.run_safe_model(__name__)
def add_site_info():
    log.debug('添加网站信息')
    site_id = SITE_ID
    name = NAME
    table = 'template_site_info'
    url = 'http://www.baidu.com'

    base_parser.add_website_info(table, site_id, url, name)

@tools.run_safe_model(__name__)
def add_root_url(search_keyword1 = [], search_keyword2 = [], search_keyword3 = []):
    log.debug('''
        添加根url
        search_keyword1 = %s
        search_keyword2 = %s
        search_keyword3 = %s
        '''%(str(search_keyword1), str(search_keyword2), str(search_keyword3)))

    url = 'http://www.baidu.com'
    base_parser.add_url('template_urls', SITE_ID, url)

    pass

@tools.run_safe_model(__name__)
def parser(url_info):
    url_info['_id'] = str(url_info['_id'])
    log.debug('处理 \n' + tools.dumps_json(url_info))

    root_url = url_info['url']
    depth = url_info['depth']
    site_id = url_info['site_id']
    remark = url_info['remark']

    # # 解析
    # html, request = tools.get_html_by_requests(root_url)
    # if not html:
    #     base_parser.update_url('urls', root_url, Constance.EXCEPTION)


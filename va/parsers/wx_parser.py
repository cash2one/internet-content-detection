import sys
sys.path.append('../../')

import init
import base.base_parser as base_parser
import utils.tools as tools
from utils.log import log

SITE_ID = 1
NAME = '微信'

@tools.run_safe_model
def add_site_info():
    log.debug('添加网站信息')
    site_id = SITE_ID
    name = NAME
    table = 'template_site_info'
    url = 'http://www.taobao.com'

    base_parser.add_website_info(table, site_id, url, name)


@tools.run_safe_model
def add_root_url():
    log.debug('添加根url')
    url = 'http://www.taobao.com'
    base_parser.add_url('template_urls', SITE_ID, url)

@tools.run_safe_model
def parser(url_info):
    log.debug('处理 ' + tools.dumps_json_(url_info))

    root_url = url_info['url']
    depth = url_info['depth']
    site_id = url_info['site_id']
    remark = url_info['remark']

    # # 解析
    # html, request = tools.get_html_by_requests(root_url)
    # if not html:
    #     base_parser.update_url('urls', root_url, Constance.EXCEPTION)


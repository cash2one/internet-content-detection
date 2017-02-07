import sys
sys.path.append('../../')

import init
import base.constance as Constance
import base.base_parser as base_parser
import utils.tools as tools
from utils.log import log

SITE_ID = 10002
NAME = 'bt磁力链'
search_type = 104

@tools.run_safe_model(__name__)
def add_site_info():
    log.debug('添加网站信息')
    site_id = SITE_ID
    name = NAME
    table = 'VA_site_info'
    url = 'http://www.bturls.net/'
    domain = 'bturls.net'
    ip = '163.44.175.163'
    address = '日本 东京都'

    base_parser.add_website_info(table, site_id, url, name, domain, ip, address)

@tools.run_safe_model(__name__)
def add_root_url(search_keyword1 = [], search_keyword2 = [], search_keyword3 = []):
    log.debug('''
        添加根url
        search_keyword1 = %s
        search_keyword2 = %s
        search_keyword3 = %s
        '''%(str(search_keyword1), str(search_keyword2), str(search_keyword3)))

    remark = {'search_keyword1': search_keyword1, 'search_keyword2': search_keyword2,
              'search_keyword3': search_keyword3}

    search_keyword = search_keyword1 + search_keyword2
    n = 100
    for j in search_keyword:
        if not j:
            continue
        for i in range(1, n + 1):
            url = 'http://www.bturls.net/search/%s_ctime_%d.html' % (j, i)
            if not base_parser.add_url('VA_urls', SITE_ID, url, remark=remark):
                base_parser.update_url('VA_urls', url, Constance.TODO)

@tools.run_safe_model(__name__)
def parser(url_info):
    log.debug('处理 ' + tools.dumps_json_(url_info))

    root_url = url_info['url']
    depth = url_info['depth']
    site_id = url_info['site_id']
    remark = url_info['remark']

    html, requests = tools.get_html_by_requests(root_url)
    titles = tools.get_tag(html, 'h3')
    video_infos = tools.get_tag(html, 'dt')
    for i in range(0, len(titles)):
        title = tools.get_text(titles[i])
        title = tools.del_html_tag(title)
        try:
            url = titles[i].a['href']
        except:
            continue
        url = 'http://www.bturls.net' + url

        release_time = video_infos[i].span
        release_time = tools.get_text(release_time)

        file_size = video_infos[i].span.next_sibling.next_sibling
        file_size = tools.get_text(file_size)

        watched_count = video_infos[i].span.next_sibling.next_sibling.next_sibling.next_sibling
        watched_count = tools.get_text(watched_count)

        print(title + '  ' + url + '  ')
        print(release_time)
        print(file_size)
        print(watched_count)
        print(url)
        regexs = ['t/(.+?)\.']
        magnet_link = 'magnet:?xt=urn:btih:'+''.join(tools.get_info(url,regexs))
        # html2, requests2 = tools.get_html_by_requests(url)
        # magnet_link = tools.get_tag(html2, 'dl', find_all=False)
        # magnet_link = tools.get_tag(magnet_link, 'a', find_all=False)
        # magnet_link = magnet_link['href']
        print(magnet_link)
        # content = tools.get_tag(html2, 'ol', find_all=False)
        # content = tools.get_text(content)
        # content = tools.del_html_tag(content)
        # print(content)

        contained_key, contained_key_count = base_parser.get_contained_key(title, '',remark['search_keyword1'],
                                                            remark['search_keyword2'], remark['search_keyword3'])
        if not contained_key:
            continue

        base_parser.add_content_info('VA_content_info', SITE_ID,url,title,file_size=file_size,
                                     watched_count=watched_count,magnet_link=magnet_link,search_type=search_type, keyword = contained_key, keyword_count = contained_key_count)
    base_parser.update_url('VA_urls', root_url, Constance.DONE)

    # # 解析
    # html, request = tools.get_html_by_requests(root_url)
    # if not html:
    #     base_parser.update_url('urls', root_url, Constance.EXCEPTION)


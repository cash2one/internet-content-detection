import sys
sys.path.append('../../')

import init
import base.constance as Constance
import base.base_parser as base_parser
import utils.tools as tools
from utils.log import log

SITE_ID = 10003
NAME = '网盘搜'
search_type = 103

@tools.run_safe_model
def add_site_info():
    log.debug('添加网站信息')
    site_id = SITE_ID
    name = NAME
    table = 'VA_site_info'
    url = 'http://www.wangpansou.cn/'
    domain = 'wangpansou.cn'
    ip = '122.114.91.8'
    address = '中国 河南 郑州 电信/联通',
    icp = '15001638'
    base_parser.add_website_info(table, site_id, url, name, domain, ip, address,icp=icp)


@tools.run_safe_model
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

    for j in search_keyword:
        for i in range(0, 91, 10):
            url = 'http://www.wangpansou.cn/s.php?q=%s&wp=0&start=%d' % (j, i)
            base_parser.add_url('VA_urls', SITE_ID, url, remark=remark)

@tools.run_safe_model
def parser(url_info):
    print('*******************************************************')
    print('-------------------------------------------------------')
    log.debug('处理 ' + tools.dumps_json_(url_info))

    root_url = url_info['url']
    depth = url_info['depth']
    site_id = url_info['site_id']
    remark = url_info['remark']

    html, requests = tools.get_html_by_requests(root_url)
    titles = tools.get_tag(html, 'div', {'id': tools.re.compile('id_cse_content_item_mid_.')})

    for i in range(0, len(titles)):
        #print(str(titles[i].previous_sibling.previous_sibling))
        url = tools.get_tag(titles[i].previous_sibling.previous_sibling, 'a', find_all=False)
        url = url['href']
        print(url)
        html2 = tools.get_html_by_urllib(url)
        regexs = ['<title>(.+?)</title>']
        mark = ''.join(tools.get_info(html2, regexs))
        regexs = ['不存在', '取消']
        if not tools.get_info(mark, regexs) and mark != '':
            title = tools.get_text(titles[i].previous_sibling.previous_sibling)
            title = tools.del_html_tag(title)
            info = tools.get_text(titles[i])
            print(title)
            # print(info)
            print('hahahahahaha  ' + url)
            file_name = tools.del_html_tag(''.join(tools.get_info(info, '文件名:(.+?)文')))
            print(file_name)
            file_size = tools.del_html_tag(''.join(tools.get_info(info, '文件大小:(.+?)分')))
            print(file_size)
            author = tools.del_html_tag(''.join(tools.get_info(info, '分享者:(.+?)时')))
            print(author)
            release_time = ''.join(tools.get_info(info, '时间:(.+?)下')).replace('\n', '')
            print(release_time)
            download_count = tools.del_html_tag(''.join(tools.get_info(info, '下载次数:(.+?)\.')))
            print(download_count + '\n')

            contained_key, contained_key_count = base_parser.get_contained_key(title, '',
                                                                remark['search_keyword1'],
                                                                remark['search_keyword2'], remark['search_keyword3'])
            if not contained_key:
                continue

            base_parser.add_content_info('VA_content_info', SITE_ID, url, title, file_size=file_size,
                                         file_name=file_name, author=author, release_time=release_time,
                                         download_count=download_count,search_type=search_type, keyword = contained_key, keyword_count = contained_key_count)
    base_parser.update_url('VA_urls', root_url, Constance.DONE)
    # # 解析
    # html, request = tools.get_html_by_requests(root_url)
    # if not html:
    #     base_parser.update_url('urls', root_url, Constance.EXCEPTION)
import sys
sys.path.append('../../')

import init
import base.constance as Constance
import base.base_parser as base_parser
import utils.tools as tools
from utils.log import log

SITE_ID = 10005
NAME = '微信'
SEARCH_TYPE = 105

HEADER = {
    'Cookie':'usid=_GW9W2q3bS3Gmnt8; IPLOC=CN1100; SUV=004074AAD39C8C4A582E927B4CCD4712; CXID=5D6D9135174B33DFACFC3DF1AD4DD4F8; ad=uMpvFZllll2YFL47lllllVPc6Ztlllll1ihGvkllllGlllllRylll5@@@@@@@@@@; SUID=4A8C9CD3536C860A584F61EC000B6DF9; ABTEST=3|1484546443|v1; weixinIndexVisited=1; JSESSIONID=aaa3ShvUeSm0y88RjUwMv; SNUID=C90F1F508486C5AC6461B17184780898; sct=19; td_cookie=18446744071226930631',
    'Host':'weixin.sogou.com',
    'Upgrade-Insecure-Requests':'1',
    'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.99 Safari/537.36'
}

@tools.run_safe_model(__name__)
def add_site_info():
    log.debug('添加网站信息')

    site_id = SITE_ID
    name = NAME
    table = 'VA_site_info'
    url = 'http://weixin.sogou.com/'
    ip = '183.36.114.45'
    address = '广东省广州市 电信'
    icp = '050897'
    public_safety = '11000002000025'

    base_parser.add_website_info(table, site_id, url, name, ip = ip, address = address, icp = icp, public_safety = public_safety)


@tools.run_safe_model(__name__)
def add_root_url(search_keyword1 = [], search_keyword2 = [], search_keyword3 = []):
    log.debug('''
        添加根url
        search_keyword1 = %s
        search_keyword2 = %s
        search_keyword3 = %s
        '''%(str(search_keyword1), str(search_keyword2), str(search_keyword3)))

    remark = {'search_keyword1': search_keyword1, 'search_keyword2': search_keyword2, 'search_keyword3': search_keyword3}

    search_keywords = search_keyword1 + search_keyword2

    for search_keyword in search_keywords:
        url = 'http://weixin.sogou.com/weixin?type=2&query=' + search_keyword
        # 最多显示10页
        for page in range(1, 11):
            url += '&page=%d&ie=utf8'%page
            base_parser.add_url('VA_urls', SITE_ID, url, remark = remark)



@tools.run_safe_model(__name__)
def parser(url_info):
    log.debug('处理 ' + tools.dumps_json_(url_info))

    root_url = url_info['url']
    depth = url_info['depth']
    site_id = url_info['site_id']
    remark = url_info['remark']

    # 解析
    html, request = tools.get_html_by_requests(root_url, headers = HEADER)

    if not html:
        base_parser.update_url('urls', root_url, Constance.EXCEPTION)
        return

    news_box = tools.get_tag(html, name = 'div', attrs={'class':"news-box"})[0]

    news_list = tools.get_tag(news_box, name = 'li')
    for news in news_list:
        # 图片
        image = tools.get_tag(news, name = 'img')[0]
        image = tools.get_json_value(image, 'src')

        # url
        url = tools.get_tag(news, name = 'h3')[0]
        try:
            url = tools.get_json_value(url.a, 'href')
        except:
            url = ''

        # 标题
        title = tools.get_tag(news, name = 'h3')[0]
        title = tools.get_text(title)
        title = tools.del_html_tag(title)

        # 内容
        content = tools.get_tag(news, name = 'p', attrs = {'class':"txt-info"})[0]
        content = tools.get_text(content)
        content = tools.del_html_tag(content)

        # 观看数
        watched_count = ''

        # 来源
        origin = tools.get_tag(news, name = 'div', attrs = {'class':"s-p"})[0]
        origin = tools.get_info(origin, '<a.*?>(.*?)<')[0]

        # 日期
        release_time = tools.get_tag(news, name = 'div', attrs = {'class':"s-p"})[0]
        release_time = tools.get_json_value(release_time, 't')
        release_time = tools.timestamp_to_date(int(release_time))

        # 判断是否有视频 根据视频播放图标判断
        regex = '<div class="img-box">.*?<i></i>.*?</div>'
        play_icon = tools.get_info(news, regex)

        log.debug('''
            标题：   %s
            内容：   %s
            来源：   %s
            原文url：%s
            图片url：%s
            观看数： %s
            日期：   %s
            有视频： %d
                  '''%(title, content, origin, url , image, watched_count, release_time, play_icon and True or False))

        contained_key, contained_key_count = base_parser.get_contained_key(title, content, remark['search_keyword1'], remark['search_keyword2'], remark['search_keyword3'])
        if not contained_key or not play_icon:
            continue

        base_parser.add_content_info('VA_content_info', SITE_ID, url, title, content, video_pic = image, release_time = release_time, origin = origin,
                                     watched_count = watched_count, search_type=SEARCH_TYPE, keyword = contained_key, keyword_count = contained_key_count)

    base_parser.update_url('VA_urls', root_url, Constance.DONE)
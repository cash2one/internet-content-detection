import sys
sys.path.append('../../')
import init
import base.constance as Constance
import base.base_parser as base_parser
import utils.tools as tools
from utils.log import log

SITE_ID = 10001
NAME = '百度'
search_type = 101

@tools.run_safe_model(__name__)
def add_site_info():
    log.debug('添加网站信息')
    site_id = SITE_ID
    name = NAME
    table = 'VA_site_info'
    url = 'http://www.baidu.com'
    domain = 'baidu.com'
    ip = '111.13.100.91'
    address = '北京市'
    public_safety = '11000002000001'
    icp = '030173'
    base_parser.add_website_info(table, site_id, url, name,domain,ip,address,public_safety=public_safety,icp=icp)

@tools.run_safe_model(__name__)
def add_root_url(search_keyword1 = [], search_keyword2 = [], search_keyword3 = []):
    log.debug('''
        添加根url
        search_keyword1 = %s
        search_keyword2 = %s
        search_keyword3 = %s
        '''%(str(search_keyword1), str(search_keyword2), str(search_keyword3)))

    remark = {'search_keyword1': search_keyword1, 'search_keyword2': search_keyword2, 'search_keyword3': search_keyword3}

    search_keyword = search_keyword1 + search_keyword2

    for i in search_keyword:
        for num in range(0, 750, 50):
            link = "http://news.baidu.com/ns?word=%s%s&pn=%s&cl=2&ct=1&tn=news&rn=50&ie=utf-8&bt=0&et=0" % (i,' 视频', num)
            link = tools.quote(link, safe='#/:?=&%')
            if not base_parser.add_url('VA_urls', SITE_ID, link, remark=remark):
                base_parser.update_url('VA_urls', link, Constance.TODO)


@tools.run_safe_model(__name__)
def parser(url_info):
    log.debug('处理 ' + tools.dumps_json_(url_info))

    root_url = url_info['url']
    depth = url_info['depth']
    site_id = url_info['site_id']
    remark = url_info['remark']

    html = tools.get_html_by_webdirver(root_url)
    headers = tools.get_tag(html,'h3', {'class': 't'})

    for i in range(0, len(headers)):
        title = tools.get_text(headers[i])
        title = tools.del_html_tag(title)
        if tools.re.compile('的相关视频在线观看_百度视频').findall(title):
            continue
        print(title)
        try:
            ssurl = headers[i].a["href"]
        except:
            continue
        r = tools.requests.head(ssurl)
        url = r.headers['Location']
        print(url)
        try:
            img = headers[i].next_sibling()[0].img['src']
        except:
            img = ''
        print(img)
        try:
            release_time = headers[i].next_sibling()[0]
            release_time = ''.join(tools.re.compile('\d\d\d\d年\d+?月\d+?日').findall(str(release_time)))
            if not release_time:
                release_time = headers[i].next_sibling()[1]
                release_time = ''.join(tools.re.compile('\d\d\d\d年\d+?月\d+?日').findall(str(release_time)))
                if not release_time:
                    release_time = headers[i].next_sibling()[2]
                    release_time = ''.join(tools.re.compile('\d\d\d\d年\d+?月\d+?日').findall(str(release_time)))
                    if not release_time:
                        release_time = headers[i].next_sibling()[3]
                        release_time = ''.join(tools.re.compile('\d\d\d\d年\d+?月\d+?日').findall(str(release_time)))
            release_time = release_time.replace('年','-').replace('月','-').replace('日','')
        except:
            release_time = ''
        print(release_time)

        for content in headers[i].next_sibling():
            content = tools.get_tag(content,'div',{'class': 'c-abstract'},find_all=False)
            if content:
                content = tools.get_text(content)
                break
        print(content)

        contained_key, contained_key_count = base_parser.get_contained_key(title,content,remark['search_keyword1'],
                                               remark['search_keyword2'],remark['search_keyword3'])
        if not contained_key:
            continue

        is_video1 = base_parser.is_have_video_by_site(url)
        if not is_video1:
            is_video2 = base_parser.is_have_video_by_judge(title, content)
            if not is_video2:
                html2 = tools.get_html_by_requests(url)
                is_video3 = base_parser.is_have_video_by_common(html2)
                if not is_video3:
                    continue


        base_parser.add_content_info('VA_content_info',SITE_ID,url=url,
                                     title=title,content=content,image_url=img,
                                     release_time=release_time,search_type=search_type, keyword = contained_key, keyword_count = contained_key_count)
    base_parser.update_url('VA_urls'  , root_url, Constance.DONE)
    # # 解析
    # html, request = tools.get_html_by_requests(root_url)
    # if not html:
    #     base_parser.update_url('urls'  , root_url, Constance.EXCEPTION)


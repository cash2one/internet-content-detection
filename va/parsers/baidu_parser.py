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

@tools.run_safe_model
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

@tools.run_safe_model
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
            link = "http://news.baidu.com/ns?word=%s&pn=%s&cl=2&ct=1&tn=news&rn=50&ie=utf-8&bt=0&et=0" % (i, num)
            link = tools.quote(link, safe='#/:?=&%')
            base_parser.add_url('VA_urls', SITE_ID, link, remark=remark)


@tools.run_safe_model
def parser(url_info):
    log.debug('处理 ' + tools.dumps_json_(url_info))

    root_url = url_info['url']
    depth = url_info['depth']
    site_id = url_info['site_id']
    remark = url_info['remark']

    html = tools.get_html_by_webdirver(root_url)
    headers = tools.get_tag(html,'h3', {'class': 'c-title'})
    ps = tools.get_tag(html,'p', {'class': 'c-author'})
    abstracts = tools.re.compile('</p>(.+?)<span class="c-info">').findall(str(html))
    for i in range(0, len(headers)):
        headers[i].get_text()
        date = tools.time.strftime("%Y-%m-%d %H:%M", tools.time.localtime(tools.time.time()))
        abstracts[i] = abstracts[i].replace('<em>', '')
        abstracts[i] = abstracts[i].replace('</em>', '')
        print(headers[i].get_text())
        issue_info = ps[i].get_text().split()
        issue_author = issue_info[0]
        issue_time = " ".join(issue_info[1:])
        issue_time = issue_time.replace('年', '-').replace('月', '-').replace('日', '')
        print(date)
        print(issue_time)
        if tools.re.compile('小时前').findall(issue_time):
            nhours = tools.re.compile('(\d+)小时前').findall(issue_time)
            hours_ago = (tools.datetime.datetime.now() - tools.datetime.timedelta(hours=int(nhours[0])))
            issue_time = hours_ago.strftime("%Y-%m-%d %H:%M")
        if tools.re.compile('分钟前').findall(issue_time):
            nminutes = tools.re.compile('(\d+)分钟前').findall(issue_time)
            minutes_ago = (tools.datetime.datetime.now() - tools.datetime.timedelta(minutes=int(nminutes[0])))
            issue_time = minutes_ago.strftime("%Y-%m-%d %H:%M")

        print(issue_author + '           ' + issue_time)
        print(abstracts[i])

        is_desired_results = base_parser.is_desired_results(headers[i].get_text(),abstracts[i],remark['search_keyword1'],
                                               remark['search_keyword2'],remark['search_keyword3'])
        if not is_desired_results:
            continue

        base_parser.add_content_info('VA_content_info',SITE_ID,url=headers[i].a['href'],
                                     title=headers[i].get_text(),content=abstracts[i],
                                     origin=issue_author,release_time=issue_time,search_type=search_type)
    base_parser.update_url('VA_urls'  , root_url, Constance.DONE)
    # # 解析
    # html, request = tools.get_html_by_requests(root_url)
    # if not html:
    #     base_parser.update_url('urls'  , root_url, Constance.EXCEPTION)


import sys
sys.path.append('../../')
import init
from bs4 import BeautifulSoup
import base.constance as Constance
import base.base_parser as base_parser
import utils.tools as tools
from utils.log import log

SITE_ID = 10005
NAME = '测试'
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
    #print(html)
    headers = tools.get_tag(html,'h3', {'class': 't'})
    #print(headers)
    # soup = BeautifulSoup(html,"html.parser")
    # imgs = soup.find_all("a", {'class': 'c-span6'})
    # print(imgs)
    ps = tools.get_tag(html,'p', {'class': 'c-author'})
    abstracts = tools.re.compile('</p>(.+?)<span class="c-info">').findall(str(html))
    for i in range(0, len(headers)):

        title = tools.get_text(headers[i])
        title = tools.del_html_tag(title)
        if tools.re.compile('的相关视频在线观看_百度视频').findall(title):
            continue
        print(title)
        ssurl = headers[i].a["href"]
        r = tools.requests.head(ssurl)
        url = r.headers['Location']
        print(url)
        try:
            img = headers[i].next_sibling()[0].img['src']
        except:
            img = ''
        print(img)
        try:
           # release_time = tools.get_tag(headers[i].next_sibling()[0],'span',{'class': 'newTimeFactor_before_abs'},find_all=False)
            release_time = headers[i].next_sibling()[0]
        except:
            release_time = ''
        print(release_time)

        print('*************************************************')
        # date = tools.time.strftime("%Y-%m-%d %H:%M", tools.time.localtime(tools.time.time()))
        # abstracts[i] = abstracts[i].replace('<em>', '')
        # abstracts[i] = abstracts[i].replace('</em>', '')
        # print(headers[i].get_text())
        # issue_info = ps[i].get_text().split()
        # issue_author = issue_info[0]
        # issue_time = " ".join(issue_info[1:])
        # issue_time = issue_time.replace('年', '-').replace('月', '-').replace('日', '')
        # print(date)
        # print(issue_time)
        # if tools.re.compile('小时前').findall(issue_time):
        #     nhours = tools.re.compile('(\d+)小时前').findall(issue_time)
        #     hours_ago = (tools.datetime.datetime.now() - tools.datetime.timedelta(hours=int(nhours[0])))
        #     issue_time = hours_ago.strftime("%Y-%m-%d %H:%M")
        # if tools.re.compile('分钟前').findall(issue_time):
        #     nminutes = tools.re.compile('(\d+)分钟前').findall(issue_time)
        #     minutes_ago = (tools.datetime.datetime.now() - tools.datetime.timedelta(minutes=int(nminutes[0])))
        #     issue_time = minutes_ago.strftime("%Y-%m-%d %H:%M")
        #
        # print(issue_author + '           ' + issue_time)
        # print(abstracts[i])

url = 'https://www.baidu.com/s?wd=%E9%A2%90%E5%92%8C%E5%9B%AD%20%E9%83%9D%E8%95%BE%20%E8%A7%86%E9%A2%91&pn=0&oq=%E9%A2%90%E5%92%8C%E5%9B%AD%20%E9%83%9D%E8%95%BE%20%E8%A7%86%E9%A2%91&ie=utf-8&rsv_pq=fd5fb336000042ce&rsv_t=5648jNaMrsL7CxJ7E88hvpOlVXLwNARTFNPGX86L4mn7VyFPQBl5BMu5sNk&gpc=stf&tfflag=0'
haha = {'url': url, 'site_id': '582ea577350b654b67dc8ac8', 'depth': 1, 'remark': ''}
parser(haha)

    # # 解析
    # html, request = tools.get_html_by_requests(root_url)
    # if not html:

#     base_parser.update_url('urls'  , root_url, Constance.EXCEPTION)

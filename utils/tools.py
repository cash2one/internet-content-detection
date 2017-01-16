# encoding=utf8

import sys
sys.path.append("..")

import re
import json
import configparser #读配置文件的
import codecs
import uuid
from urllib.parse import quote
from utils.log import log
from tld import get_tld
from urllib import request
from urllib.parse import urljoin
from selenium import webdriver
import requests
import time
from bs4 import BeautifulSoup
from threading import Timer
import functools
import datetime
import time
import os
import execjs   # pip install PyExecJS

TIME_OUT = 30
TIMER_TIME = 5

# 装饰器
def log_function_time(func):
    try:
        @functools.wraps(func)  #将函数的原来属性付给新函数
        def calculate_time(*args, **kw):
            began_time = time.time()
            callfunc = func(*args, **kw)
            end_time = time.time()
            log.debug(func.__name__ + " run time  = " + str(end_time - began_time))
            return callfunc
        return calculate_time
    except:
        log.debug('求取时间无效 因为函数参数不符')
        return func

def run_safe_model(func):
    try:
        @functools.wraps(func)  #将函数的原来属性付给新函数
        def run_func(*args, **kw):
            callfunc = ''
            try:
                callfunc = func(*args, **kw)
            except Exception as e:
                log.error(func.__name__ + " " + str(e))
            return callfunc
        return run_func
    except Exception as e:
        log.error(func.__name__ + " " + str(e))
        return func
#######################################################

@log_function_time
def get_html_by_urllib(url, code = 'utf-8'):
    html = None
    if not url.endswith('.exe') and not url.endswith('.EXE'):
        page = None
        is_timeout = False
        try:
            def timeout_handler(response):
                is_timeout = True
                if response:
                    response.close()

            page = request.urlopen(quote(url,safe='/:?=&'), timeout = TIME_OUT)
            # 设置定时器 防止在read时卡死
            t = Timer(TIMER_TIME, timeout_handler, [page])
            t.start()
            html = page.read().decode(code,'ignore')
            t.cancel()

        except Exception as e:
            log.error(e)
        finally:
            # page and page.close()
            if page and not is_timeout:
                page.close()

    return html and len(html) < 1024 * 1024 and html or None


@log_function_time
def get_html_by_webdirver(url):
    html = ''
    try:
        driver = webdriver.PhantomJS()
        driver.get(url)
        # time.sleep(10)
        html = driver.page_source
        driver.close()
    except Exception as e:
        log.error(e)
    return html

@log_function_time
def get_html_by_requests(url, code = 'utf-8'):
    html = None
    if not url.endswith('.exe') and not url.endswith('.EXE'):
        r = None
        try:
            r = requests.get(url, timeout = TIME_OUT)
            if code:
                r.encoding = code
            html = r.text

        except Exception as e:
            log.error(e)
        finally:
            r and r.close()

    return html and len(html) < 1024 * 1024 and html or None, r

def get_json_by_requests(url, params = None):
    json = {}
    try:
        response = requests.get(url, params = params)
        json = response.json()
    except Exception as e:
        log.error(e)

    return json

def get_urls(html):
    urls = re.compile('<a.*?href="(.*?)"').findall(str(html))
    return sorted(set(urls), key = urls.index)

def get_full_url(root_url, sub_url):
    '''
    @summary: 得到完整的ur
    ---------
    @param root_url: 根url （网页的url）
    @param sub_url:  子url （带有相对路径的 可以拼接成完整的）
    ---------
    @result: 返回完整的url
    '''

    # if sub_url.begin
    return urljoin(root_url, sub_url)

def joint_url(url, params):
    param_str = "?"
    for key, value in params.items():
        value = isinstance(value, str) and value or str(value)
        param_str += key + "=" + value + "&"

    return url + param_str[:-1]

def fit_url(urls, identis):
    identis = isinstance(identis, str) and [identis] or identis
    fit_urls = []
    for link in urls:
        for identi in identis:
            if identi in link:
                fit_urls.append(link)
    return list(set(fit_urls))

_regexs = {}
@log_function_time
def get_info(html,regexs, allow_repeat = False):
    regexs = isinstance(regexs, str) and [regexs] or regexs

    infos = []
    for regex in regexs:
        try:
            if regex == '':
                continue
            infos = _regexs[regex].findall(str(html))
        except:
            _regexs[regex] = re.compile(regex, re.S)
            infos = _regexs[regex].findall(str(html))

        # infos = re.findall(regex,str(html),re.S)
        # infos = re.compile(regexs, re.S).findall(str(html))
        if len(infos) > 0:
            break

    return allow_repeat and infos or sorted(set(infos),key = infos.index)

def get_domain(url):
    return get_tld(url)

def get_tag(html, name=None, attrs={}, find_all = True):
    if html:
        soup = BeautifulSoup(html, "html.parser") if isinstance(html, str) else html
        return soup.find_all(name, attrs) if find_all else soup.find(name, attrs)
    else:
        return ''

def get_text(soup, *args):
    try:
        return soup.get_text()
    except:
        return ''

def del_html_tag(content):
    content = replace_str(content, '<script(.|\n)*?</script>')
    content = replace_str(content, '<style(.|\n)*?</style>')
    content = replace_str(content, '<!--(.|\n)*?-->')
    content = replace_str(content, '<(.|\n)*?>')
    content = replace_str(content, '&.*?;')
    content = replace_str(content, '\s')

    return content

def is_have_chinese(content):
    regex = '[\u4e00-\u9fa5]+'
    chinese_word = get_info(content, regex)
    return chinese_word and True or False

##################################################
def get_json(json_str):
    '''
    @summary: 取json对象
    ---------
    @param json_str: json格式的字符串
    ---------
    @result: 返回json对象
    '''

    return json.loads(json_str)

def dumps_json(json_):
    '''
    @summary: 格式化json 用于打印
    ---------
    @param json_: json格式的字符串或json对象
    ---------
    @result: 格式化后的字符串
    '''
    try:
        if isinstance(json_, str):
            json_ = get_json(json_)

        json_ = json.dumps(json_, ensure_ascii=False, indent=4, skipkeys = True)

    except Exception as e:
        json_ = str(json_)

    return json_

def dumps_json_(json_):
    '''
    @summary: 格式化json字符串， key value中不能包含逗号 适用于mongodb中的json

    ---------
    @param json_: json格式
    ---------
    @result: 格式化后的字符串
    '''

    json_ = str(json_)
    json_str = json_[1: -1]

    key_values = json_str.split(',')

    json_str = '\n{\n'
    for key_value in key_values:
        json_str += ' ' * 4
        json_str = json_str + key_value.strip() + '\n'
    json_str += '}\n'

    return json_str

def get_json_value(json_object, key):
    '''
    @summary:
    ---------
    @param json_object: json对象或json格式的字符串
    @param key: 建值 如果在多个层级目录下 可写 key1.key2  如{'key1':{'key2':3}}
    ---------
    @result: 返回对应的值，如果没有，返回''
    '''
    current_key = ''
    value = ''
    try:
        json_object = isinstance(json_object, str) and get_json(json_object) or json_object

        current_key = key.split('.')[0]
        value      = json_object[current_key]

        key        = key[key.find('.') + 1:]
    except Exception as e:
            return value

    if key == current_key:
        return value
    else:
        return get_json_value(value, key)

##################################################
def replace_str(source_str, regex, replace_str = ''):
    '''
    @summary: 替换字符串
    ---------
    @param source_str: 原字符串
    @param regex: 正则
    @param replace_str: 用什么来替换 默认为''
    ---------
    @result: 返回替换后的字符串
    '''
    str_info = re.compile(regex)
    return str_info.sub(replace_str, source_str)

##################################################
def get_conf_value(config_file, section, key):
    cp = configparser.ConfigParser(allow_no_value = True)
    with codecs.open(config_file, 'r', encoding='utf-8') as f:
        cp.read_file(f)
    return cp.get(section, key)

################################################
def capture(url, save_fn="capture.png"):
    directory = os.path.dirname(save_fn)
    mkdir(directory)

    browser = webdriver.PhantomJS()
    browser.set_window_size(1200, 900)
    browser.get(url) # Load page
    browser.execute_script("""
            (function () {
              var y = 0;
              var step = 100;
              window.scroll(0, 0);

              function f() {
                if (y < document.body.scroll_height) {
                  y += step;
                  window.scroll(0, y);
                  set_timeout(f, 50);
                } else {
                  window.scroll(0, 0);
                  document.title += "scroll-done";
                }
              }

              set_timeout(f, 1000);
            })();
        """)

    for i in range(30):
        if "scroll-done" in browser.title:
            break
        time.sleep(1)

    browser.save_screenshot(save_fn)
    browser.close()

def mkdir(path):
    try:
        os.makedirs(path)
    except OSError as exc: # Python >2.5
        pass

def download_file(url, base_path, filename = '', call_func = ''):
    file_path = base_path + filename
    directory = os.path.dirname(file_path)
    mkdir(directory)

    if url:
        try:
            log.debug('''
                         正在下载 %s
                         存储路径 %s
                      '''
                         %(url, file_path))

            request.urlretrieve(url, file_path)

            log.debug('''
                         下载完毕 %s
                         文件路径 %s
                      '''
                         %(url, file_path)
                     )

            call_func and call_func()
            return 1
        except Exception as e:
            log.error(e)
            return 0
    else:
        return 0

#############################################

def exec_js(js_code):
    '''
    @summary: 执行js代码
    ---------
    @param js_code: js代码
    ---------
    @result: 返回执行结果
    '''

    return execjs.eval(js_code)

def compile_js(js_func):
    '''
    @summary: 编译js函数
    ---------
    @param js_func:js函数
    ---------
    @result: 返回函数对象 调用 fun('js_funName', param1,param2)
    '''

    ctx = execjs.compile(js_func)
    return ctx.call

###############################################

def date_to_timestamp(date, time_format = '%Y-%m-%d %H:%M:%S'):
    '''
    @summary:
    ---------
    @param date:将"2011-09-28 10:00:00"时间格式转化为时间戳
    @param format:时间格式
    ---------
    @result: 返回时间戳
    '''

    timestamp = time.mktime(time.strptime(date, time_format))
    return int(timestamp)

def timestamp_to_date(timestamp, time_format = '%Y-%m-%d %H:%M:%S'):
    '''
    @summary:
    ---------
    @param timestamp: 将时间戳转化为日期
    @param format: 日期格式
    ---------
    @result: 返回日期
    '''

    date = time.localtime(timestamp)
    return time.strftime(time_format, date)

def get_current_timestamp():
    return int(time.time())

def get_current_date(date_format = '%Y-%m-%d %H:%M:%S'):
    return time.strftime(date_format, time.localtime(time.time()))


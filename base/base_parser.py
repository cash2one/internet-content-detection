# -*- coding: utf-8 -*-
'''
Created on 2017-01-03 11:05
---------
@summary: 提供一些操作数据库公用的方法
---------
@author: Boris
'''

import base.constance as Constance
import utils.tools as tools
from db.mongodb import MongoDB

db = MongoDB()

def get_site_id(table, site_name):
    result = db.find(table, {'name':site_name})
    if result:
        return result[0]['site_id']
    else:
        raise AttributeError('%s表中无%s信息'%(table, site_name))

def add_website_info(table, site_id, url, name, domain = '', ip = '', address = '', video_license = '', public_safety = '', icp = ''):
    '''
    @summary: 添加网站信息
    ---------
    @param table: 表名
    @param site_id: 网站id
    @param url: 网址
    @param name: 网站名
    @param domain: 域名
    @param ip: 服务器ip
    @param address: 服务器地址
    @param video_license: 网络视听许可证|
    @param public_safety: 公安备案号
    @param icp: ICP号
    ---------
    @result:
    '''

    # 用程序获取domain,ip,address,video_license,public_safety,icp 等信息
    domain = tools.get_domain(url)

    site_info = {
        'site_id':site_id,
        'name':name,
        'domain':domain,
        'url':url,
        'ip':ip,
        'address':address,
        'video_license':video_license,
        'public_safety':public_safety,
        'icp':icp,
        'read_status':0,
        'record_time': tools.get_current_date()
    }
    db.add(table, site_info)

def add_content_info(table, site_id, url='', title='', content='',
                     author='', video_url='', image_url='', origin='',
                     watched_count='', comment_count='', share_count='',
                     praise_count='', release_time='',file_size='',
                     file_name='',magnet_link='',download_count='',
                     reposts_count='',attitudes_count='',video_pic=''):
    '''
    @summary: 添加网站信息
    ---------
    @param table: 表名
    @param site_id: 网站id
    @param url: 网址
    @param title: 标题
    @param content: 正文
    @param author: 作者
    @param origin: 来源
    @param release_time: 发布时间
    @param file_name: 文件名
    @param file_size: 文件大小
    @param video_url: 视频url
    @param image_url: 图片url
    @param magnet_link: 磁力链接
    @param download_count: 下载次数
    @param watched_count: 观看数
    @param comment_count: 评论数
    @param share_count: 分享数
    @param praise_count: 点赞数
    @param reposts_count: 转发数
    @param attitudes_count: 点赞数
    @param video_pic: 视频封面图片链接
    ---------
    @result:
    '''

    site_info = {
        'site_id':site_id,
        'title':title,
        'url':url,
        'content':content,
        'author':author,
        'video_url':video_url,
        'image_url':image_url,
        'origin':origin,
        'watched_count':watched_count,
        'comment_count': comment_count,
        'share_count': share_count,
        'praise_count': praise_count,
        'release_time': release_time,
        'file_size':file_size,
        'magnet_link':magnet_link,
        'download_count':download_count,
        'file_name':file_name,
        'reposts_count':reposts_count,
        'attitudes_count':attitudes_count,
        'video_pic':video_pic,
        'read_status':0,
        'record_time': tools.get_current_date()
    }
    db.add(table, site_info)

def add_appsite_info(table, site_id, url, name , app_url = '', summary = '', update_info = '', author = '', image_url = '', classify = '', size = '', tag = '', platform = 'android', download_count = '', release_time = ''):
    '''
    @summary: 添加app 网站信息
    ---------
    @param table: 表名
    @param site_id: 网站id
    @param url: 网址
    @param name: app名
    @param app_url: app url
    @param summary: 简介
    @param update_info: 更新信息
    @param author: 开发者
    @param image_url: 图标url
    @param classify: 分类
    @param size: 大小
    @param tag: 版本
    @param platform: 平台 默认android
    @param download_count: 下载次数
    @param release_time: 发布时间
    ---------
    @result:
    '''

    app_info = {
        'site_id':site_id,
        'url':url,
        'name':name,
        'app_url':app_url,
        'summary':summary,
        'update_info':update_info,
        'author':author,
        'image_url':image_url,
        'classify':classify,
        'size':size,
        'tag':tag,
        'platform':platform,
        'download_count':download_count,
        'release_time':release_time,
        'read_status':0,
        'record_time': tools.get_current_date()
    }

    db.add(table, app_info)

def add_url(table, site_id, url, depth = 0, remark = '', status = Constance.TODO):
    url_dict = {'site_id':site_id, 'url':url, 'depth':depth, 'remark':remark, 'status':status}
    db.add(table, url_dict)

def update_url(table, url, status):
    db.update(table, {'url':url}, {'status':status})
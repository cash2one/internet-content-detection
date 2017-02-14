
import sys
sys.path.append('../../')

import init
import base.base_parser as base_parser
import utils.tools as tools
from utils.log import log

# 必须定义 网站id
SITE_ID = 1
# 必须定义 网站名
NAME = '映客'

@tools.run_safe_model(__name__)
# 必须定义 添加网站信息
def add_site_info():
    log.debug('添加网站信息')
    site_id = SITE_ID
    name = NAME
    table = 'LiveApp_site_info'
    url = 'http://www.inke.cn/hotlive_list.html'

    base_parser.add_website_info(table, site_id, url, name)

@tools.run_safe_model(__name__)
# 必须定义 添加根url
def add_root_url(search_keyword1 = [], search_keyword2 = [], search_keyword3 = []):
    log.debug('''
        添加根url
        search_keyword1 = %s
        search_keyword2 = %s
        search_keyword3 = %s
        '''%(str(search_keyword1), str(search_keyword2), str(search_keyword3)))

    remark = {'search_keyword1': search_keyword1, 'search_keyword2': search_keyword2,
              'search_keyword3': search_keyword3}

    secret_key="8D2E##1[5$^(38#%#d3z96;]35q#MD28"
    current_timestamp = tools.get_current_timestamp()

    s_sg = tools.get_md5(secret_key + str(current_timestamp)) #Sig由固定密钥

    params = {
        'gender'      :1,
        'gps_info'    :'116.348605,39.902727',
        'loc_info'    :'CN,北京市,北京市',
        'is_new_user' :0,
        'lc'          :'0000000000000048',
        'cc'          :'TG0001',
        'cv'          :'IK3.8.60_Iphone',
        'proto'       :7,
        'idfa'        :'D2E02B97-0F35-486F-9CD4-A2EC13BBC8FB',
        'idfv'        :'5779214D-BC8F-446E-A547-913048F7F935',
        'devi'        :'0a4392f06ab0ff10b44c6f88d95bf4d6db67f0e7',
        'osversion'   :'ios_10.200000',
        'ua'          :'iPhone9_2',
        'imei'        :'',
        'imsi'        :'',
        'uid'         :207821358,
        'sid'         :'20RUXGrYPxpJy75btYQYlVp6lYxi0wj1xV50Ttnls6ty3DcXE5i1',
        'conn'        :'wifi',
        'mtid'        :'987c70ecbcd643998ea6bcd3b8868934',
        'mtxid'       :'b0958e29253f',
        'logid'       :133,
        's_sg'        :s_sg,
        's_sc'        :100,
        's_st'        :current_timestamp
    }

    url = tools.joint_url('http://120.55.238.158/api/live/simpleall', params)
    base_parser.add_url('LiveApp_urls', SITE_ID, url, remark=remark)


# 必须定义 解析网址
def parser(url_info):
    url_info['_id'] = str(url_info['_id'])
    log.debug('处理 \n' + tools.dumps_json(url_info))

    root_url = url_info['url']
    depth = url_info['depth']
    site_id = url_info['site_id']
    remark = url_info['remark']

    json = tools.get_json_by_requests(root_url)
    json = tools.dumps_json(json)

    # 主播信息
    lives = tools.get_json_value(json, 'lives')
#     |name||||主播名|
# |sex||||性别|
# |image_url||||贴图|
# |age||||年龄|
# |address||||地区|
# |fans_count||||粉丝数|
# |watched_count||||观众数 |
# |ranklist_day||||日排行榜|
# |ranklist_week||||周排行榜|
# |ranklist_month||||月排行榜|
# |room||||房间号|
# |room_url||||房间连接|
# |video_path||||直播视频流路径|
# |record_time||||记录时间|
# |site_id||||网站id|
# |read_status||||读取状态（0 没读， 1读取）|
    for live in lives:
        name = tools.get_json_value(live, 'creator.nick')
        image_url = tools.get_json_value(live, 'creator.portrait')
        room = tools.get_json_value(live, 'creator.id')
        room_url = tools.get_json_value(live, 'share_addr')
        video_path = tools.get_json_value(live, 'stream_addr')
        watched_count = tools.get_json_value(live, 'online_users')
        address = tools.get_json_value(live, 'city')

        print(tools.dumps_json(live))
        break




if __name__ == '__main__':
    secret_key="8D2E##1[5$^(38#%#d3z96;]35q#MD28"
    current_timestamp = tools.get_current_timestamp()

    s_sg = tools.get_md5(secret_key + str(current_timestamp)) #Sig由固定密钥

    params = {
        'gender'      :1,
        'gps_info'    :'116.348605,39.902727',
        'loc_info'    :'CN,北京市,北京市',
        'is_new_user' :0,
        'lc'          :'0000000000000048',
        'cc'          :'TG0001',
        'cv'          :'IK3.8.60_Iphone',
        'proto'       :7,
        'idfa'        :'D2E02B97-0F35-486F-9CD4-A2EC13BBC8FB',
        'idfv'        :'5779214D-BC8F-446E-A547-913048F7F935',
        'devi'        :'0a4392f06ab0ff10b44c6f88d95bf4d6db67f0e7',
        'osversion'   :'ios_10.200000',
        'ua'          :'iPhone9_2',
        'imei'        :'',
        'imsi'        :'',
        'uid'         :207821358,
        'sid'         :'20RUXGrYPxpJy75btYQYlVp6lYxi0wj1xV50Ttnls6ty3DcXE5i1',
        'conn'        :'wifi',
        'mtid'        :'987c70ecbcd643998ea6bcd3b8868934',
        'mtxid'       :'b0958e29253f',
        'logid'       :133,
        's_sg'        :s_sg,
        's_sc'        :100,
        's_st'        :current_timestamp
    }

    url = tools.joint_url('http://120.55.238.158/api/live/simpleall', params)

    url_info = {
        "status": 0,
        "site_id": 1,
        'url':url,
        "remark": {
            "search_keyword3": [],
            "search_keyword2": [],
            "search_keyword1": []
        },
        "depth": 0,
        "_id": "58a2cec55344652a48ab2f5a"
    }

    parser(url_info)


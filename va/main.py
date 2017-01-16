import sys
sys.path.append('../')
import init
from utils.log import log
from base.spider import Spider
import utils.tools as tools
from db.oracledb import OracleDB
from utils.export_data import ExportData
import time

# 需配置
from va.parsers import *
def main():
    log.info('\n********** VA begin **********')
    search_task_sleep_time = int(tools.get_conf_value('config.conf', 'task', 'search_task_sleep_time'))
    db = OracleDB()
    #  更新任务状态 正在做的更新为等待
    sql = 'update tab_ivms_task_info set task_status = 501 where task_status = 502'
    db.update(sql)
    while True:
        sql = 'select t.* from TAB_IVMS_TASK_INFO t where task_status = 502'
        do_task = db.find(sql, fetch_one=True)
        if do_task:
            time.sleep(search_task_sleep_time)
            continue

        # 查任务
        log.debug('查询任务...')
        sql = 'select t.* from TAB_IVMS_TASK_KEYWORD t where t.task_id in (select task_id from TAB_IVMS_TASK_INFO where task_status = 501)'
        results = list(db.find(sql))
        if not results:
            time.sleep(search_task_sleep_time)
            continue

        result = [0, 0, '', '', '']
        for r in results:
            result[0] = r[0]
            result[1] = r[1]
            result[2] += r[2] + ","
            result[3] += r[3] + ","
            result[4] += r[4] + ","

        search_keyword1 = result[2][:-1].split(',')
        search_keyword2 = result[3][:-1].split(',')
        search_keyword3 = result[4][:-1].split(',')
        task_id = result[1]

        def begin_callback():
            log.info('\n********** template begin **********')
            # 更新任务状态 正在做
            sql = 'update TAB_IVMS_TASK_INFO set task_status = 502 where task_id = %d'%task_id
            db.update(sql)

        def end_callback():
            log.info('\n********** template end **********')

            # 更新任务状态 做完
            sql = 'update TAB_IVMS_TASK_INFO set task_status = 503 where task_id = %d'%task_id
            db.update(sql)

            # 导出数据
            key_map = {
                'program_id': 'vint_sequence.nextval',
                'search_type': 'int_search_type',
                'program_name': 'str_title',
                'program_url': 'str_url',
                'release_date': 'date_release_time',
                'image_url': 'str_video_url',
                'program_content':'str_content',
                'task_id': 'vint_%d' % task_id,
                'keyword':'str_keyword',
                'keyword_count':'int_keyword_count'
            }

            export = ExportData('VA_content_info', 'tab_ivms_program_info', key_map, 'program_url')
            export.export_to_oracle()

        # 配置spider

        spider = Spider(tab_urls = 'VA_urls', tab_site = 'VA_site_info', tab_content = 'VA_content_info',
                        parser_count = 1, begin_callback = begin_callback, end_callback = end_callback,
                        search_keyword1 = search_keyword1, search_keyword2 = search_keyword2, search_keyword3 = search_keyword3)

        # 添加parser
        spider.add_parser(baidu_parser)
        spider.add_parser(magnet_parser)
        spider.add_parser(netdisk_parser)
        spider.add_parser(weibo_parser)
        spider.add_parser(wechat_parser)

        spider.start()

        time.sleep(search_task_sleep_time)

if __name__ == '__main__':
    main()

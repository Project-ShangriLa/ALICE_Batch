import time
import pixiv
import sys
import json
import pymysql.cursors
from datetime import date
from datetime import datetime
import requests
import re
from optparse import OptionParser

#'stats': {'favorited_count': {'public': 2, 'private': 0}, 'scored_count': 2, 'score': 20, 'views_count': 24, 'commented_count': 0},

parser = OptionParser()

parser.add_option(
    '-d', '--day',
    action = 'store_true',
    dest = 'day_switch',
    help = 'day mode on'
)

parser.add_option(
    '-s', '--sleep_second',
    action = 'store',
    type = 'int',
    dest = 'sleep_sec',
)

parser.set_defaults(
    year = 2016,
    cours_id = 1,
    day_switch = False,
    sleep_sec = 30
)

options, args = parser.parse_args()

day_switch = options.day_switch
sleep_sec = options.sleep_sec

def status_table_init(master_ids):
    connection = pymysql.connect(host='localhost',
                                 user='root',
                                 password='',
                                 db='anime_admin_development',
                                 charset='utf8mb4',
                                 cursorclass=pymysql.cursors.DictCursor)

    try:
        with connection.cursor() as cursor:
            # Create a new record
            sql = "delete FROM pixiv_stats_status WHERE bases_id IN (" + ",".join(master_ids) + ")"
            cursor.execute(sql)

        connection.commit()
    except:
        print("Unexpected error:", sys.exc_info()[0])
    finally:
        connection.close()

def regist_pixiv_datta(id, get_date, key, total, note, json, history_table):
    connection = pymysql.connect(host='localhost',
                                 user='root',
                                 password='',
                                 db='anime_admin_development',
                                 charset='utf8mb4',
                                 cursorclass=pymysql.cursors.DictCursor)

    try:
        with connection.cursor() as cursor:
            sql = "INSERT INTO `pixiv_stats_status` (`bases_id`, `get_date`, `search_word`, `total`,`note`, `json`, `created_at`, `updated_at`) " \
                  "VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"
            cursor.execute(sql, (id, get_date, key, total, note, json, datetime.now(), datetime.now()))

            sql = "INSERT INTO " + history_table + " (`bases_id`, `get_date`, `search_word`, `total`,`note`, `json`, `created_at`, `updated_at`) " \
                  "VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"
            cursor.execute(sql, (id, get_date, key, total, note, json, datetime.now(), datetime.now()))

            connection.commit()

    finally:
        connection.close()


SLEEP_TIME_SEC = sleep_sec
history_table = "pixiv_stats_hourly"
get_date = datetime.now()
param = sys.argv

if (day_switch):
    history_table = "pixiv_stats_daily"
    get_date = date.today()

print(history_table)


master_list = json.loads(result.text)
master_ids = []
for master in master_list:
    master_ids.append(str(master['id']))
status_table_init(master_ids)

for master in master_list:

    json_result = pixiv.api.search_works(titles, page=1, mode='tag')
    total = json_result.pagination.total
    print(total)

    regist_pixiv_datta(master['id'], get_date, titles, total, '', '', history_table)

    print("sleep!")
    time.sleep(SLEEP_TIME_SEC)

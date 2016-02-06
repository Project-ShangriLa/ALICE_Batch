import time
import pixiv
import sys
import json
import pymysql.cursors
from datetime import date
from datetime import datetime
import requests
import re

# 引数が-dの時はデイリーテーブルに保存する


def status_table_init():
    connection = pymysql.connect(host='localhost',
                                 user='root',
                                 password='',
                                 db='anime_admin_development',
                                 charset='utf8mb4',
                                 cursorclass=pymysql.cursors.DictCursor)

    try:
        with connection.cursor() as cursor:
            # Create a new record
            sql = "truncate pixiv_tag_status"
            cursor.execute(sql)
        connection.commit()

    finally:
        connection.close()

# スペースが入っていたら()で囲む、全角+は半角に
def trim_keyword(keyword):
    #(第二期)などを消去
    if re.search("\(", keyword) != None:
        keyword =re.sub(r'(\(.*\))', "", keyword)
    # 機動戦士ガンダム サンダーボルトなど
    if re.search("\s" , keyword) != None:
        keyword = re.sub(r'(.*)', "(" + r"\1" + ")", keyword)
    # ノルン＋ノネットのため
    if re.search("＋" , keyword) != None:
        keyword = keyword.replace('＋', '+')

    return keyword


def regist_pixiv_datta(id, get_date, key, total, note, json, history_table):
    connection = pymysql.connect(host='localhost',
                                 user='root',
                                 password='',
                                 db='anime_admin_development',
                                 charset='utf8mb4',
                                 cursorclass=pymysql.cursors.DictCursor)

    try:
        with connection.cursor() as cursor:
            sql = "INSERT INTO `pixiv_tag_status` (`bases_id`, `get_date`, `search_word`, `total`,`note`, `json`, `created_at`, `updated_at`) " \
                  "VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"
            cursor.execute(sql, (id, get_date, key, total, note, json, datetime.now(), datetime.now()))

            sql = "INSERT INTO " + history_table + " (`bases_id`, `get_date`, `search_word`, `total`,`note`, `json`, `created_at`, `updated_at`) " \
                  "VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"
            cursor.execute(sql, (id, get_date, key, total, note, json, datetime.now(), datetime.now()))

            connection.commit()

    finally:
        connection.close()


SLEEP_TIME_SEC = 30
history_table = "pixiv_tag_hourly"
get_date = datetime.now()
daily_flag = False
param = sys.argv

if (len(param) > 1 and param[1] == '-d'):
    history_table = "pixiv_tag_daily"
    daily_flag = True
    get_date = date.today()


print(history_table)

status_table_init()

url = 'http://api.moemoe.tokyo/anime/v1/master/2016/1'
result = requests.get(url)

master_list = json.loads(result.text)

for master in master_list:

    titles = trim_keyword(master['title'])
    if len(master['title_short1']) > 0 and titles != trim_keyword(master['title_short1']):
        titles += ' or ' + trim_keyword(master['title_short1'])
    if len(master['title_short2']) > 0:
        titles += ' or ' + trim_keyword(master['title_short2'])
    if len(master['title_short3']) > 0:
        titles += ' or ' + trim_keyword(master['title_short3'])

    print(titles)
    continue
    json_result = pixiv.api.search_works(titles, page=1, mode='tag')
    total = json_result.pagination.total
    print(total)

    regist_pixiv_datta(master['id'], get_date, titles, total, '', '', history_table)

    print("sleep!")
    time.sleep(SLEEP_TIME_SEC)

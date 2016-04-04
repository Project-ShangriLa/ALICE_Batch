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

#python3 alice.py -y 2016 -c 2
#python3 alice.py -y 2016 -c 2 -d
#python3 alice.py -y 2016 -c 2 -d -s 5
parser = OptionParser()

parser.add_option(
    '-d', '--day',
    action = 'store_true',
    dest = 'day_switch',
    help = 'day mode on'
)

parser.add_option(
    '-y', '--year',
    action = 'store',
    type = 'str',
    dest = 'year',
)

parser.add_option(
    '-c', '--cours',
    action = 'store',
    type = 'str',
    dest = 'cours',
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
year = options.year
cours = options.cours
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
            sql = "delete FROM pixiv_tag_status WHERE bases_id IN (" + ",".join(master_ids) + ")"
            cursor.execute(sql)

        connection.commit()
    except:
        print("Unexpected error:", sys.exc_info()[0])
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


SLEEP_TIME_SEC = sleep_sec
history_table = "pixiv_tag_hourly"
get_date = datetime.now()
param = sys.argv

if (day_switch):
    history_table = "pixiv_tag_daily"
    get_date = date.today()

print(history_table)

url = 'http://api.moemoe.tokyo/anime/v1/master/' + year + '/' + cours
result = requests.get(url)

master_list = json.loads(result.text)
master_ids = []
for master in master_list:
    master_ids.append(str(master['id']))
status_table_init(master_ids)

for master in master_list:

    titles = trim_keyword(master['title'])
    if len(master['title_short1']) > 0 and titles != trim_keyword(master['title_short1']):
        titles += ' or ' + trim_keyword(master['title_short1'])
    if len(master['title_short2']) > 0:
        titles += ' or ' + trim_keyword(master['title_short2'])
    if len(master['title_short3']) > 0:
        titles += ' or ' + trim_keyword(master['title_short3'])

    print(titles)
#    continue
    json_result = pixiv.api.search_works(titles, page=1, mode='tag')
    total = json_result.pagination.total
    print(total)

    regist_pixiv_datta(master['id'], get_date, titles, total, '', '', history_table)

    print("sleep!")
    time.sleep(SLEEP_TIME_SEC)

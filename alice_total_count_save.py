import time
import pixiv
import sys
import json
import pymysql.cursors
from datetime import date
from datetime import datetime
from bs4 import BeautifulSoup
import requests
import re
from pprint import pprint
import urllib
import urllib.parse


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
    '-f', '--filename',
    dest = 'stats_save_list_file',
    action = 'store',
    type = 'string',
)

parser.add_option(
    '-s', '--sleep_second',
    action = 'store',
    type = 'int',
    dest = 'sleep_sec',
)

parser.set_defaults(
    stats_save_list_file = "./config/view_list.json",
    day_switch = False,
    sleep_sec = 10
)

options, args = parser.parse_args()

day_switch = options.day_switch
sleep_sec = options.sleep_sec
stats_save_list_file = options.stats_save_list_file

def status_table_init(bases_id, search_word_list):
    connection = pymysql.connect(host='localhost',
                                 user='root',
                                 password='',
                                 db='anime_admin_development',
                                 charset='utf8mb4',
                                 cursorclass=pymysql.cursors.DictCursor)

    try:
        with connection.cursor() as cursor:

            dq = '"'

            # Create a new record
            sql = "delete FROM pixiv_stats_status WHERE search_word IN (" + dq + "\",\"".join(search_word_list) + dq + ") and bases_id = " + bases_id

            print(sql)

            cursor.execute(sql)

        connection.commit()
    except:
        print("Unexpected error:", sys.exc_info()[0])
    finally:
        connection.close()

def regist_pixiv_data(record_data, history_table):
    connection = pymysql.connect(host='localhost',
                                 user='root',
                                 password='',
                                 db='anime_admin_development',
                                 charset='utf8mb4',
                                 cursorclass=pymysql.cursors.DictCursor)
    id = record_data["id"]
    get_date = record_data["get_date"]
    search_word = record_data["search_word"]
    favorited_count_public = record_data["favorited_count_public"]
    favorited_count_private = record_data["favorited_count_private"]
    scored_count = record_data["scored_count"]
    score = record_data["score"]
    views_count = record_data["views_count"]
    commented_count = record_data["commented_count"]
    note = record_data["note"]
    json = record_data["json"]

    try:
        with connection.cursor() as cursor:
            sql = "INSERT INTO `pixiv_stats_status` (`bases_id`, `get_date`, `search_word`, `favorited_count_public`, `favorited_count_private`, `scored_count`, `score`, `views_count`, `commented_count`, `note`, `json`, `created_at`, `updated_at`) " \
                  "VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
            cursor.execute(sql, (id, get_date, search_word, favorited_count_public, favorited_count_private,  scored_count, score, views_count, commented_count, note, json, datetime.now(), datetime.now()))

            sql = "INSERT INTO " + history_table + " (`bases_id`, `get_date`, `search_word`, `favorited_count_public`, `favorited_count_private`, `scored_count`, `score`, `views_count`, `commented_count`, `note`, `json`, `created_at`, `updated_at`) " \
                                                   "VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
            cursor.execute(sql, (id, get_date, search_word, favorited_count_public, favorited_count_private,  scored_count, score, views_count, commented_count, note, json, datetime.now(), datetime.now()))

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

print(stats_save_list_file)

f = open(stats_save_list_file, 'r')
master_list = json.load(f)
f.close

pprint(master_list)

keyword_list = []
for bases_id in master_list:
    print(master_list[bases_id])
    status_table_init(bases_id, master_list[bases_id])

for bases_id in master_list:
    for search_word in master_list[bases_id]:

        favorited_count_public = 0
        favorited_count_private = 0
        scored_count = 0
        score = 0
        views_count = None
        commented_count = 0

        # pixiv大百科
        # http://dic.pixiv.net/a/%E5%94%90%E6%BE%A4%E6%B4%8B

        url = "http://dic.pixiv.net/a/" + urllib.parse.quote(search_word)
        print(url)

        try:
            html = urllib.request.urlopen(url)
        except Exception as e:
            pprint(e)
            continue


        bsObj = BeautifulSoup(html, "html.parser")

        #  <h2>このタグがついたpixivの作品閲覧データ <span class="total-count">総閲覧数: 37897330</span></h2>
        total_count = bsObj.find("span", class_="total-count")

        pprint(total_count)

        if (total_count == None):
            continue

        print(total_count.string.replace("総閲覧数: ", ""))

        views_count = int(total_count.string.replace("総閲覧数: ", ""))

        record_data = {
            'id': bases_id,
            'get_date': get_date,
            'search_word': search_word,
            'favorited_count_public': favorited_count_public,
            'favorited_count_private': favorited_count_private,
            'scored_count': scored_count,
            'score': score,
            'views_count': views_count,
            'commented_count': commented_count,
            'note': 'total-count',
            'json': ''
        }
        regist_pixiv_data(record_data, history_table)
        time.sleep(SLEEP_TIME_SEC)




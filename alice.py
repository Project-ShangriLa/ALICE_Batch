import time
import pixiv
import sys
import json
import pymysql.cursors
from datetime import date
from datetime import datetime

# 引数が-dの時はデイリーテーブルに保存する

history_table = "pixiv_tag_hourly"
get_date = datetime.now()
daily_flag = False
param = sys.argv

if (len(param) > 1 and param[1] == '-d'):
    history_table = "pixiv_tag_daily"
    daily_flag = True
    get_date = date.today()


print(history_table)
SLEEP_TIME_SEC = 30




#time.sleep(SLEEP_TIME_SEC)
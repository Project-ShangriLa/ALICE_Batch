import time
import sys
import json
import pymysql.cursors
from datetime import date
from datetime import datetime
import requests
import re

connection = pymysql.connect(host='localhost',
                             user='root',
                             password='',
                             db='anime_admin_development',
                             charset='utf8mb4',
                             cursorclass=pymysql.cursors.DictCursor)

url = 'http://api.moemoe.tokyo/anime/v1/master/2016/1'
result = requests.get(url)

master_list = json.loads(result.text)
master_ids = []
for master in master_list:
    master_ids.append(str(master['id']))


print(",".join(master_ids))

try:

    with connection.cursor() as cursor:
        # Create a new record
        sql = "delete FROM pixiv_tag_status WHERE bases_id IN (" + ",".join(master_ids) + ")"
        cursor.execute(sql)

    connection.commit()
except:
    print("Unexpected error:", sys.exc_info()[0])
finally:
    print("Unexpected error:", sys.exc_info()[0])
    connection.close()

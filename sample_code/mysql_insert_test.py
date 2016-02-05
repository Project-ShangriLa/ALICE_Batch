import pymysql.cursors
from datetime import date
from datetime import datetime
# Connect to the database
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

        sql = "INSERT INTO `pixiv_tag_status` (`bases_id`, `get_date`, `search_word`, `total`,`note`, `json`, `created_at`, `updated_at`) " \
              "VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"
        cursor.execute(sql, (1, date.today(),'あああ',333, 'あああ','ううう', datetime.now(),datetime.now()))

    # connection is not autocommit by default. So you must commit to save
    # your changes.
    connection.commit()

finally:
    connection.close()

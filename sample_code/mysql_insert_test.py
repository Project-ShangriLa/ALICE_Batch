import pymysql.cursors

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
        sql = "INSERT INTO `pixiv_tag_status` (`bases_id`, `get_date`, `search_word`, `total`,`note`, `json`, `created_at`, `updated_at`) " \
              "VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"
        cursor.execute(sql, (1, '2015-02-01 10:00:00','あああ',333, 'あああ','ううう', '2015-02-01 10:00:00','2015-02-01 10:00:00'))

    # connection is not autocommit by default. So you must commit to save
    # your changes.
    connection.commit()

finally:
    connection.close()

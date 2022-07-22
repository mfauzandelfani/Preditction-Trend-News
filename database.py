import pymysql

conn = pymysql.connect(host='localhost',
                         user='root',
                         password='',
                         db='berita')
cursor = conn.cursor()
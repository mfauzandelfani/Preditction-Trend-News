import pymysql

conn = pymysql.connect(host='localhost',
                         user='root',
                         password='',
                         db='data_berita')
cursor = conn.cursor()
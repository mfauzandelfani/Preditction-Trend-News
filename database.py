import pymysql

conn = pymysql.connect(host='localhost',
                         user='root',
                         password='',
                         db='n1681648_berita')
cursor = conn.cursor()
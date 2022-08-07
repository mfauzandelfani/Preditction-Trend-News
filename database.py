import pymysql

global connect_timeout
global max_allowed_packet
conn = pymysql.connect(host='localhost',
                         user='root',
                         password='',
                         db='berita'
                      )
cursor = conn.cursor()
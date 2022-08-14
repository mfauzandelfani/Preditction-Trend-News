import pymysql
# from pymysql.cursors import DictCursor


conn = pymysql.connect(host='localhost',
                         user='root',
                         password='',
                         db='berita'
                       
                      )

cursor = conn.cursor()



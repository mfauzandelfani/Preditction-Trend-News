import mysql.connector
# from pymysql.cursors import DictCursor
import pymongo
from pymongo import MongoClient

conn = mysql.connector.connect(host='localhost',
                         user='root',
                         password='',
                         db='berita'
                       
                      )

cursor = conn.cursor()

cluster = MongoClient('mongodb+srv://admin:rhoiOqUAvMel4UWt@cluster0.pvms5.mongodb.net/test')

from pickle import TRUE
from urllib import response
from flask import Flask, render_template, request
from flask_cors import CORS, cross_origin
from flask_bootstrap import Bootstrap5
from flask_mysqldb import MySQL
import os
from flask import jsonify
from flask import flash, request
import urllib.request
import requests
from database import *
app = Flask(__name__)
CORS(app)

app.env = "development"

cursor.execute('''Select DISTINCT antecedents, consequents, date, time, length from trends group by antecedents''')
cursor.connection.commit()
rv = cursor.fetchall()
#Closing the cursor
cursor.close()

bootstrap = Bootstrap5(app)

@app.route("/")
def home():
        #Creating a connection cursor
   
    return render_template('index.html', data= rv)
    #return render_template('index.html', tables = [hasil.to_html(classes='data')], header = "true" )

@app.route('/emp')
def emp():
    try:
        cursor = conn.cursor()
        cursor.execute("SELECT * from trends")
        empRows = cursor.fetchall()
        respone = jsonify(empRows)
        respone.status_code = 200
        return respone
    except Exception as e:
        print(e)
        return response('', 'ERROR !')
        # cursor.close() 
        # conn.close()


@app.route('/wordcloud')    
def word():
    return render_template('wordcloud.html')    

@app.route('/harian')    
def hari():

    return render_template('harian.html')

@app.route('/mingguan')    
def minggu():
   
    return render_template('mingguan.html')

@app.route('/bulanan')    
def bulan():
    return render_template('bulanan.html')


@app.errorhandler(404)
def showMessage(error=None):
    message = {
        'status': 404,
        'message': 'Record not found: ' + request.url,
    }
    respone = jsonify(message)
    respone.status_code = 404
    return respone

if __name__ == '__main__':
   app.run(host="localhost", debug = True)
   os.environ.setdefault('app.env', 'development')    
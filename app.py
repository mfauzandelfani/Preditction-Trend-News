from cProfile import label
from pickle import TRUE
from urllib import response
from flask import Flask, redirect, render_template, request, url_for
from flask_cors import CORS, cross_origin
from flask_bootstrap import Bootstrap5
from flask_mysqldb import MySQL
import os
from flask import jsonify
from flask import flash, request
import urllib.request
from matplotlib.font_manager import json_dump, json_load
from matplotlib.pyplot import bar_label
from pendulum import time
import requests
from flask import json
from database import *
from livereload import Server


PEOPLE_FOLDER = 'static/'

app = Flask(__name__)
CORS(app)

app.env = "development"
bootstrap = Bootstrap5(app)

app.config['UPLOAD_FOLDER'] = PEOPLE_FOLDER


    
@app.route("/")
def home():
        #Creating a connection cursor
    cursor.execute('''Select antecedents, consequents, date, length from trends where Date(date) = CURDATE()''')
    cursor.connection.commit()
    rv = cursor.fetchall()

#Closing the cursor  
    return render_template('index.html', data = rv)
    #return render_template('index.html', tables = [hasil.to_html(classes='data')], header = "true" )


@app.route("/berita")
def berita():
        #Creating a connection cursor
    cursor.execute('''Select title, media, date from berita_mentah where Date(date) = CURDATE() ''')
    cursor.connection.commit()
    rv = cursor.fetchall()

#Closing the cursor  
    return render_template('berita.html', data = rv)    

@app.route('/wordcloud',methods = ["POST","GET"])    
def word():
    if request.method == 'POST':
        if request.method == 'POST' and request.form.get('hr', '') == 'hr':
            data = "per-hari"
            full_filename = os.path.join(app.config['UPLOAD_FOLDER'], 'harian.png')
            return render_template('wordcloud.html', user_image = full_filename, data = data)
        elif request.method == 'POST' and request.form.get('mg', '') == 'mg':
            data = "per-minggu"
            full_filename = os.path.join(app.config['UPLOAD_FOLDER'], 'mingguan.png')
            return render_template('wordcloud.html', user_image = full_filename, data = data)
        elif request.method == 'POST' and request.form.get('bl', '') == 'bl':
            data = "per-bulan"
            full_filename = os.path.join(app.config['UPLOAD_FOLDER'], 'bulanan.png')
            return render_template('wordcloud.html', user_image = full_filename, data = data)  

    data = "per-hari"
    full_filename = os.path.join(app.config['UPLOAD_FOLDER'], 'harian.png')
    return render_template('wordcloud.html', user_image = full_filename, data = data)
        
    


@app.route('/media')

def media():
    legend = 'Today Data'
    cursor.execute('''SELECT media from berita_mentah group by media;''')
    cursor.connection.commit()
    bar_labels = cursor.fetchall()

    cursor.execute('''SELECT count(media) from berita_mentah where Date(date) = CURDATE() group by media;''')
    cursor.connection.commit()
    bar_values = cursor.fetchall()
    listvalues = json.dumps(bar_values)
    return render_template('media.html', labels=bar_labels, values = listvalues, legend = legend )    


@app.route('/harian',methods = ["POST","GET"])    
def hari():
    lb = '3'
    gb = '5'
    if request.method == 'POST':
        lb = request.form["fq"]
        gb = request.form["sg"]
 
        
    cursor.execute("SELECT DISTINCT concat(antecedents,', ',consequents) from trends WHERE length = "+lb+" and DATE(date) = curdate() group by rand() limit "+gb+";")
    cursor.connection.commit()
    bar_labels = cursor.fetchall()

    cursor.execute("SELECT length from trends WHERE length = "+lb+" and DATE(date) = curdate() limit "+gb+";")
    cursor.connection.commit()
    bar_values = cursor.fetchall()
    listvalues = json.dumps(bar_values)

    cursor.execute("SELECT count(length) from trends where DATE(date) = curdate() group by length;")
    cursor.connection.commit()
    bar_values2 = cursor.fetchall()
    listvalues2 = json.dumps(bar_values2)

    return render_template("harian.html", labels = bar_labels, values = listvalues, values2 = listvalues2)

@app.route('/mingguan',methods = ["POST","GET"])    
def minggu():
    lb = '3'
    gb = '5'
    if request.method == 'POST':
        lb = request.form["fq"]
        gb = request.form["sg"]
 
        
    cursor.execute("SELECT DISTINCT concat(antecedents,', ',consequents) from trends WHERE length = "+lb+" and date between date_sub(now(),INTERVAL 1 WEEK) and now() group by rand() limit "+gb+";")
    cursor.connection.commit()
    bar_labels = cursor.fetchall()

    cursor.execute("SELECT length from trends WHERE length = "+lb+" and date between date_sub(now(),INTERVAL 1 WEEK) and now() limit "+gb+";")
    cursor.connection.commit()
    bar_values = cursor.fetchall()
    listvalues = json.dumps(bar_values)

    cursor.execute("SELECT count(length) from trends where date between date_sub(now(),INTERVAL 1 WEEK) and now() group by length;")
    cursor.connection.commit()
    bar_values2 = cursor.fetchall()
    listvalues2 = json.dumps(bar_values2)

    return render_template("mingguan.html", labels = bar_labels, values = listvalues, values2 = listvalues2)


@app.route('/bulanan',methods = ["POST","GET"])    
def bulan():
    lb = '3'
    gb = '5'
    if request.method == 'POST':
        lb = request.form["fq"]
        gb = request.form["sg"]
 
        
    cursor.execute("SELECT DISTINCT concat(antecedents,', ',consequents) from trends WHERE length = "+lb+" and MONTH(date)=MONTH(NOW()) group by rand() limit "+gb+";")
    cursor.connection.commit()
    bar_labels = cursor.fetchall()

    cursor.execute("SELECT length from trends WHERE length = "+lb+" and MONTH(date)=MONTH(NOW()) limit "+gb+";")
    cursor.connection.commit()
    bar_values = cursor.fetchall()
    listvalues = json.dumps(bar_values)

    cursor.execute("SELECT count(length) from trends where MONTH(date)=MONTH(NOW()) group by length;")
    cursor.connection.commit()
    bar_values2 = cursor.fetchall()
    listvalues2 = json.dumps(bar_values2)

    return render_template("bulanan.html", labels = bar_labels, values = listvalues, values2 = listvalues2)

    



if __name__ == '__main__':
   app.run(host="localhost", debug = True)

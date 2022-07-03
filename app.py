from flask import Flask, render_template
from flask_bootstrap import Bootstrap5
from trend import data


app = Flask(__name__)
headings = ('Antecedents', 'Consequents', 'Length')
#hasil = ('aku','sayang','kamu'), ('dia', 'cinta', 'siapa')
bootstrap = Bootstrap5(app)
@app.route("/")
def home():
    return render_template('index.html', data = data)
    #return render_template('index.html', tables = [hasil.to_html(classes='data')], header = "true" )

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

if __name__ == '__main__':
   app.run(debug=True)    
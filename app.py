import requests
from textblob import TextBlob
from bs4 import BeautifulSoup
import pandas as pd
import nltk
from nltk.tokenize import word_tokenize
nltk.download('punkt')
from Sastrawi.StopWordRemover.StopWordRemoverFactory import StopWordRemoverFactory
from Sastrawi.Stemmer.StemmerFactory import StemmerFactory
import re
import pandas as pd
from mlxtend.preprocessing import TransactionEncoder
from mlxtend.frequent_patterns import apriori
from mlxtend.frequent_patterns import association_rules
from wordcloud import WordCloud
import matplotlib.pyplot as plt
import numpy as np
from wordcloud.wordcloud import STOPWORDS
from flask import Flask, render_template
from flask_bootstrap import Bootstrap5
from flask import send_file
import pendulum
from datetime import datetime

factory = StopWordRemoverFactory()
factory2 = StemmerFactory()
stopword = factory.create_stop_word_remover()
stemmer = factory2.create_stemmer()

#enter URL
url = ["https://www.suara.com/rss",
       "https://www.antaranews.com/rss/top-news.xml",
       "https://www.cnbcindonesia.com/news/rss",
       "https://www.suara.com/rss/news",
       "https://www.vice.com/id_id/rss",  
       "https://www.cnnindonesia.com/nasional/rss",
       "https://www.cnbcindonesia.com/news/rss",
       "https://www.jawapos.com/nasional/rss",
       "https://lapi.kumparan.com/v2.0/rss/"
   
       ]
  
data = []
title = []
date = []
for i in url:
    print(i)
    resp = requests.get(i)
    soup = BeautifulSoup(resp.content, features="xml")
    items = soup.findAll('item')
    news_items = []
    for x in items:
      news_item = {}
      #PRE-PROCESSING
      #Case Folding
      news_item['Title'] = x.title.text.lower()
      #news_item['Date'] = x.pubDate.text.lower()
      title.append(news_item['Title'])
      #date.append(news_item['Date'])
      #print(news_item)+
      #Stopword
      stop = stopword.remove(news_item['Title'])
      #Removing FUnctional
      res = re.sub(r'[^\w\s]', '', stop)
      #Stemming
      output   = stemmer.stem(res)
      #Tokenizing
      tokens = nltk.tokenize.word_tokenize(output)
      data.append(tokens)

column_names = ['Title',#'Date',
                'Item']
hasil = {"Title": title,#"Date": date, 
        "Item": data}
berita = pd.DataFrame(hasil, columns = column_names)        
#print (berita)    
dataset = berita['Item']

te = TransactionEncoder()
te_ary = te.fit(dataset).transform(dataset)
df = pd.DataFrame(te_ary, columns=te.columns_)


apriori(df, min_support=0.005, use_colnames=True)
frequent_itemsets = apriori(df, min_support=0.005, use_colnames=True)
frequent_itemsets['length'] = frequent_itemsets['itemsets'].apply(lambda x: len(x))
frequent_itemsets

rules = association_rules(frequent_itemsets, metric="confidence", min_threshold=0.7)
hasil = pd.DataFrame(rules)
hasil = hasil.drop(columns=['conviction','leverage','lift','confidence','support','consequent support','antecedent support'], axis=1, inplace=False)
hasil['length'] = hasil['antecedents'].apply(lambda x: len(x))+hasil['consequents'].apply(lambda y: len(y))
hasil = hasil[(hasil['length'] >= 3) &(hasil['length'] <= 7)]
print(hasil)


kolom1 = list(hasil['antecedents'])
list1 = []
for i in kolom1:
  list1.append(list(i))
#print(list1)

kolom2 = list(hasil['consequents'])
list2 = []
for i in kolom2:
  list2.append(list(i))
#print(list2)

ist = pendulum.timezone('Asia/Jakarta')
time = []
for i in kolom1:
  time.append(datetime.now(ist).strftime('%Y-%m-%d %H:%M:%S'))

length = np.array(hasil['length'])

kolombaru = []
word = []
for x in range(len(hasil)):
  test = [list1[x],list2[x],time[x],length[x]]
  test2 = [list1[x],list2[x]]
  kolombaru.append(test)
  word.append(test2)

data = kolombaru

'''
sw = set(STOPWORDS)
sw.update(['antecedents','consequents','columns','rows','length',''])
wordcloud = WordCloud(collocations = False, stopwords = sw, width=3000, height=800, max_font_size=400, background_color='white',
                        max_words=10000)
wordcloud.generate(str(word))
plt.figure(figsize=(10,10))
plt.imshow(wordcloud, interpolation='bilinear')
plt.axis("off")
plt.tight_layout(pad=0)
#plt.show()
'''

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
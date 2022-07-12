from distutils.log import error
from tkinter import Variable
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
import pendulum
from datetime import datetime
import time
import json
from database import *
import schedule


data = []
title = []
date = []
list1 = []
list2 = []
time = []
kolombaru = []
word = []


def scraping():
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
  
  ist = pendulum.timezone('Asia/Jakarta')
  hasil['date'] = datetime.now(ist).strftime('%Y-%m-%d')
  hasil['time'] = datetime.now(ist).strftime('%H:%M:%S')
    
  hasil['length'] = hasil['antecedents'].apply(lambda x: len(x))+hasil['consequents'].apply(lambda y: len(y))
  hasil = hasil[(hasil['length'] >= 3) &(hasil['length'] <= 7)]
  
  hasil['antecedents'] = hasil['antecedents'].astype('string')
  hasil['consequents'] = hasil['consequents'].astype('string')
 
  print(hasil)
  print(hasil.dtypes)
    # print('=======')
    # print(list(hasil))
    
# creating column list for insertion
  cols = "`,`".join([str(i) for i in hasil.columns.tolist()])

# Insert DataFrame recrds one by one.
  for i,row in hasil.iterrows():
    sql = "INSERT INTO `trends` (`" +cols + "`) VALUES (" + "%s,"*(len(row)-1) + "%s)"
    cursor.execute(sql, tuple(row))


  # the connection is not autocommitted by default, so we must commit to save our changes
  sql2 = "UPDATE trends set antecedents = replace(antecedents, 'frozenset({', '');"
  sql3 = "UPDATE trends set antecedents = replace(antecedents, '})', '');"
  sql4 = "UPDATE trends set consequents = replace(consequents, 'frozenset({', '');"
  sql5 = "UPDATE trends set consequents = replace(consequents, '})', '');"
  
  cursor.execute(sql2)  
  cursor.execute(sql3)
  cursor.execute(sql4)
  cursor.execute(sql5)
  conn.commit()
  

def wordcloud():
  
  wordcloudsql = 'select antecedents, consequents from trends'
  cursor.execute(wordcloudsql) 
  cursor.conn.commit()
  rv = cursor.fetchall()
  cursor.close()

  #sw = set(STOPWORDS)
  #sw.update("'")
  wordcloud = WordCloud(collocations = False, width=3000, height=800, max_font_size=200, background_color='white',
                        max_words=10000)
  wordcloud.generate(str(rv))
  plt.figure(figsize=(10,10))
  plt.imshow(wordcloud, interpolation='bilinear')
  plt.axis("off")
  plt.tight_layout(pad=0)
  plt.show()      


# from apscheduler.schedulers.blocking import BlockingScheduler

# scheduler = BlockingScheduler()
# scheduler.add_job(scraping, 'interval', minutes=5)
# scheduler.start()
scraping()
#wordcloud()

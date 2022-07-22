# from distutils.log import error
# from tkinter import Variable
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
link = []
media=[]
media2=[]



def scraping():
  factory = StopWordRemoverFactory()
  factory2 = StemmerFactory()
  stopword = factory.create_stop_word_remover()
  stemmer = factory2.create_stemmer()
  #enter URL
  url = ["https://www.suara.com/rss",
       "https://www.antaranews.com/rss/top-news.xml",
       "https://www.cnbcindonesia.com/news/rss",
       "https://www.vice.com/id_id/rss",  
       "https://www.voaindonesia.com/api/zmgqoebmoi",
       "https://www.jawapos.com/nasional/rss",
       "https://lapi.kumparan.com/v2.0/rss/",
       "https://rss.tempo.co/nasional",
       "https://www.republika.co.id/rss",
       "https://sindikasi.okezone.com/index.php/rss/1/RSS2.0",
       "https://www.tribunnews.com/rss",
       "https://www.inews.id/feed/news"
 
  ]

  thislist = ("Suara", "Antara", "CNBC", "Vice", "VOA", "Jawapos","Kumparan", 
  "Tempo", "Republika", "Okezone", "Tribunnews", "INews")
  z = 0
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
      news_item['Link'] = x.link.text.lower()
      #news_item['Date'] = x.pubDate.text.lower()
      title.append(news_item['Title'])
      link.append(news_item['Link'])
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
      media.append(thislist[z])
    
    z += 1
  #print(media)

  ist = pendulum.timezone('Asia/Jakarta')
  date = datetime.now(ist).strftime('%Y-%m-%d %H:%M:%S')
  column_names = ['Title','Link','Date','Item']
  column_names2 = ['Title','Media','Link','Date']
  hasil = {"Title": title,"Link": link, "Date": date, "Item": data}
  hasil2 = {"Title": title, "Media": media, "Link": link, "Date": date}
  berita = pd.DataFrame(hasil, columns = column_names)
  berita2 = pd.DataFrame(hasil2, columns = column_names2)
  berita2['Title'] = berita['Title'].astype('string')
  berita2['Link'] = berita['Link'].astype('string')
  #berita2['Date'] = berita['Date'].astype('string')            
  # print (berita2)
  # print (berita2.dtypes)

  cols = "`,`".join([str(i) for i in berita2.columns.tolist()])
  for i,row in berita2.iterrows():
    sql = "INSERT INTO `berita_mentah` (`" +cols + "`) VALUES (" + "%s,"*(len(row)-1) + "%s)"
    cursor.execute(sql, tuple(row))
  conn.commit()
  sql2 = '''DELETE t1 FROM berita_mentah t1 INNER JOIN berita_mentah t2 WHERE t1.no < t2.no AND t1.title = t2.title AND t1.link = t2.link;'''

  cursor.execute(sql2)
  conn.commit()  
    
  dataset = berita['Item']

  te = TransactionEncoder()
  te_ary = te.fit(dataset).transform(dataset)
  df = pd.DataFrame(te_ary, columns=te.columns_)

  apriori(df, min_support=0.008, use_colnames=True)
  frequent_itemsets = apriori(df, min_support=0.008, use_colnames=True)
  frequent_itemsets['length'] = frequent_itemsets['itemsets'].apply(lambda x: len(x))
  frequent_itemsets

  rules = association_rules(frequent_itemsets, metric="confidence", min_threshold=0.7)
  print(rules)
 
  hasil = pd.DataFrame(rules)
  hasil = hasil.drop(columns=['conviction','leverage','lift','confidence','support','consequent support','antecedent support'], axis=1, inplace=False)
  
  
  hasil['date'] = datetime.now(ist).strftime('%Y-%m-%d %H:%M:%S')
  hasil['length'] = hasil['antecedents'].apply(lambda x: len(x))+hasil['consequents'].apply(lambda y: len(y))
  hasil = hasil[(hasil['length'] >= 3) &(hasil['length'] <= 7)]
  
  hasil['antecedents'] = hasil['antecedents'].astype('string')
  hasil['consequents'] = hasil['consequents'].astype('string')
 
  # print(hasil)
  # print(hasil.dtypes)
    # print('=======')
    # print(list(hasil))
    
# # creating column list for insertion
  cols = "`,`".join([str(i) for i in hasil.columns.tolist()])

# # # Insert DataFrame recrds one by one.
  for i,row in hasil.iterrows():
    sql = "INSERT INTO `trends` (`" +cols + "`) VALUES (" + "%s,"*(len(row)-1) + "%s)"
    cursor.execute(sql, tuple(row))


#   # the connection is not autocommitted by default, so we must commit to save our changes
  sql2 = "UPDATE trends set antecedents = replace(antecedents, 'frozenset({', '');"
  sql3 = "UPDATE trends set antecedents = replace(antecedents, '})', '');"
  sql4 = "UPDATE trends set consequents = replace(consequents, 'frozenset({', '');"
  sql5 = "UPDATE trends set consequents = replace(consequents, '})', '');"
  cursor.execute(sql2)  
  cursor.execute(sql3)
  cursor.execute(sql4)
  cursor.execute(sql5)
  cursor.execute('''UPDATE trends set antecedents = replace(antecedents, "'" , ''  );''')
  cursor.execute('''UPDATE trends set consequents = replace(consequents, "'" , ''  );''')
  conn.commit()
  sql6 = '''DELETE t1 FROM trends t1 INNER JOIN trends t2 WHERE t1.no < t2.no AND t1.antecedents = t2.antecedents AND t1.consequents = t2.consequents;'''
  cursor.execute(sql6)
  conn.commit()

def wordcloud():
  
  wordcloudsql = 'select antecedents, consequents from trends where DATE(date) = curdate()'
  cursor.execute(wordcloudsql) 
  conn.commit()
  rv = cursor.fetchall()
  cursor.close()

 
  # sw = set(STOPWORDS)
  # sw.update("`")
  rv = str(rv)
  res = re.sub(r"[^\w\s\<.*?>]", '', rv)
  print(res)
  
  wordcloud = WordCloud(collocations = False, width=1000, height=800, max_font_size=500, background_color='white',
                        max_words=10000)
  wordcloud.generate(res)
  plt.figure(figsize=(10,10))
  plt.imshow(wordcloud, interpolation='bilinear')
  plt.axis("off")
  plt.tight_layout(pad=0)
  #plt.show()     
  plt.savefig('static/harian.png')

# from apscheduler.schedulers.blocking import BlockingScheduler

# scheduler = BlockingScheduler()
# scheduler.add_job(scraping, 'interval', minutes=5)
# scheduler.start()
#scraping()
wordcloud()

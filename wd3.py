from pack import*


def wordcloud3():
   
  wordcloudsql = 'SELECT antecedents, consequents FROM trends WHERE MONTH(date)=MONTH(NOW());'
  cursor.execute(wordcloudsql) 
  conn.commit()
  rv = cursor.fetchall()
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
  plt.savefig('static/bulanan.png')

from apscheduler.schedulers.blocking import BlockingScheduler
scheduler = BlockingScheduler()
scheduler.add_job(wordcloud3, 'interval', minutes=1)
scheduler.start()    
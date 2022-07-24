from pack import*

def wordcloud2():
   
  wordcloudsql = 'select antecedents, consequents from trends where date between date_sub(now(),INTERVAL 1 WEEK) and now();'
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
  plt.savefig('static/mingguan.png')

from apscheduler.schedulers.blocking import BlockingScheduler
scheduler = BlockingScheduler()
scheduler.add_job(wordcloud2, 'interval', minutes=1)
scheduler.start()  
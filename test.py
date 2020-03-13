#!/usr/bin/env python
# coding: utf-8

# In[8]:


def QueryMonolit(sql):
    
    import pymysql
    import pandas as pd
    db = pymysql.connect(
      user='develop', 
      passwd='ZW0rdypjKhfOxaA3eQ32',
      host="192.168.100.187",
      port=3307, 
      db='biglion', 
      charset='utf8' 
    )
    
    cur = db.cursor(pymysql.cursors.DictCursor)
  
    cur.execute(sql)
    return pd.DataFrame(cur.fetchall())



QueryMonolit('''
    SELECT count(PURCHASE_ID) FROM PURCHASE
    WHERE PURCHASE_ID>119449625
''')






#!/usr/bin/env python3
# -*- coding:utf-8 -*-
from google.cloud import bigquery
from mog_op import MongoOp
def execute_sql():
    client = bigquery.Client()
    query_job = client.query("""
SELECT b.id as tweet_id,
a.screen_name AS screen_name,
a.user_id AS user_id,
b.created_at AS created_at,
b.mfv AS max_fav,
b.mrt AS max_rt,
b.text AS text
FROM 
(SELECT id as user_id,screen_name
FROM twitter.temp_user
GROUP BY id,screen_name
) a
JOIN 
(select 
id,user_id,created_at,text,max(favorite_count) as mfv,
max(retweet_count) as mrt
from 
twitter.temp_retweeted_status
group by id,user_id,created_at,text
having mfv > 5000 or mrt > 5000
) b
ON a.user_id=b.user_id
""")
    return query_job.result()
def insert_mp(mp,results):
    rlist=[]
    for r in results:
        rlist.append(dict(
            tweet_id = r.tweet_id,
            screen_name = r.screen_name,
            user_id = r.user_id,
            created_at = r.created_at,
            max_fav = r.max_fav,
            max_rt = r.max_rt,
            text = r.text
        ))
    result  = mp.col.insert_many(rlist)
    print(result)
def main():
    mp = MongoOp('localhost')
    results = execute_sql()
    insert_mp(mp,results)
if __name__=='__main__':main()

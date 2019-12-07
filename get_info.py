#!/usr/bin/env python3
# -*- coding:utf-8 -*-
from google.cloud import bigquery
from mog_op import MongoOp
def execute_sql():
    client = bigquery.Client()
    query_job = client.query("""
select 
id AS tweet_id,
user_id,created_at,text,max(favorite_count) as max_fav,
max(retweet_count) as max_rt
from 
twitter.temp_retweeted_status
group by id,user_id,created_at,text
having max_fav > 5000 or max_rt > 5000
""")
    return query_job.result()
def insert_mp(mp,results):
    rlist=[]
    for i,r in enumerate(results):
        url = 'https://twitter.com/_/status/{}'.format(r.tweet_id)
        rlist.append(dict(
            tweet_id = r.tweet_id,
            user_id = r.user_id,
            created_at = r.created_at,
            max_fav = r.max_fav,
            max_rt = r.max_rt,
            text = r.text,
            url=url
        ))
        if i>0 and i%10000 == 0:
            if(rlist):
                result  = mp.col.insert_many(rlist)
                print('i={} result={}'.format(i,result))
                rlist=[]
    if(rlist):
        result  = mp.col.insert_many(rlist)
        print('i={} result={}'.format(i,result))
        rlist=[]

    
def main():
    mp = MongoOp('localhost')
    results = execute_sql()
    insert_mp(mp,results)
if __name__=='__main__':main()

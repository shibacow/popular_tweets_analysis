#!/usr/bin/env python3
# -*- coding:utf-8 -*-
from mog_op import MongoOp
import get_png
import logging
fmt = "%(asctime)s %(levelname)s %(name)s :%(message)s"
logging.basicConfig(level=logging.INFO,filename='fetch.log',format=fmt)
import pymongo
import time

def add_fpath():
    mp=MongoOp('localhost',)
    k='max_rt'
    cnt=mp.col.count({k:{'$gt':50_000}})
    ql=mp.col.find({k:{'$gt':50_000}}).sort([(k,pymongo.DESCENDING)])
    for i,a in enumerate(ql):
        url = a['url']
        (r,path) = get_png.check_path('static',url)
        up_elm={'$set':{'fpath':path}}
        if not r:
            up_elm={'$set':{'fpath':'NotFound'}}
        col_r = mp.col.update_one({'_id':a['_id']},up_elm)
        msg='k={} cnt={} i={} url={} path={} col_r={}'.format(k,cnt,i,url,path,col_r)
        logging.info(msg)
def get_img():
    mp=MongoOp('localhost',db='fav_tweet',col='hage')
    driver = get_png.factory()
    cond={'fpath':{'$exists':False}}
    cnt=mp.col.count(cond)
    k='created_at'
    ql=mp.col.find(cond).sort([(k,pymongo.DESCENDING)])
    #https://twitter.com/terrakei07/status/1211085215696732160
    ql=list(ql)
    for i,a in enumerate(ql):
        if 'user' in a and  'screen_name' in a['user']:
            screen_name=a['user']['screen_name']
        else:
            screen_name='_'
        tid=a['tweet_id']
        url='http://twitter.com/{}/status/{}'.format(screen_name,tid)
        if 'fpath' in a:continue
        (r,path) = get_png.check_path('static',url)
        if r:
            up_elm={'$set':{'fpath':path}}
            mp.col.update_one({'_id':a['_id']},up_elm)
            msg='file exists={}'.format(path)
            logging.info(msg)
            continue
        result = get_png.save_png(driver,url,'static',logging)
        msg='k={} cnt={} i={} url={} fpath={}'.format(k,cnt,i,url,result)
        logging.info(msg)
        up_elm={'$set':{'fpath':path}}
        if not result:
            up_elm={'$set':{'fpath':'NotFound'}}
        col_r = mp.col.update_one({'_id':a['_id']},up_elm)
        time.sleep(5)
    get_png.close(driver)

def main():
    #add_fpath()
    get_img()
if __name__=='__main__':main()

    

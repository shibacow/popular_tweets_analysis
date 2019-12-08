#!/usr/bin/env python3
# -*- coding:utf-8 -*-
from mog_op import MongoOp
import get_png
import logging
logging.basicConfig(level=logging.INFO)

def add_fpath():
    mp=MongoOp('localhost')
    k='max_rt'
    cnt=mp.col.count({k:{'$gt':50_000}})
    for i,a in enumerate(mp.col.find({k:{'$gt':50_000}})):
        url = a['url']
        (r,path) = get_png.check_path('static',url)
        up_elm={'$set':{'fpath':path}}
        if not r:
            up_elm={'$set':{'fpath':'NotFound'}}
        col_r = mp.col.update_one({'_id':a['_id']},up_elm)
        msg='k={} cnt={} i={} url={} path={} col_r={}'.format(k,cnt,i,url,path,col_r)
        logging.info(msg)
def get_img():
    mp=MongoOp('localhost')
    driver = get_png.factory()
    k='max_fav'
    cond={k:{'$gt':50_000},'fpath':{'$exists':False}}
    cnt=mp.col.count(cond)
    for i,a in enumerate(mp.col.find(cond)):
        url = a['url']
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
    get_png.close(driver)

def main():
    #add_fpath()
    get_img()
if __name__=='__main__':main()

    

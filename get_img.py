#!/usr/bin/env python3
# -*- coding:utf-8 -*-
from mog_op import MongoOp
import get_png
import logging
logging.basicConfig(level=logging.INFO)

def main():
    mp=MongoOp('localhost')
    driver = get_png.factory()
    for k in ('max_rt','max_fav'):
        cnt=mp.col.count({k:{'$gt':50_000}})
        for i,a in enumerate(mp.col.find({k:{'$gt':50_000}})):
            url = a['url']
            get_png.save_png(driver,url,'static',logging)
            msg='k={} cnt={} i={} url={}'.format(k,cnt,i,url)
            logging.info(msg)
    get_png.close(driver)
if __name__=='__main__':main()

    

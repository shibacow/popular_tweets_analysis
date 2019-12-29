#!/usr/bin/env python3
# -*- coding:utf-8 -*-
import pymongo
import re,os
from datetime import datetime
import logging
from dotenv import load_dotenv, find_dotenv
load_dotenv(find_dotenv())
MONGO_HOST=os.environ.get("MONGO_HOST")
MONGO_USER=os.environ.get("MONGO_USER")
PASSWORD=os.environ.get("PASSWORD")
AUTHSOURCE=os.environ.get("AUTHSOURCE")

class MongoOp(object):
    def __init__(self,host,db,col):
        self.con = pymongo.MongoClient(MONGO_HOST,
                                       27017,
                                       username=MONGO_USER,
                                       password=PASSWORD,
                                       authSource=AUTHSOURCE,
                                       authMechanism='SCRAM-SHA-1')
        
        self.db=self.con[db]
        self.col=self.db[col]
        for k in ('url','tweet_id','user_id','created_at'):
            self.col.create_index(k)
    def __del__(self):
        if self.con:
            self.con.close()
            self.con=None
    def close(self):
        if self.con:
            self.con.close()
            self.con=None

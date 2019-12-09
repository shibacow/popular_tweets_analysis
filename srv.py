#!/usr/bin/env python3
from flask import Flask,render_template,request,redirect, url_for,g
from flask_paginate import Pagination, get_page_parameter
from mog_op import MongoOp
from datetime import datetime
import pymongo

app = Flask(__name__)

@app.before_request
def before():
    g.mp = MongoOp('localhost')

@app.after_request
def after_request(response):
    if g.mp:
        g.mp.close()
    g.mp = None
    return response

class TW(object):
    def __init__(self,k,mp):
        self.k=k
        self.mp=mp
    def fetch(self,skip,limit):
        return self.mp.col.find({'fpath':{'$regex':'^static'}}).\
               sort([(self.k,pymongo.DESCENDING)]).skip(skip).limit(limit)
    def count(self):
        return self.mp.col.count({'fpath':{'$regex':'^static'}})
def conv_args(k):
    if request.args.get(k,None):
        mx_base=request.args.get(k)
        return int(mx_base)
    else:
        None

@app.route('/')
def index():
    page = request.args.get(get_page_parameter(), type=int, default=1)
    limit = int(request.args.get('limit',100))
    skip = (page-1) * limit
    app.logger.info(u'page={}'.format(page))
    mode = 'max_rt'
    mode_r = request.args.get('mode',None)
    if mode_r and mode_r == 'max_fav':
        mode = 'max_fav'
    app.logger.info('mode={}'.format(mode))
    popular_tweets = TW(mode,g.mp)
    dcnt = popular_tweets.count()
    pagination = Pagination(page=page, total=dcnt, per_page=limit,\
                            record_name='dbs',css_framework='bootstrap4')
    return render_template('index.html',\
                           mode=mode,popular_tweets=popular_tweets.fetch(skip,limit),pagination = pagination)

if __name__=='__main__':
    app.debug=True
    app.run(host='0.0.0.0',port=4997)



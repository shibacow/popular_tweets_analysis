#!/usr/bin/env python3
from flask import Flask,render_template,request,redirect, url_for,g
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
    return response

class TW(object):
    def __init__(self,k,mx,mn,mp):
        self.k=k
        self.mx=mx
        self.mn=mn
        self.mp=mp
    def fetch(self):
        return self.mp.col.find({self.k:{'$gt':self.mn,'$lte':self.mx}}).\
               sort([(self.k,pymongo.DESCENDING)])

@app.route('/')
def index():
    mx=250_000
    mn=230_000
    tfav = TW('max_fav',mx,mn,g.mp)
    trt = TW('max_rt',mx,mn,g.mp)
    return render_template('index.html',max_favs=tfav.fetch(),\
                           max_rts=trt.fetch())

if __name__=='__main__':
    app.debug=True
    app.run(host='0.0.0.0',port=4997)



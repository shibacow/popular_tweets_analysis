#!/usr/bin/env python3
# -*- coding:utf-8 -*-

from selenium import webdriver
import time
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import NoSuchElementException
import os
import logging

def factory():
    options = Options()
    options.add_argument('--headless')
    options.add_argument('--disable-gpu')
    options.add_argument('--no-sandbox')
    options.add_argument('--window-size=1440,2560')
    driver = webdriver.Chrome(executable_path="/usr/lib/chromium-browser/chromedriver", chrome_options=options);
    return driver

def check_path(base_path,url):
    bname=url.split('/')[-1][:4]
    tid=url.split('/')[-1]
    bname_path=base_path + os.sep + bname
    fpath = bname_path+os.sep+tid+'.png'
    if os.path.isfile(fpath):
        return True,fpath
    else:
        return False,fpath
    
def get_path(base_path,url):
    if not os.path.isdir(base_path):
        os.mkdir(base_path)
    bname=url.split('/')[-1][:4]
    tid=url.split('/')[-1]
    bname_path=base_path + os.sep + bname
    if not os.path.isdir(bname_path):
        os.mkdir(bname_path)
    return bname_path+os.sep+tid+'.png'

def save_png(driver,url,base_path,logging):
    driver.get(url)
    driver.implicitly_wait(3.0)
    try:
        png = driver.find_element_by_xpath('/html/body/div[30]/div[2]/div[3]/div/div/div[1]/div[1]')
        if png:
            fpath = get_path(base_path,url)
            png = png.screenshot_as_png
            with open(fpath, "wb") as f:
                f.write(png)
                logging.info(fpath)
            return fpath
        else:
            msg="error file not save={}".format(url)
            logging.error(msg)
            return None
    except NoSuchElementException as err:
        msg="error url is not css selector={}".format(url)
        logging.error(msg)
        return None
    #driver.save_screenshot('screenshot.png')
def close(driver):
    driver.close()

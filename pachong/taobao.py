# -*- coding: utf-8 -*-
"""
Created on Thu Jul 12 15:20:11 2018

@author: DELL
"""

from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from urllib.parse import quote
from pyquery import PyQuery as pq
from pymongo import MongoClient
import time
import random

browser = webdriver.Chrome()
wait = WebDriverWait(browser,10)
KEYWORD = 'iphone'

def index_page(page):
    """
    抓取索引页
    :param :页码
    """
    print('正在爬取第%d页' %page)
    try:
        url = 'https://s.taobao.com/search?q='+quote(KEYWORD)
        browser.get(url)
        if page >1:
            inputt = wait.until(
                    EC.presence_of_element_located((By.CSS_SELECTOR,
                                                    '#mainsrp-pager div.form > input')))
            submit = wait.until(
                    EC.element_to_be_clickable((By.CSS_SELECTOR,
                                                '#mainsrp-pager div.form > span.btn.J_Submit')))
            inputt.clear()
            inputt.send_keys(page)
            submit.click()
        wait.until(
                EC.text_to_be_present_in_element((By.CSS_SELECTOR,
                                                  '#mainsrp-pager li.item.active > span'),str(page)))
        wait.until(
                EC.presence_of_element_located((By.CSS_SELECTOR,
                                                '.m-itemlist .items .item')))
        get_products()
    except TimeoutException:
        index_page(page)

        
        
def get_products():
    '''
    提取商品信息
    '''
    html = browser.page_source
    doc = pq(html)
    items = doc('#mainsrp-itemlist .items .item').items()
    for item in items:
        product = {
                'image':item.find('.pic .img').attr('data-src'),
                'price':item.find('.price').text(),
                'deal':item.find('.deal-cnt').text(),
                'title':item.find('.title').text(),
                'shop':item.find('.shop').text(),
                'location':item.find('.location').text()
                }
        print(product)
        save_to_mongo(product)        
        
MONGO_URL = 'localhost'
MONGO_DB = 'taobao'
MONGO_COLLECTION = 'products'
client = MongoClient(MONGO_URL)
db = client[MONGO_DB]

def save_to_mongo(result):
    try:
        if db[MONGO_DB].insert_one(result):
            print('Save Successfully')
    except Exception:
        print('Save Faild')
       
MAX_PAGE = 10
def main():
    for i in range(1,MAX_PAGE+1):
        index_page(i)
        t = random.randint(0,3)
        time.sleep(t)

if __name__ == '__main__':
    main()      
    
######################################################
import csv
from pymongo import MongoClient

client = MongoClient()
db = client['taobao']
    
with open('taobao.csv','w',encoding='utf-8') as f:
    writer1 = csv.writer(f)
    fieldlist ={'id','image','price','deal','title','shop','location'}
    writer1.writerow(fieldlist)
    content = db.taobao.find()
    for record in content:
        recordvaluelst = []
        for field in fieldlist:
            if field not in record:
                recordvaluelst.append('None')
            else:
                recordvaluelst.append(record[field])
        try:
            writer1.writerow(recordvaluelst)
        except Exception as e:
            print(f"write csv exception.e = {e}")
    
    
    
    
    
    
    
    
    
    
    
    
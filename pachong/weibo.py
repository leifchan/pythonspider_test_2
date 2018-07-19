# -*- coding: utf-8 -*-
"""
Created on Wed Jun 27 20:15:40 2018

@author: DELL
"""

from urllib.parse import urlencode
import requests

base_url = 'https://m.weibo.cn/api/container/getIndex?'

headers = {
        'Referer':'https://m.weibo.cn/u/2830678474',
        'User-Agent':
            'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36',
        'X-Requested-With':'XMLHttpRequest'
        }
    
def get_page(page):
    params = {
            'type':'uid',
            'value':'2830678474',
            'containerid':'1076032830678474',
            'page':page
            }
    url = base_url + urlencode(params)
    try:
        response = requests.get(url,headers=headers)
        if response.status_code == 200:
            return response.json()
    except requests.ConnectionError as e:
        print('Error',e.args)
            
from pyquery import PyQuery as pq

def parse_page(json):
    if json:
        items = json.get('data').get('cards')
        for item in items:
            item = item.get('mblog')
            if item is None:
                continue
            else:
                weibo = {}
                weibo['id'] = item.get('id')
                weibo['text'] = pq(item.get('text')).text()
                weibo['attitudes'] = item.get('attitudes_count')
                weibo['comments'] = item.get('comments_count')
                weibo['reposts'] = item.get('reposts_count')
            yield weibo

from pymongo import MongoClient

client = MongoClient()
db = client['weibo']
collection = db['weibo']

def save_to_mongo(result):
    if collection.insert_one(result):
        print('Saved to Mongo')
            
if __name__ == '__main__':
    for page in range(1,11):
        json = get_page(page)
        results = parse_page(json)
        for result in results:
            save_to_mongo(result)
            print(result)

    
        

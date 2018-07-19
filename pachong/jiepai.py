# -*- coding: utf-8 -*-
"""
Created on Wed Jul 11 14:21:42 2018

@author: DELL
"""

import requests
from urllib.parse import urlencode
import os
from hashlib import md5
from multiprocessing.pool import Pool

headers = {
        "user-agent":
            'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36',
        'authority':'www.toutiao.com',
        'referer':'https://www.toutiao.com/search/?keyword=%E8%A1%97%E6%8B%8D',
        'x-requested-with':'XMLHttpRequest'
        }

def get_page(offset):
    params = {
            'offset':offset,
            'format':'json',
            'keyword':'街拍',
            'autoload':'true',
            'count':'20',
            'cur_tab':'1',
            'from':'search_tab'
            }
    url = 'https://www.toutiao.com/search_content/?' + urlencode(params)
    try:
        response = requests.get(url,headers=headers)
        if response.status_code == 200:
            return response.json()
    except requests.ConnectionError as er:
        return None

def get_image(json):
    if json.get('data'):        
        for item in json.get('data'):
            title = item.get('title')
            images = item.get('image_list')
            if images is None:
                continue
            for image in images:
                yield{
                        'image':image.get('url'),
                        'title':title}
                
def save_image(item):
    if not os.path.exists(item.get('title')):
        os.mkdir(item.get('title'))
    try:
        local_image_url = item.get('image')    # item.get('image')得到的是没有http前缀的字符串
        new_image_url = local_image_url.replace('list','large')
        response = requests.get('http:'+new_image_url) #发送请求浏览图片
        if response.status_code == 200:
            file_path = '{0}/{1}.{2}' .format(item.get('title'),
                         md5(response.content).hexdigest(),'jpg')
            if not os.path.exists(file_path):
                with open(file_path,'wb') as file:         #wb,写入二进制格式
                    file.write(response.content)
            else:
                print('Already Download',file_path)
    except requests.ConnectionError :
        print('Faild to save Image')
        
def main(offset):
    json = get_page(offset)
    items = get_image(json)
    for item in items:
        print(item)
        save_image(item)

GROUP_START = 0
GROUP_END = 20

if __name__ == '__main__':
    pool= Pool()
    groups = [x*20 for x in range(GROUP_START,GROUP_END)]
    pool.map(main,groups)
    pool.close()
    pool.join()
    
        



            
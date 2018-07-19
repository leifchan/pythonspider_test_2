# -*- coding: utf-8 -*-
"""
Created on Thu Jul  5 17:01:16 2018

@author: DELL
"""

import requests
import re
import json
from requests.exceptions import RequestException
import time

#读取网页
def get_one_page(url):   
    try:
        headers = {
            'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36',
            'Host':'maoyan.com'}
        response = requests.get(url,headers=headers)
        if response.status_code == 200:
            return response.text
        return None
    except RequestException:
        return None
#解析网页
def parse_on_page(html):
    pattern = re.compile(
            '<dd>.*?board-index.*?>(.*?)</i>.*?data-src="(.*?)".*?<a.*'+
            '?data-val.*?>(.*?)</a>.*?star.*?>(.*?)</p>.*?releasetime.'+
            '*?>(.*?)</p>.*?integer.*?>(.*?)</i>.*?fraction.*?>(.*?)</i>',
            re.S
            )
    items = re.findall(pattern,html)
    for item in items:
        yield{
                'index':item[0],
                'image':item[1],
                'title':item[2],
                'actor':item[3].strip()[3:] if len(item[3]) >3 else '',
                'time':item[4].strip()[5:] if len(item[4]) > 3 else '',
                'score':item[5].strip()+item[6].strip()
                }
 #写入文件   
def write_to_file(content):
    with open('result.txt','a',encoding='utf-8') as f:
        print(type(json.dumps(content)))
        f.write(json.dumps(content,ensure_ascii=False)+'\n')
#主函数
def main(offset):
    url = 'https://maoyan.com/board/4?offset='+str(offset)
    html = get_one_page(url)
    items = parse_on_page(html)
    for item in items:
        print(item)
        write_to_file(item)

#运行
if __name__ == '__main__':
    for i in range(10):
        main(i*10)
        time.sleep(2.55)
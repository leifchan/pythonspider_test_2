# -*- coding: utf-8 -*-
"""
Created on Mon Jul 16 11:27:07 2018

@author: DELL
"""

import os
import sys
import requests
from bs4 import BeautifulSoup

Proxy_POOL_URL = 'http://localhost:5000/random'

def get_proxy():
    try:
        response = requests.get(Proxy_POOL_URL)
        if response.status_code == 200:
            return response.text
    except ConnectionError:
        return None
    
proxy = get_proxy()
proxies = {
        'http':'http://'+proxy,
        'https':'https://'+proxy
        }

try:
    response = requests.get('http://httpbin.org/get',proxies=proxies)
    print(response.text)
except requests.exceptions.ConnectionError as e:
    print('Error',e.args)
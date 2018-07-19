# -*- coding: utf-8 -*-
"""
Created on Mon Jul 16 19:41:52 2018

@author: DELL
"""


#Redis数据库地址
REDIS_HOST = '127.0.0.1'
#Redis数据库端口
REDIS_PORT = 6379
# Redis密码，如无填None
REDIS_PASSWORD = None
REDIS_KEY = 'proxies'

# 代理分数
MAX_SCORE = 100
MIN_SCORE = 0
INIT_SCORE = 10

#响应码
VALID_STATUS_CODES = [200,302]

# 最大批测试量
BATCH_TEST_SIZE = 30

#测试API
TEST_URL = 'http://weixin.sogou.com'

# 代理池数量界限
POOL_UPPER_THRESHOLD = 50000

# API配置
API_HOST = '0.0.0.0'
API_PORT = 5000

#检查、获取周期
TESTER_CYCLE = 10
GETTER_CYCLE = 20

#开关
TESTER_ENABLE = True
GETTER_ENABLE = True
API_ENABLE = True   


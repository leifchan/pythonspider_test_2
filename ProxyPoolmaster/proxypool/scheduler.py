# -*- coding: utf-8 -*-
"""
Created on Mon Jul 16 20:45:19 2018

@author: DELL
"""

#TESTER_CYCLE = 20
#GETTER_CYCLE = 20
#TESTER_ENABLE = True
#GETTER_ENABLE = True
#API_ENABLE = True

from multiprocessing import Process
from proxypool.api import app
from proxypool.getter import Getter
from proxypool.tester import Tester
from proxypool.setting import TEST_URL,TESTER_CYCLE,TESTER_ENABLE
from proxypool.setting import GETTER_CYCLE,GETTER_ENABLE,API_ENABLE,API_HOST,API_PORT
import time

class Scheduler():
    def scheduler_tester(self,cycle=TESTER_CYCLE):
        '''
        定时测试代理
        '''
        tester = Tester()
        while True:
            print('测试开始运行')
            tester.run()
            time.sleep(cycle)
    
    def scheduler_getter(self,cycle=GETTER_CYCLE):
        '''
        定时获取代理
        '''
        getter = Getter()
        while True:
            print('开始抓取代理')
            getter.run()
            time.sleep(cycle)
    
    def scheduler_api(self):
        '''
        开启API
        '''
        app.run(API_HOST,API_PORT)
    
    def run(self):
        print('代理池开始运行')
        if TESTER_ENABLE:
            tester_process = Process(target=self.scheduler_tester)
            tester_process.start()
        if GETTER_ENABLE:
            getter_process = Process(target=self.scheduler_getter)
            getter_process.start()
        if API_ENABLE:
            api_process = Process(target=self.scheduler_api)
            api_process.start()
            
            



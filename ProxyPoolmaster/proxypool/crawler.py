# -*- coding: utf-8 -*-
"""
Created on Mon Jul 16 13:15:30 2018

@author: DELL
"""
import re
import json
from proxypool.utils import get_page
from pyquery import PyQuery as pq

class ProxyMetaclass(type):
    def __new__(cls,name,bases,attrs):
        count = 0
        attrs['__CrawlFunc__'] = []
        for k,v in attrs.items():
            if 'crawl_' in k:
                attrs['__CrawlFunc__'].append(k)
                count +=1
        attrs['__CrawlFuncCount__'] = count
        return type.__new__(cls,name,bases,attrs)

class Crawler(object,metaclass=ProxyMetaclass):
    def get_proxies(self,callback):
        proxies = []
        for proxy in eval('self.{}()'.format(callback)):
            print('成功抓取代理',proxy)
            proxies.append(proxy)
        return proxies
    
    def crawl_daili66(self,page_count=6):
        '''
        获取代理66
        param page_count：页码
        return：代理
        '''
        start_url = 'http://www.66ip.cn/{}.html'
        urls = [start_url.format(page) for page in range(1,page_count+1)]
        for url in urls:
            print('Crawlering',url)
            html = get_page(url)
            if html:
                doc = pq(html)
                trs = doc('.containerbox table tr:gt(0)').items()
                for tr in trs:
                    ip = tr.find('td:nth-child(1)').text()
                    port = tr.find('td:nth-child(2)').text()
                    yield ':'.join([ip,port])
    
    def crawl_xici(self,page_count=10):
        '''
        获取西刺代理
        param page_count：页码
        return：代理
        '''
        start_url = 'http://www.xicidaili.com/nn/{}'
        urls = [start_url.format(page) for page in range(1,page_count+1)]
        for url in urls:
            print('Crawlering',url)
            html = get_page(url)
            if html:
                doc = pq(html)
                trs = doc('#ip_list tr:gt(0)').items()
                for tr in trs:
                    ip = tr.find('td:nth-child(2)').text()
                    port=tr.find('td:nth-child(3)').text()
                    yield ':'.join([ip,port])
    
    def crawl_kuaidaili(self,page_count=10):
        '''
        获取快代理
        param page_count：页码
        return：代理
        '''
        start_url = 'https://www.kuaidaili.com/free/inha/{}'
        urls = [start_url.format(page) for page in range(1,page_count)]
        for url in urls:
            print('Crawlering',url)
            html = get_page(url)
            if html:
                doc = pq(html)
                trs = doc('#list table tbody tr').items()
                for tr in trs:
                    ip = tr.find('td:nth-child(1)').text()
                    port = tr.find('td:nth-child(2)').text()
                    yield ":".join([ip,port])
    def crawl_yqie(self):
        start_url = 'http://ip.yqie.com/ipproxy.htm'
        html = get_page(start_url)
        ip_address = re.compile('<tr.*?>\s*<td>(.*?)</td>\s*<td>(.*?)</td>',re.S)
        # \s* 匹配空格，起到换行作用
        re_ip_address = ip_address.findall(html)
        for address,port in re_ip_address:
            result = address + ':' + port
            yield result.replace(' ', '')
       
    def crawl_89ip(self):
        for i in range(1,10):
            start_url = 'http://www.89ip.cn/index_{}.html'.format(i)
            html = get_page(start_url)
            if html:
                ip_address = re.compile('<tr.*?>\s*<td>(.*?)</td>\s*<td>(.*?)</td>',re.S)
                # \s* 匹配空格，起到换行作用
                re_ip_address = ip_address.findall(html)
                for address,port in re_ip_address:
                    result = address.strip() + ':' + port.strip()
                    yield result 
                    
#    def crawl_ip3366(self):
#        for page in range(1, 4):
#            start_url = 'http://www.ip3366.net/free/?stype=1&page={}'.format(page)
#            html = get_page(start_url)
#            ip_address = re.compile('<tr>\s*<td>(.*?)</td>\s*<td>(.*?)</td>',re.S)
            # \s * 匹配空格，起到换行作用
#            re_ip_address = ip_address.findall(html)
#            for address, port in re_ip_address:
#                result = address+':'+ port
#                yield result.replace(' ', '')          
    
    def crawl_iphai(self):
        start_url = 'http://www.iphai.com/'
        html = get_page(start_url)
        if html:
            find_tr = re.compile('<tr>(.*?)</tr>', re.S)
            trs = find_tr.findall(html)
            for s in range(1, len(trs)):
                find_ip = re.compile('<td>\s+(\d+\.\d+\.\d+\.\d+)\s+</td>', re.S)
                re_ip_address = find_ip.findall(trs[s])
                find_port = re.compile('<td>\s+(\d+)\s+</td>', re.S)
                re_port = find_port.findall(trs[s])
                for address,port in zip(re_ip_address, re_port):
                    address_port = address+':'+port
                    yield address_port.replace(' ','')

#    def crawl_89ip(self):
#        start_url = 'http://www.89ip.cn/apijk/?&tqsl=1000&sxa=&sxb=&tta=&ports=&ktip=&cf=1'
#        html = get_page(start_url)
#        if html:
#            find_ips = re.compile('(\d+\.\d+\.\d+\.\d+:\d+)', re.S)
#            ip_ports = find_ips.findall(html)
#           for address_port in ip_ports:
#               yield address_port

    def crawl_data5u(self):
        start_url = 'http://www.data5u.com/free/gngn/index.shtml'
        headers = {
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
            'Accept-Encoding': 'gzip, deflate',
            'Accept-Language': 'en-US,en;q=0.9,zh-CN;q=0.8,zh;q=0.7',
            'Cache-Control': 'max-age=0',
            'Connection': 'keep-alive',
            'Cookie': 'JSESSIONID=47AA0C887112A2D83EE040405F837A86',
            'Host': 'www.data5u.com',
            'Referer': 'http://www.data5u.com/free/index.shtml',
            'Upgrade-Insecure-Requests': '1',
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.108 Safari/537.36',
        }
        html = get_page(start_url, options=headers)
        if html:
            ip_address = re.compile('<span><li>(\d+\.\d+\.\d+\.\d+)</li>.*?<li class=\"port.*?>(\d+)</li>', re.S)
            re_ip_address = ip_address.findall(html)
            for address, port in re_ip_address:
                result = address + ':' + port
                yield result.replace(' ', '')
    
    def crawl_premproxy(self):
        for i in ['China-01','China-02','China-03','China-04','Taiwan-01']:
            start_url = 'https://premproxy.com/proxy-by-country/{}.htm'.format(i)
            html = get_page(start_url)
            if html:
                ip_address = re.compile('<td data-label="IP:port ">(.*?)</td>',re.S) 
                re_ip_address = ip_address.findall(html)
                for address_port in re_ip_address:
                    yield address_port.replace(' ','')

    def crawl_xroxy(self):
        for i in ['CN','TW']:
            start_url = 'http://www.xroxy.com/proxylist.php?country={}'.format(i)
            html = get_page(start_url)
            if html:
                ip_address1 = re.compile("title='View this Proxy details'>\s*(.*).*")
                re_ip_address1 = ip_address1.findall(html)
                ip_address2 = re.compile("title='Select proxies with port number .*'>(.*)</a>") 
                re_ip_address2 = ip_address2.findall(html)
                for address,port in zip(re_ip_address1,re_ip_address2):
                    address_port = address+':'+port
                    yield address_port.replace(' ','')
                    
    def crawl_ip181(self):
        start_url = 'http://www.ip181.com/'
        html = get_page(start_url)
        ip_address = re.compile('<tr.*?>\s*<td>(.*?)</td>\s*<td>(.*?)</td>',re.S)
        # \s* 匹配空格，起到换行作用
        re_ip_address = ip_address.findall(html)
        for address,port in re_ip_address:
            result = address + ':' + port
            yield result.replace(' ', '')
                
    def crawl_ipjai(self):
        url = 'http://www.iphai.com/free/ng'
        html = get_page(url)
        ip_address = re.compile('<tr>\s*<td>(.*?)</td>\s*<td>(.?*)</td>',re.S)
        re_ip_address = ip_address.findall(html)
        for address,port in re_ip_address:
            result = address + ':' + port
            yield result.replace(' ','')
            
  
            
            




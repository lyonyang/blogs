#!/usr/bin/env python
# -*- coding:utf-8 -*-
# Author：Lyon
from multiprocessing import Pool
import requests
import re
def get_page(url, pattern):
    response = requests.get(url)
    if response.status_code == 200:
        print(response.text)
        return (response.text,pattern)

def parse_page(info):
    page_content,pattern = info
    res=re.findall(pattern, page_content)
    for item in res:
        dic={
            'index':item[0],
            'title':item[1],
            'actor':item[2].strip()[3:],
            'time':item[3][5:],
            'score':item[4]+item[5]
        }
        print(dic)

if __name__ == '__main__':
    pattern1=re.compile(r'<dd>.*?board-index.*?>(\d+)<.*?title="(.*?)".*?star.*?>(.*?)<.*?releasetime.*?>(.*?)<.*?integer.*?>(.*?)<.*?fraction.*?>(.*?)<',re.S)
    url_dic={
        'http://maoyan.com/board/7': pattern1,
    }
    p=Pool()
    res_l=[]
    for url,pattern in url_dic.items():
        res = p.apply_async(get_page,args=(url,pattern),callback=parse_page)
        res_l.append(res)
    for i in res_l:
        i.get()
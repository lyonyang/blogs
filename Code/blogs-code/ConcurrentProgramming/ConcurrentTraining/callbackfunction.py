#!/usr/bin/env python
# -*- coding:utf-8 -*-
# Author：Lyon
import multiprocessing
import requests
import os
def get_page(url):
    print('Process %s get %s...' % (os.getpid(), url))
    respone = requests.get(url)
    if respone.status_code == 200:
        return {'url': url, 'text': respone.text}

# 进行回调的函数
def pasrse_page(res):
    print('Process %s parse %s...' % (os.getpid(), res['url']))
    parse_res = 'url : %s\nsize : %s\n' % (res['url'], len(res['text']))
    with open('db.txt', 'a') as f:
        f.write(parse_res)

if __name__ == '__main__':
    urls = [
        'https://www.baidu.com',
        'https://www.python.org',
        'https://www.openstack.org',
        'https://help.github.com/',
        'http://www.sina.com.cn/'
    ]
    p = multiprocessing.Pool(3)
    res_list = []
    for url in urls:
        res = p.apply_async(get_page, args=(url,), callback=pasrse_page)
        res_list.append(res)
    p.close()
    p.join()
    # 拿到的是get_page的结果,其实完全没必要拿该结果,该结果已经传给回调函数处理了
    print([res.get() for res in res_list])
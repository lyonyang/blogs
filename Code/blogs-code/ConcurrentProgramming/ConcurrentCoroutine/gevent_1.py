#!/usr/bin/env python
# -*- coding:utf-8 -*-
# Author：Lyon
from gevent import monkey
monkey.patch_all()
import gevent
import requests
import time

def get_page(url):
    print('GET: %s' % url)
    response = requests.get(url)
    if response.status_code == 200:
        print('%d bytes received from %s' % (len(response.text), url))
start_time = time.time()
gevent.joinall([
    gevent.spawn(get_page, 'https://www.python.org/'),
    gevent.spawn(get_page, 'https://www.yahoo.com/'),
])
end_time = time.time()
print('run time is %s' % (end_time - start_time))

# Python之路 - 多进程实例及回调函数

## 进程池实例  🍀

**使用进程池维护固定数目的进程** 

server.py

```python
import socket
import os
import multiprocessing
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server.bind(('127.0.0.1', 8080))
server.listen(5)
def talk(conn, client_addr):
    print("Process pid : %s" % os.getpid())
    while True:
        try:
            msg = conn.recv(1024)
            if not msg:break
            conn.send(msg.upper())
        except Exception:
            break
if __name__ == '__main__':
    pool = multiprocessing.Pool()
    while True:
        conn, client_addr = server.accept()
        # 同步则一时间只有一个客户端能访问,所以使用异步
        pool.apply_async(talk,args=(conn, client_addr,))
```

client.py

```python
import socket
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(('127.0.0.1', 8080))
while True:
    msg = input("Please input message:").strip()
    if not msg: continue
    client.send(msg.encode('utf-8'))
    data = client.recv(1024)
    print(data.decode('utf-8'))
```

## 回调函数  🍀

回调函数就是一个通过函数指针调用的函数 , 如果你把函数的指针(地址)作为参数传递给另一个函数 , 当这个指针被用来调用其所指向的函数时 , 我们就说这是回调函数 

回调函数不是由该函数的实现方直接调用 , 而是在特定的事件或条件发生时由另外的一方调用的 , 用于对该事件或条件进程响应

进程池中使用回调函数

`apply_async`(*func*[, *args*[, *kwds*[, *callback*[, *error_callback*]]]])

```python
If callback is specified then it should be a callable which accepts a single argument. When the result becomes ready callback is applied to it, that is unless the call failed, in which case the error_callback is applied instead.
'''
意思是如果指定了回调,那么它应该是可调用的,调用失败则会应用error_callback
'''
```

实例

```python
import multiprocessing
import requests
import os
def get_page(url):
    print('Process %s get %s...' % (os.getpid(), url))
    respone = requests.get(url)
    if respone.status_code == 200:
        return {'url': url, 'text': respone.text}
# 进行回调的函数,处理结果
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
        # 执行并返回结果,异步,
        res = p.apply_async(get_page, args=(url,), callback=pasrse_page)
        res_list.append(res)
    p.close()
    p.join()
    # 拿到的是get_page的结果,其实完全没必要拿该结果,该结果已经传给回调函数处理了
    print([res.get() for res in res_list]) 
```

处理结果db.txt

```txt
url : https://www.openstack.org
size : 60191
url : https://www.python.org
size : 49081
url : https://www.baidu.com
size : 2443
url : https://help.github.com/
size : 118622
url : http://www.sina.com.cn/
size : 601426
```

爬虫案例

```python
from multiprocessing import Pool
import requests
import re
def get_page(url, pattern):
    response = requests.get(url)
    if response.status_code == 200:
        print(response.text)
        return (response.text,pattern)
def parse_page(info):
    page_content, pattern = info
    res=re.findall(pattern, page_content)
    for item in res:
        dic={
            'index' : item[0],
            'title' : item[1],
            'actor' : item[2].strip()[3:],
            'time' : item[3][5:],
            'score' : item[4]+item[5]
        }
        print(dic)
if __name__ == '__main__':
    pattern1=re.compile(r'<dd>.*?board-index.*?>(\d+)<.*?title="(.*?)".*?star.*?>(.*?)<.*?releasetime.*?>(.*?)<.*?integer.*?>(.*?)<.*?fraction.*?>(.*?)<',re.S)
    url_dic={
        'http://maoyan.com/board/7' : pattern1,
    }
    p=Pool()
    res_l=[]
    for url,pattern in url_dic.items():
        res = p.apply_async(get_page, args=(url, pattern), callback=parse_page)
        res_l.append(res)
    for i in res_l:
        i.get()
 '''
 不是每次抓取都能成功
 '''
```
# Welcome to Lyon's blog!

[![Build Status](https://travis-ci.org/lyonyang/blogs.svg?branch=master)](https://travis-ci.org/lyonyang/blogs)
[![Python Versions](https://img.shields.io/badge/python-2.x%2C%203.x-blue.svg)](https://www.python.org/)
[![License](https://img.shields.io/badge/license-Apache%202.0-blue.svg)](https://github.com/lyonyang/blogs/blob/master/LICENSE)
[![Downloads](https://img.shields.io/badge/downloads-4.02MB-blue.svg)](https://codeload.github.com/lyonyang/blogs/zip/master)


## 关于作者

> @Email : [lyon.yang@qq.com](http://wpa.qq.com/msgrd?v=3&uin=547903993&site=qq&menu=yes)

> @GitHub : [https://github.com/lyonyang](https://github.com/lyonyang)

> @QQ : [547903993](http://mail.qq.com/cgi-bin/qm_share?t=qm_mailme&email=WTUgNjd3IDg3PhkoKHc6NjQ)

> @微博 : 年纪大了,欣赏不了微博的世界

### 友情链接

https://notes.yangjinjie.xyz/zh_CN/latest/

***

## 博客说明

欢迎收藏交流 , 如需转载 , 请注明出处 : [`https://lyonyang.github.io/blogs`](https://lyonyang.gitbooks.io/blog/)

文章使用`Markdown`格式编写 , 托管于Github , 主要使用工具 : 

- [GitBook](https://www.gitbook.com/) , 构建本书
- [Travis-CI](https://www.travis-ci.org/) , 持续构建
- [Typora](https://www.typora.io/) , 编写MarkDown

文档目录 : 

```tree
.
├── Python           
├── MySQL          
├── WebD        
├── Web-Framework
│   ├── Django
│   └── Flask
├── Django-Rest-Framework
├── Vue
├── DesignPattern   
├── Algorithms     
├── Git             
└── Othres     
```

如果你也想和我一样 , 搭建一个这样的博客 , 点这里 : [如何利用GitHub Pages搭建个人博客](https://lyonyang.github.io/blogs/09-Git/%E5%A6%82%E4%BD%95%E5%88%A9%E7%94%A8GitHub%20Pages%E6%90%AD%E5%BB%BA%E4%B8%AA%E4%BA%BA%E5%8D%9A%E5%AE%A2.html)

## 阅读说明

查看目录: [SUMMARY](SUMMARY.md)

**网页浏览**

[`GitHub Pages方式展示(强烈推荐)`](https://lyonyang.github.io/blogs/)

[`GitBook方式展示(速度慢,不推荐)`](https://lyonyang.gitbooks.io/blog/)

**本地浏览**

可以使用 `GitBook` 本地浏览 , 具体步骤如下 : 

1. 克隆主分支
2. 执行项目根目录下的目录生成脚本 `summary_create.sh` 
3. 执行 `gitbook install` 安装插件
4. 执行 `gitbook serve .` 启动服务
5. 使用浏览器访问 `http://localhost:4000` 

使用 `git bash` 命令行 : 

```shell
$ git clone --depth=1 https://github.com/lyonyang/Blogs.git

$ bash summary_create.sh

$ gitbook install

# 由于文件数量较多,启动大概需要100秒
# 出现如下信息表示启动成功
#     Starting server ...
#     Serving book on http://localhost:4000
$ gitbook serve .
```



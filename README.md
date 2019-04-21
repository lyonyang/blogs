# Welcome to Lyon's blog!  🍀

[![Build Status](https://travis-ci.org/lyonyang/blogs.svg?branch=master)](https://travis-ci.org/lyonyang/blogs)
[![Author](https://img.shields.io/badge/Author-Lyon-orange.svg)]()
[![Python Versions](https://img.shields.io/badge/python-2.x%2C%203.x-blue.svg)](https://www.python.org/)
[![License](https://img.shields.io/badge/license-Apache%202.0-blue.svg)](https://github.com/lyonyang/blogs/blob/master/LICENSE)
[![Downloads](https://img.shields.io/badge/downloads-4.46MB-blue.svg)](https://codeload.github.com/lyonyang/blogs/zip/master)

由于博文技术层次较低,完整度不高,本博客将在后期断断续续重构~

## 关于作者  🍀

> Email : [lyon.yang@qq.com](http://mail.qq.com/cgi-bin/qm_share?t=qm_mailme&email=WTUgNjd3IDg3PhkoKHc6NjQ)

> GitHub : [https://github.com/lyonyang](https://github.com/lyonyang)

> QQ : [547903993](http://wpa.qq.com/msgrd?v=3&uin=547903993&site=qq&menu=yes)

> 微信 : [Happy547903993]()

> 技术交流群 : [590092348](https://jq.qq.com/?_wv=1027&k=52VgMo7)

> 微博 : [年纪大了, 欣赏不了微博的世界]()

### 友情链接  🍀

[yangjinjie](https://notes.yangjinjie.xyz)

[Litter Rookie](https://www.cnblogs.com/52-qq/)

[Derek](https://www.cnblogs.com/derek1184405959/)

***

## 博客说明  🍀

**欢迎收藏交流 , 欢迎[Issues](https://github.com/lyonyang/blogs/issues) ! 如需转载 , 请注明出处 : [`https://lyonyang.github.io/blogs`](https://lyonyang.github.io/blogs)**

> 如果本博客对你有帮助,请顺手点个🍀[star](https://github.com/lyonyang/blogs)🍀吧!

文章使用`Markdown`格式编写 , 托管于Github , 主要使用工具 : 

- [GitBook](https://www.gitbook.com/) , 构建本书
- [Travis-CI](https://www.travis-ci.org/) , 持续构建
- [Typora](https://www.typora.io/) , 编写MarkDown

文档目录 : 

```tree
.
├── Python   
├── Go
├── MySQL          
├── Front-End   
│   └── Vue 
├── Web-Framework
│   ├── Django
│   ├── Django-Rest-Framework
│   └── Flask
├── Redis
├── DesignPattern   
├── Algorithms     
├── Linux
│   └── Git
├── Others
└── Read
```

如果你也想和我一样 , 搭建一个这样的博客 , 点这里 : [GitHub Pages&Gitbook&Travis CI持续构建博客](https://lyonyang.github.io/blogs/09-Linux/Git/GitHub%20Pages&Gitbook&Travis%20CI%E6%8C%81%E7%BB%AD%E6%9E%84%E5%BB%BA%E5%8D%9A%E5%AE%A2.html)

## 阅读说明  🍀

查看目录: [SUMMARY](SUMMARY.md)

### 网页阅读  🍀

[`GitHub Pages方式展示(强烈推荐)`](https://lyonyang.github.io/blogs/)

[`GitBook方式展示(速度慢,不推荐)`](https://lyonyang.gitbooks.io/blog/)

### 本地阅读  🍀

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



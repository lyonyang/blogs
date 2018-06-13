# Web框架介绍

## 主流Web框架  🍀

### Django  🍀

Django 是当前 Python 世界中最负盛名且最成熟的网络框架 , 最初用来制作在线新闻的 Web 站点 , 目前已经发展为应用最广泛的 Python 网络框架

Django 的各模块之间结合得比较紧密 , 所以在功能强大的同时又是一个相对封闭的系统 , 但是它提供了非常齐备的官方文档 , 提供了译站式的解决方案 , 其中包含缓存 , ORM , 管理后台 , 验证 , 表单处理等 ,  使得开发复杂的数据库驱动的网站变得很简单 ; 当然也因为系统耦合度太高 , 替换掉内置的功能往往需要花费一些功夫 , 所以学习曲线也相当陡峭

### Flask  🍀

Flask 是一个轻量级 Web 应用框架 , 它基于 Werkzeug 实现的 WSGI 和 Jinjia2 模板引擎 

Flask 的作者是 Armin Ronacher , 本来这只是作者愚人节开的一个玩笑 , 但是开源之后却受到 Python 程序员的喜爱 , 目前在 GitHub 上的 Star 数量已经超过了 Django . 设计上 , 它只保留核心 , 通过扩展机制来增加其他功能 , Flask 用到的依赖都是 Pocoo 团队开发的 , Pocoo 团队其他的项目还有 Pygments , Sphinx , 以及 lodgeit . Flask 的扩展环境非常繁荣 , 基本上 Web 应用的每个环节都有对应的扩展供选择 , 就算没有对应的扩展也能很方便的自己实现一个

### Pyramid  🍀

Pyramid  在国内知名度并不高 , 主要原因是中文文档匮乏 , 其高级用法需要通过阅读源代码获取灵感 , 尽管被 Django 和 Flask 的光芒遮蔽 , 但是它的性能要比 Flask 高 . Pyramid 的灵感来源于 Zope , Pylons 1.0 和 Django . Pyramid 在努力朝着胜任不同级别应用的框架的方向在走 , 虽然它默认使用 Chameleon 和 Mako 模块 , 但很容易切换成 Jinja2 , 甚至可以让多种模板引擎共存 , 通过文件后缀名来识别 

豆瓣赞赏和豆瓣钱包等产品就是基于此框架实现的 , 代码量级和 Flask 相同 , 性能比 Flask 要略高

### Bottle  🍀

Bottle 也是一个轻量级的 Web 框架 , 它的特点是单文件 , 代码只使用了 Python 标准库 , 而不需要额外依赖其他的第三方库 , 它更符合微框架的定义 , 截止到今天只有 4100 多行的代码

### Tornado  🍀

Tornado 全称 Tornado Web Server , 最初是由 FriendFeed 开发的非阻塞式 Web 服务器 , 现在我们看到的是被 Fackbook 收购后开源出来的版本 , 它和其他主流框架有个明显的区别 : 它是非阻塞式服务器 , 而且速度相当快 , 得益于其非阻塞的方式和对 epoll 的运用 , Tornado 每秒可以处理数以千计的连接 , 这意味着对于长轮询 , WebSocket 等实时 Web 服务来说 , Tornado 是一个理想的 Web 框架

### Web.py  🍀

Web.py 也是一个微框架 , 由 Reddit 联合创始人 , RSS 规格合作创造者 , 著名计算机黑客 Aaron Swartz 开发 , Web.py 使用基于类的视图 , 简单易学却功能强大

### Twisted  🍀

Twisted 是一个有着十多年历史的开源事件驱动框架 , 它适用于从传输层到自定义应用协议的所有类型的网络程序的开发 , 而不着眼于网络 HTTP 应用开发 , 并且它能在不同的操作系统上提供很高的运行效率

## 小众的Web框架  🍀

### Quixote  🍀

Quixote 是由美国全国研究创新联合会的工程师 A.M.Kuchling , Neil Schemenauer 和 Greg Ward 开发的一个轻量级 Web 框架 , 它简单 , 高校 , 代码简洁 , 豆瓣的大部分用户产品都使用定制版的 Quixote 作为 Web 框架

它使用目录式的 URL 分发规则 , 用 Python 来写模板 , PTL 模板更适合程序员 , 但是并不适合美工参与前端代码的编写和修改 , 豆瓣在开发中使用了 Mako 替代 PTL ; 不建议在生产环境中选用 Quixote

### Klein  🍀

Klein 是 Twisted 组织开源出来的基于 werkzeug 和 twisted.web 的为框架 , Flask 很不错 , 但是不能使用异步非阻塞的方式编程 , 根本原因是它和 Django , Pyramid 一样 , 都基于 WSGI , 而WSGI 的接口是同步阻塞的 , Klein 用法非常像 Flask , 却可以使用异步的方式开发 Web 应用

## 选择 Web 框架时应遵循的原则  🍀

1. 选择更主流的 Web 框架 , 因为他们文档齐全 , 技术积累更多 , 社区更繁盛 , 能得到更好的支持
2. 关注框架的活跃情况 , 如果一个框架长时间没有更新 , 或者有一堆的问题需要解决但是没有得到回应 , 就不应该将这样的框架放在生产环境中
3. 确认框架是否足够满足需求 , 没有最好的框架 , 只有最合适的框架

# Python之路 - Python介绍

## 什么是Python  🍀

Python的创始人是Guido van Rossum , 因为他是一个叫Monty Python的喜剧团体的爱好者 , 所以该语言就命名Python了

Python是一种强类型、解释型、动态类型的脚本语言

强类型 : 一旦一个变量被指定了某个数据类型 , 如果不经过强制转换 , 那么它就永远是这个数据类型了

解释型 : 在程序执行的前一刻 , 还只有源程序而没有可执行程序 , 边解释边执行

动态类型 : 永远不用给任何变量指定数据类型 , 只有在运行期间才会去做数据类型检查

**相对其他汇编语言的特点 :** 

优点

- Python的定位是"优雅" , "明确" , "简单" , 所以Python程序看上去总是简单移动
- 开发效率非常高 , Python有非常强大的第三方库 , 基本上你想通过计算机实现任何功能 , Python官方库里都有相应的模块进行支持 , 直接下载调用后 , 在基础库的基础上再进行开发 , 大大降低开发周期
- Python是开源的 , 所以可移植性强
- 可扩展性 , 如果你需要你的一段关键代码运行得更快或者希望某些算法不公开 , 你可以把你的部分程序用C或者C++编写 , 然后在你的Python程序中使用
- 可嵌入性 , 你可以把Python嵌入你的C/C++程序 , 从而向你的程序用户提供脚本功能

缺点

- 速度慢 , Python的运行速度相比C语言确实慢很多 , 跟Java相比也要慢一些 , 因为这也是很多所谓的大牛不屑使用Python的主要原因
- 代码不能加密 , 因为Python是解释性语言 , 它们的源码都是以明文形式存放的
- 线程无法利用多CPU , Python中有一个GIL (Global Interpreter Lock , 全局解释器锁) , Python的线程是原生线程 , 在Linux上为pthread , 在Windows上为Win thread , 完全由操作系统调度线程的执行 ; 一个Python解释器进程内有一条主线程 , 以及多用户程序的执行线程 , 即使在多核CPU平台上 , 由于GIL的存在 , 所以禁止多线程的并行执行

## Python主要应用  🍀

Python可以应用于众多领域 , 如 : 数据分析、组件集成、网络服务、图像处理、数值计算和科学计算等众多领域

目前业内几乎所有大中型互联网企业都在使用Python , 如 : Youtube、Dropbox、BT、Quora (中国知乎)、豆瓣、知乎、Google、Yahoo!、Facebook、NASA、百度、腾讯、汽车之家、美团等

目前Python主要应用领域 : 

- **云计算：**云计算最火的语言，典型应用OpenSack
- **WEB开发 : **众多优秀的WEB框架，众多大型网站均为Python开发，Youtube、Dropbox、豆瓣等，典型WEB 框架有Diango
- **科学运算、人工智能 : **典型库NumPy，SciPy，Matplotlib，Enthought librarys，Pandas
- **系统运维 : **运维人员必备语言
- **金融 : **量化交易 , 金融分析 , 在金融工程领域 , Python不但在用 , 且用的最多 , 而且重要性逐年提高 ; 原因 : 作为动态语言的Python , 语言结构清晰简单 , 库丰富 , 成熟稳定 , 科学计算和统计分析都很牛逼 , 生产效率远远高于C , C++ , Java , 尤其擅长策略回测
- **图形GUI : **PyQT , WxPython , Tklnter

Python的强大不言而喻 , Python丰富和强大的库 , 使它常常被昵称胶水语言

## Python版本区别  🍀

Python 2.x 与Python 3.x存在一些差异 , 官方文档如下 : 

Python 2.x is legacy , Pythn 3.x is the present and future of the language

Python 3.0 was released in 2008.The final 2.x branch will see no new major releases after  that 3.x is

Under active  development and has already seen over five years of stale releases, including version 3.3 in 2012.

3.4 in 2014,and 3.5 in 2015.This means that all recent standard library improvements, for example, are only

available by default in Python 3.x.

Guido van Rossum (the original ceator of the Python language) decide to clean up Python 2.x properly,with less regard for backwards compatibility than is the case fot new releases in the 2.x range. The most drastic improvement is  the better Unicode support (with all text strings being Unicode by default) as well as saner bytes /Unicode separation.

Besides, several aspects of the core language (such as print and exec being statements, integers using floor division) have been adjusted to be easier for newcomers to learn and to be more consistent with the rest of the language, and old cruft has been removed (for example, all classes are now new-style,"range()" returns a memory efficient iterable, not a list as in 2.x).

更多相关信息见Python官网 : https://www.python.org/
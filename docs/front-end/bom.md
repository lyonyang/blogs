# Web开发之路 - BOM








<extoc></extoc>

## 介绍

由于JavaScript的出现就是为了能在浏览器中运行 , BOM , 即浏览器对象模型(Browser Object Model)  , BOM使JavaScript有能力与浏览器进行"对话"

由于现代浏览器已经(几乎) 实现了JavaScript交互性方面的相同方法和属性 , 因此常被认为是BOM的方法和属性

**BOM是为了控制浏览器的行为而出现的接口 , 不同浏览器之间定义与实现存在差异**

下面就开始介绍浏览器对象啦

## Window

所有的浏览器都支持`window`对象 , 它表示浏览器窗口 , 所有JavaScript全局对象 , 函数以及变量均自动成为window对象的成员 , 也就是说Window对象是客户端JavaScript最高层对象之一

由于`window`对象是全局对象 , 所有的表达式都在当前的环境中计算 , 所以要引用当前窗口不需要特殊的语法 , 可以直接把窗口的属性作为全局变量来使用 , 如 : `window.document`可以直接写`document` 

Window对象属性

| 属性                                       | 描述                                       |
| ---------------------------------------- | ---------------------------------------- |
| [closed](http://www.w3school.com.cn/jsref/prop_win_closed.asp) | 返回窗口是否已被关闭                               |
| [defaultStatus](http://www.w3school.com.cn/jsref/prop_win_defaultstatus.asp) | 设置或返回窗口状态栏中的默认文本                         |
| [document](http://www.w3school.com.cn/jsref/dom_obj_document.asp) | 文档对象  |
| [history](http://www.w3school.com.cn/jsref/dom_obj_history.asp) | 包含窗口的浏览历史 |
| [innerheight](http://www.w3school.com.cn/jsref/prop_win_innerheight_innerwidth.asp) | 返回窗口的文档显示区的高度                            |
| [innerwidth](http://www.w3school.com.cn/jsref/prop_win_innerheight_innerwidth.asp) | 返回窗口的文档显示区的宽度                            |
| length                                   | 设置或返回窗口中的框架数量                            |
| [location](http://www.w3school.com.cn/jsref/dom_obj_location.asp) | 包含有关当前URL的信息 |
| [name](http://www.w3school.com.cn/jsref/prop_win_name.asp) | 设置或返回窗口的名称                              |
| [navigator](http://www.w3school.com.cn/jsref/dom_obj_navigator.asp) | 包含有关浏览器的信息 |
| [opener](http://www.w3school.com.cn/jsref/prop_win_opener.asp) | 返回对创建此窗口的窗口的引用                           |
| [outerheight](http://www.w3school.com.cn/jsref/prop_win_outerheight.asp) | 返回窗口的外部高度                                |
| [outerwidth](http://www.w3school.com.cn/jsref/prop_win_outerwidth.asp) | 返回窗口的外部宽度                                |
| pageXOffset                              | 设置或返回当前页面相对于窗口显示区左上角的 X 位置               |
| pageYOffset                              | 设置或返回当前页面相对于窗口显示区左上角的 Y 位置               |
| parent                                   | 返回父窗口。                                   |
| [screen](http://www.w3school.com.cn/jsref/dom_obj_screen.asp) | 包含有关显示浏览器屏幕的信息  |
| [self](http://www.w3school.com.cn/jsref/prop_win_self.asp) | 返回对当前窗口的引用 , 等价于 Window 属性               |
| [status](http://www.w3school.com.cn/jsref/prop_win_status.asp) | 设置窗口状态栏的文本                               |
| [top](http://www.w3school.com.cn/jsref/prop_win_top.asp) | 返回最顶层的先辈窗口                               |
| window                                   | window 属性等价于 self 属性 , 它包含了对窗口自身的引用      |
| screenLeftscreenTopscreenXscreenY        | 只读整数 , 声明了窗口的左上角在屏幕上的的 x 坐标和 y 坐标 , IE、Safari 和 Opera 支持 screenLeft 和 screenTop , 而 Firefox 和 Safari 支持 screenX 和 screenY |

Window对象方法

| 方法                                       | 描述                             |
| ---------------------------------------- | ------------------------------ |
| [alert()](http://www.w3school.com.cn/jsref/met_win_alert.asp) | 显示带有一段消息和一个确认按钮的警告框            |
| [blur()](http://www.w3school.com.cn/jsref/met_win_blur.asp) | 把键盘焦点从顶层窗口移开                   |
| [clearInterval()](http://www.w3school.com.cn/jsref/met_win_clearinterval.asp) | 取消由 setInterval() 设置的 timeout  |
| [clearTimeout()](http://www.w3school.com.cn/jsref/met_win_cleartimeout.asp) | 取消由 setTimeout() 方法设置的 timeout |
| [close()](http://www.w3school.com.cn/jsref/met_win_close.asp) | 关闭浏览器窗口                        |
| [confirm()](http://www.w3school.com.cn/jsref/met_win_confirm.asp) | 显示带有一段消息以及确认按钮和取消按钮的对话框        |
| [createPopup()](http://www.w3school.com.cn/jsref/met_win_createpopup.asp) | 创建一个 pop-up 窗口                 |
| [focus()](http://www.w3school.com.cn/jsref/met_win_focus.asp) | 把键盘焦点给予一个窗口                    |
| [moveBy()](http://www.w3school.com.cn/jsref/met_win_moveby.asp) | 可相对窗口的当前坐标把它移动指定的像素            |
| [moveTo()](http://www.w3school.com.cn/jsref/met_win_moveto.asp) | 把窗口的左上角移动到一个指定的坐标              |
| [open()](http://www.w3school.com.cn/jsref/met_win_open.asp) | 打开一个新的浏览器窗口或查找一个已命名的窗口         |
| [print()](http://www.w3school.com.cn/jsref/met_win_print.asp) | 打印当前窗口的内容                      |
| [prompt()](http://www.w3school.com.cn/jsref/met_win_prompt.asp) | 显示可提示用户输入的对话框                  |
| [resizeBy()](http://www.w3school.com.cn/jsref/met_win_resizeby.asp) | 按照指定的像素调整窗口的大小                 |
| [resizeTo()](http://www.w3school.com.cn/jsref/met_win_resizeto.asp) | 把窗口的大小调整到指定的宽度和高度              |
| [scrollBy()](http://www.w3school.com.cn/jsref/met_win_scrollby.asp) | 按照指定的像素值来滚动内容                  |
| [scrollTo()](http://www.w3school.com.cn/jsref/met_win_scrollto.asp) | 把内容滚动到指定的坐标                    |
| [setInterval()](http://www.w3school.com.cn/jsref/met_win_setinterval.asp) | 按照指定的周期（以毫秒计）来调用函数或计算表达式       |
| [setTimeout()](http://www.w3school.com.cn/jsref/met_win_settimeout.asp) | 在指定的毫秒数后调用函数或计算表达式             |

实例

```javascript
// 返回窗口尺寸
alert('window inner size:' + window.innerWidth + 'x' + window.innerHeight);
// 直接在浏览器中consle下执行
```

## document

每个载入浏览器的HTML文档都会成为document对象 , document对象使我们可以从脚本中对HTML页面中的所有元素进行访问 

document对象是Window对象的一部分 , 可通过`window.document`属性对其进行访问 , 或直接使用`document`

document对象属性

| 属性                                       | 描述                                       |
| ---------------------------------------- | ---------------------------------------- |
| body                                     | 提供对 < body > 元素的直接访问 , 对于定义了框架集的文档 , 该属性引用最外层的 < frameset > |
| [cookie](http://www.w3school.com.cn/jsref/prop_doc_cookie.asp) | 设置或返回与当前文档有关的所有 cookie                   |
| [domain](http://www.w3school.com.cn/jsref/prop_doc_domain.asp) | 返回当前文档的域名                                |
| [lastModified](http://www.w3school.com.cn/jsref/prop_doc_lastmodified.asp) | 返回文档被最后修改的日期和时间                          |
| [referrer](http://www.w3school.com.cn/jsref/prop_doc_referrer.asp) | 返回载入当前文档的文档的 URL                         |
| [title](http://www.w3school.com.cn/jsref/prop_doc_title.asp) | 返回当前文档的标题                                |
| [URL](http://www.w3school.com.cn/jsref/prop_doc_url.asp) | 返回当前文档的 URL                              |

document对象方法

| 方法                                       | 描述                                       |
| ---------------------------------------- | ---------------------------------------- |
| [close()](http://www.w3school.com.cn/jsref/met_doc_close.asp) | 关闭用 document.open() 方法打开的输出流 , 并显示选定的数据  |
| [getElementById()](http://www.w3school.com.cn/jsref/met_doc_getelementbyid.asp) | 返回对拥有指定 id 的第一个对象的引用                     |
| [getElementsByName()](http://www.w3school.com.cn/jsref/met_doc_getelementsbyname.asp) | 返回带有指定名称的对象集合                            |
| [getElementsByTagName()](http://www.w3school.com.cn/jsref/met_doc_getelementsbytagname.asp) | 返回带有指定标签名的对象集合                           |
| [open()](http://www.w3school.com.cn/jsref/met_doc_open.asp) | 打开一个流 , 以收集来自任何 document.write() 或 document.writeln() 方法的输出 |
| [write()](http://www.w3school.com.cn/jsref/met_doc_write.asp) | 向文档写 HTML 表达式 或 JavaScript 代码            |
| [writeln()](http://www.w3school.com.cn/jsref/met_doc_writeln.asp) | 等同于 write() 方法 , 不同的是在每个表达式之后写一个换行符      |

实例

```javascript
// 改变title
document.title = '努力学习JavaScript!';
```

## navigator

navigator对象包含有关浏览器的信息 , 所有浏览器中都支持 , navigator对象的实例是唯一的 , 它是Window对象的子对象 , 所以可以用Window对象的navigator属性来引用它 , 即`window.navigator` , 当然也可以直接`navigator` 

navigator对象属性

| 属性                                       | 描述                           |
| ---------------------------------------- | ---------------------------- |
| [appCodeName](http://www.w3school.com.cn/jsref/prop_nav_appcodename.asp) | 返回浏览器的代码名                    |
| [appMinorVersion](http://www.w3school.com.cn/jsref/prop_nav_appminorversion.asp) | 返回浏览器的次级版本                   |
| [appName](http://www.w3school.com.cn/jsref/prop_nav_appname.asp) | 返回浏览器的名称                     |
| [appVersion](http://www.w3school.com.cn/jsref/prop_nav_appversion.asp) | 返回浏览器的平台和版本信息                |
| [browserLanguage](http://www.w3school.com.cn/jsref/prop_nav_browserlanguage.asp) | 返回当前浏览器的语言                   |
| [cookieEnabled](http://www.w3school.com.cn/jsref/prop_nav_cookieenabled.asp) | 返回指明浏览器中是否启用 cookie 的布尔值     |
| [cpuClass](http://www.w3school.com.cn/jsref/prop_nav_cpuclass.asp) | 返回浏览器系统的 CPU 等级              |
| [onLine](http://www.w3school.com.cn/jsref/prop_nav_online.asp) | 返回指明系统是否处于脱机模式的布尔值           |
| [platform](http://www.w3school.com.cn/jsref/prop_nav_platform.asp) | 返回运行浏览器的操作系统平台               |
| [systemLanguage](http://www.w3school.com.cn/jsref/prop_nav_systemlanguage.asp) | 返回 OS 使用的默认语言                |
| [userAgent](http://www.w3school.com.cn/jsref/prop_nav_useragent.asp) | 返回由客户机发送服务器的 user-agent 头部的值 |
| [userLanguage](http://www.w3school.com.cn/jsref/prop_nav_userlanguage.asp) | 返回 OS 的自然语言设置                |

navigator对象方法

| 方法                                       | 描述                            |
| ---------------------------------------- | ----------------------------- |
| [javaEnabled()](http://www.w3school.com.cn/jsref/met_nav_javaenabled.asp) | 规定浏览器是否启用 Java                |
| [taintEnabled()](http://www.w3school.com.cn/jsref/met_nav_taintenabled.asp) | 规定浏览器是否启用数据污点 (data tainting) |

实例

```javascript
alert('appName = ' + navigator.appName + '\n' +
      'appVersion = ' + navigator.appVersion + '\n' +
      'language = ' + navigator.language + '\n' +
      'platform = ' + navigator.platform + '\n' +
      'userAgent = ' + navigator.userAgent);
```

## screen

screen对象中存放着有关显示浏览器屏幕的信息 , 可用Window对象中的screen属性直接引用 , 即`window.screen` , 或者`screen` , 所有浏览器都支持

screen对象属性

| 属性                                       | 描述                          |
| ---------------------------------------- | --------------------------- |
| [availHeight](http://www.w3school.com.cn/jsref/prop_screen_availheight.asp) | 返回显示屏幕的高度 (除 Windows 任务栏之外) |
| [availWidth](http://www.w3school.com.cn/jsref/prop_screen_availwidth.asp) | 返回显示屏幕的宽度 (除 Windows 任务栏之外) |
| [bufferDepth](http://www.w3school.com.cn/jsref/prop_screen_bufferdepth.asp) | 设置或返回调色板的比特深度               |
| [colorDepth](http://www.w3school.com.cn/jsref/prop_screen_colordepth.asp) | 返回目标设备或缓冲器上的调色板的比特深度        |
| [deviceXDPI](http://www.w3school.com.cn/jsref/prop_screen_devicexdpi.asp) | 返回显示屏幕的每英寸水平点数              |
| [deviceYDPI](http://www.w3school.com.cn/jsref/prop_screen_deviceydpi.asp) | 返回显示屏幕的每英寸垂直点数              |
| [fontSmoothingEnabled](http://www.w3school.com.cn/jsref/prop_screen_fontsmoothingenabled.asp) | 返回用户是否在显示控制面板中启用了字体平滑       |
| [height](http://www.w3school.com.cn/jsref/prop_screen_height.asp) | 返回显示屏幕的高度                   |
| [logicalXDPI](http://www.w3school.com.cn/jsref/prop_screen_logicalxdpi.asp) | 返回显示屏幕每英寸的水平方向的常规点数         |
| [logicalYDPI](http://www.w3school.com.cn/jsref/prop_screen_logicalydpi.asp) | 返回显示屏幕每英寸的垂直方向的常规点数         |
| [pixelDepth](http://www.w3school.com.cn/jsref/prop_screen_pixeldepth.asp) | 返回显示屏幕的颜色分辨率(比特每像素)         |
| [updateInterval](http://www.w3school.com.cn/jsref/prop_screen_updateinterval.asp) | 设置或返回屏幕的刷新率                 |
| [width](http://www.w3school.com.cn/jsref/prop_screen_width.asp) | 返回显示器屏幕的宽度                  |

实例

```javascript
alert('screen size = ' + screen.width + ' x ' + screen.height);
```

## history

history对象最初设计来表示窗口的浏览历史 , 但出于隐私方面的原因 , history对象不在允许脚本访问已经访问过的实际URL , 唯一保持使用的功能只有[back()](http://www.w3school.com.cn/jsref/met_his_back.asp)、[forward()](http://www.w3school.com.cn/jsref/met_his_forward.asp) 和 [go()](http://www.w3school.com.cn/jsref/met_his_go.asp) 方法 

可通过`window.history`或者`history`进行访问 

history对象属性

| 属性                                       | 描述                 |
| ---------------------------------------- | ------------------ |
| [length](http://www.w3school.com.cn/jsref/prop_his_length.asp) | 返回浏览器历史列表中的 URL 数量 |

history对象方法

| 方法                                       | 描述                     |
| ---------------------------------------- | ---------------------- |
| [back()](http://www.w3school.com.cn/jsref/met_his_back.asp) | 加载 history 列表中的前一个 URL |
| [forward()](http://www.w3school.com.cn/jsref/met_his_forward.asp) | 加载 history 列表中的下一个 URL |
| [go()](http://www.w3school.com.cn/jsref/met_his_go.asp) | 加载 history 列表中的某个具体页面  |

实例

```javascript
// 该操作与单击后退按钮执行的操作一样
history.back()
// 返回结果:undefined
```

## location

location对象包含有关当前URL的信息 , location对象是Window对象的一部分 , 可通过`window.location`属性来访问 , 或者`location`

location对象属性

| 属性                                       | 描述                         |
| ---------------------------------------- | -------------------------- |
| [hash](http://www.w3school.com.cn/jsref/prop_loc_hash.asp) | 设置或返回从井号 (#) 开始的 URL（锚）    |
| [host](http://www.w3school.com.cn/jsref/prop_loc_host.asp) | 设置或返回主机名和当前 URL 的端口号       |
| [hostname](http://www.w3school.com.cn/jsref/prop_loc_hostname.asp) | 设置或返回当前 URL 的主机名           |
| [href](http://www.w3school.com.cn/jsref/prop_loc_href.asp) | 设置或返回完整的 URL               |
| [pathname](http://www.w3school.com.cn/jsref/prop_loc_pathname.asp) | 设置或返回当前 URL 的路径部分          |
| [port](http://www.w3school.com.cn/jsref/prop_loc_port.asp) | 设置或返回当前 URL 的端口号           |
| [protocol](http://www.w3school.com.cn/jsref/prop_loc_protocol.asp) | 设置或返回当前 URL 的协议            |
| [search](http://www.w3school.com.cn/jsref/prop_loc_search.asp) | 设置或返回从问号 (?) 开始的 URL（查询部分） |

location 对象方法

| 属性                                       | 描述          |
| ---------------------------------------- | ----------- |
| [assign()](http://www.w3school.com.cn/jsref/met_loc_assign.asp) | 加载新的文档      |
| [reload()](http://www.w3school.com.cn/jsref/met_loc_reload.asp) | 重新加载当前文档    |
| [replace()](http://www.w3school.com.cn/jsref/met_loc_replace.asp) | 用新的文档替换当前文档 |

实例

```html
<html>
<head>
    <script type="text/javascript">
    function currLocation()
    {
    alert(window.location)
    }
    function newLocation()
    {
    window.location="/index.html"
    }
    </script>
</head>
<body>
    <input type="button" onclick="currLocation()" value="显示当前的 URL">
    <input type="button" onclick="newLocation()" value="改变 URL">
</body>
</html>
```

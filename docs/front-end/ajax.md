# Web开发之路 - Ajax








<extoc></extoc>

## 介绍


Ajax : `Asynchronous JavaScript and XML` , 意思就是用JavaScript执行异步网络请求 

Ajax是一种用于创建快速动态网页的技术 , 通过在后台与服务器进行少量数据交换 , Ajax可以使网页实现异步更新 ,  这意味着可以在不重新加载整个网页的情况下 , 对网页的某部分进行更新

2005年 , Google通过其Google Suggest使用Ajax创造出动态性极强的Web界面 , 于是Ajax开始流行起来

Ajax是基于现有的Internet标准 , 并且联合使用它们 : 

- XMLHttpRequest对象 (异步的与服务器交换数据)
- JavaScript/DOM (信息显示/交互)
- CSS (给数据定义样式)
- XML (作为转换数据的格式)

AJAX应用程序与浏览器和平台无关的

## XHR创建对象

`XMLHttpRequest`是Ajax的基础 , 所有现代浏览器均支持XMLHttpRequest对象 (IE5 和 IE6使用ActiveXObject)

XMLHttpRequest用于在后台与服务器交换数据 , 也就是完成不重新加载整个页面实现某部分进行更新

创建XMLHttpRequest对象

```javascript
variable=new XMLHttpRequest();
variable=new ActiveXObject("Microsoft.XMLHTTP");  // IE5和IE6使用ActiveX对象
```

应对所有浏览器

```javascript
var xmlhttp;
if (window.XMLHttpRequest)
{
    //  IE7+, Firefox, Chrome, Opera, Safari 浏览器执行代码
    xmlhttp=new XMLHttpRequest();
}
else
{
    // IE6, IE5 浏览器执行代码
    xmlhttp=new ActiveXObject("Microsoft.XMLHTTP");
}
```

## XHR请求

将请求发送到服务器 , 使用XMLHttpRequest对象的open() 和 send()

| 方法                           | 描述                                       |
| ---------------------------- | ---------------------------------------- |
| open(*method*,*url*,*async*) | 规定请求的类型 , URL 以及是否异步处理请求  <br>method : 请求的类型 , GET 或 POST<br>url : 文件在服务器上的位置<br>async : true(异步)或 false(同步) |
| send(*string*)               | 将请求发送到服务器 , *string* : 仅用于 POST 请求       |

**GET 与 POST**

与 POST 相比 , GET 更简单也更快 , 并且在大部分情况下都能用

然而 , 在以下情况中 , 请使用 POST 请求 : 

- 无法使用缓存文件 (更新服务器上的文件或数据库)
- 向服务器发送大量数据 (POST 没有数据量限制)
- 发送包含未知字符的用户输入时 , POST 比 GET 更稳定也更可靠

GET请求

```javascript
xmlhttp.open("GET","/try/ajax/demo_get.php",true);  // url-服务器上的文件
xmlhttp.send();
```

POST请求

```javascript
xmlhttp.open("POST","/try/ajax/demo_post.php",true);
xmlhttp.send();
```

HTML表单POST数据使用`setRequestHeader(header,value)` 来添加HTTP头

```javascript
xmlhttp.open("POST","/try/ajax/demo_post2.php",true);
xmlhttp.setRequestHeader("Content-type","application/x-www-form-urlencoded");
xmlhttp.send("fname=Henry&lname=Ford");
```

## XHR响应

获取服务器的响应 , 可以使用XMLHttpRequest对象的`responseText`或`responseXML`属性

| 属性           | 描述             |
| ------------ | -------------- |
| responseText | 获得字符串形式的响应数据   |
| responseXML  | 获得 XML 形式的响应数据 |

responseText

```javascript
document.getElementById("myDiv").innerHTML=xmlhttp.responseText;
```

responseXML

```javascript
xmlDoc=xmlhttp.responseXML;
txt="";
x=xmlDoc.getElementsByTagName("ARTIST");
for (i=0;i<x.length;i++)
{
    txt=txt + x[i].childNodes[0].nodeValue + "<br>";
}
document.getElementById("myDiv").innerHTML=txt;
```

## XHR readyState

**onreadystatechange 事件**

当请求被发送到服务器时 , 我们需要执行一些基于响应的任务 ; 每当readyState改变时 , 就会触发`onreadystatechange`事件

XMLHttpRequest对象的三个重要属性 : 

| 属性                 | 描述                                       |
| ------------------ | ---------------------------------------- |
| onreadystatechange | 存储函数(或函数名) , 每当 readyState 属性改变时 , 就会调用该函数 |
| readyState         | 存有 XMLHttpRequest 的状态 , 从 0 到 4 发生变化<br>0: 请求未初始化<br>1: 服务器连接已建立<br>2: 请求已接收<br>3: 请求处理中<br>4: 请求已完成 , 且响应已就绪 |
| status             | 200 : "OK"404 : 未找到页面                    |

在onreadystatechange事件中 , 我们规定当服务器响应已做好被处理的准备时所执行的任务

```javascript
xmlhttp.onreadystatechange=function()
{
    if (xmlhttp.readyState==4 && xmlhttp.status==200)
    {
        document.getElementById("myDiv").innerHTML=xmlhttp.responseText;
    }
}
// onreadystatechange 事件被触发 5 次(0-4),对应着 readyState 的每个变化
```

回调函数

```javascript
function myFunction()
{
    loadXMLDoc("/try/ajax/ajax_info.txt",function()
    {
        if (xmlhttp.readyState==4 && xmlhttp.status==200)
        {
            document.getElementById("myDiv").innerHTML=xmlhttp.responseText;
        }
    });
}
```

## Ajax数据库

Ajax可用来与数据库进行动态通信 , 使用showCustomer()函数

showCustomer() 函数执行以下任务 : 

- 检查是否已选择某个客户
- 创建 XMLHttpRequest 对象
- 当服务器响应就绪时执行所创建的函数
- 把请求发送到服务器上的文件
- 请注意我们向 URL 添加了一个参数 q (带有输入域中的内容)

实例

```javascript
function showCustomer(str)
{
  var xmlhttp;    
  if (str=="")
  {
    document.getElementById("txtHint").innerHTML="";
    return;
  }
  if (window.XMLHttpRequest)
  {
    // IE7+, Firefox, Chrome, Opera, Safari 浏览器执行代码
    xmlhttp=new XMLHttpRequest();
  }
  else
  {
    // IE6, IE5 浏览器执行代码
    xmlhttp=new ActiveXObject("Microsoft.XMLHTTP");
  }
  xmlhttp.onreadystatechange=function()
  {
    if (xmlhttp.readyState==4 && xmlhttp.status==200)
    {
      document.getElementById("txtHint").innerHTML=xmlhttp.responseText;
    }
  }
  xmlhttp.open("GET","/try/ajax/getcustomer.php?q="+str,true);
  xmlhttp.send();
}
```

## jQuery Ajax方法

在jQuery中我们为我们封装了有关Ajax的操作 , 方法如下 : 

| 方法                                       | 描述                                       |
| ---------------------------------------- | ---------------------------------------- |
| [$.ajax()](http://www.runoob.com/jquery/ajax-ajax.html) | 执行异步 AJAX 请求                             |
| $.ajaxPrefilter()                        | 在每个请求发送之前且被 $.ajax() 处理之前 , 处理自定义 Ajax 选项或修改已存在选项 |
| [$.ajaxSetup()](http://www.runoob.com/jquery/ajax-ajaxsetup.html) | 为将来的 AJAX 请求设置默认值                        |
| $.ajaxTransport()                        | 创建处理 Ajax 数据实际传送的对象                      |
| [$.get()](http://www.runoob.com/jquery/ajax-get.html) | 使用 AJAX 的 HTTP GET 请求从服务器加载数据            |
| [$.getJSON()](http://www.runoob.com/jquery/ajax-getjson.html) | 使用 HTTP GET 请求从服务器加载 JSON 编码的数据          |
| [$.getScript()](http://www.runoob.com/jquery/ajax-getscript.html) | 使用 AJAX 的 HTTP GET 请求从服务器加载并执行 JavaScript |
| [$.param()](http://www.runoob.com/jquery/ajax-param.html) | 创建数组或对象的序列化表示形式（可用于 AJAX 请求的 URL 查询字符串）  |
| [$.post()](http://www.runoob.com/jquery/ajax-post.html) | 使用 AJAX 的 HTTP POST 请求从服务器加载数据           |
| [ajaxComplete()](http://www.runoob.com/jquery/ajax-ajaxcomplete.html) | 规定 AJAX 请求完成时运行的函数                       |
| [ajaxError()](http://www.runoob.com/jquery/ajax-ajaxerror.html) | 规定 AJAX 请求失败时运行的函数                       |
| [ajaxSend()](http://www.runoob.com/jquery/ajax-ajaxsend.html) | 规定 AJAX 请求发送之前运行的函数                      |
| [ajaxStart()](http://www.runoob.com/jquery/ajax-ajaxstart.html) | 规定第一个 AJAX 请求开始时运行的函数                    |
| [ajaxStop()](http://www.runoob.com/jquery/ajax-ajaxstop.html) | 规定所有的 AJAX 请求完成时运行的函数                    |
| [ajaxSuccess()](http://www.runoob.com/jquery/ajax-ajaxsuccess.html) | 规定 AJAX 请求成功完成时运行的函数                     |
| [load()](http://www.runoob.com/jquery/ajax-load.html) | 从服务器加载数据，并把返回的数据放置到指定的元素中                |
| [serialize()](http://www.runoob.com/jquery/ajax-serialize.html) | 编码表单元素集为字符串以便提交                          |
| [serializeArray()](http://www.runoob.com/jquery/ajax-serializearray.html) | 编码表单元素集为 names 和 values 的数组              |

GET

```javascript
var jqxhr = $.get('/path/to/resource', {
    name: 'Bob Lee',
    check: 1
});
```

POST

```javascript
var jqxhr = $.post('/path/to/resource', {
    name: 'Bob Lee',
    check: 1
});
```

JSON

```javascript
var jqxhr = $.getJSON('/path/to/resource', {
    name: 'Bob Lee',
    check: 1
}).done(function (data) {
    // data已经被解析为JSON对象了
});
```


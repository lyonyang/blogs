# Web开发之路 - HTML-head


<extoc></extoc>

## 介绍  🍀

**HTML是什么 ?** 

超文本标记语言(Hyper Text Markup Language , HTML) , 是一种用于创建网页的标准标记语言

HTML使用一套标记标签来描述网页 , HTML文档 = 网页 , Web浏览器的作用是读取HTML文档 , 并以网页的形式显示出来 , 浏览器不会显示HTML标签 , 而是使用标签来解释页面的内容

**HTML标签**

HTML标签是由尖括号包围的关键字 , `<HTML tag> Content </HTMLtag>` 

"HTML 标签" 和 "HTML 元素" 通常都是描述同样的意思 , 但是严格来讲 , 一个HTML元素包含了开始标签与结束标签

**HTML元素**

HTML元素以开始标签起始(起始标签) , 以结束标签终止(闭合标签) , 元素的内容是开始标签与结束标签之间的内容

HTML元素分为**块级元素**和**内联元素** , 块级元素在浏览器显示时 , 通常会以新的行来开始(和结束) , 而内联元素显示时通常就在行内开始(和结束) , 如下 :

- 块级元素 : < h > , < p > , < ul > , < table >等
- 内联元素 : < b > , < td > , < a> , < img >等

**HTML属性**

HTML标签可以拥有属性 , 属性提供了有关HTML元素的更多信息 , 属性是以键/值对的形式出现 , 如 : name="Lyon" ; 

属性在HTML元素的起始标签中规定 , 如 :`<a href="http://www.baidu.com">点我进百度</a>`

HTML中有很多标准属性 , 当然也可以自定义属性 , 适用于大多数HTML元素的属性如下 :

- class , 为html元素定义一个或多个类名(类名从样式文件引入)
- id , 定义元素的id
- style , 规定元素的行内样式
- title , 描述了元素的额外信息

**HTML文档**

```html
file.html
├── <!DOCTYPE html>    
└── <html>
    ├── <head>
    │   ├── <meta>
    │   ├── <title>
    │   ├── <base>
    │   ├── <link>
    │   ├── <style>
    │   └── <script>
    └── <body>
```

## < !DOCTYPE html >  🍀

`DOCTYPE`告诉浏览器使用什么样的html或xhtml规范来解析html文档 

如果html文档没有DOCTYPE声明 , 那么`compatMode` 默认为`BackCompat(标准兼容模式未开启,称为怪异模式或混杂模式)` , 使用该模式时 , 浏览器会按照自己的方式解析渲染页面 , 并且在不同的浏览器就会显示不同的样式

如果html文档添加了声明 , 那么compatMode就是`CSS1Compat(标准兼容模式已开启,称为严格模式)`  , 即按照W3C的标准解析渲染页面 , 这样所有的浏览器显示的就是一个样子了

## &lt; html &gt;  🍀

< html > 元素是HTML页面的根元素 , HTML文档由嵌套的HTML元素构成

一般包括< head >与< body > , 如下

### &lt; head &gt;  🍀

< head >元素包含了所有的头部标签元素 , 在< head >元素中可以插入脚本(Script) , 样式(CSS) , 及各种meta信息

#### &lt; meta &gt;  🍀

meta标签描述了一些基本的元数据

1. 页面编码

   ```html
   < meta content= "text/html;charset=utf-8" >
   ```

2. 刷新和跳转

   ```html
   <!-- 每30秒刷新当前页面 -->
   <meta http-equiv="refresh" content="30">
   <!-- 5秒后跳转至baidu -->
   <meta http-equiv="refresh" content="5;url=http://www.baidu.com">
   ```

3. 关键词

   ```html
   <meta name="keywords" content="HTML, CSS, XML, XHTML, JavaScript">
   ```

4. 描述

   ```html
   <meta name="description" content="Python & Lyon">
   ```

5. X-UA-Compatible

   ```html
   <!-- 定义文档兼容性,模仿IE7模式兼容性 -->
   <meta http-equiv="X-UA-Compatible" content="IE=EmulateIE7" >
   ```

#### &lt; title &gt;  🍀

定义网页头部信息 , 在HTML/XHTML文档中是必须的

title元素 :

- 定义了浏览器工具栏的标题
- 当网页添加收藏夹时 , 显示在收藏夹中的标题
- 显示在搜索引擎结果页面的标题

```html
<!DOCTYPE html>
<html>
<head> 
	<meta charset="utf-8"> 
	<title>Lyon</title>
</head>
<body>
	<!-- 文档内容 -->
</body>
</html>
```

#### &lt; base &gt;  🍀

< base > 标签描述了基本的链接地址/链接目标 , 该标签作为HTML文档中所有的链接默认链接

```html
<head>
  	<base href="http://www.baidu.com/" target="baidu">
</head>
```

#### &lt; link &gt;   🍀

< link > 标签定义了文档与外部资源之间的关系 , 通常用于链接到样式表 :

```html
<head>
<!-- css -->
<link rel="stylesheet" href="mystyle.css">
<!-- icon -->
<link rel="shortcut icon" href="image/favicon.ico">  
</head>
```

#### &lt; style &gt;  🍀

< style > 标签定义HTML文档的样式文件引用地址 , 在< style > 元素中也可以直接添加样式来渲染HTML文档

```html
<head>
    <meta charset="UTF-8">
    <title>Lyon</title>
    <style>
        body {
            background-color: yellowgreen;
            font-size: inherit;
        }
    </style>
</head>
<body>
    <h1 style="color:black;background-color: darkred">I am Lyon!!</h1>
</body>
</html>
```

#### &lt; script &gt;  🍀

< script > 标签用于加载脚本文件 , 也可直接写脚本代码

```html
<!-- 加载文件 -->
<script type="text/javascript" src="myjavascript.js"></script>
<!-- 写JS代码 -->
<script type="text/javascript">
	<!-- JS内容 -->
</script>
```

### &lt; body &gt;  🍀

body元素是html文档中的主体 , 表示网页的主题部分 , 也就是用户可以看到的内容 , 可以包含文本 , 图片 , 音频 , 视频等各种内容

为避免篇幅过长 , body部分请看下一篇

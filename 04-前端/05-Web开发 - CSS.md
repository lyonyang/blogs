# Web开发之路 - CSS


<extoc></extoc>

## 介绍  🍀

CSS指的是**层叠样式表(Cascading Style Sheets)** , 用于定义如何显示HTML元素

CSS是在HTML 4 开始使用的 , 是为了更好的渲染HTML元素而引入的 , CSS可以通过以下方式加到HTML中 :

- 内联样式 : 在HTML元素中使用 "style" 属性
- 内部样式表 : 在HTML文档头部< head >区域使用 < style > 元素来包含CSS
- 外部引用 : 是用外部CSS文件

最好的方式就是通过外部引用CSS文件 , 三种方式如下 :

**内联样式**

```html
<body style="background-color:yellow;">
    <h2 style="background-color:red;">标题</h2>
    <p style="background-color:green;">段落</p>
</body>
```

**内部样式表**

```html
<head>
    <style type="text/css">
        body {background-color:yellow;}
        p {color:blue;}
	</style>
</head>
```

**外部引用**

```html
<head>
	<link rel="stylesheet" type="text/css" href="mystyle.css">
</head>
```

## 选择器  🍀

CSS规则由两个主要的部分构成 : 选择器 , 以及一条或多条声明 , 如下 :

```html
selector {declaration1;declaration2;... declarationN}
```

选择器的种类有很多 , 下面就开始介绍各种选择器

### 元素选择器  🍀

元素选择器又称标签选择器

文档的元素就是最基本的选择器

```html
div {background-color:red;}
```

### Class选择器  🍀

class选择器用于描述一组元素的样式 , class可以在多个元素中使用

class选择器在HTML中以class属性表示 , 在CSS中 , 类选择器以一个点 **"." 号**显示

```html
<!-- 所有拥有center类的HTML元素均为居中 -->
.center {text-align:center;}
<!-- 所有的p元素使用class="center"居中 -->
p.center {text-align:center;}
```

类名的第一个字符不能使用数字 , 它无法在Mozilla或Firefox中起作用/ 

### ID选择器  🍀

ID选择器可以为标有特定id的HTML元素指定特定的样式

CSS中ID选择器以"#"来定义

```html
#para1 {
  color:red;
}
```

ID属性不要以数字开头 , 数字开头的ID在Mozilla/Firefox浏览器中不起作用

### 属性选择器  🍀

选择拥有某些属性的元素 , 也可设置特定属性

```html
<!-- 所有的包含title属性的元素变为红色 -->
*[title] {color:red;}
<!-- 同时具有href和title属性的a元素变为红色-->
a[href][title] {color:red;}
<!-- 所有的包含class属性并且value为"important warning"的p元素变为红色 -->
p[class="important warning"] {color: red;}
<!-- 所有的包含class属性并且value包含"important"的p元素变为红色 -->
p[class~="important"] {color: red;}
```

### 后代选择器  🍀

后代选择器又称包含选择器 , 后代选择器可以选择作为**某元素后代**的元素

```html
<!-- 选择h1元素后代的em元素文本,变为红色 -->
h1 em {color:red;}
```

### 子元素选择器  🍀

与后代选择器相比 , 子元素选择器只能选择作为某元素子元素中的元素

```html
<!-- 选择h1元素中的strong子元素 -->
h1 > strong {color:red;}
```

### 相邻兄弟选择器  🍀

相邻兄弟选择器可以选择紧接在另一元素后的元素 , 且二者有相同父元素

```html
<!-- 选择紧接在h1元素后出现的段落,h1和p元素拥有共同的父元素 -->
h1 + p {margin-top:50px;}
```

### 伪类  🍀

伪类用于向某些选择器添加特殊的效果

伪类的语法 :

```html
selector : pseudo-class {property:value}
<!-- CSS类与伪类搭配使用 -->
selector.class : pseduo-class {property:value}
```

实例 

```html
<!-- 已访问的链接添加颜色 -->
a.red : visited {color: #FF0000}
<a class="red" href="css_syntax.asp">CSS Syntax</a>
```

### 伪元素  🍀

伪元素用于向某些选择器设置特殊效果

伪元素的语法 :

```html
selector:pseudo-element {property:value;}
<!-- CSS类与伪元素搭配使用 -->
selector.class:pseudo-element {property:value;}
```

```html
<!-- 对第一行文本进行格式化 -->
p:first-line
  {
  color:#ff0000;
  font-variant:small-caps;
  }
```

> 组合选择器 : 

```html
input,div,p { background-color:red; } 
```

> 关联选择器 :

```html
<style>
   idselect p { background-color:red; }
</style>
<div id='idselect' > <p> </p> </div>
```

## 常用属性  🍀

### background  🍀

**背景色**

`background-color`属性可以为元素设置背景色

```css
/* 把元素背景设置为灰色 */
p {background-color: gray;}
```

background-color属性默认值为`transparent` , 即"透明"

**背景图像**

`background-image`属性可以把图像作为背景

```css
/* 设置图像时,必须为该属性设置一个url值 */
body {background-image: url(/i/eg_bg_04.gif);}
```

background-image属性默认值为`none` , 表示背景上没有放置任何图像

**背景重复**

`background-repeat`属性可以将背景图像在页面上进行平铺

属性repeat导致图像在水平垂直方向都平铺 , `repeat-x`和`repeat-y`分别导致图像只在水平或垂直方向上重复 , `no-repea`t则不允许图像在任何方向上平铺

```css
/* 默认从左上角开始,垂直方向上平铺 */
body {
  background-image: url(/i/eg_bg_03.gif);
  background-repeat: repeat-y;
}
```

**背景定位**

`background-position`属性可以改变图像在背景中的位置

```css
body { 
  background-image:url('/i/eg_bg_03.gif');
  background-repeat:no-repeat;
  background-position:center;
}
```

background-position有以下关键字 : top , bottom , left , right 和center , 这些关键字通常成对出现 , 也可以使用长度值 , 如 : 100px或5cm(**长度值是元素边距区左上角的便宜偏移**) , 以及使用百分数

```css
body { 
  background-image:url('/i/eg_bg_03.gif');
  background-repeat:no-repeat;
  background-position:50% 50%;
}
```

背景关联

background-attachment属性可以使图像相对于可视区固定 , 即不会受到滚动的影响

```css
body {
  background-image:url(/i/eg_bg_02.gif);
  background-repeat:no-repeat;
  background-attachment:fixed
}
```

### border  🍀

border属性允许规定元素边框的样式 , 宽度和颜色

元素的边框是围绕元素内容和内边距的一条或多条线

```css
/* 一个边框定义多个样式 */
p.aside {border-style: solid dotted dashed double;}
<p>看看我的边框</p>
```

更多边框样式及边框相关 , [在我这里](http://www.w3school.com.cn/css/css_border.asp)

### margin  🍀

margin属性可以用来设置外边距 , 接受任何长度单位 , 百分数甚至负值

围绕在元素边框的空白区域就是外边距 , 设置外边距会在元素外创建额外的"空白"

```css
/* h1元素的各个边上设置了1/4英寸的空白 */
h1 {margin : 0.25in;}
h1 {margin : 10px 0px 15px 5px;}
/* margin: top right bottom left */
```

**值复制**

- 如果缺少左外边距的值 , 则使用右外边距的值
- 如果缺少下外边距的值 , 则使用上外边距的值
- 如果缺少右外边距的值 , 则使用上外边距的值

```css
h1 {margin: 0.25em 1em 0.5em;}	/* 等价于 0.25em 1em 0.5em 1em */
h2 {margin: 0.5em 1em;}		    /* 等价于 0.5em 1em 0.5em 1em */
p {margin: 1px;}			    /* 等价于 1px 1px 1px 1px */
```

**单边外边距**

- [margin-top](http://www.w3school.com.cn/cssref/pr_margin-top.asp)
- [margin-right](http://www.w3school.com.cn/cssref/pr_margin-right.asp)
- [margin-bottom](http://www.w3school.com.cn/cssref/pr_margin-bottom.asp)
- [margin-left](http://www.w3school.com.cn/cssref/pr_margin-left.asp)

### padding  🍀

padding属性可以设置内边距 , 接受长度值或百分比值 , 但不允许使用负值

元素的内边距在边框和内容区之间

```css
/* 同样具有值复制规则,与margin一样 */
h1 {padding: 10px;}
h1 {padding: 10px 0.25em 2ex 20%;}
```

单边内边距

- [padding-top](http://www.w3school.com.cn/cssref/pr_padding-top.asp)
- [padding-right](http://www.w3school.com.cn/cssref/pr_padding-right.asp)
- [padding-bottom](http://www.w3school.com.cn/cssref/pr_padding-bottom.asp)
- [padding-left](http://www.w3school.com.cn/cssref/pr_padding-left.asp)

### display  🍀

display属性规定元素应该生成的框的类型

```css
/* 使段落生出行内框 */
p.inline {
  display:inline;
}
```

display属性常用的值 :

- none , 此元素不会被显示
- block , 此元素将显示为块级元素 , 此元素前后会带有换行符
- inline , 默认 , 此元素会被显示为内联元素 , 元素前后没有换行符
- inline-block , 行内块元素

更多[display属性](http://www.w3school.com.cn/cssref/pr_class_display.asp)

### cursor  🍀

cursor属性规定要显示的光标的类型

该属性定义了鼠标指针放在一个元素边界范围内时锁用的光标形状

| 值         | 描述                                       |
| --------- | ---------------------------------------- |
| url       | 需使用的自定义光标的 URL , 末端始终定义一种普通的光标 , 以防没有由 URL 定义的可用光标 |
| default   | 默认光标(通常是一个箭头)                            |
| auto      | 默认 , 浏览器设置的光标                            |
| crosshair | 光标呈现为十字线                                 |
| pointer   | 光标呈现为指示链接的指针(一只手)                        |
| move      | 此光标指示某对象可被移动                             |
| e-resize  | 此光标指示矩形框的边缘可被向右(东)移动                     |
| ne-resize | 此光标指示矩形框的边缘可被向上及向右移动(北/东)                |
| nw-resize | 此光标指示矩形框的边缘可被向上及向左移动北(西)                 |
| n-resize  | 此光标指示矩形框的边缘可被向上(北)移动。                    |
| se-resize | 此光标指示矩形框的边缘可被向下及向右移动(南/东)                |
| sw-resize | 此光标指示矩形框的边缘可被向下及向左移动(南/西)                |
| s-resize  | 此光标指示矩形框的边缘可被向下移动(南)                     |
| w-resize  | 此光标指示矩形框的边缘可被向左移动(西)                     |
| text      | 此光标指示文本                                  |
| wait      | 此光标指示程序正忙(通常是一只表或沙漏)                     |
| help      | 此光标指示可用的帮助(通常是一个问号或一个气球)                 |

```html
<html>
<body>
    <p>请把鼠标移动到单词上，可以看到鼠标指针发生变化：</p>
    <span style="cursor:auto">
    Auto</span><br />
    <span style="cursor:crosshair">
    Crosshair</span><br />
    <span style="cursor:default">
    Default</span><br />
    <span style="cursor:pointer">
    Pointer</span><br />
    <span style="cursor:move">
    Move</span><br />
    <span style="cursor:e-resize">
    e-resize</span><br />
    <span style="cursor:ne-resize">
    ne-resize</span><br />
    <span style="cursor:nw-resize">
    nw-resize</span><br />
    <span style="cursor:n-resize">
    n-resize</span><br />
    <span style="cursor:se-resize">
    se-resize</span><br />
    <span style="cursor:sw-resize">
    sw-resize</span><br />
    <span style="cursor:s-resize">
    s-resize</span><br />
    <span style="cursor:w-resize">
    w-resize</span><br />
    <span style="cursor:text">
    text</span><br />
    <span style="cursor:wait">
    wait</span><br />
    <span style="cursor:help">
    help</span>
</body>
</html>
```

### position  🍀

CSS有三种基本的定位机制 : 普通流 , 浮动和绝对定位 ; 除非专门指定 , 否则所有框都在普通流中定位

position属性有以下属性值 :

- static , 默认值 , 元素没有被定位 , 而且在文档中出现在它应该在的位置 , 一般不用指定 , 除非需要覆盖之前设置的定位
- relative , 元素框偏移某个距离 , 元素实际上依然占据文档中的原有位置 , 只是视觉上相对于它在文档中的原有位置移动了 , **相对定位**
- absolute , 元素在文档中不占据位置 , 定位后生成一个块级框 , 不论原来它在正常流中生成何种类型的框 , **绝对定位**
- fixed , 是特殊的absolute , 即fixed总是以body为定位对象的 , 按照浏览器的窗口进行定位

相对定位

```html
<html>
<head>
    <style type="text/css">
    h2.pos_left
    {
    position:relative;
    left:-20px
    }
    h2.pos_right
    {
    position:relative;
    left:20px
    }
    </style>
</head>
<body>
    <h2>这是位于正常位置的标题</h2>
    <h2 class="pos_left">这个标题相对于其正常位置向左移动</h2>
    <h2 class="pos_right">这个标题相对于其正常位置向右移动</h2>
    <p>相对定位会按照元素的原始位置对该元素进行移动。</p>
    <p>样式 "left:-20px" 从元素的原始左侧位置减去 20 像素。</p>
    <p>样式 "left:20px" 向元素的原始左侧位置增加 20 像素。</p>
</body>
</html>
```

绝对定位

```html
<html>
<head>
    <style type="text/css">
    h2.pos_abs
    {
    position:absolute;
    left:100px;
    top:150px
    }
    </style>
</head>
<body>
    <h2 class="pos_abs">这是带有绝对定位的标题</h2>
    <p>通过绝对定位，元素可以放置到页面上的任何位置。下面的标题距离页面左侧 100px，距离页面顶部 150px。</p>
</body>
</html>
```

固定定位

```html
<html>
<head>
    <style type="text/css">
    p.one
    {
    position:fixed;
    left:5px;
    top:5px;
    }
    p.two
    {
    position:fixed;
    top:30px;
    right:5px;
    }
    </style>
</head>
    <body>
    <p class="one">一些文本。</p>
    <p class="two">更多的文本。</p>
    </body>
</html>
```



### float  🍀

float属性可以实现浮动的框

```css
/* 图像向右浮动 */
img {
  float:right;
}
```

float属性值 :

- left , 元素向左浮动
- right , 元素向右浮动
- none , 默认值 , 元素不浮动
- inherit , 规定应该从父元素继承float属性的值

注意 : 假如在一行之上只有极少的空间可供浮动元素，那么这个元素会跳至下一行，这个过程会持续到某一行拥有足够的空间为止。

clear属性可以阻止框围绕浮动框 , clear属性值 : 

- left , 在左侧不允许浮动元素
- right , 在右侧不允许浮动元素
- both , 在左右两侧均不允许浮动元素
- none , 默认值 , 允许浮动元素出现在两侧
- inherit , 规定应该从父元素继承 clear 属性的值


```css
/* 图像左侧和右侧均不允许出现浮动元素 */
img {
  float:left;
  clear:both;
}
```


### opacity  🍀

opacity属性用于定义透明效果 , opacity属性能设置的值从0.0到1.0 , 值越小则越透明

```css
img {
  opacity:0.4;
  filter:alpha(opacity=40); /* 针对 IE8 以及更早的版本 */
}
```

更过CSS内容 , [CSS教程](http://www.w3school.com.cn/css/index.asp)
# Web开发之路 - DOM








<extoc></extoc>

## 介绍

上一篇中了解了BOM , 其存在是为了控制浏览器的行为 , 而这一篇所说的DOM则是为了操作HTML和XML文档出现的接口

DOM全称为`Document Object Model` , 也就是文档对象模型 , DOM是W3C(万维网联盟)的标准 , 所有浏览器公共遵守的标准 

当网页被加载时 , 浏览器会创建页面的DOM ; DOM是一个树形结构 , 在HTML DOM中 , 每一个元素都是节点 

同样的 , 通过JavaScript可以来操作DOM

## DOM查找

**直接查找**

```javascript
document.getElementById()  // 获取指定ID节点
document.getElementsByName()  // 获取指定name属性节点
document.getElementsByClassName()  // 获取指定class属性节点
document.getElementsByTagName() // 获取指定标签节点
```

**间接查找**

```javascript
parentNode             // 父节点
childNodes             // 所有子节点
firstChild             // 第一个子节点
lastChild              // 最后一个子节点
nextSibling            // 下一个兄弟节点
previousSibling        // 上一个兄弟节点
parentElement          // 父节点标签元素
children               // 所有子标签
firstElementChild      // 第一个子标签元素
lastElementChild       // 最后一个子标签元素
nextElementtSibling    // 下一个兄弟标签元素
previousElementSibling // 上一个兄弟标签元素
```

实例

```javascript
// 返回ID为'test'的节点：
var test = document.getElementById('test');
// 先定位ID为'test-table'的节点，再返回其内部所有tr节点：
var trs = document.getElementById('test-table').getElementsByTagName('tr');
// 先定位ID为'test-div'的节点，再返回其内部所有class包含red的节点：
var reds = document.getElementById('test-div').getElementsByClassName('red');
// 获取节点test下的所有直属子节点:
var cs = test.children;
// 获取节点test下第一个、最后一个子节点：
var first = test.firstElementChild;
var last = test.lastElementChild;
```

## DOM修改

对于DOM的修改操作有很多, 比如内容 , 样式 , 属性等等 , 都是可以用DOM进行修改的

### 内容

```javascript
innerHTML // 设置或获取位于对象起始和结束标签内的HTML,符合W3C标准 
innerText // 设置或获取位于对象起始和结束标签内的文本 
outerHTML // 设置或获取对象及其内容的HTML形式 
outerText // 设置(包括标签)或获取(不包括标签)对象的文本 
value     // 设置或返回隐藏输入域的value属性的值
```

实例

```javascript
// 获取<p id="p-id">...</p>
var p = document.getElementById('p-id');
// 设置文本为abc:
p.innerHTML = 'ABC'; // <p id="p-id">ABC</p>
// 设置HTML:
p.innerHTML = 'ABC <span style="color:red">RED</span> XYZ';
// <p>...</p>的内部结构已修改
```

### 属性

```javascript
attribute  // 获取所有标签属性
setAttribute(key,value)  // 设置标签属性
getAttribute(key)  // 获取指定标签属性
```

实例

```javascript
// 创建class属性
var atr = document.createAttribute("class");
// 设置属性值
atr.nodeValue="democlass";
// 设置属性节点
document.getElementById('n1').setAttributeNode(atr);
```

### Class

```javascript
className  // 获取所有类名
classList.remove(cls)  // 删除指定类
classList.add(cls)  // 添加类
```

### 标签

**创建标签**

```javascript
// 方式一
var tag = document.createElement('a')
tag.innerText = "baidu"
tag.className = "c1"
tag.href = "http://www.baidu.com/"
// 方式二
var tag = "<a class='c1' href='http://www.baidu.com/'>baidu</a>"
```

**插入标签**

```javascript
// 方式一
var obj = "<input type='text' />";
xxx.insertAdjacentHTML("beforeEnd",obj);
xxx.insertAdjacentElement('afterBegin',document.createElement('p'))
//注意：第一个参数只能是'beforeBegin'、 'afterBegin'、 'beforeEnd'、 'afterEnd'
// 方式二
var tag = document.createElement('a')
xxx.appendChild(tag)
xxx.insertBefore(tag,xxx[1])
```

### 样式

```javascript
var obj = document.getElementById('i1')
obj.style.fontSize = "32px";
obj.style.backgroundColor = "red";
```

实例

```html
<input onfocus="Focus(this);" onblur="Blur(this);" id="search" value="请输入关键字" style="color: gray;" />
<script>
    function Focus(ths){
    ths.style.color = "black";
    if(ths.value == '请输入关键字' || ths.value.trim() == ""){
      ths.value = "";
    }
  }
  function Blur(ths){
    if(ths.value.trim() == ""){
      ths.value = '请输入关键字';
      ths.style.color = 'gray';
    }else{
      ths.style.color = "black";
    }
  }
</script>
```

### 位置

```javascript
document.documentElement.offsetHeight  // 总文档高度
document.documentElement.clientHeight  // 当前文档占屏幕高度
tag.offsetHeight  // 自身高度
tag.offsetTop  // 距离上级定位高度
tag.offsetParent  // 父定位标签  
tag.scrollTop  // 滚动高度
/*
clientHeight -> 可见区域：height + padding
clientTop    -> border高度
offsetHeight -> 可见区域：height + padding + border
scrollHeight -> 全文高：height + padding
特别的：
document.documentElement代指文档根节点
*/
```

实例

```javascript
<script>
    var i1 = document.getElementById('i1');
    console.log(i1.clientHeight); // 可见区域：height + padding
    console.log(i1.clientTop);    // border高度
    console.log('=====');
    console.log(i1.offsetHeight); // 可见区域：height + padding + border
    console.log(i1.offsetTop);    // 上级定位标签的高度
    console.log('=====');
    console.log(i1.scrollHeight);   //全文高：height + padding
    console.log(i1.scrollTop);      // 滚动高度
    console.log('=====');
</script>
```

### 表单

```javascript
document.geElementById('form').submit()
```

### 其他

```javascript
console.log                 // 输出框
alert                       // 弹出框
confirm                     // 确认框
// URL和刷新
location.href               // 获取URL
location.href = "url"       // 重定向
location.reload()           // 重新加载
// 定时器
setInterval                 // 多次定时器
clearInterval               // 清除多次定时器
setTimeout                  // 单次定时器
clearTimeout                // 清除单次定时器
```

## DOM事件

**鼠标事件**

| 属性                                       | 描述                  | DOM  |
| ---------------------------------------- | ------------------- | ---- |
| [onclick](http://www.runoob.com/jsref/event-onclick.html) | 当用户点击某个对象时调用的事件句柄   | 2    |
| [oncontextmenu](http://www.runoob.com/jsref/event-oncontextmenu.html) | 在用户点击鼠标右键打开上下文菜单时触发 |      |
| [ondblclick](http://www.runoob.com/jsref/event-ondblclick.html) | 当用户双击某个对象时调用的事件句柄   | 2    |
| [onmousedown](http://www.runoob.com/jsref/event-onmousedown.html) | 鼠标按钮被按下             | 2    |
| [onmouseenter](http://www.runoob.com/jsref/event-onmouseenter.html) | 当鼠标指针移动到元素上时触发      | 2    |
| [onmouseleave](http://www.runoob.com/jsref/event-onmouseleave.html) | 当鼠标指针移出元素时触发        | 2    |
| [onmousemove](http://www.runoob.com/jsref/event-onmousemove.html) | 鼠标被移动               | 2    |
| [onmouseover](http://www.runoob.com/jsref/event-onmouseover.html) | 鼠标移到某元素之上           | 2    |
| [onmouseout](http://www.runoob.com/jsref/event-onmouseout.html) | 鼠标从某元素移开            | 2    |
| [onmouseup](http://www.runoob.com/jsref/event-onmouseup.html) | 鼠标按键被松开             | 2    |

**键盘事件**

| 属性                                       | 描述           | DOM  |
| ---------------------------------------- | ------------ | ---- |
| [onkeydown](http://www.runoob.com/jsref/event-onkeydown.html) | 某个键盘按键被按下    | 2    |
| [onkeypress](http://www.runoob.com/jsref/event-onkeypress.html) | 某个键盘按键被按下并松开 | 2    |
| [onkeyup](http://www.runoob.com/jsref/event-onkeyup.html) | 某个键盘按键被松开    | 2    |

更多DOM事件 , [HTML DOM事件对象](http://www.runoob.com/jsref/dom-obj-event.html)

搜索框实例

```html
<!DOCTYPE html>
<html>
    <head>
        <meta charset='utf-8' />
        <title>Title</title>
        <style>
            .gray{
                color:gray;
            }
            .black{
                color:black;
            }
        </style>
        <script type="text/javascript">
            function Enter(){
               var id= document.getElementById("tip")
               id.className = 'black';
               if(id.value=='请输入关键字'||id.value.trim()==''){
                    id.value = ''
               }
            }
            function Leave(){
                var id= document.getElementById("tip")
                var val = id.value;
                if(val.length==0||id.value.trim()==''){
                    id.value = '请输入关键字'
                    id.className = 'gray';
                }else{
                    id.className = 'black';
                }
            }
        </script>
    </head>
    <body>
        <input type='text' class='gray' id='tip' value='请输入关键字' onfocus='Enter()' onblur='Leave()' />
    </body>
</html>
```

跑马灯实例

```html
<!DOCTYPE html>
<html>
    <head>
        <meta charset='utf-8' >
        <title>欢迎blue shit莅临指导&nbsp;&nbsp;</title>
        <script type='text/javascript'>
            function Go(){
                var content = document.title;
                var firstChar = content.charAt(0)
                var sub = content.substring(1,content.length)
                document.title = sub + firstChar;
            }
            setInterval('Go()',1000);
        </script>
    </head>
    <body>    
    </body>
</html>
```


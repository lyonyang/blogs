# Web开发之路 - JavaScript








<extoc></extoc>

## 介绍

JavaScript是属于网络的脚本语言 , 是因特网上最流行的脚本语言

JavaScript被数百万计的网页用来改进设计 , 验证表单 , 检测浏览器 , 创建cookies , 以及更多的应用

浏览器内置了JavaScript语言的解释器 , 所以浏览器上按照JavaScript的规则编写相应代码 , 浏览器可以解释并作出相应的处理

完整的JavaScript实现是由一下三个不同部分组成的 : 

- 核心 , ECMAScript
- 文档对象模型 (DOM) , Document Object Model (整合JS , CSS , HTML)
- 浏览器对象模型 (BOM) , Broswer Object Model (整合JS和浏览器)

简单的说 , ECMAScript描述了JavsScript语言本身的相关内容

**存在形式**

```html
<!-- 方式一 -->
<script type="text/javascript" src="js文件"></script>
<!-- 方式二 -->
<script type="text/javascript">
  	js代码内容
</script>
```

**存放位置**

1. HTML的head中
2. HTML的body代码块底部

由于HTML代码是从上到下执行的 , 如果Head中的JS代码耗时严重 , 会导致用户长时间无法看到页面 , 所以将JS代码防止HTML的body代码块底部是最好的 , 因为不会影响用户看到页面效果 , 只是JS实现特效慢而已

**JavaScript注释**

单行注释 : //

多行注释 : `/* ... */` , (CSS注释也是如此)

## 变量

在JavaScript中 , 变量的声明默认表示声明的全局变量 , 局部变量必须以`var`开头

生命周期 : 
  - JavaScript变量的声明周期从它们被声明的时间开始
        
  - 局部变量会在函数运行以后被删除
        
  - 全局变量会在页面关闭后被删除

```javascript
<script type="text/javascript">
    // 全局变量
    name = 'Lyon';
    function func(){
        // 局部变量
        var age = 18;
        // 全局变量
        gender = "男"
    }
</script>
```

**注意 : JavaScript中严格区分大小写 , 并且以 ";" 号结束** 

## 数据类型

JavaScript中的数据类型有字符串 , 数字 , 布尔 , 数组 , 对象 , Null , Undefined 

其中`Null`是JavaScript语言的关键字 , 它表示一个特殊的值 , 常用来描述"空值" , `Undefined`是一个特殊值 , 表示变量未定义 , 即声明后若不定义则变量的值为Undefined 

1. **数字(Number)**

   JavaScript中不区分整数值和浮点数值 , 所有数字均用浮点数值表示 , 还有两个特殊值NaN和Infinity , 如下

   ```javascript
   123; // 整数
   0.456; //浮点数
   1.2345e3; // 科学计数法表示1.2345x1000，等同于1234.5
   NaN; // NaN表示Not a Number，当无法计算结果时用NaN表示
   Infinity; // Infinity表示无限大，当数值超过了JavaScript的Number所能表示的最大值时，就表示为Infinity
   ```

   Number可以直接做四则运算 , 规则和数学一致 :

   ```javascript
   1 + 2; // 3
   (1 + 2) * 5 / 2; // 7.5
   2 / 0; // Infinity
   0 / 0; // NaN
   10 % 3; // 取余,1
   10.5 % 3; // 1.5
   ```

   如果要执行常见的算数任务 , 可以使用Math对象进行计算 , [Math对象](http://www.runoob.com/js/js-obj-math.html)

2. **字符串(String)**

   字符串是由字符组成的数组 , 在JavaScript中字符串不可变的

   常见功能

   ```javascript
   string.length                          // 长度
   string.trim()                          //移除空白
   string.trimLeft()
   string.trimRight)
   string.charAt(n)                       //返回字符串中的第n个字符
   string.concat(value, ...)              //拼接
   string.indexOf(substring,start)        //子序列位置
   string.lastIndexOf(substring,start)    //子序列位置
   string.substring(from, to)             //根据索引获取子序列
   string.slice(start, end)               //切片
   string.toLowerCase()                   //大写
   string.toUpperCase()                   //小写
   string.split(delimiter, limit)         //分割
   string.search(regexp)                  //从头开始匹配,返回匹配成功的第一个位置(g无效)
   string.match(regexp)                   //全局搜索,如果正则中有g表示找到全部，否则只找到第一个。
   string.replace(regexp, replacement)    //替换,正则中有g则替换所有,否则只替换第一个匹配项
   ```

3. **布尔**

   布尔类型即`true`和`false` 

   比较运算符

   ```javascript
   ==  //比较值相等
   !=  //不等于
   === //比较值和类型相等
   !=== //不等于
   ||  //或
   &&  //且
   ```

4. **数组**

   JavaScript中的数组与Python中的列表类似 , 是一组按顺序排列的集合 , 集合的每个值称为元素

   ```javascript
   [1, 2, 3.14, 'Hello', null, true];
   // 通过Array()函数创建
   new Array(1, 2, 3);
   ```

   常用功能

   ```javascript
   array.length          //数组的大小
   array.push(ele)       //尾部追加元素
   array.pop()           //尾部获取一个元素
   array.unshift(ele)    //头部插入元素
   array.shift()         //头部移除元素
   array.splice(start, deleteCount, value, ...)  //插入,删除或替换数组的元素
   array.splice(n,0,val) //指定位置插入元素
   array.splice(n,1,val) //指定位置替换元素
   array.splice(n,1)     //指定位置删除元素
   array.slice( )        //切片
   array.reverse( )      //反转
   array.join(sep)       //将数组元素连接起来以构建一个字符串
   array.concat(val,..)  //连接数组
   array.sort( )         //对数组元素进行排序
   ```

5. **对象**

   对象由花括号分隔 , 在括号内部 , 对象的属性以名称和值对的形式定义 , 属性由逗号分隔

   ```javascript
   var person={
       name:"Lyon",
       age:20
   }
   ```

   要获取对象的属性 , 只需用`对象变量.属性名`即可 , 也可`对象变量[属性名]`

## 语句与异常

1. **条件语句**

   JavaScript中支持两个条件语句 , 分别是`if`和`switch`

   ```javascript
   // if语句
   if(条件){
   }
   else if(条件){
   }
   else{
   }
   // switch语句,选择要执行的多个代码块之一
   switch(n){
   case 1:
     执行代码块 1
     break;
   case 2:
     执行代码块 2
     break;
   default:
     n 与 case 1 和 case 2 不同时执行的代码
   }
   ```
 
注意 : 使用switch语句时 , 如果不使用break , 那么程序将继续往下执行 
 
2. **循环语句**

   与Python一样 , for循环和while循环

   ```javascript
   // for循环
   var names = ["Lyon", "Kenneth", "Eva"];
   for(var i=0;i<names.length;i++){
       console.log(i);
       console.log(names[i]);
   }
   // 遍历
   for(var index in names){
       console.log(index);
       console.log(names[index]);
   }
   // while循环
   while(条件){
       // break;
       // continue;
   }
   ```

3. **异常处理**

   ```javascript
   try {
       // 捕获异常
   }
   catch (e) {
       // 如果try代码块中捕获到了异常，catch代码块中的代码就会被执行。
       //e是一个局部变量，用来指向Error对象或者其他抛出的对象
   }
   finally {
        //无论发生啥,最后都要执行,即使遇到return
   }
   // throw Error(e) 主动抛出异常,如Python中的raise
   ```

## 函数

1. **基本函数**

   JavaScript中函数基本上可以分为以下三类

   ```javascript
   // 普通函数
       function func(arg){
           return true;
       }      
   // 匿名函数
       var func = function(arg){
           return "Lyon";
       }
   // 自执行函数
       (function(arg){
           console.log(arg);
       })('123')
   ```

   上例中函数的参数都属于显示参数(Parameters) , 显示参数在函数定义时列出 ; 还有隐式参数(Arguments) , 其在函数调用时传递给函数真正的值 , 如果函数在调用时未提供隐式参数 , 参数会默认设置为`undefined`

   JavaScript函数有个内置的对象`arguments`对象 , 包含了函数调用的参数数组 , 通过这种方式可以方便的找到最大的参数的值 , 或者创建一个函数用来统计所有数值的和

   ```javascript
   x = findMax(1, 123, 500, 115, 44, 88);
   function findMax() {
       var i, max = arguments[0];
       if(arguments.length < 2) return max;
       for (i = 0; i < arguments.length; i++) {
           if (arguments[i] > max) {
               max = arguments[i];
           }
       }
       return max;
   }
   ```

   对于Python来讲 , 显示与隐式不过就是实参与形参而已 ; 在JavaScript中都是按照位置参数进行传递的 , 特殊对象arguments的存在 , 使得JavaScript中实际参数可能小于形式参数的个数
   

2. **作用域**

   JavaScript中每个函数都有自己的作用域 , 当出现函数嵌套时 , 就出现了作用域链 , 即函数使用变量时 , 会随着作用域链从内而外的一层层寻找 , 找不到就异常

   ```javascript
   function f2(){
       var arg= 111;
       function f3(){
           console.log(arg);
       }
       return f3;
   }
   ret = f2();
   ret();
   ```

   **PS1 : 所有的作用域在创建函数且未执行时就已经存在**

   PS2 : JavaScript函数在被执行之前 , 所有的变量都已经声明 , 但是却不会赋值 , 所以即使你在使用参数的后面再定义变量也不会报错 , 因为它是存在的并且值为`undefined`

   ```javascript
   function Mytest(){
       console.log(name);
     	var name = "Lyon";
   }
   Mytest();
   // 输出结果:undefined
   ```

3. **闭包**

   闭包在很多语言中都可以看到 , 就像Python中 , 闭包必须是内部定义的函数(嵌套函数) , 该函数包含对外部作用域而不是全局作用域名字的引用 , JavaScript中也一样

   闭包是一个函数 , 它记住了周围发生了什么

   由于作用域链只能从内而外的找 , 默认外部无法获取函数内部变量 , 闭包则实现了在外部获取函数内部的变量

   ```javascript
   function f2(){
       var arg= [11,22];
       function f3(){
           return arg;
       }
       return f3;
   }
   ret = f2();
   ret();
   ```

4. **面向对象**

   ```javascript
   function Foo (name,age) {
       this.Name = name;
       this.Age = age;
       this.Func = function(arg){
           return this.Name + arg;
       }
   }
   var obj = new Foo('Lyon', 18);
   var ret = obj.Func("Kenneth");
   console.log(ret);
   ```

   上述代码中 : 

   - Foo充当构造函数
   - this代指对象
   - 创建对象时需要使用new

   但是在上述代码中每个对象中均保存了一个相同的Func函数 , 可以使用原型优化处理
   
   ```javascript
   function Foo (name,age) {
       this.Name = name;
       this.Age = age;
   }
   Foo.prototype = {
       GetInfo: function(){
           return this.Name + this.Age
       },
       Func : function(arg){
           return this.Name + arg;
       }
   }
   ```

## 其他

1.  **序列化**

      ```javascript
      - JSON.stringify(obj)   序列化
      - JSON.parse(str)        反序列化
      ```

2.  **转义**

      ```javascript
      - decodeURI( )            URl中未转义的字符
      - decodeURIComponent( )   URI组件中的未转义字符
      - encodeURI( )            URI中的转义字符
        - encodeURIComponent( )   转义URI组件中的字符
        - escape( )               对字符串转义
        - unescape( )             给转义字符串解码
        - URIError                由URl的编码和解码方法抛出
      ```

3.  **eval**

   ```javascript
   // JavaScript中的eval是Python中eval和exec的合集,既可以编译代码也可以获取返回值
   -eval() 
   -EvalError   // 执行字符串中的JavaScript代码
   ```

4.  **正则表达式**

   *定义正则表达式*

   ```javascript
   /.../  用于定义正则表达式
   /.../g 表示全局匹配
   /.../i 表示不区分大小写
   /.../m 表示多行匹配
   // JS正则匹配时本身就是支持多行,此处多行匹配只是影响正则表达式^和$,m模式也会使用^$来匹配换行的内容
   ```

   实例

   ```javascript
   var pattern = /^Java\w*/gm;
   var text = "JavaScript is more fun than \nJavaEE or JavaBeans!";
   result = pattern.exec(text)
   result = pattern.exec(text)
   result = pattern.exec(text)
   // 定义正则表达式也可以使用RegExp对象
   ```

   *匹配*

   JavaScript中主要提供了以下两个功能 : 

   - test(string)      检查字符串中是否和正则匹配

     ```javascript
     n = 'uui99sdf'
     reg = /\d+/
     reg.test(n)  ---> true
     // 只要正则在字符串中存在就匹配,如果想要开头和结尾匹配的话,就需要在正则前后加^和$
     ```

   - exec(string)      获取正则表达式匹配的内容 , 如果未匹配 , 值为null , 否则 , 获取匹配成功的数组

     ```javascript
     非全局模式
     // 获取匹配结果数组，注意：第一个元素是第一个匹配的结果，后面元素是正则子匹配（正则内容分组匹配）
     var pattern = /\bJava\w*\b/;
     var text = "JavaScript is more fun than Java or JavaBeans!";
     result = pattern.exec(text)
     var pattern = /\b(Java)\w*\b/;
     var text = "JavaScript is more fun than Java or JavaBeans!";
     result = pattern.exec(text)
     全局模式
     // 需要反复调用exec方法，来一个一个获取结果,直到匹配获取结果为null表示获取完毕
     var pattern = /\bJava\w*\b/g;
     var text = "JavaScript is more fun than Java or JavaBeans!";
     result = pattern.exec(text)
     var pattern = /\b(Java)\w*\b/g;
     var text = "JavaScript is more fun than Java or JavaBeans!";
     result = pattern.exec(text)
     ```

   字符串中相关方法

   ```javascript
   obj.search(regexp) // 获取索引位置,搜索整个字符串,返回匹配成功的第一个位置(g模式无效)
   obj.match(regexp)  // 获取匹配内容,搜索整个字符串,获取找到第一个匹配内容,如果正则是g模式找到全部
   obj.replace(regexp, replacement) //替换匹配替换,正则中有g则替换所有,否则只替换第一个匹配项
   // $数字：匹配的第n个组内容；
   // $&：当前匹配的内容；
   // $`：位于匹配子串左侧的文本；
   // $'：位于匹配子串右侧的文本
   // $$：直接量$符号
   ```

5.  **时间处理**

   Date对象用于处理日期和时间

   获取系统当前时间

   ```javascript
   var now = new Date();
   now; // Wed Jun 24 2015 19:49:22 GMT+0800 (CST)
   now.getFullYear(); // 2015, 年份
   now.getMonth(); // 5, 月份，注意月份范围是0~11，5表示六月
   now.getDate(); // 24, 表示24号
   now.getDay(); // 3, 表示星期三
   now.getHours(); // 19, 24小时制
   now.getMinutes(); // 49, 分钟
   now.getSeconds(); // 22, 秒
   now.getMilliseconds(); // 875, 毫秒数
   now.getTime(); // 1435146562875, 以number形式表示的时间戳
   // 注意当前时间是浏览器从本机操作系统获取的时间,所以不一定准确
   ```

   创建一个指定日期和时间的Date对象

   ```javascript
   var d = new Date(2015, 5, 19, 20, 15, 30, 123);
   d; // Fri Jun 19 2015 20:15:30 GMT+0800 (CST)
   ```

   第二中创建方式

   ```javascript
   var d = Date.parse('2015-06-24T19:49:22.875+08:00');
   d; // 1435146562875
   ```

   **PS : Date对象表示的时间总是按浏览器所在的时区显示的 , 我们可以进行调整 **

   ```javascript
   var d = new Date(1435146562875);
   d.toLocaleString(); // '2015/6/24 下午7:49:22'，本地时间（北京时区+8:00），显示的字符串与操作系统设定的格式有关
   d.toUTCString(); // 'Wed, 24 Jun 2015 11:49:22 GMT'，UTC时间，与本地时间相差8小时
   ```

更多JavaScript内容可以通过 , 以下链接学习 , [菜鸟教程](http://www.runoob.com/js/js-tutorial.html) , [廖雪峰官网教程](https://www.liaoxuefeng.com/wiki/001434446689867b27157e896e74d51a89c25cc8b43bdb3000) , [w3school](http://www.w3school.com.cn/js/index.asp)

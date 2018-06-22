# Web开发之路 - HTML-body

## 前言  🍀

为避免上一篇篇幅过长 , body部分在这一篇进行整理 , 主要介绍常用标签

## &lt; h &gt;  🍀

定义标题 , < h1 > ~ < h6 > , 标题从大到小

```html
<h1>标题一</h1>
<h2>标题二</h2>
<h3>标题三</h3>
<h4>标题四</h4>
<h5>标题五</h5>
<h6>标题六</h6>
```

## &lt; p &gt; and &lt; br &gt;   🍀

< p > 标签用于定义段落 , 默认段落之间是有间隔的 , 并且浏览器会自动地在段落前后添加空行(块级标签)

< br > 标签用于换行 , 即不产生一个新段落的情况下进行换行

```html
<p>这是第一个段落</p>
<p>这是第二个段落</p><br>
<p>这是第三个段落</p>
```

## &lt; b &gt; and &lt; i &gt;  🍀

定义文本粗体和斜体

```html
<b>我是粗体</b>
<i>我是斜体</i>
```

更多

```html
<u>我是下划线</u>
<s>我是删除线</s>
```

## &lt; ul &gt; &lt; ol &gt; &lt; dl &gt;  🍀

定义列表 , 区别如下 :

- ul , 无序列表
- ol , 有序列表
- li , 定义列表项
- dl , 自定义列表
- dt , 自定义列表项
- dd , 自定义列表项的描述

```html
<!-- 无序列表 -->
<ul>
<li>Coffee</li>
<li>Milk</li>
</ul>
<!-- 有序列表 -->
<ol>
<li>Coffee</li>
<li>Milk</li>
</ol>
<!-- 自定义列表 -->
<dl>
<dt>Coffee</dt>
<dd>- black hot drink</dd>
<dt>Milk</dt>
<dd>- white cold drink</dd>
</dl>
```

## &lt; select &gt;  🍀

定义下拉列表 , < select > 元素中的 < option > 标签定义了列表中的可用选项

```html
<!-- 仅显示1条信息的下拉框,单选 -->
<select>
  	<option value="1">上海</option>
  	<option value="2">北京</option>
  	<option value="3" selected="selected">广州</option> <!-- 设置默认选项 -->  
</select>
<!-- 显示2条信息,单选 -->
<select size="2">
  	<option value="1">上海</option>
  	<option value="2">北京</option>
  	<option value="3">广州</option>
  	<option value="3">武汉</option>
</select>
<!-- 显示2条信息,多选 -->
<select size="2" multiple="multiple">
  	<option value="1">上海</option>
  	<option value="2">北京</option>
  	<option value="3">广州</option>
  	<option value="3">武汉</option>
</select>
<!-- 禁用选项 -->
<select size="2">
  	<optgroup label="湖北省">
        <option>武汉</option>
        <option>湖里</option>
  	</optgroup>
    <optgroup label="河北省">
        <option>石家庄</option>
        <option>河里</option>
  	</optgroup>
</select>
```

## &lt; img &gt;  🍀

插入图像

< img > 是空标签 , 只包含属性 , 没有闭合标签 , 属性如下 :

- src , 源属性(source) , 值为图像的url地址
- alt , 定义图像的预备可替换文本 , 即无法载入图像时显示

```html
<!-- width和height则是宽度与高度属性 -->
<img src="pulpit.jpg" alt="Pulpit rock" width="304" height="228">
```

## &lt; table &gt;  🍀

定义表格 , 每个表格均有若干行(< tr > 标签定义) , 每行分为若干单元格(< td > 标签定义) , 以及表格的标头(由< th > 标签定义)

< table > 标签也可以用于页面的布局 , 用法与< div > 一样

```html
<table border="1">
    <tr>
        <td>row 1, cell 1</td>
        <td>row 1, cell 2</td>
    </tr>
    <tr>
        <td>row 2, cell 1</td>
        <td>row 2, cell 2</td>
    </tr>
</table>
```

## &lt; div &gt; and &lt; span &gt;  🍀

HTML可以通过< div > 和 < span >将元素组合起来

< div > 为块级标签 ; < span > 为内联标签 , 可以作文本的容器

块级标签与内联标签的区别 : 

- 块级标签是另起一行开始渲染 , 而行内联标签则不需要另起一行
- 单独在页面中插入这两个标签, 不会对页面产生任何影响 , 这两个标签是专门为定义CSS样式而生的

关于标签嵌套 : 通常块级标签可以包含内联标签或某些块级标签 ; 但是内联标签不能包含块级标签 , 它只能包含其他内联标签

```html
<div id="container" style="width:500px">
    <div id="header" style="background-color:steelblue;">
        <h1 style="margin-bottom:0;">Welcome To Lyon's Blog</h1>
    </div>
    <div id="menu" style="background-color:burlywood;height:200px;width:100px;float:left;">
        <b>菜单</b><br>
        HTML<br>
        CSS<br>
        JavaScript
    </div>
    <div id="content" style="background-color:#EEEEEE;height:200px;width:400px;float:left;">
    	Welcom to lyon's blog!
  	</div>
    <div id="footer" style="background-color:honeydew;clear:both;text-align:center;">
        版权 © Lyon.com
  	</div>
</div>
```

## &lt; form &gt;  🍀

< form >为表单标签 , 表单是一个包含表单元素的区域

表单元素允许用户在表单中输入内容 , 比如 : 文本域(textarea) , 下拉列表 , 单选框(radio-buttons) , 复选框(checkboxes)等 , 格式如下 :

```html
<form>
.
input 元素
.
<form
```

实例

```html
<!-- 用户名与密码 -->
<form>
username:<input type="text" name="username"><br>
password:<input type="password" name="pwd">
</form>
```

## &lt; input &gt;  🍀

< input >标签规定了用户可以在其中输入数据的输入字段 , 输入字段可以通过多种方式改变 , 取决于type属性

```html
<!-- 复选框 -->
湖北<input type="checkbox">
湖南<input type="checkbox" checked>
北京<input type="checkbox" checked="checked">
<!-- 单选框 -->
男<input type="radio" value="man">
女<input type="radio" value="male">
<br/><br/>
男<input type="radio"  name="gender" value="man">
女<input type="radio"  name="gender" value="male">
<!-- 密码框 -->
password:<input type="password" name="pwd">
<!-- 按钮 -->
<input type="button" value="Commit">
<!-- 文件 -->
<input type="file" name="img"> <!-- 提交文件时： enctype='multipart/form-data' method='POST' -->
```

以上简单的介绍了几个属性 , 更多input元素属性可以通过访问[W3school](http://www.w3school.com.cn/tags/tag_input.asp)进行学习  

## &lt; lable &gt;  🍀

< label > 标签为input元素定义标注(标记) 

lable元素不会向用户呈现任何特殊效果 , 不过当鼠标点击时 , 浏览器会自动将焦点转到和标签相关的表单控件上

标签的for属性应当与相关元素的id属性相同

```html
姓名：<input id='name1' type='text'/>
婚否：<input id='marriy1' type='checkbox'/>
<br/>
<label for='name2'>姓名：<input id='name2' type='text'></label>
<label for='marriy2'>婚否：<input id='marriy2' type='checkbox'></label>
```

## &lt; textarea &gt;  🍀

用于定义多行文本

可以通过`cols`和`rows`属性来规定textarea的尺寸 , 不过更好的办法是使用CSS的 `height`和`width`属性 

如果需要启动自动换行功能 , 可以通过设置`wrap`属性为`virtual`或`physical` 

```html
<textarea></textarea>
<textarea style='width:500px;height: 200px;'></textarea>
```

## &lt; fieldset &gt;  🍀

< fieldset >标签用于将表单内容的一部分打包 , 生成一组相关表单的字段 , 浏览器会以特殊方式来显示 , 它们可能有特殊的边界 , 3D效果 , 或者甚至可创建一个子表单来处理这些元素

< legend > 标签为fieldset元素定义标题

```html
<fieldset>
  	<legend>登录</legend>
  	<p>用户名：</p>
  	<p>密码：</p>
</fieldset>
```

更多[:dash:](http://www.w3school.com.cn/tags/tag_html.asp)
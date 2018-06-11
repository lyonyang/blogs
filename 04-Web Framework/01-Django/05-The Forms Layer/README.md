# Python之路 - Django之Forms

## 介绍  🍀

表单在网页中主要负责数据采集功能 , 比如我们可以利用表单来采集访问者的某些信息 , 例如 : 名字 , email地址 , 留言簿等等

Django提供了大量的工具和库来帮助我们构建表单来接收网站访问者的输入 , 然后处理以及响应输入

**HTML表单**

在HTML中 , 表单的作用是收集标签中的内容 , 即form标签中间可以由访问者添加类似于文本 , 选择 , 或者一些控制模块等等 , 然后这些内容将会被送到服务端

`<form>`与 `<input>` 元素一样 , 一个表单必须指定两样东西 : 

- where : 响应用户输入数据的URL
- how : 发送数据所使用的HTTP方式

例如 , Django Admin站点的登录表单包含如下几个元素 : 

- type="text" , 用户名
- type="password" , 密码
- type="submit" , 用于"Log in" 按钮

它还包含一些用户看不到的隐藏的文本字段 , Django使用他们来决定下一步的行为

它还告诉浏览器表单数据应该发往`<form>`元素的`action`属性指定的URL , 如 : `/admin/` 

而且应该使用`method`属性指定的HTTP机制来发送 , 即是使用GET还是POST

**GET和POST**

处理表单时只会用到POST和GET方法

Django的登录表单使用POST方法 , 在这个方法中浏览器组合表单数据 , 对它们进行编码以用于传输 , 将它们发送到服务器然后接收它的响应

mysite/myapp/views.py

```python
from django.shortcuts import render
from django.views.decorators import csrf
# 接收POST请求数据
def search_post(request):
    ctx ={}
    if request.POST:
        ctx['rlt'] = request.POST['q']
    return render(request, "post.html", ctx)
```

mysite/templates/post.html

```html
<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
<title>Lyon's Blog</title>
</head>
<body>
    <form action="/search-post" method="post">
        {% csrf_token %}
        <input type="text" name="q">
        <input type="submit" value="Submit">
    </form>
    <p>{{ rlt }}</p>
</body>
</html>
```

相反 , GET组合提交的数据为一个字符串 , 然后是用它来生成一个URL ; 这个URL将包含数据发送的地址以及数据的键和值 , 比如你在Django documentation中进行一次搜索 , 其将会生成一个URL `https://docs.djangoproject.com/search/?` 

mysite/myapp/views.py

```python
from django.http import HttpResponse
from django.shortcuts import render_to_response
# 表单
def search_form(request):
    return render_to_response('search_form.html')
# 接收请求数据
def search(request):  
    request.encoding='utf-8'
    if 'q' in request.GET:
        message = 'The content of your search is' + request.GET['q']
    else:
        message = 'The form is empty'
    return HttpResponse(message)
```

mysite/templates/get.html

```html
<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
<title>Lyon's Blog</title>
</head>
<body>
    <form action="/search" method="get">
        <input type="text" name="q">
        <input type="submit" value="搜索">
    </form>
</body>
</html>
```

POST和GET用于实现不同的目的

如果需要改变系统状态的请求应该使用POST , 如果不影响系统状态的请求则应该使用GET

GET还不适合密码表单 , 因为这意味着你的密码将出现在URL中, 以及浏览器的历史和服务器的日志中 , 而且都是以普通的文本格式 ; 它还不适合数据量大的表单和二进制数据 , 例如一张图片 ; 使用GET请求作为管理站点的表单具有安全隐患 : 攻击者很容易模拟表单请求来取得系统的敏感数据 

不过GET方式适合网页搜索这样的表单 , 因为这种表示一个GET请求的URL可以很容易地作为书签 , 分享和重新提交

## Forms In Django  🍀

Django的表单功能可以简化自动化大部分工作 , 而且还可以比大部分程序员自己所编写的代码更安全

Django会处理表单工作中的三个显著不同的部分 : 

- 准备数据 , 重构数据 , 以便下一步提交
- 为数据创建HTML表单
- 接收并处理客户端提交的表单和数据

这些我们可以自己手工编写来实现 , 但是Django可以帮你完成这些所有的工作

在一个Web应用中 , 表单可能指HTML中的`<form>` , 或者生成它的Django的[`Form`](https://docs.djangoproject.com/en/1.11/ref/forms/api/#django.forms.Form) , 或者提交时发送的结构化数据、或者这些部分的总和

**Django 的Form类**

表单系统的核心部分是Django的Form类 , Django的模型描述一个对象的逻辑结构 , 行为以及展现给我们的方式 , 与此类似 , Form类描述一个表单并决定它如何工作和展现

就将Model中的`ORM`一样 , 表单类的字段会映射到HTML的`<input>` 表单元素 (ModelForm通过一个Form映射模型类的字段到HTML表单的`<input>`元素 ; Django的Admin站点就是基于这个的)

表单的字段本身就是一个个的类 ; 它们管理表单数据 , 并在提交表单时执行验证

表单字段在浏览器中呈现给用户的是一个HTML的"小部件" , 即用户界面的一个片段

每个字段类型都有一个合适的默认 [Widget class](https://docs.djangoproject.com/en/1.11/ref/forms/widgets/) , 在我们需要时可以将其覆盖

## 实例化、处理和渲染  🍀

在Django中渲染一个对象时 , 我们通常 : 

1. 在视图中获得它 (例如 , 通过视图函数从数据库中获取)
2. 将它传递给模板上下文
3. 使用模板变量将它扩展为HTML标记

在模板中渲染表单和渲染其他类型的对象几乎一样 , 除了有几个比较例外

在模型实例不包含数据的情况下 , 在模板中对它做处理很少有什么用处 ; 但是渲染一个未填充的表单却是非常有意义的 , 我们希望用户去填充它 ; 所以当我们的视图中处理模型实例时  , 我们一般从数据库中获取它 , 当我们处理表单时  , 我们一般在视图中实例化它

当我们实例化表单时 , 我们可以选择让它为空还是预先填充它

## 构建一个表单  🍀

### HTML Form

如果我们想在自己的网站上创建一个简单的表单 , 以获取用户的名字 , 模板如下 :

```html
<form action="/your-name/" method="post">
    <label for="your_name">Your name: </label>
    <input id="your_name" type="text" name="your_name" value="{{ current_name }}">
    <input type="submit" value="OK">
</form>
```

这告诉浏览器以POST方式发送表单的数据到URL `/your-name/` , 它将显示一个"Your name"文本字段 , 以及一个"OK"按钮 , 如果模板上下文包含一个`your_name`变量 , 它将用于预填充`current_name`字段

你将需要一个视图来渲染这个包含HTML表单的模板 , 并提供合适的`current_name`字段

当表单提交时 , 发往服务器的POST请求将包含表单数据

这是一个非常简单的表单 , 实际应用中 , 一个表单可能包含几十上百个字段 , 其中大部分需要预填充 , 而且我们预料到用户将来回编辑 , 提交几次才能完成操作 ; 即使在提交表单之前 , 我们也可能需要在浏览器中进行一些验证 , 我们可能想要使用更复杂的字段 , 这样可以让用户做一些事情 , 例如从日历中选择日期等等 , 那么这个时候 , 让Django来为我们完成大部分工作是很容易的

### Django Form  🍀

上面我们已经构建好了一个HTML表单 , 那么现在我们就需要来构建一个Django表单了

```pyhotn
from django import forms
class NameForm(forms.Form):
	your_name = forms.CharField(label='Your name', max_length=100)
```

这个Form类仅仅定义了一个字段`your_name` , 字段允许的最大长度通过`max_length` 定义 , 它完成两件事情 ; 首先 , 它在HTML`<input>` 上放置一个`maxlength=100` , 这样浏览器将在第一时间阻止输入多于这个数目的字符 , 它还意味着当Django收到浏览器发送过来的表单时 , 它将验证数据的长度

Form的实例具有一个`is_valid()` 方法 , 它会为所有的字段执行验证程序 ; 如果所有的字段都包含有效的数据它将会返回True并且将表单的数据放到`cleaned_data`属性中

完整的表单 , 第一次渲染时 , 看上去将如下 : 

```python
<label for="your_name">Your name: </label>
<input id="your_name" type="text" name="your_name" maxlength="100" required />
```

注意 : 它不包含`<form>` 标签 , 以及提交按钮 , 所以我们必须自己在模板中提供它们

### 视图  🍀

发送回Django网站的表单数据由视图处理 , 通常是发布表单的相同视图 , 这允许我们重用一些相同的逻辑

views.py

```python
from django.shortcuts import render
from django.http import HttpResponseRedirect
from .forms import NameForm
def get_name(request):
    # if this is a POST request we need to process the form data
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = NameForm(request.POST)
        # check whether it's valid:
        if form.is_valid():
            # process the data in form.cleaned_data as required
            # ...
            # redirect to a new URL:
            return HttpResponseRedirect('/thanks/')

    # if a GET (or any other method) we'll create a blank form
    else:
        form = NameForm()

    return render(request, 'name.html', {'form': form})
```

如上 , 如果访问视图的是一个GET请求 , 它将创建一个空的表单实例并将它放置到要渲染的模板的上下文中 , 这是我们在第一次访问该URL时发生的事情

如果使用POST请求提交表单 , 该视图将再次创建一个表单实例 , 并使用请求中的数据填充表单 , 即`form = NameForm(request.POST)` 这种方式称为绑定 , 即将数据绑定到表单

我们调用`is_valid()`方法 ; 如果不是True , 也就是说我们的所有数据中存在不合法的项 , 那么它就会返回到HTML Form  , 也就是我们提交之前的位置 , 但是这个时候这个实例不是空的 (这一步是未绑定的) , HTML Form将使用前面提交合法的数据进行填充 , 而对于不合法的我们就可以对其进行编辑和修改

如果`is_valid()` 返回True , 我们就可以在`cleaned_data`属性中找到所有合法的表单数据 , 我们就可以使用这些数据去更新数据库或进行其他操作 , 然后将HTTP重定向发送给浏览器 , 告诉它下一步怎么走

### 模板  🍀

我们不需要在模板中做很多的工作 , 最简单的例子 : 

```html
<form action="/your-name/" method="post">
    {% csrf_token %}
    {{ form }}
    <input type="submit" value="Submit" />
</form>
```

这样我们就可以通过模板语言中的form变量将所有的form字段和属性都会打包为HTML中的form

**跨站请求伪造的防护**

Django原生支持一个简单易用的 [protection against Cross Site Request Forgeries](https://docs.djangoproject.com/en/1.11/ref/csrf/) , 当提交一个启用CSRF防护的POST表单时 , 你必须使用上面例子中的`csrf_token` 模板标签

HTML 5 输入类型和浏览器验证

如果你的表单包含`URLField` , `EmailField` 或其它整数字段类型 , Djanog将使用url , email 和 number这样的HTML 5 输入类型 ; 默认情况下 , 浏览器可能会对这些字段进行它们自身的验证 , 这些验证可能比Django的验证更严格 , 如果你想禁用这个行为 , 可以通过设置form标签的`novalidate` 属性 , 或者指定一个不同的字段 , 如`TextInput` 

## More about Django Form classes  🍀

所有的表单类都被创建为`django.forms.Form` 的子类 , 包括Django Admin中的 [ModelForm](https://docs.djangoproject.com/en/1.11/topics/forms/modelforms/) 

实际上 , 如果你的表单打算直接用来添加和编辑Django的模型 , [ModelForm](https://docs.djangoproject.com/en/1.11/topics/forms/modelforms/) 可以节省你的许多时间 , 精力和代码 , 因为它将根据Model类中构建一个表单以及相应的字段和属性

### 绑定和未绑定  🍀

绑定和未绑定的表单实例之间的区别如下 : 

- 未绑定的表单没有关联的数据 , 当渲染给用户时 , 它将为空或包含默认的值
- 绑定的表单具有提交的数据 , 因此可以用来检验数据是否合法 ,如果渲染一个不合法的绑定的表单 , 它将包含内联的错误信息 , 告诉用户如何纠正数据

表单的`is_bound` 属性将告诉你一个表示是否具有绑定的数据

### 字段  🍀

前面的例子中 , 我们仅使用了一个字段 , 当然字段还有很多 , 我们可以在 [Form fields](https://docs.djangoproject.com/en/1.11/ref/forms/fields/) 中找到完整的列表

### 窗口小部件  🍀

每个表单字段都有一个对应的 [Widget class](https://docs.djangoproject.com/en/1.11/ref/forms/widgets/) , 它对应一个HTML表单小部件 , 例如 : `<input type="text">` 

在大部分情况下 , 字段都具有一个合理的默认Widget , 例如 , 默认情况下 , `CharField`具有一个`TextInput` Widget , 它在HTML中生成一个`<input type="text">` 

```python
>>> from django import forms
>>> name = forms.TextInput(attrs={'size': 10, 'title': 'Your name',})
>>> name.render('name', 'A name')
'<input title="Your name" type="text" name="name" value="A name" size="10" required />'
```

### 字段数据  🍀

不管提交的是什么数据 , 一旦通过调用`is_valid()` 成功验证后 , 验证后的表单数据将位于`form.cleaned_data` 字典中 , 并且这些数据已经为你转换好Python类型

此时你依然可以从`request.POST` 中直接访问到未验证的数据 , 但是访问验证后的数据更好一些

```python
from django.core.mail import send_mail

if form.is_valid():
    subject = form.cleaned_data['subject']
    message = form.cleaned_data['message']
    sender = form.cleaned_data['sender']
    cc_myself = form.cleaned_data['cc_myself']

    recipients = ['info@example.com']
    if cc_myself:
        recipients.append(sender)

    send_mail(subject, message, sender, recipients)
    return HttpResponseRedirect('/thanks/')
```

有些字段类型需要一些额外的处理 , 例如 , 使用表单上传的文件需要不同地处理 (它们可以从`request.POST`获取 , 而不是`request.FILES` ) , 图和使用表单处理文件上传的更多细节 , 见[Binding uploaded files to a form](https://docs.djangoproject.com/en/1.11/ref/forms/api/#binding-uploaded-files)

关于Django中如何发送邮件的更多信息 , 见[Sending email](https://docs.djangoproject.com/en/1.11/topics/email/)

## 使用表单模板  🍀

### 表单渲染选项  🍀

对于`<input>/<label>` 来说 , 还有其他几个输出选项 : 

- form.as_table , 以表格的形式将他们渲染在`<tr>`标签中
- form.as_p , 将它们渲染在`<p>`标签中
- form.as_ul , 将它们渲染在`<li>`标签中

注意 , 我们必须自己提供`<ul>或<table>` 

实例

```html
# 实例输出{{ form.as_p }}
<p><label for="id_subject">Subject:</label>
    <input id="id_subject" type="text" name="subject" maxlength="100" required /></p>
<p><label for="id_message">Message:</label>
    <textarea name="message" id="id_message" required></textarea></p>
<p><label for="id_sender">Sender:</label>
    <input type="email" name="sender" id="id_sender" required /></p>
<p><label for="id_cc_myself">Cc myself:</label>
    <input type="checkbox" name="cc_myself" id="id_cc_myself" /></p>
```

### 手动渲染字段  🍀

我们不必让Django打开表单的字段 , 如果我们想要 , 我们也可以手动执行 (例如 , 允许我们重新排序字段) , 每个字段都是表单的一个属性 , 可以使用

```html
{{ form.name_of_field }}
```

来访问 , 并将在Django模板中正确地渲染 , 如下 : 

```html
<- 查找每个字段的错误 -> 
{{ form.non_field_errors }}
<div class="fieldWrapper">
    {{ form.subject.errors }}
    <label for="{{ form.subject.id_for_label }}">Email subject:</label>
    {{ form.subject }}
</div>
<div class="fieldWrapper">
    {{ form.message.errors }}
    <label for="{{ form.message.id_for_label }}">Your message:</label>
    {{ form.message }}
</div>
<div class="fieldWrapper">
    {{ form.sender.errors }}
    <label for="{{ form.sender.id_for_label }}">Your email address:</label>
    {{ form.sender }}
</div>
<div class="fieldWrapper">
    {{ form.cc_myself.errors }}
    <label for="{{ form.cc_myself.id_for_label }}">CC yourself?</label>
    {{ form.cc_myself }}
</div>
```

完整的`<label>` 元素还可以使用`label_tag()` 生成

```html
<div class="fieldWrapper">
    {{ form.subject.errors }}
    {{ form.subject.label_tag }}
    {{ form.subject }}
</div>
```

### 渲染表单错误信息  🍀

对于错误信息 , Django已经帮我们处理好了 , 如下我们将自己处理每个字段的错误和表单整体的各种错误

```html
<- 使用{{ form.name_of_filed.errors }}显示表单错误的一个清单,并渲染成一个ul ->
<ul class="errorlist">
    <li>Sender is required.</li>
</ul>
```

这个ul有一个`errorlist` CSS class , 你可以用它来定义外观

### field属性  🍀

```html
{{ field.label }}
<- 
The label of the field, e.g. Email address.
->
  
{{ field.label_tag }}
<- 
The field’s label wrapped in the appropriate HTML <label> tag. This includes the form’s label_suffix. For example, the default label_suffix is a colon:
  
<label for="id_email">Email address:</label>
->
  
{{ field.id_for_label }}
<- 
The ID that will be used for this field (id_email in the example above). If you are constructing the label manually, you may want to use this in lieu of label_tag. It’s also useful, for example, if you have some inline JavaScript and want to avoid hardcoding the field’s ID.
->
  
{{ field.value }}
<-
The value of the field. e.g someone@example.com.
->
  
{{ field.html_name }}
<-
The name of the field that will be used in the input element’s name field. This takes the form prefix into account, if it has been set.
->
  
{{ field.help_text }}
<-
Any help text that has been associated with the field.
->
  
{{ field.errors }}
<-
Outputs a <ul class="errorlist"> containing any validation errors corresponding to this field. You can customize the presentation of the errors with a {% for error in field.errors %} loop. In this case, each object in the loop is a simple string containing the error message.
->
  
{{ field.is_hidden }}
<-
This attribute is True if the form field is a hidden field and False otherwise. It’s not particularly useful as a template variable, but could be useful in conditional tests such as:
{% if field.is_hidden %}
   {# Do something special #}
{% endif %}
->
  
{{ field.field }}
<-
The Field instance from the form class that this BoundField wraps. You can use it to access Field attributes, e.g. {{ char_field.field.max_length }}.
->
```

完整的属性和方法列表 , 见[`BoundField`](https://docs.djangoproject.com/en/1.11/ref/forms/api/#django.forms.BoundField) 

### 循环隐藏和可见的字段  🍀

如果你在模板中手动布局一个表单 , 而不是依赖Django的默认表单布局 , 你可能会想要用不同于非隐藏的字段来处理不同的字段 ; 例如 , 因为隐藏的字段不显示任何内容 , 将错误信息放在 "旁边" 可能会引起用户的混淆 , 因此这些字段的错误应该以不同的方式处理

Django提供了两种方法 , 让你可以独立地遍历隐藏和可见字段 : `visible_fields()`和`hidden_fields()` , 如下 :

```html
{# Include the hidden fields #}
{% for hidden in form.hidden_fields %}
{{ hidden }}
{% endfor %}
{# Include the visible fields #}
{% for field in form.visible_fields %}
    <div class="fieldWrapper">
        {{ field.errors }}
        {{ field.label_tag }} {{ field }}
    </div>
{% endfor %}
```

这个示例没有处理隐藏字段中的任何错误信息 , 通常 , 隐藏字段中的错误意味着表单被篡改 , 因为正常的表单填写不会改变他们

### 可重用表单模板  🍀

如果你的网站在多个地方对表单使用相同的渲染逻辑 , 你可以保存表单的循环到一个单独的模板来减少重复 , 然后在其他模板中使用`include` 标签来重用它 : 

```html
# In your form template:
{% include "form_snippet.html" %}

# In form_snippet.html:
{% for field in form %}
    <div class="fieldWrapper">
        {{ field.errors }}
        {{ field.label_tag }} {{ field }}
    </div>
{% endfor %}
```

如果传递到模板上写问中的表单对象具有一个不同的名称 , 你可以使用`include`标签的with参数来给它起个别名 : 

```html
{% include "form_snippet.html" with form=comment_form %}
```

上面只是一些基础 , 表单还可以完成更多的工作 , 更多内容见 : [The Forms Reference](https://docs.djangoproject.com/en/1.11/ref/forms/) 
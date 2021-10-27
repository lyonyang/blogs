# Django - Template Language








<extoc></extoc>

## 介绍

模板只是一个文本文件 , 它能够生成以下文本格式的文件 , 如 : HTML , XML , CSV , etv等

下面是一个简单的基本模板 , 每个元素将在本文后面解释

```html
{% extends "base_generic.html" %}
{% block title %}{{ section.title }}{% endblock %}
{% block content %}
<h1>{{ section.title }}</h1>
{% for story in story_list %}
<h2>
  <a href="{{ story.get_absolute_url }}">
    {{ story.headline|upper }}
  </a>
</h2>
<p>{{ story.tease|truncatewords:"100" }}</p>
{% endfor %}
{% endblock %}
```

**模板包括在使用时会被替换掉的变量 , 以及控制模板逻辑的标签**

## 变量

**定义变量**

变量名称由字母数字和下划线组成 ,  `"."和"_"` 也可以出现在变量部分 ; 变量名中不能有空格或标点符号

```html
{{ variable }}
```

实例

```html
My first name is {{ first_name }}. My last name is {{ last_name }}.
```

在上下文中 ,  `{'first_name': 'John', 'last_name': 'Doe'}` , 将呈现如下效果 : 

```html
My first name is John. My last name is Doe.
```

字典查找 , 属性查找和列表索引查找用 "." 号实现 :

```html
{{  my_dict.key  }} 
{{  my_object.attribute  }} 
{{  my_list.0  }}
```

当模板系统遇到 "." 时 , 会按照以下顺序进行查找 : 

- Dictionary lookup
- Attribute or method lookup
- Numeric index lookup

如果结果值是可调用的 , 它将不使用参数进行调用 , 而调用的结果则成为模板值

这个查找顺序可能会导致一些无法预料的行为 , 这些对象覆盖了字典查找 , 如下 : 

```html
{% for k, v in defaultdict.iteritems %}
    Do something with k and v here...
{% endfor %}
# 由于字典查找首先发生,该行为将启动并提供一个默认值,而不是使用预期的iteritems()方法,在这种情况下,我们应该考虑先转换成字典
```

## 过滤器

可以通过过滤器来修改变量的显示 , 使用 "|" 来应用过滤器

**单个过滤器**

```html
# 将文本转换为小写
{{ name|lower}}
```

**链接过滤器**

```html
# 转义文本内容,将换行符转换为p标签
{{ text|escape|linebreaks}}
```

**带参数过滤器**

```html
# 显示bio变量的前30个单词
{{ bio|truncatewords:30 }}
# 过滤器参数中包含空格的必须被引用,用逗号和空格连接列表
{{ list|join:", "}}
```

Django中提供了大约60个内置的模板过滤器 , 以下是一些常用的模板过滤器 :

- default : 如果一个变量是错误或者为空 , 则使用默认给定的 , 否则就使用变量的值

```html
{{ value|default:"nothing"}}
```

- length : 返回值的长度 , 适用于字符串和列表

```html
{{ value|length}}
```

- filesizeformat : 格式化值为一个人们可读的文件大小 , 如 : '13KB' , '4.1MB' , '102bytes'等

```html
{{ value|filesizeformat}}
# value = 123456789
# output : 117.7MB
```

更多内置过滤器 :  [built-in filter reference](https://docs.djangoproject.com/en/1.10/ref/templates/builtins/#ref-templates-builtins-filters)

## 标签

标签比变量更复杂 : 标签可以在输出中创建文本 ; 执行循环或逻辑控制 ; 将外部信息加载到模板中以供以后的变量使用

**定义标签**

```html
{% tag %}
```

Django附带大约二十个内置模板标签 , 以下是一些常用标签 : 

- for : 遍历数组中的每个项目

```html
# 展示运动员名单
<ul>
  {% for athlete in athlete_list %}
    <li>{{ athlete.name }}</li>
  {% endfor %}
</ul>
```

- for ... empty : 当给出的组为空或者没有被找到时 , 所执行的操作

```html
{% for person in person_list %}
    <p>{{ person.name }}</p>
{% empty %}
    <p>sorry,no person here</p>
{% endfor %}
```

- if , elif 和else : 流程控制

```html
{% if athlete_list %}
    Number of athletes: {{ athlete_list|length }}
{% elif athlete_in_locker_room_list %}
    Athletes should be out of the locker room soon!
{% else %}
    No athletes.
{% endif %}
```

使用过滤器和各种操作符

```html
{% if athlete_list|length > 1 %}
    Team: {% for athlete in athlete_list %} ... {% endfor %}
{% else %}
    Athlete: {{ athlete_list.0.name }}
{% endif %}
```

**注意 : 大多数模板的过滤器返回字符串 , 所以使用过滤器在数学上通常不会像所期望的那样工作 , length是一个列外**

**block和extends**

这两个标签用户设置模板继承 , 这是一种在模板中减少 "样板" 的强大方法 , 见下文

内置标签参考 : [built-in tag reference](https://docs.djangoproject.com/en/1.10/ref/templates/builtins/#ref-templates-builtins-tags) 

自定义模板标签和过滤器 : [Custom template tags and filters](https://docs.djangoproject.com/en/1.10/howto/custom-template-tags/)

## 注释

要在模板中注释行的一部分 , 可以使用注释语法 : 

```html
# 单行注释
{# ... #}
# 多行注释
{% comment %}
...
{% endcomment %}
```

## 模板继承

Django模板引擎中最强大 , 也是最复杂的部分是模板继承 , 模板继承允许你创建一个基本 "框架" 模板 , 其中包含网站所有常用元素 , 并定义子模板可以覆盖的块

base.html

```html
<!DOCTYPE html>
<html lang="en">
<head>
    <link rel="stylesheet" href="style.css" />
    <title>{% block title %}My amazing site{% endblock %}</title>
</head>
<body>
    <div id="sidebar">
        {% block sidebar %}
        <ul>
            <li><a href="/">Home</a></li>
            <li><a href="/blog/">Blog</a></li>
        </ul>
        {% endblock %}
    </div>

    <div id="content">
        {% block content %}{% endblock %}
    </div>
</body>
</html>
```

上面定义了一个简单的HTML框架文档 , 在这个例子中 , `block`标签定义了三个子模板可以填充的块 , 所有的`block` 标签都告诉模板引擎一个子模板可以覆盖模板的哪些部分

子模板可能如下所示 : 

```html
{% extends "base.html" %}

{% block title %}My amazing blog{% endblock %}

{% block content %}
{% for entry in blog_entries %}
    <h2>{{ entry.title }}</h2>
    <p>{{ entry.body }}</p>
{% endfor %}
{% endblock %}
```

`extends` 标签用于告诉模板引擎 , 该模板扩展了另一个模板 , 当模板系统执行这个模板时 , 首先会找到父模板 , 也就是这里的`base.html` 

于是 , 模板引擎就将block标签中的内容替换`base.html` 中block标签中的内容 , 根据`blog_entries` 的值 , 输出可能如下 : 

```html
<!DOCTYPE html>
<html lang="en">
<head>
    <link rel="stylesheet" href="style.css" />
    <title>My amazing blog</title>
</head>
<body>
    <div id="sidebar">
        <ul>
            <li><a href="/">Home</a></li>
            <li><a href="/blog/">Blog</a></li>
        </ul>
    </div>
    <div id="content">
        <h2>Entry one</h2>
        <p>This is my first entry.</p>
        <h2>Entry two</h2>
        <p>This is my second entry.</p>
    </div>
</body>
</html>
```

在子模板中为定义的块 , 会使用父模板中的块 , 也就是说 , 没有定义则以父模板作为备用

为了增加可读性 , 可以给标签进行命名 , 如下 : 

```html
{% block content %}
...
{% endblock content %}
```

## 自动HTML转义

为了避免变量值中带有的HTML字符被解析 , 我们有两种方式 : 

1. 将潜在有害的HTML字符转换为无害的字符 , 这种方式会把责任放在我们身上 , 需要我们自己来逃避数据 , 所以明显这不够安全 ; 这也是Django头几年的默认解决方案
2. 利用Django的自动HTML转义

默认情况下 , 在Django中 , 每个模板都会自动转义每个变量标签的输出 , 具体来说 , 以下五个字符是会被转义的 : 

- < 被转换成`&lt;` 
- \> 被转换成`&gt;` 
- ' (单引号) 转换为`&#39;` 
- " (双引号) 转换为`&quot;` 
- & 被转换为`&amp;` 

**注意 : 这种行为默认是开启的**

**关闭自动HTML转义**

> 对于个人变量

使用safe过滤器 : 

```html
# 会被转义
This will be escaped: {{ data }}
# 不会被转义
This will not be escaped: {{ data|safe }}
```

data中包含`<b>` , 结果如下 : 

```html
This will be escaped: &lt;b&gt;
This will not be escaped: <b>
```

> 对于模板块

使用`autoscape`标签 :  

```html
{% autoescape off %}
    Hello {{ name }}
{% endautoescape %}
```

`autoscape`标签接收两个参数 , on和off , 如下 : 

```html
Auto-escaping is on by default. Hello {{ name }}
{% autoescape off %}
    This will not be auto-escaped: {{ data }}.
    Nor this: {{ other_data }}
    {% autoescape on %}
        Auto-escaping applies again: {{ name }}
    {% endautoescape %}
{% endautoescape %}
```

自动转义标记将其影响传递到扩展当前的模板和包含通过include标记的模板 , 如下 : 

base.html

```html
{% autoescape off %}
<h1>{% block title %}{% endblock %}</h1>
{% block content %}
{% endblock %}
{% endautoescape %}
```

child.html

```html
{% extends "base.html" %}
{% block title %}This &amp; that{% endblock %}
{% block content %}{{ greeting }}{% endblock %}
```

呈现如下 : 

```html
<h1>This &amp; that</h1>
<b>Hello!</b>
```
自定义标签和过滤器 :

https://docs.djangoproject.com/en/1.10/howto/custom-template-tags/

https://docs.djangoproject.com/en/1.10/ref/templates/language/#custom-tag-and-filter-libraries

更多Template Language相关 : https://docs.djangoproject.com/en/1.10/ref/templates/language/

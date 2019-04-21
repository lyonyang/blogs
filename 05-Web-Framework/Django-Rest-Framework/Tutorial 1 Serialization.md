# Tutorial 1: Serialization

## 介绍   🍀

本教程将会通过一些简单的代码来实现 Web API. 这个过程将会介绍 `REST framework` 的各个组件, 带你深入理解各个组件是如何一起工作

## 创建一个新的环境   🍀

为了确保我们的包配置与我们正在进行的其他项目保持良好的隔离 , 我们将使用 `virtualenv` 来创建一个新的虚拟环境

```shell
virtualenv env
source env/bin/activate
```

在新的虚拟环境中安装 `django`  与 `django rest framework` 

```shell
pip install django
pip install djangorestframework
pip install pygments  # 我们将使用这个模块来提高代码高亮
```

友情链接 : [`virtualenv`](https://virtualenv.pypa.io/en/stable/)  , [`pygments`](http://pygments.org/) 

## 开始   🍀

首先我们创建一个新的项目

```shell
cd ~
django-admin.py startproject tutorial
cd tutorial
```

创建应用 `snippets` 

```shell
python manage.py startapp snippets
```

配置应用

```python
INSTALLED_APPS = [
    ...
    'rest_framework',
    'snippets.apps.SnippetsConfig',
]
```

## 创建一个Model   🍀

我们首先创建一个简单的模型

```python
from django.db import models
from pygments.lexers import get_all_lexers
from pygments.styles import get_all_styles

# get_all_lexers() 返回所有的词法分析器
LEXERS = [item for item in get_all_lexers() if item[1]]

# 语言类别
LANGUAGE_CHOICES = sorted([(item[1][0], item[0]) for item in LEXERS])

# get_all_styles() 返回所有样式的名称
STYLE_CHOICES = sorted((item, item) for item in get_all_styles())


class Snippet(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    title = models.CharField(max_length=100, blank=True, default='')
    code = models.TextField()
    linenos = models.BooleanField(default=False)
    language = models.CharField(choices=LANGUAGE_CHOICES, default='python', max_length=100)
    style = models.CharField(choices=STYLE_CHOICES, default='friendly', max_length=100)

    class Meta:
        ordering = ('created',)
```

我们还需要为我们的代码片段模型创建一个初始迁移 , 并第一次同步数据库

```shell
python manage.py makemigrations snippets
python manage.py migrate
```

## 创建一个序列化类   🍀

我们在Web API上首先需要做的一件事是提供一种将 `Snippet` 实例序列化和反序列化的方法 , 使之成为诸如`json`之类的表示形式的方式

我们可以通过声明与Django的表单非常相似的序列化器 `(serializer)` 来做到这一点

在 `snippets` 目录中创建 `serializers.py` , 内容如下 : 

```python
from rest_framework import serializers
from snippets.models import Snippet, LANGUAGE_CHOICES, STYLE_CHOICES


class SnippetSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    title = serializers.CharField(required=False, allow_blank=True, max_length=100)
    code = serializers.CharField(style={'base_template': 'textarea.html'})
    linenos = serializers.BooleanField(required=False)
    language = serializers.ChoiceField(choices=LANGUAGE_CHOICES, default='python')
    style = serializers.ChoiceField(choices=STYLE_CHOICES, default='friendly')

    def create(self, validated_data):
        """
        根据已验证的数据,创建并返回一个新的 Snippet 实例
        """
        return Snippet.objects.create(**validated_data)

    def update(self, instance, validated_data):
        """
        根据已验证的数据,更新并返回一个新 Snippet 实例
        """
        instance.title = validated_data.get('title', instance.title)
        instance.code = validated_data.get('code', instance.code)
        instance.linenos = validated_data.get('linenos', instance.linenos)
        instance.language = validated_data.get('language', instance.language)
        instance.style = validated_data.get('style', instance.style)
        instance.save()
        return instance
```

序列化器类分为两个部分 : 

- 第一部分定义了序列化/反序列化的字段
- 第二部分 `create()` 和 `update()` 方法定义了当调用 `serializer.save()` 时如何创建或修改实例

序列化器类与Django Form类非常相似 , 并且在各个字段中包含相似的验证标志 , 例如 `required` , `max_length` , `default` 等

另外 , 在某些情况下字段标志还可以控制序列化器如何显示 , 比如渲染到HTML时 ,  `{'base_template': 'textarea.html'}` 等同于Django `Form`  类中的  `widget=widgets.Textarea` , 这对于控制如何显示可浏览的API特别有用 , 我们将在后面的教程中看到

我们还可以通过使用 `ModelSerializer` (`相当于ModelForm`) 类来节省一些时间 , 稍后我们将会看到 , 但是现在我们将显式的定义序列化器

## 使用序列化器   🍀

在我们进一步讨论之前 , 我们将熟悉使用新的序列化器类 , 让我们先进入 `Django shell` 

```python
python manage.py shell
```

那么接下来我们将在 `shell` 中创建几个 `Snippet` 实例一起工作

```python
# 导入相关依赖
from snippets.models import Snippet
from snippets.serializers import SnippetSerializer
from rest_framework.renderers import JSONRenderer
from rest_framework.parsers import JSONParser

snippet = Snippet(code='foo = "bar"\n')
snippet.save()

snippet = Snippet(code='print "hello, world"\n')
snippet.save()
```

现在我们已经有一些实例了 , 让我们看一看如何将实例序列化

注 : Model  →  Serialiezer

```python
serializer = SnippetSerializer(snippet)
serializer.data
# {'id': 2, 'title': '', 'code': 'print "hello, world"\n', 'linenos': False, 'language': 'python', 'style': 'friendly'}
```

现在我们将模型实例 (model instance) 转化成Python原生数据类型 , 为了完成实例化过程 ,  我们将数据渲染成 `json`

注 : Serialiezer  →  JSON

```python
content = JSONRenderer().render(serializer.data)
content
# '{"id":2,"title":"","code":"print \\"hello, world\\"\\n","linenos":false,"language":"python","style":"friendly"}'
```

反序列化是相似的 , 首先我们将流 `(stream)` 解析成Python原生数据类型…

```python
from django.utils.six import BytesIO

stream = BytesIO(content)
data = JSONParser().parse(stream)
```

然后, 我们将Python原生数据恢复成正常的对象实例

注 : JSON  →  Serialiezer

```python
serializer = SnippetSerializer(data=data)
serializer.is_valid()
# True
serializer.validated_data
# OrderedDict([('title', ''), ('code', 'print "hello, world"\n'), ('linenos', False), ('language', 'python'), ('style', 'friendly')])
serializer.save()
# <Snippet: Snippet object>
```

请注意 , API和表单很相似 . 当我们用我们的序列器 (serializer) 写视图的时候 , 相似性会更明显.

除了将模型模型实例 (model instance) 序列化外 , 我们也能序列化查询集 (querysets) , 只需要添加一个序列化参数 `many=True`

```python
serializer = SnippetSerializer(Snippet.objects.all(), many=True)
serializer.data
# [OrderedDict([('id', 1), ('title', u''), ('code', u'foo = "bar"\n'), ('linenos', False), ('language', 'python'), ('style', 'friendly')]), OrderedDict([('id', 2), ('title', u''), ('code', u'print "hello, world"\n'), ('linenos', False), ('language', 'python'), ('style', 'friendly')]), OrderedDict([('id', 3), ('title', u''), ('code', u'print "hello, world"'), ('linenos', False), ('language', 'python'), ('style', 'friendly')])]
```

## 使用ModelSerializers   🍀

我们的 `SnippetSerializer` 类复制了 `Snippet` 模型中的许多信息 , 如果我们能让代码更简洁一些 , 那就太好了

就像Django提供了 `Form` 类和 `ModelForm` 类一样 , `REST` 框架也有 `Serializer` 类和 `ModelSerializer` 类

让我们使用 `ModelSerializer` 类重构我们的序列化器

```python
class SnippetSerializer(serializers.ModelSerializer):
    class Meta:
        model = Snippet
        fields = ('id', 'title', 'code', 'linenos', 'language', 'style')
```

序列化器有一个很好的特性 , 就是你可以通过打印序列实例的结构 (representation) 查看它的所有字段 . 输入 `python manage.py shell` 打开Django shell , 尝试如下代码 :

```python
from snippets.serializers import SnippetSerializer
serializer = SnippetSerializer()
print(repr(serializer))
# SnippetSerializer():
#    id = IntegerField(label='ID', read_only=True)
#    title = CharField(allow_blank=True, max_length=100, required=False)
#    code = CharField(style={'base_template': 'textarea.html'})
#    linenos = BooleanField(required=False)
#    language = ChoiceField(choices=[('Clipper', 'FoxPro'), ('Cucumber', 'Gherkin'), ('RobotFramework', 'RobotFramework'), ('abap', 'ABAP'), ('ada', 'Ada')...
#    style = ChoiceField(choices=[('autumn', 'autumn'), ('borland', 'borland'), ('bw', 'bw'), ('colorful', 'colorful')...
```

要记住 , `ModelSerializer` 类没有做任何神奇的事情 , 它们只是创建序列化器类的快捷方式 : 

- 一组自动确定的字段
- 简单默认实现的 `create()` 和 `update()` 方法

## 用序列化器写常规的Django视图   🍀

让我们看看如何使用我们的序列化器类来编写一些API视图 , 目前 , 我们不会使用REST框架的其他特性 , 只是写一些常规的Django视图

编辑 `snippets/views.py` :

```python
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.renderers import JSONRenderer
from rest_framework.parsers import JSONParser
from snippets.models import Snippet
from snippets.serializers import SnippetSerializer
```

我们的根API将会是一个视图 , 它支持列出所有现有的 `snippets` , 或者创建一个新的 `snippets` 

```python
@csrf_exempt
def snippet_list(request):
    """
    列出所有的 snippets,或者创建一个新的 snippet.
    """
    if request.method == 'GET':
        snippets = Snippet.objects.all()
        serializer = SnippetSerializer(snippets, many=True)
        return JsonResponse(serializer.data, safe=False)

    elif request.method == 'POST':
        data = JSONParser().parse(request)
        serializer = SnippetSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, status=201)
        return JsonResponse(serializer.errors, status=400)
```

注意 , 因为我们希望能够从没有CSRF令牌的客户端 `POST` 数据到这个视图 , 所以我们需要将视图标记为 `csrf_exempt` , 通常我们是不会这样做 , `REST` 框架视图使用了比这更合理的方式 , 不过那不是我们现在的目的

我们还需要一个视图对应单个 `snippet` , 并且我们可以使用这个视图进行检索 , 更新或删除 `snippet` 

```python
@csrf_exempt
def snippet_detail(request, pk):
    """
    检索、更新或删除 snippet.
    """
    try:
        snippet = Snippet.objects.get(pk=pk)
    except Snippet.DoesNotExist:
        return HttpResponse(status=404)

    if request.method == 'GET':
        serializer = SnippetSerializer(snippet)
        return JsonResponse(serializer.data)

    elif request.method == 'PUT':
        data = JSONParser().parse(request)
        serializer = SnippetSerializer(snippet, data=data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data)
        return JsonResponse(serializer.errors, status=400)

    elif request.method == 'DELETE':
        snippet.delete()
        return HttpResponse(status=204)
```

最后 , 我们需要使用路由将这些视图对应起来 , 创建 `snippets/urls.py` 文件

```python
from django.conf.urls import url
from snippets import views

urlpatterns = [
    url(r'^snippets/$', views.snippet_list),
    url(r'^snippets/(?P<pk>[0-9]+)/$', views.snippet_detail),
]
```

同时需要配置 `tutorial/urls.py` , 添加我们的 `snippet` 应用的 `URLs`

```python
from django.conf.urls import url, include

urlpatterns = [
    url(r'^', include('snippets.urls')),
]
```

值得注意的是 , 我们目前还有一些边界情况没有进行处理 , 如果我们发送错误的 `json` 数据 , 或者一个请求是用一个视图无法处理的方法进行的 , 那么我们将得到一个500的错误 , `“Server Error”` 

## 测试我们的API   🍀

首先退出 `shell` 

```shell
quit()
```

随后启动Django开发服务器

```shell
python manage.py runserver

Validating models...

0 errors found
Django version 1.11, using settings 'tutorial.settings'
Development server is running at http://127.0.0.1:8000/
Quit the server with CONTROL-C.
```

在另一个终端窗口中 , 我们可以来测试这个服务器

我们可以使用 `curl` , 或者 `httpie` , `Httpie` 是一个使用Python编写的对用户友好的http客户端 , 让我们安装它 (虽然上一章节中已经说明过)

```python
pip install httpie
```

我们可以获取 `snippets` 列表

```shell
http http://127.0.0.1:8000/snippets/

HTTP/1.0 200 OK
...

[
    {
        "code": "foo = \"bar\"\n",
        "id": 1,
        "language": "python",
        "linenos": false,
        "style": "friendly",
        "title": ""
    },
    {
        "code": "print \"hello, world\"\n",
        "id": 2,
        "language": "python",
        "linenos": false,
        "style": "friendly",
        "title": ""
    },
]
```

我们也可以指定 `id` 获取响应 `snippet` 

```shell
http http://127.0.0.1:8000/snippets/2/

HTTP/1.0 200 OK
...

{
    "code": "print \"hello, world\"\n",
    "id": 2,
    "language": "python",
    "linenos": false,
    "style": "friendly",
    "title": ""
}
```

类似地 , 我们也可以使用浏览器访问获得相同的 `json` 数据

到目前为止 , 我们做得很好 , 我们编写的序列化 `API` 和 `Django's Forms API` 比较相似 , 同时编写了一些常规的Django视图.

我们的 `API` 没有做什么特殊的事情 , 除了作出json响应外 , 还有一些边缘事件没有处理 , 但至少是一个还有点功能的 `Web API`.

在教程的第2部分 , 我们将介绍如何对我们的 `API` 进行改进.








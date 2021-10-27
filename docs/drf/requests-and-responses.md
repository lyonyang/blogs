# Tutorial 2: Requests and Responses

从这节开始, 我们会接触到 `REST` 框架的核心. 让我们介绍一些基本构建组件








<extoc></extoc>

## Request对象

`REST framework` 引入了一个 `Request` 对象 , 它扩展了常规的 `HttpRequest` , 并提供了灵活的请求解析 .  `Request` 对象的核心功能是 `request.data` 属性 , 它和 `request.POST` 属性很相似 , 但是它对 `Web APIs` 更加有用

```python
request.POST  # 只处理表单数据,仅用于 'POST' 方法.
request.data  # 处理任意数据,可以用于 'POST', 'PUT' 和 'PATCH' 方法.
```

## Response对象

`REST framework` 也引入了 `Response` 对象 , 它是一类用为渲染和使用内容协商来决定返回给客户端的正确内容类型的 `TemplateResponse ` 

```python
return Response(data)  # 按照客户的需求类型来渲染内容
```

## 状态码

在视图中使用HTTP状态码并不总是易读的 , 错误代码很容易被忽略 .  `REST framework` 为每一个状态码提供了更明确的标识符，例如状态模块中的  `HTTP_400_BAD_REQUEST`  , 使用这些标识符代替纯数字标识符是一个不错的注意

## 装饰API视图

`REST framework` 提供了两个装饰器来编写API视图

1.  `@api_view` , 用于 `FBV (function based view)` 
2.  `APIView` , 用于 `CBV (class-based view)` 

这些装饰器提供了一些功能 , 例如确保从你的视图中获取 `Request` 对象 , 以及在 `Response` 对象中添加上下文

同时还提供一些行为 , 例如在合适的时候返回 `405 Method Not Allowed` 响应 , 例如处理在访问错误输入的 `request.data` 时出现的 `ParseError` 异常

## 协同工作

好了 , 让我们开始使用这些新组件来写一些视图吧

在 `views.py` 中我们不再需要 `JSONResponse` 类 , 现在删除它们 , 我们可以轻微地重构我们的视图

```python
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from snippets.models import Snippet
from snippets.serializers import SnippetSerializer


@api_view(['GET', 'POST'])
def snippet_list(request):
    """
    列出所有的 snippets,或者创建一个新的 snippet.
    """
    if request.method == 'GET':
        snippets = Snippet.objects.all()
        serializer = SnippetSerializer(snippets, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        serializer = SnippetSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
```

我们的实例视图是前面的修改版 , 更简洁 , 和我们使用的 `Form API` 很相似 , 同时使用了命名状态码 , 让响应代码意义更明显

下面是 `views.py` 中单个 `snippet` 的视图

```python
@api_view(['GET', 'PUT', 'DELETE'])
def snippet_detail(request, pk):
    """
    检索、更新或删除 snippet.
    """
    try:
        snippet = Snippet.objects.get(pk=pk)
    except Snippet.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = SnippetSerializer(snippet)
        return Response(serializer.data)

    elif request.method == 'PUT':
        serializer = SnippetSerializer(snippet, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        snippet.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
```

这应该是非常熟悉的 , 与常规的Django视图并没有太多的不同

请注意 , 我们不再明确指定请求或响应的上下文类型 ,  `request.data` 可以处理的 `json` 格式的请求 , 同样也可以处理其他格式 . 同样的 , 我们允许 `REST framework` 将响应对象的数据渲染成正确的内容类型返回给客户端

## 在URLs中添加可选格式后缀

为了充分利用我们的响应不再是单一内容类型的事实 , 我们可以在API尾部添加格式后缀 , 格式后缀为我们提供了一个参考的格式 , 这意味着我们的API将能够处理诸如  `http://example.com/api/items/4.json` 之类的url

在视图中添加一个 `format` 关键字参数 , 像这样

```python
def snippet_list(request, format=None):
```

和

```python
def snippet_detail(request, pk, format=None):
```

现在更新 `snippets/urls.py` , 在已经存在的URL中添加一个 `format_suffix_patterns` 集合

```python
from django.conf.urls import url
from rest_framework.urlpatterns import format_suffix_patterns
from snippets import views

urlpatterns = [
    url(r'^snippets/$', views.snippet_list),
    url(r'^snippets/(?P<pk>[0-9]+)$', views.snippet_detail),
]

urlpatterns = format_suffix_patterns(urlpatterns)
```

我们并不需要添加这些额外的url , 但是它为我们提供了一种简单明了的方式来指定特定的格式

## 进行测试

继续像我们在教程第1部分中所做的那样 , 通过命令行测试API , 所有的工作都是类似的 , 同时我们可以很好地处无效请求产生的错误

我们可以像之前一样 , 获得 `snippets` 列表

```shell
http http://127.0.0.1:8000/snippets/

HTTP/1.1 200 OK
...
[
  {
    "id": 1,
    "title": "",
    "code": "foo = \"bar\"\n",
    "linenos": false,
    "language": "python",
    "style": "friendly"
  },
  {
    "id": 2,
    "title": "",
    "code": "print \"hello, world\"\n",
    "linenos": false,
    "language": "python",
    "style": "friendly"
  }
]
```

我们可以通过使用 `Accept` 响应头控制返回响应的格式 :

```shell
http http://127.0.0.1:8000/snippets/ Accept:application/json  # Request JSON
http http://127.0.0.1:8000/snippets/ Accept:text/html         # Request HTML
```

或者在URL后添加格式后缀 :

```shell
http http://127.0.0.1:8000/snippets.json  # JSON 后缀
http http://127.0.0.1:8000/snippets.api   # 可浏览的 API 后缀
```

同样的 , 我们可以使用 `Content-Type` 头控制我们请求的格式

```shell
# POST using form data
http --form POST http://127.0.0.1:8000/snippets/ code="print 123"

{
  "id": 3,
  "title": "",
  "code": "print 123",
  "linenos": false,
  "language": "python",
  "style": "friendly"
}

# POST using JSON
http --json POST http://127.0.0.1:8000/snippets/ code="print 456"

{
    "id": 4,
    "title": "",
    "code": "print 456",
    "linenos": false,
    "language": "python",
    "style": "friendly"
}
```

如果你使用 `--debug` 参数 , 那么你可以看到请求头中的请求类型

使用浏览器打开 `http://127.0.0.1:8000/snippets/`

## 浏览可视化

由于 `API` 响应类型是根据客户端的请求进行选择的 , 因此 , 当使用 `web` 浏览器请求的时候 , 默认会使用 `HTML` 格式来表示资源 , 这允许 `API` 返回一个完整的浏览器可视的 `HTML` 表示

拥有一个浏览器可视化的 `API` 是非常有用的 , 这会使得开发和使用 `API` 变的极为简单 , 这也让其他开发者更容易查看和使用你的 `API`

查看 [`browsable api`](http://www.django-rest-framework.org/topics/browsable-api/) 主题获取更更多关于 `browsable API` 的信息 , 比如 特性 , 定制

## 下一步

在教程的第3部分, 我们将开始使用基于类的视图`(CBV)` , 并介绍如何使用通用的视图来减少代码量
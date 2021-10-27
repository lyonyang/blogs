# Tutorial 5: Relationships & Hyperlinked APIs

目前 , 我们的API中的关系是通过使用主键来表示的 . 在本教程的这一部分中 , 我们将改进我们的API的内聚性和可见性 , 通过使用超链接来实现关系 








<extoc></extoc>

## 为我们的根API创建一个端点

现在我们有了 `'snippets'` 和 `'users'` 的端点 , 但是没有为我们的API设置单独的入口 . 为了创建一个单独的入口 , 我们将使用一个常规的基于函数的视图以及 `@api_view` 装饰器创建一个入口端点 . 在文件 `snippets/views.py` 中添加 :

```python
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.reverse import reverse


@api_view(['GET'])
def api_root(request, format=None):
    return Response({
        'users': reverse('user-list', request=request, format=format),
        'snippets': reverse('snippet-list', request=request, format=format)
    })
```

在这里我们需要注意两点 , 首先我们使用 `REST framework` 的 `reverse` 方法限定返回的 `URLs` , 其次 , `URL` 格式使用方便的名字作为标识符 , 稍后会在 `snippets/urls.py` 中声明

## 创建一个高亮的snippets断点

还有一个明显的事情就是我们的 `pastebin API` 缺乏代码高亮的端点

与我们其他的API端点不同 , 我们不想使用 `JSON` , 而只使用 `HTML` 显示 . `REST framework` 提供了两种渲染方式 , 一种是用模板渲染 , 另一种是用预渲染 `HTML` , 在这个端点 , 我们使用第二种渲染方式

另一个需要我们思考的是 , 在创建高亮代码视图的时候 , 高亮视图在通用视图中是不存在的 , 我们不会返回一个对象实例 , 而是返回对象的一个属性

我们不使用 `generic ` 视图 , 而是通过基础类 , 在 `snippets/views.py` 中创建我们自己的 `.get()` 方法

```python
from rest_framework import renderers
from rest_framework.response import Response

class SnippetHighlight(generics.GenericAPIView):
    queryset = Snippet.objects.all()
    renderer_classes = (renderers.StaticHTMLRenderer,)

    def get(self, request, *args, **kwargs):
        snippet = self.get_object()
        return Response(snippet.highlighted)
```

像往常一样 , 我们需要添加新的视图到 `URL` 配置中 , 文件`snippets/urls.py` 

```python
url(r'^$', views.api_root),
```

然后为高亮 `snippet` 添加一个url样式

```python
url(r'^snippets/(?P<pk>[0-9]+)/highlight/$', views.SnippetHighlight.as_view()),
```

## 为我们的API添加超链接

在Web API设计中 , 处理实体之间的关系是一项非常有挑战的事情 , 代表一种关系可以有很多种方式

- 使用主键
- 在实体间使用超链接
- 在相关的实体上使用唯一的 `slug` 字段
- 使用相关实体的默认字符串
- 在父表示中使用嵌套的实体
- 其他自定义的表示

`REST framework` 支持以上所有的方式 , 正向或反向关系均可以使用 , 或者像使用一般外键一样使用自定义的管理方式

在这种情况下 , 我们在实体间使用超链接方法 , 为了达到目的 , 我们将修改我们的序列 ( `serializers` ) , 扩展  `HyperlinkedModelSerializer` 代替 `ModelSerializer`

`HyperlinkedModelSerializer` 和 `ModelSerializer` 有以下几点不同 : 

- 默认不包含 `id` 字段
- 它包含一个 `url` 字段 , 使用 `HyperlinkedIdentityField` 
- 关系使用 `HyperlinkedRelatedField` 代替 `PrimaryKeyRelatedField` 

我们可以快速的将存在的序列重写成超链接的方式 , 文件 `snippets/serializers.py` 

```python
class SnippetSerializer(serializers.HyperlinkedModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.username')
    highlight = serializers.HyperlinkedIdentityField(view_name='snippet-highlight', format='html')

    class Meta:
        model = Snippet
        fields = ('url', 'id', 'highlight', 'owner',
                  'title', 'code', 'linenos', 'language', 'style')


class UserSerializer(serializers.HyperlinkedModelSerializer):
    snippets = serializers.HyperlinkedRelatedField(many=True, view_name='snippet-detail', read_only=True)

    class Meta:
        model = User
        fields = ('url', 'id', 'username', 'snippets')
```

注意 , 我们还新添加了一个 `'highlighted'` 字段 , 这个字段的类型和 `url` 字段类型一致 , 只是它指向 `'snippet-highlight'` 端点 , 而不是 `'snippet-detail'` 

因为我们已经配置了 `URLs` 后缀 , 比如 `'.json'` , 同时我们需要在 `highlight` 字段中指明后缀 , `.html` 

## 确保我们的URL模式均已命名

如果我们要使用超链接 API , 我们必须确保对 `URL` 模型进行命名 , 让我们看看哪些链接需要命名 : 

- 根API指向 `user-list` 和 `snippet-list`
- `snippet` 序列包含一个指向 `snippet-highlight` 字段
- `user` 序列包含一个指向 `snippet-detail` 字段
- 我们的 `snippet` 和 `user` 序列包含 `'url'` 字段默认指向 `'{model_name}-detail'` , 当前情况指向 `'snippet-detail'` 和 `'user-detail'` 

命名加入 URL 配置之后 , `snippets/urls.py` 应该是下面这样子 : 

```python
from django.conf.urls import url, include
from rest_framework.urlpatterns import format_suffix_patterns
from snippets import views

# API endpoints
urlpatterns = format_suffix_patterns([
    url(r'^$', views.api_root),
    url(r'^snippets/$',
        views.SnippetList.as_view(),
        name='snippet-list'),
    url(r'^snippets/(?P<pk>[0-9]+)/$',
        views.SnippetDetail.as_view(),
        name='snippet-detail'),
    url(r'^snippets/(?P<pk>[0-9]+)/highlight/$',
        views.SnippetHighlight.as_view(),
        name='snippet-highlight'),
    url(r'^users/$',
        views.UserList.as_view(),
        name='user-list'),
    url(r'^users/(?P<pk>[0-9]+)/$',
        views.UserDetail.as_view(),
        name='user-detail')
])
```

## 添加分页

`users` 和 `snippets` 的列表视图可能会返回大量的实例 , 所以我们要对返回的结果进行分页 , 并允许客户端访问每个页面

我们可以改变默认的列表样式来使用分页 , 在 `tutorial/settings.py` 文件 , 添加如下配置 

```python
REST_FRAMEWORK = {
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 10
}
```

`REST framework` 的所有设置都是在 `settings` 中 `REST_FRAMEWORK` 字典中的 , 它可以帮我们区分项目中的其他配置

同时 , 我们也可以自定义分页的样式 , 在这里 , 我们使用默认方式

## 浏览API

如果我们打开浏览器 , 并访问可浏览的 `API` , 你会发现你可以使用下面的链接使用 `API` 

你也可以看到 `snippet` 实例的 `'highlight'` 链接 , 这些链接会返回高亮的 `HTML` 代码

在教程的第6部分 , 我们会介绍怎么使用 `ViewSets` 和 `Routers` 通过更少的代码 , 实现我们的 `API`
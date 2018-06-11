# Tutorial 4: Authentication & Permissions

当前 , 我们的 `API` 没有限制, 谁都可以编辑或删除 `snippets` , 我们需要一些更高级的行为来确保 :

- 代码片段总是与创建者联系在一起
- 只有授权用户才能创建 `snippets`
- 只有 `snippet` 创建者可以更新或者删除它
- 未授权的请求只有只读权限

## 添加信息到模型中  🍀

我们需要对我们的 `Snippet` 模型类做一些修改 , 首先 , 添加两个字段 , 一个用来代表代码片段的创建者 , 另一个用来存储高亮显示的HTML代码

修改 `models.py` 添加字段到 `Snippet` 模型中 

```python
owner = models.ForeignKey('auth.User', related_name='snippets', on_delete=models.CASCADE)
highlighted = models.TextField()
```

同时 , 我们需要确保 , 模型在保存的时候 , 使用 `pyments` 代码高亮库填充 `highlighted` 字段

我们需要额外导入 : 

```python
from pygments.lexers import get_lexer_by_name
from pygments.formatters.html import HtmlFormatter
from pygments import highlight
```

现在我们可以模型类中添加 `.save()` 方法 : 

```python
def save(self, *args, **kwargs):
    """
    使用 `pygments` 库来创建代码高亮的HTML代替 snippet
    """
    lexer = get_lexer_by_name(self.language)
    linenos = 'table' if self.linenos else False
    options = {'title': self.title} if self.title else {}
    formatter = HtmlFormatter(style=self.style, linenos=linenos,
                              full=True, **options)
    self.highlighted = highlight(self.code, lexer, formatter)
    super(Snippet, self).save(*args, **kwargs)
```

完成这些工作后 , 我们需要更新数据库表 , 通常我们会创建一个数据库迁移来完成这个任务 , 但是为了本教程的目的 , 我们只需要删除原来的数据库 , 然后重新创建

```shell
rm -f db.sqlite3
rm -r snippets/migrations
python manage.py makemigrations snippets
python manage.py migrate
```

你需要创建一些不同的用户 , 用来测试 API , 最快的方式是使用 `createsuperuser` 命令

```shell
python manage.py createsuperuser
```

## 为我们的模型添加端口  🍀

现在我们已经创建了一些用户 , 我们最好将用户添加到我们的 API , 我们很容易创建一个新的序列 , 在`serializers.py` 文件中添加 :

```python
from django.contrib.auth.models import User

class UserSerializer(serializers.ModelSerializer):
    snippets = serializers.PrimaryKeyRelatedField(many=True, queryset=Snippet.objects.all())

    class Meta:
        model = User
        fields = ('id', 'username', 'snippets')
```

因为 `snippets` 与 `User` 模型是反向关系 , 使用 `ModelSerializer` 类 , 默认不会包含它 , 所以我们需要手动为用户序列添加这个字段

我们还需要添加两个视图到 `views.py` 中 , 我们为用户添加只读视图, 因此我们使用基于视图的一般类 `ListAPIView` 和 `RetrieveAPIView` 

```python
from django.contrib.auth.models import User


class UserList(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class UserDetail(generics.RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
```

确保导入了 `UserSerializer` 类

```python
from snippets.serializers import UserSerializer
```

最后我们需要修改 `URL` 配置 , 添加这些视图到 `API` 中 , 添加以下内容到 `urls.py` 中

```python
url(r'^users/$', views.UserList.as_view()),
url(r'^users/(?P<pk>[0-9]+)/$', views.UserDetail.as_view()),
```

## 将Snippets与Users关联  🍀

现在 , 如果我们创建一个 `snippet`  , 我们没法将用户和创建的 `snippet` 实例联系起来 , 虽然用户不是序列表示的部分 , 但是它代表传入请求的一个属性

我们通过重写 `snippet` 视图的 `.perform_create()` 方法来处理这个问题 , 它允许我们修改如何保存实例 , 并且处理传入请求或请求的URL中隐含的任何信息

在 `SnippetList` 类中 , 添加以下方法 : 

```python
def perform_create(self, serializer):
    serializer.save(owner=self.request.user)
```

现在 , 我们序列的 `create()` 方法将会传入一个有效请求数据的 `owner` 字段

## 更新我们的serializer  🍀

现在 , `snippets` 和创建他们的用户已经建立了联系 , 更新我们的 `SnippetSerializer` 来表示用户 , 在 `serializers.py` 中添加字段 

```python
owner = serializers.ReadOnlyField(source='owner.username')
```

**PS :** 确保你在 `Meta` 的字段列表中也添加了 `owner` 

这个字段会做一些有趣的事情 , `source` 参数控制哪个属性被作用于一个字段 , 并且可以指向 `serialized` 实例上的任何属性 , 它也能像上面一样使用点标记 (`.`) , 在这种情况下 , 它将遍历给定的属性 , 就像Django的模板语言一样

我们添加的字段是无类型的 `ReadOnlyField` 类 , 与其他类型字段 , 如 `CharField` , `BooleanField` 等相比 , 无类型的 `ReadOnlyfField` 总是只读的 , 它用于序列化表示 , 但是不能用于数据反序列化时更新模型实例 , 在这里我们也可以使用 `CharField(read_only=True)` 

## 为视图添加权限  🍀

现在 , `snippets` 与 `users` 已经相关联 , 我们希望确保只有经过身份验证的用户才能创建 , 更新和删除 `snippets` 

`REST framework`  中包含了许多权限类 , 我们可以使用这些类来限制谁可以访问给定的视图 , 在这种情况下 , 我们需要 使用`IsAuthenticatedOrReadOnly`  , 它将确保经过身份验证的请求获得读写访问 , 而未经身份验证的请求则只有只读权限

首先 , 在 `views.py` 中导入如下代码 : 

```python
from rest_framework import permissions
```

 然后在 `SnippetList` 和 `SnippetDetail` 视图类中添加如下属性

```python
permission_classes = (permissions.IsAuthenticatedOrReadOnly,)
```

## 在可浏览API中添加登录  🍀

如果你打开浏览器并操控可浏览的API , 你将发现你不再有创建新的 `snippets` 的权限 , 为了做到这一点 , 我们需要以用户的身份登录

我们可以在我们的项目级别的 `URLconf` : `urls.py` 文件中添加一个登录视图 

添加入到语句

```python
from django.conf.urls import include
```

并添加一个包含登录和注销视图的 `url` 

```python
urlpatterns += [
    url(r'^api-auth/', include('rest_framework.urls')),
]
```

`r'^api-auth/'`  可以使用你想要的URL

现在 , 如果再次打开浏览器 , 刷新页面 , 你将可以看到一个 `Login` 链接在页面的右上角 , 现在可以使用已经创建的用户登录 , 创建 `snippets` 

一旦你创建了一些 `snippets` , 访问 `'/user/'` 端 , 你会注意到在每个用户的 `snippets` 字段 , 会显示跟用户有关的 `snippets` id

## 对象级别权限  🍀

虽然我们希望所有 `snippets` 都能被任何人看到 , 但是也要确保只有创建该 `snippets` 的用户才能更新或删除它

要做到这一点 , 我们需要创建一个用户权限

在 `snippets` 应用下 , 创建一个新文件 , `permissions.py`

```python
from rest_framework import permissions


class IsOwnerOrReadOnly(permissions.BasePermission):
    """
    自定义仅允许对象的owners可修改的权限
    """

    def has_object_permission(self, request, view, obj):
        # 读权限允许任何请求,
        # 因此我们总是允许GET,HEAD或者OPTIONS请求
        if request.method in permissions.SAFE_METHODS:
            return True

        # 写权限仅允许该snippet对戏那个的所有者,owner
        return obj.owner == request.user
```

现在 , 通过编辑 `SnipetDetail` 视图类中的 `permission_classes` 属性 ,我们可以添加自定义权限到我们的 `snippet` 实例端

```python
permission_classes = (permissions.IsAuthenticatedOrReadOnly,
                      IsOwnerOrReadOnly,)
```

确保导入 `IsOwnerOrReadOnly` 类

```python
from snippets.permissions import IsOwnerOrReadOnly
```

现在 , 如果你再使用浏览器 , 你会发现只有你登录与创建 `snippets` 一致的用户 , 你才有权限使用 `DELETE` 和 `PUT` 动作

## 验证API  🍀

由于现在 API 有权限集合 , 在我们需要编辑任何 `snippets` 的时候 , 需要认证我们的请求 , 我们没有设置他任何认证类 ( `authentication classes` ) , 默认情况下只有 `SessionAuthentication` 和 `BasicAuthentication` 

当我们通过浏览器进行交互时 , 我们可以登录 , 浏览器会话 (`session`) 将为请求提供认证

如果我们以编程的方式使用API , 我们需要为每个请求提供明确的 `认证凭证`

如果我们尝试在没有认证的情况下创建 `snippet` , 我们会获得一个 error

```shell
http POST http://127.0.0.1:8000/snippets/ code="print 123"

{
    "detail": "Authentication credentials were not provided."
}
```

我们可以通过提供之前创建的用户的用户名和密码 , 来创建 `snippet` 

```shell
http -a admin:password123 POST http://127.0.0.1:8000/snippets/ code="print 789"

{
    "id": 1,
    "owner": "admin",
    "title": "foo",
    "code": "print 789",
    "linenos": false,
    "language": "python",
    "style": "friendly"
}
```

## 概要  🍀

我们的 `API` 已经具有一个相当精细的权限集合 , 同时为系统用户和他们创建的 `snippets` 提供了端点

在教程的第5部分 , 我们将介绍如何为高亮的 `snippets` 创建一个HTML端点 , 将所有内容联系起来 , 同时为系统中的关系使用超链接提高我们 `API` 的凝聚力
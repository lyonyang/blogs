# Tutorial 3: Class-based Views

我们也可以使用基于类的视图编写我们的 `API` , 如我们所见 , 这是一个有利的模式 , 允许我们重用共同的功能 , 使3我们的代码不重复

## 用基于类的视图重构我们的API  🍀

重构 `views.py` 

```python
from snippets.models import Snippet
from snippets.serializers import SnippetSerializer
from django.http import Http404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status


class SnippetList(APIView):
    """
    列出所有的 snippets,或者创建一个新的 snippet.
    """
    def get(self, request, format=None):
        snippets = Snippet.objects.all()
        serializer = SnippetSerializer(snippets, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = SnippetSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
```

到目前为止 , 一起都很好 , 它和之前的情况非常类似 , 但我们可以更好的区分不同的 `HTTP ` 方法 , 我们需要继续更新 `views.py` 中的实例视图

```python
class SnippetDetail(APIView):
    """
    检索、更新或删除 snippet.
    """
    def get_object(self, pk):
        try:
            return Snippet.objects.get(pk=pk)
        except Snippet.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        snippet = self.get_object(pk)
        serializer = SnippetSerializer(snippet)
        return Response(serializer.data)

    def put(self, request, pk, format=None):
        snippet = self.get_object(pk)
        serializer = SnippetSerializer(snippet, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        snippet = self.get_object(pk)
        snippet.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
```

接下来 , 我们还需要用基于类的视图的方式 , 重构 `snippets/urls.py`

```python
from django.conf.urls import url
from rest_framework.urlpatterns import format_suffix_patterns
from snippets import views

urlpatterns = [
    url(r'^snippets/$', views.SnippetList.as_view()),
    url(r'^snippets/(?P<pk>[0-9]+)/$', views.SnippetDetail.as_view()),
]

urlpatterns = format_suffix_patterns(urlpatterns)
```

至此 , 如果你运行你的开发服务器 , 那么一切还是和之前的一样

## 使用mixins  🍀

使用基于类的视图的一大优势是 , 它允许我们轻松地创建可重用的行为

到目前为止 , 我们所使用的 `create/retriev/update/delete` 操作和我们所创建的任何模型API视图都是非常相似 , 这些常见的行为是在 `REST` 框架的 `mixin` 类中实现的

让我们看看如何使用 `mixin` 类来编写 `views.py` 模块

```python
from snippets.models import Snippet
from snippets.serializers import SnippetSerializer
from rest_framework import mixins
from rest_framework import generics

class SnippetList(mixins.ListModelMixin,
                  mixins.CreateModelMixin,
                  generics.GenericAPIView):
    queryset = Snippet.objects.all()
    serializer_class = SnippetSerializer

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)
```

 我们将花一点时间来看看这里到底发生了什么 , 我们使用 `GenericAPIView` 来构建我们的视图 , 并添加 `ListModelMixin` 和 `CreateModelMixin`

基类提供了核心功能 , `mixin` 类提供了`.list()` 和 `.create()`  , 然后我们绑定 `get` 和 `post` 方法到合适的动作, 到目前为止 , 已经变得足够简单

```python
class SnippetDetail(mixins.RetrieveModelMixin,
                    mixins.UpdateModelMixin,
                    mixins.DestroyModelMixin,
                    generics.GenericAPIView):
    queryset = Snippet.objects.all()
    serializer_class = SnippetSerializer

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)

    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)
```

类似地 , 我们使用 `GenericAPIView` 类提供核心功能 , 添加 `mixins` 提供 `.retrieve()` , `.update()` and `.destroy()` 动作

## 使用基于generic类的视图  🍀

我们使用 `mixin` 类使用比之前较少的代码编写视图 , 但我们可以更进一步 , `REST framework` 提供了一组已经混合的 `generics` 视图 , 我们可以使用它来进一步缩减 `views.py` 模块

```python
from snippets.models import Snippet
from snippets.serializers import SnippetSerializer
from rest_framework import generics


class SnippetList(generics.ListCreateAPIView):
    queryset = Snippet.objects.all()
    serializer_class = SnippetSerializer


class SnippetDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Snippet.objects.all()
    serializer_class = SnippetSerializer
```

现在我们的代码已经越来越像Django的使用了

接下来 , 我们将介绍本教程的第4部分 , 我们将了解如何处理 `API` 的认证和权限
# Tutorial 7: Schemas & client libraries

`schema` 是一种机器可读的文档 , 用于描述可用的API端点 , URLS , 以及他们支持的操作

`schema` 可以用于自动生成文档 , 也可以用于驱动可以与API交互的动态客户端库








<extoc></extoc>

## Core API

为了提供 `schema` 支持, `REST` 框架使用 [Core API](http://www.coreapi.org/)

`Core API` 是用于描述 `APIs` 的文档规范 . 它可以用来提供内部可用端点内部表示格式和API暴露的可能的交互 . 它可以用于服务端或客户端

当用于服务端时 , `Core API` 允许API支持呈现 `schema` 或渲染超媒体格式

当用于客户端 , `Core API` 允许动态驱动的客户端库与任何支持 `schema` 或超媒体格式的 `API` 交互

## 添加一个schema

`REST framework` 支持明确定义的 `schema` 视图 , 或自动生成的 `schemas`. 由于我们使用 `ViewSets` 和`Routers` , 我们可以很简单的自动生成 `schema` 

你需要安装 `coreapi` 

```shell
pip install coreapi
```

在 URL 配置中包含一个自动生成的 `schema` 视图

```python
from rest_framework.schemas import get_schema_view

schema_view = get_schema_view(title='Pastebin API')

urlpatterns = [
    url(r'^schema/$', schema_view),
    ...
]
```

如果你使用浏览器访问 API 根节点 , 在选项中 , 你可以看到 `corejson` 选项变成可用的状态

![corejson-format](http://oux34p43l.bkt.clouddn.com/corejson-format.png)

我们也可以使用命令行 , 通过在 `Accept` 请求头中指定期望的内容类型 , 请求 `schema` 

```shell
$ http http://127.0.0.1:8000/schema/ Accept:application/coreapi+json
HTTP/1.0 200 OK
Allow: GET, HEAD, OPTIONS
Content-Type: application/coreapi+json

{
    "_meta": {
        "title": "Pastebin API"
    },
    "_type": "document",
    ...
```

默认的输出风格使用的是[Core JSON](http://www.coreapi.org/specification/encoding/#core-json-encoding)编码

其他的 `schema` 格式 , 比如 [Open API](https://openapis.org/) (以前称作Swagger) , 同样支持

## 使用命令行客户端

现在 , 我们的 API 暴露了一个 `schema` 端点 , 我们可以使用动态客户端库与 API 交互 , 为了证明这点 , 我们是用 `Core API` 命令行客户端

命令行客户端需要使用 `coreapi-cli` 包

```shell
pip install coreapi-cli
```

通过命令行检查 , `coreapi-cli` 是否可用

```shell
$ coreapi
Usage: coreapi [OPTIONS] COMMAND [ARGS]...

  Command line client for interacting with CoreAPI services.

  Visit http://www.coreapi.org for more information.

Options:
  --version  Display the package version number.
  --help     Show this message and exit.

Commands:
...
```

首先我们使用命令行客户端加载 `API schema` 

```shell
$ coreapi get http://127.0.0.1:8000/schema/
<Pastebin API "http://127.0.0.1:8000/schema/">
    snippets: {
        highlight(id)
        list()
        read(id)
    }
    users: {
        list()
        read(id)
    }
```

我们还没有认证 , 所以我们只能看到只读端点 , 符合我们设计的 `API` 权限

让我们尝试使用命令行客户端 , 列出已经存在的 `snippets` 

```shell
$ coreapi action snippets list
[
    {
        "url": "http://127.0.0.1:8000/snippets/1/",
        "id": 1,
        "highlight": "http://127.0.0.1:8000/snippets/1/highlight/",
        "owner": "lucy",
        "title": "Example",
        "code": "print('hello, world!')",
        "linenos": true,
        "language": "python",
        "style": "friendly"
    },
    ...
```

有些 API 端点依赖命名参数 , 比如 , 我们要获取指定 `snippet` 的高亮 HTML , 需要提供一个 `id` 

```shell
$ coreapi action snippets highlight --param id=1
<!DOCTYPE html PUBLIC "-//W3C//DTD HTML 4.01//EN" "http://www.w3.org/TR/html4/strict.dtd">

<html>
<head>
  <title>Example</title>
  ...

```

## 认证我们的客户端

如果我们想要创建 , 编辑 , 删除 `snippets`  , 我们需要认证一个有效的用户 , 这种情况下 , 我们只使用基本身份验证

将 `<username>` 和 `<password>` 替换成真实的用户名和密码

```shell
$ coreapi credentials add 127.0.0.1 <username>:<password> --auth basic
Added credentials
127.0.0.1 "Basic <...>"
```

现在 , 如果我们重新获取 `schema`  , 我们可以看到所有的可用交互的集合

```shell
$ coreapi reload
Pastebin API "http://127.0.0.1:8000/schema/">
    snippets: {
        create(code, [title], [linenos], [language], [style])
        delete(id)
        highlight(id)
        list()
        partial_update(id, [title], [code], [linenos], [language], [style])
        read(id)
        update(id, code, [title], [linenos], [language], [style])
    }
    users: {
        list()
        read(id)
    }
```

现在我们可以 和这些端点交互 , 比如 , 创建一个新的 `snippet` 

```shell
$ coreapi action snippets create --param title="Example" --param code="print('hello, world')"
{
    "url": "http://127.0.0.1:8000/snippets/7/",
    "id": 7,
    "highlight": "http://127.0.0.1:8000/snippets/7/highlight/",
    "owner": "lucy",
    "title": "Example",
    "code": "print('hello, world')",
    "linenos": false,
    "language": "python",
    "style": "friendly"
}
```

删除 `snippet`

```shell
coreapi action snippets delete --param id=7
```

除了使用命令行客户端 , 开发者也可以使用客户端库与你的 API 进行交互 , Python客户端第一个可用的库 `Javascript` , 将在不久之后发布

有关定义 `schema` 生成和使用 `Core API` 客户端库 , 你可以参考完整的文档

## 回到我们的工作

我们使用很少的代码 , 拥有了一个完整的可浏览的 `pastebin Web API` , 它包含一个 `schema-driven` 客户端库 , 完整的身份认证 , 对象级权限和多格式渲染器

我们走过了设计过程的每一步, 看到了如何使用常规的Django视图进行定制.

你可以在GitHub上查阅最终的代码 [tutorial code](https://github.com/encode/rest-framework-tutorial) , 或者在 [the sandbox](https://restframework.herokuapp.com/) 中进行尝试

到这里 , 我们已经完成了教程 , 如果你想跟多的参与到 `REST framework` 项目 , 你可以使用以下几种方式 :

- 在 [GitHub](https://github.com/encode/django-rest-framework) 上进行审查 , 提交问题 , 发出 `pull requests`
- 加入 [REST framework discussion group](https://groups.google.com/forum/?fromgroups#!forum/django-rest-framework) , 帮助构建社区
- 在Twitter上关注 [作者](https://twitter.com/_tomchristie) , 并发送 `hi`
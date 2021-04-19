# REST


<extoc></extoc>

## 介绍  🍀

REST 是 Representational State Transfer (表征状态转移) 的缩写

表征实际上指的是资源的表现特征 , 而资源指的是 Web 上一切可识别 , 可命名 , 可找到并被处理的实体 , 比如 HTML 页面 , 音频文件 , 图片等

用一个 URI (统一资源定位符) 指向资源 , 使用 HTTP 请求方法操作资源 , URL 可进一步划分为统一资源名 (URN , 代表资源的名字) 和统一资源定位符 (URL , 代表资源的地址) , 其中 URL 可以定位 HTTP 网址 , FTP 服务器和文件路径等 , 符合绝大多数场景 , 所以一般都可以用 URL 代替 URI

## REST架构约束  🍀

REST 架构风格最重要的架构约束有如下 5 个 : 

1. 客户端-服务端 , 这种 Client/Server 的架构形式提供了基本的分布式 , 客户端发起请求 , 服务端决定响应或者拒绝请求 , 如果出错则返回错误信息 , 由客户端处理异常
2. 无状态 , 通信的会话状态应该全部由客户端负责维护 , 也就是请求中包含了全部必要的信息 . 如果使用基于服务端的会话 , 要么需要保证指定会话会使用同一个服务端响应所有请求 , 要么得创建一个可供所有服务器访问的公用的会话存储区 , 对每个请求都额外访问这个几种式的数据存储区获得会话状态
3. 缓存 , 无状态就表示可能出现重复的请求 , 事实上这些请求只需要第一次真正的执行 , 其余的请求都可以享用这个已完成的记过而直接响应 , 所以缓存可以抵消一部分无状态带来的影响
4. 统一接口 , 统一接口意味着每个 REST 应用都共享一种通用架构 , 那么熟悉这种架构的人一眼就能看明白接口的意义 , 并会继续延承下去
5. 分层系统 , 将系统划分为几个部分 , 每个部分负责一部分相对单一的职责 , 然后通过上层对下层的依赖和调用组成一个完整的系统 , 通常可以划分为如下三层 : 
   1. 应用层 : 负责返回 JSON 数据和其他业务逻辑
   2. 服务层 : 为应用层提供服务支持 , 如全站的账号系统 , 以及文件托管服务等
   3. 数据访问层 : 提供数据访问和存储的服务 , 如数据库 , 缓存系统 , 文件系统 , 搜索引擎等

如果一个架构符合 REST 原则 , 就称它为 RESTful 架构

## RESTful API设计指南  🍀

### 使用名词表示资源  🍀

URI 不应该包含动词 , 动词应该通过不同的 HTTP 方法来体现 

错误用法 : 

```
GET /getusers/1
POST /users/1/delete
POST /users/1/create
```

正确用法 : 

```
GET /users/1
DELETE /users/1
PUT /users/1
```

### 关注请求头  🍀

一定要看请求头信息 , 并给予正确的状态码 , 例如 , 假设服务端只能返回 JSON 格式 , 如果客户端的头信息的 Accept 字段要求返回 `application/xml` , 这个时候就不应该返回 `application/json` 类型的数据 , 而应该返回 406 错误

### 合理使用请求方法和状态码  🍀

方法语义说明

| 方法    | 语义                                                         |
| ------- | ------------------------------------------------------------ |
| OPTIONS | 用于获取资源支持的所有 HTTP 方法                             |
| HEAD    | 用于只获取请求某个资源返回的头信息                           |
| GET     | 用于从服务器获取某个资源的信息 : <br />1. 完成请求后 , 返回状态码 200 OK<br />2. 完成请求后 , 需要返回被请求的资源详细信息 |
| POST    | 用于创建新资源 : <br />1. 创建完成后 , 返回状态码 201 Created<br />2. 完成请求后 , 需要返回被创建的资源详细信息 |
| PUT     | 用于完整的替换资源后者创建指定身份的资源 , 比如创建 id 为 123的某个资源 : <br />1. 如果是创建了资源 , 则返回 201 Created<br />2. 如果是替换了资源 , 则返回 200 OK |
| PATCH   | 用于局部更新资源 :<br />1. 完成请求后 , 返回状态码 200 OK<br />2. 完成请求后 , 需要返回被修改的资源详细信息 |
| DELETE  | 用于删除某个资源 , 完成请求后返回状态码 204 NO Content       |

### 使用嵌套对象序列化  🍀

对象应该合理地嵌套 , 不应该都在一个层次上 , 如下的格式是不正确的 : 

```python
{
    'id': 1,
    'post_id': '10001',
    'post_name': 'Post1',
    'post_content': 'this is a post'
}
```

尽可能把相关联的资源信息内联在一起 , 应该把 post 作为一个键 : 

```python
{
    'id': 1,
    'post': {
        'id' : '10001',
        'name': 'Post1',
        'content': 'this is a post'
    }
}
```

### 版本  🍀

常见的区分版本方法有三种 : 

- 保存在 URI 中 , 比如 `"https://api.lyonyang.com/api/v2"`
- 放在请求头中 , 比如 GitHub 的用于 : `"Accept:application/vnd.github.v3+json"`
- 自定义请求头 , 比如 , `"X-Api-Version:1"` 

推荐使用第一种方法

### URI失效和迁移  🍀

随着业务发展 , 会出现一些 API 失效或者迁移 , 对失效的 API , 应该返回 "404 not found" 或 "401 gone" ; 对迁移的 API , 返回 301 重定向

## 速度限制  🍀

为了避免请求泛滥 , 给 API 设置速度限制很重要 , 为此 RFC 6585 引入了 HTTP 状态码 429 (too many requests) 

加入限制功能后 , 应该提示用户 , 参照 GitHub 如下 : 

- X-RateLimit-Limit : 当前时间段允许的并发请求书
- X-RateLimit-Remaining : 当前时间段保留的请求数
- X-RateLimit-Reset : 当前时间段剩余的秒数

我们使用 `httpie` 或者 `curl` 来访问 `https://api.github.com/users/whatever` :

```shell
>curl -i https://api.github.com/users/whatever
HTTP/1.1 200 OK
Date: Mon, 01 Jun 2013 17:27:06 GMT
Content-Type: application/json; charset=utf-8
Content-Length: 1350
Server: GitHub.com
Status: 200 OK
X-RateLimit-Limit: 60
X-RateLimit-Remaining: 59
X-RateLimit-Reset: 1530220396
...
```

## 缓存  🍀

数据内容在一段时间不会变动 , 这个时候我们就可以合理地减少 HTTP 响应内容 , 应该在响应头中携带 Last-Modified , ETag , Vary , Date 等信息 , 客户端可以在随后请求这些资源时 , 在请求头中使用 `If-Modified-Since` , `If-None-Match` 等来确认资源是否进过修改 , 如果资源没有做过修改 , 那么就可以响应 `"304 Not Modified"` , 并且不在响应实体中返回任何内容

GitHub 用法如下 (隐藏了无关的自定义头) : 

```shell
>http https://api.github.com/users/lyonyang --headers
HTTP/1.1 200 OK
Access-Control-Allow-Origin: *
Access-Control-Expose-Headers: ETag, Link, Retry-After, X-GitHub-OTP, X-RateLimit-Limit, X-RateLimit-Remaining, X-RateLimit-Reset, X-OAuth-Scopes, X-Accepted-OAuth-Scopes, X-Poll-Interval
Cache-Control: public, max-age=60, s-maxage=60
Content-Encoding: gzip
Content-Security-Policy: default-src 'none'
Content-Type: application/json; charset=utf-8
Date: Thu, 04 Feb 2016 14:05:03 GMT
ETag: W/"02742979edf9240e6ea171ac41914d44"
Last-Modified: Mon, 25 Jun 2018 08:15:42 GMT
Referrer-Policy: origin-when-cross-origin, strict-origin-when-cross-origin
Server: GitHub.com
Status: 200 OK
Strict-Transport-Security: max-age=31536000; includeSubdomains; preload
Transfer-Encoding: chunked
Vary: Accept
Vary: Accept-Encoding
...
```

通过 `If-Modified-Since` 实现缓存 : 

```shell
>http https://api.github.com/users/lyonyang "If-Modified-Since: Thu, 04 Feb 2016 14:05:03 GMT" --headers
```

## 并发控制  🍀

缺少并发控制的 PUT 和 PATCH 请求可能导致 "更新丢失" , 这个时候可以使用 Last-Modified 和 ETag 头来实现条件请求 , 具体原则如下 : 

- 客户端发起的请求如果没有包含 If-Unmodified-Since 或者 If-Match 头 , 就返回 "403 Forbidden" , 在响应正文中解释为何返回该状态码
- 客户端发起的请求所提供的 If-Unmodified-Since 或者 If-Match 头与服务器记录的实际修改时间或 ETag 值不匹配时 , 返回状态码 "412 Precondition Failed"
- 客户端发起的请求所提供的 If-Unmodified-Since 或者 If-Match 头与服务器记录的实际修改时间或 ETag 的历史值匹配 , 但资源已经被修改过事 , 返回状态码 "409 Conflict"
- 客户端发起的请求所提供的条件服务实际值  就更新资源 , 响应 "200 Ok" 或者 "204 No Content" , 并且包含更新过的 Last-Modified 和 / 或 ETag 头 , 同时包含 Content-Location 头 , 其值为更新后的资源 URI
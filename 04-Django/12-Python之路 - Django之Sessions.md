# Python之路 - Django之Cookie与Sessions

## 介绍  🍀

基于 Internet的各种服务系统应运而生 , 建立商业站点或者功能比较完善的个人站点 , 常常需要记录访问者的一些信息 ; 论坛作为 Internet发展的产物之一 , 在 Internet 中发挥着越来越重要的作用 , 是用户获取、交流、传递信息的主要场所之一 , 论坛常常也需要记录访问者的一些基本信息 (如身份识别号码、密码、用户在 Web 站点购物的方式或用户访问该站点的次数) ; 目前公认的是 , 通过 Cookie 和 Session 技术来实现记录访问者的一些基本信息

**Cookie**

Cookie 是在 HTTP 协议下 , 服务器或脚本可以维护客户工作站上信息的一种方式

Cookie 是由 Web 服务器保存在用户浏览器 (客户端) 上的小文本文件 , 它可以包含有关用户的信息 ; 无论何时用户链接到服务器 , Web 站点都可以访问 Cookie 信息

目前Cookie是临时的 , 有些则是持续的 , 临时的Cookie只在浏览器上保存一段规定的时间 , 一旦超过规定的时间 , 该Cookie就会被系统清除

持续的 Cookie 则保存在用户的 Cookie 文件中 , 下一次用户返回时 , 仍然可以对它进行调用 ; 在 Cookie 文件中保存 Cookie , 有些用户担心 Cookie 中的用户信息被一些别有用心的人窃取 , 而造成一定的损害 ; 其实 , 网站以外的用户无法跨过网站来获得 Cookie 信息 ; 如果因为这种担心而屏蔽 Cookie , 肯定会因此拒绝访问许多站点页面 , 因为 , 当今有许多 Web 站点开发人员使用 Cookie 技术 , 例如 Session 对象的使用就离不开 Cookie 的支持

Cookie可以弥补HTTP协议无状态的不足 , 在Session出现之前 , 基本上所有的网站都采用Cookie来跟踪会话

**Django实现的Cookie**

获取Cookie

```python
request.COOKIES['key']
requset.get_signed_cookie(self, key, default=RAISE_ERROR, salt='', max_age=None)
"""
get_signed_cookie()
Attempts to return a signed cookie. If the signature fails or the
cookie has expired, raises an exception... unless you provide the
default argument in which case that value will be returned instead.
"""
```

设置Cookie

```python
# 响应对象
rep = HttpResponse(...)
rep ＝ render(request, ...)
rep ＝ redirect()
 # 设置Cookie
rep.set_cookie(self, key, value='', max_age=None, expires=None, path='/',domain=None, secure=False, httponly=False)
"""
set_cookie()
Sets a cookie.
``expires`` can be:
- a string in the correct format,
- a naive ``datetime.datetime`` object in UTC,
- an aware ``datetime.datetime`` object in any time zone.
If it is a ``datetime.datetime`` object then ``max_age`` will be calculated.
"""
rep.set_signed_cookie(self, key, value, salt='', **kwargs)
```

由于cookie保存在客户端的电脑上 , 所以 , JavaScript和jquery也可以操作Cookie

**Session** 

Cookie虽然一定程度上解决了"保持状态" 的需求 , 但是由于Cookie本身最大支持4096字节 , 以及Cookie本身保存在客户端 , 可能被拦截或窃取 , 因此就需要一种新的东西 . 它能支持更多的字节 , 并且他保存在服务器 , 有较高的安全性

在计算机中 , 尤其是在网络应用中 , 我们将Session称为“会话控制”

Session 对象存储特定用户会话所需的属性及配置信息 , 这样 , 当用户在应用程序的 Web 页之间跳转时 , 存储在 Session 对象中的变量将不会丢失 , 而是在整个用户会话中一直存在下去 ; 当用户请求来自应用程序的 Web 页时 , 如果该用户还没有会话 , 则 Web 服务器将自动创建一个 Session 对象 , 当会话过期或被放弃后 , 服务器将终止该会话

Session 对象最常见的一个用法就是存储用户的首选项 , 例如 , 如果用户指明不喜欢查看图形 , 就可以将该信息存储在 Session 对象中 ; 注意会话状态仅在支持Cookie的浏览器中保留

Django支持所有的匿名会话 , 简单说就是使用跨网页之间可以进行通讯 , 比如显示用户名 , 用户是否已经发表评论 ; 这个Session框架让你存储和获取每个站点访客的任意数据

它将数据存储在服务端 , 并以Cookies的形式进行发送和接收数据 , Cookies包含一个Session ID , 而不是数据本身 (除非你使用的基于Cookie的后端)

## 启用Sessions  🍀

Django中的Sessions是通过中间件实现的

如果我们要启用Session功能 , 需要执行以下操作 : 

- 编辑`settings.py`中的`MIDDLEWARE` , 确保其中包含`django.contrib.sessions.middleware.SessionMiddleware` ; 默认在我们使用`django-admin startproject` 命令时 , `settings.py`中已经启用该中间件
- 如果你不想使用Sessions , 你可以将`MIDDLEWARE`中的`SessionMiddleware`移除以及将`INSTALLED_APPS`中的`django.contrib.sessions`移除 , 它能够为你节省一点开销

## 配置Session引擎  🍀

默认情况下 , Django存储会话到你的数据库中 (使用`django.contrib.sessions.models.Session`) , 尽管这很方便 , 但是在某些情况下 , 在其他地方存储会话数据的速度更快 , 因此Django可以配置为在文件系统或缓存中存储会话数据

### 数据库  🍀

如果你想使用数据库支持的会话 , 你需要添加`django.contrib.sessions` 到你`settings.py`中的INSTALLED_APP设置中 , 默认就是使用的数据库

在配置完成之后 , 需要执行`manage.py migrate` 来安装村粗会话数据的一张数据库表

### 缓存  🍀

为了更好的性能 , 我们可以使用一个基于缓存的会话后端

使用Django的缓存系统存储会话数据之前 , 我们需要确保已经配置好了我们的缓存 , 关于缓存的配置见 : [cache documentation](https://docs.djangoproject.com/en/1.11/topics/cache/) 

注意 : 如果你使用的是Memcached缓存后端 , 那么你应该只使用基于缓存的会话 ; 本地内存缓存后端不会保留足够长的数据 , 它会更快地使用文件或数据库会话 , 而不是通过文件或数据库缓存的后端发送所有数据 , 此外 , 本地内存缓存后端不是多进程安全的 , 因此对于生产环境来说可能不是一个好的选择

如果在 [`CACHES`](https://docs.djangoproject.com/en/1.11/ref/settings/#std:setting-CACHES) 中定义了多个缓存 , Django将使用默认的缓存 , 要使用另外的缓存 , 需要将`SESSION_CACHE_ALIAS` 设置为该缓存的名称

配置好缓存之后 , 对于如何在缓存中存储数据你有两个选择 : 

- 对于简单的缓存会话存储 , 可以设置`SESSION_ENGINE`为`django.contrib.sessions.backends.cache` , 此时会话数据将直接存储在你的缓存中 , 然而缓存数据可能不会持久 : 如果缓存填满或者缓存服务器重启 , 缓存数据可能会被清理掉
- 若要持久的缓存数据 , 可以设置`SESSION_ENGINE`为`django.contrib.sessions.backends.cached_db` , 这使用直接写缓存 , 每次写入高速缓存也将写入数据库 , 会话读取仅在数据不在缓存中时才使用数据库

两种会话的存储都非常快 , 但是简单的缓存更快 , 因为它放弃了持久性 , 大部分情况下 , `cached_db`后端已经足够快 , 但是如果你需要榨干最后一点性能 , 并且接收会话数据丢失的风险 , 那么你可以使用`cache` 后端

注意使用`cached_db`会话后端 , 需要遵循 [using database-backed sessions](https://docs.djangoproject.com/en/1.11/topics/http/sessions/#using-database-backed-sessions) 

### 文件  🍀

要使用基于文件的会话 , 将`SESSION_ENGINE`为`django.contrib.sessions.backends.file` 

你可以设置`SESSION_FILE_PATH`来控制Djanog存储会话文件的地址 , 默认来自`tempfile.gettempdir()` ,大多数情况下为`/tmp` , 当然请确保你的Web服务器具有读取和写入这个位置的权限

### Cookie  🍀

同样 , 使用基于Cookie的会话 , 设置`SESSION_ENGINE`为`django.contrib.sessions.backends.signed_cookies` , 此时 , 会话数据的存储将使用Django的工具进行[cryptographic signing](http://python.usyiyi.cn/documents/Django_111/topics/signing.html) 和 [SECRET_KEY](https://docs.djangoproject.com/en/1.11/ref/settings/#std:setting-SECRET_KEY) 设置

建议保留`SESSION_COOKIE_HTTPONLY`设置为True , 以防止从JavaScript中访问存储的数据

注意 : 

- 如果`SECRET_KEY`不保密 , 而你正在使用 [PickleSerializer](https://docs.djangoproject.com/en/1.11/topics/http/sessions/#django.contrib.sessions.serializers.PickleSerializer) 这可能导致任意远程执行代码

  拥有`SECRET_KEY`的攻击者不仅可以生成你的站点新人的伪造会话数据 , 而且还可以远程执行任意代码 , 因为数据是用pickle序列化的

  如果你使用基于Cookie的会话 , 需要格外注意安全密钥对于任何可以远程访问的系统都是永远完全保密的

- 会话数据已签名但未加密

  如果使用基于Cookie的会话 , 则会话数据可以被客户端读取

  MAC(消息认证码)被用来保护数据不被客户端修改 , 这样会话数据在被篡改时就会失效 ; 如果保存Cookie的客户端 (例如你的浏览器) 不能保存所有的会话Cookie或丢失数据 , 会话同样会变得不合法 ; 尽管Django对数据进行压缩 , 仍然完全有可能超过每个Cookie常见的4096个字节的限制

- 没有实时保证


  MAC可以保证数据的权威性 (由你的站点生成 , 而不是任何其他人) 和完整性 (包含全部的数据并且是正确的) , 但是它不能保证是最新的 ; 这意味着对于某些会话数据的使用 , 基于Cookie可能让你受到 [replay attacks](https://en.wikipedia.org/wiki/Replay_attack) 

  其它方式的会话后端在服务器端保存每个会话并在用户注销时使它无效 , 而基于Cookie的会话不会在用户注销时失效 , 因此 , 如果攻击者窃取了用户的Cookie  , 那么即使用户注销了 , 他们也可以使用该Cookie进行登录 ; Cookies只能被当做是"过期的" , 如果它们比你的[`SESSION_COOKIE_AGE`](https://docs.djangoproject.com/en/1.11/ref/settings/#std:setting-SESSION_COOKIE_AGE) 还要旧

- 性能

  最后 , Cookie的大小对你网站的速度有影响

##  视图中使用Session  🍀

当`SessionMiddleware`激活时 , 每个HttpRequest对象 , 也就是传递给Django视图函数的第一个参数 , 将会具有一个`session`属性 , 它是一个类似字典对象

你可以在你的视图中任何地方读取并写入`request.session`  , 并且可以多次编辑它

```python
class backends.base.SessionBase
	"""这是所有会话对象的基类,它具有以下标准字典方法"""
    __getitem__(key)
    	'''Example: fav_color = request.session['fav_color']'''

	__setitem__(key, value)
		'''Example: request.session['fav_color'] = 'blue''''

	__delitem__(key)
       '''Example: del request.session['fav_color']. 
        This raises KeyError if the given key isn’t already in the session.'''

	__contains__(key)
		'''Example: 'fav_color' in request.session'''

	get(key, default=None)
		'''Example: fav_color = request.session.get('fav_color', 'red')'''

	pop(key, default=__not_given)
		'''Example: fav_color = request.session.pop('fav_color', 'blue')'''

	keys()
	items()
	setdefault()
	clear()
'''It also has these methods:'''

	flush()
    	'''
		Deletes the current session data from the session and deletes the session cookie. This is used if you want to ensure that the previous session data can’t be accessed again from the user’s browser (for example, the django.contrib.auth.logout() function calls it).
		'''
	set_test_cookie()
    	'''
		Sets a test cookie to determine whether the user’s browser supports cookies. Due to the way cookies work, you won’t be able to test this until the user’s next page request. See Setting test cookies below for more information.
		'''
	test_cookie_worked()
    	'''
		Returns either True or False, depending on whether the user’s browser accepted the test cookie. Due to the way cookies work, you’ll have to call set_test_cookie() on a previous, separate page request. See Setting test cookies below for more information.
		'''
	delete_test_cookie()
    	'''
		Deletes the test cookie. Use this to clean up after yourself.
		'''
	set_expiry(value)
		'''
		Sets the expiration time for the session. You can pass a number of different values:

        If value is an integer, the session will expire after that many seconds of inactivity. For example, calling request.session.set_expiry(300) would make the session expire in 5 minutes.
        If value is a datetime or timedelta object, the session will expire at that specific date/time. Note that datetime and timedelta values are only serializable if you are using the PickleSerializer.
        If value is 0, the user’s session cookie will expire when the user’s Web browser is closed.
        If value is None, the session reverts to using the global session expiry policy.
        Reading a session is not considered activity for expiration purposes. Session expiration is computed from the last time the session was modified.
		'''
	get_expiry_age()
    	'''
        Returns the number of seconds until this session expires. For sessions with no custom expiration (or those set to expire at browser close), this will equal SESSION_COOKIE_AGE.

        This function accepts two optional keyword arguments:

        modification: last modification of the session, as a datetime object. Defaults to the current time.
        expiry: expiry information for the session, as a datetime object, an int (in seconds), or None. Defaults to the value stored in the session by set_expiry(), if there is one, or None.
         '''
	get_expiry_date()
    	'''
        Returns the date this session will expire. For sessions with no custom expiration (or those set to expire at browser close), this will equal the date SESSION_COOKIE_AGE seconds from now.

        This function accepts the same keyword arguments as get_expiry_age().
		'''
	get_expire_at_browser_close()
    	'''
        Returns either True or False, depending on whether the user’s session cookie will expire when the user’s Web browser is closed.
		'''
	clear_expired()
    	'''
		Removes expired sessions from the session store. 
		This class method is called by clearsessions.
		'''
	cycle_key()
    	'''
		Creates a new session key while retaining the current session data. django.contrib.auth.login() calls this method to mitigate against session fixation.
		'''
```

### 序列化  🍀

默认情况下 , Django使用JSON序列化会话数据 , 你额可以使用`SESSION_SERIALIZER`设置顶顶亿会话序列化格式 , 即使是使用我们写自己的序列化器 , 同样强烈建议使用JSON , 特别是在使用Cookie后端时 ; 自定义序列化器 :  [Write your own serializer](https://docs.djangoproject.com/en/1.11/topics/http/sessions/#custom-serializers)

例如 , 如果使用pickle序列化会话数据 , 则会出现攻击情况 ; 如果你使用的是签署Cookie会话后端 , 并且`SECRET_KEY`被攻击者知道 (Django本身没有漏洞会导致它被泄漏) , 攻击者就可以在会话中插入一个字符串 , 在unpickle之后可以在服务器上执行任何代码 

在因特网上这个攻击技术很简单并且很容易差到 , 尽管Cookie会话的存储对Cookie保存的数据进行了签名以防止篡改 , `SECRET_KEY`的泄漏会立即使得可以执行远程代码

### 捆绑序列化器  🍀

```python
class serializers.JSONSerializer:
    """
    对django.core.signing中的JSON序列化方法的一个包装,
    只能序列化基本数据类型
    """
```

另外 , 因为JSON只支持字符串作为键 , 注意使用非字符串作为`request.session`的键将不工作

```python
>>> # initial assignment
>>> request.session[0] = 'bar'
>>> # subsequent requests following serialization & deserialization
>>> # of session data
>>> request.session[0]  # KeyError
>>> request.session['0']
'bar'
```

类似地 , 无法在JSON中编码的数据 , 如非UTF-8字节 , 如`\xd9`将不能被存储

```python
class serializers.PickleSerializer:
    """支持任意Python对象,但是可能导致远程执行代码的漏洞,如果攻击者知道了SECRET_KEY"""
```

### 自定义序列化器  🍀

对于`PickleSerializer`与`JSONSerializer`两者的差别 , 这是常见的情况 , 需要我们在便利性和安全性之间权衡

但是如果我们希望在JSON格式的会话中存储更高级的数据类型比如`request.session`和`datatime` , 我们需要自己编写一个序列化器 (或者在保存它们到Decimal中之前转换这些值使其成为一个可JSON序列化的对象) ; 虽然序列化这些值是相当简单的 (比如我们可以使用DjangoJSONEncoder) , 但是编写一个能够可靠地返回您所输入的相同内容的解码器是更加脆弱的 , 例如 , 返回一个`datatime`时 , 它可能实际上是与`datatime`格式碰巧相同的一个字符串

我们自定义序列化器时 , 必须实现两个方法 , `dumps(self, obj)`和`loads(self,data)` 来分别序列化和反序列化会话数据的字典

### 会话对象  🍀

- 在`request.session`上使用普通的Python字符串作为字典的键 , 这主要是为了方便而不是一条必须遵守的规则
- 以一个下划线开始的会话字典的键被Django保留作为内部使用
- 不要用新的对象覆盖`request.session` , 且不要访问或设置它的属性 , 要像Python中的字典一样使用它

## 设置Cookie测试  🍀

为了方便 , Django提供了一个简单的方法来测试用户的浏览器是否支持Cookie ; 只需要在一个视图中调用`request.session`中的`set_cookie_worked()` , 并在下一个视图中调用`test_cookie_worked()` , 注意不是在同一个视图中调用

由于Cookie的工作方式 , 在`set_test_cookie()`和`test_cookie_worked()`之间这种笨拙的分离是必要的 , 因为我们设置一个Cookie , 在浏览器的下一个请求之前 , 你不可能知道浏览器是否接受它

验证Cookie测试之后 , 我们可以使用`delete_test_cookie()`来进行清除操作

实例

```python
from django.http import HttpResponse
from django.shortcuts import render

def login(request):
    if request.method == 'POST':
        if request.session.test_cookie_worked():
            request.session.delete_test_cookie()
            return HttpResponse("You're logged in.")
        else:
            return HttpResponse("Please enable cookies and try again.")
    request.session.set_test_cookie()
    return render(request, 'foo/login_form.html')
```

##视图外使用Sessions  🍀

这一节中的示例直接从`django.contrib.session.backends.db`导入`SessionStore` , 在我们的代码中应该从`SESSION_ENGINE`中导入SessionStore , 如下 : 

```python
>>> from importlib import import_module
>>> from django.conf import settings
>>> SessionStore = import_module(settings.SESSION_ENGINE).SessionStore
```

可以使用一个API来操作视图之外的会话数据 :

```python
>>> from django.contrib.sessions.backends.db import SessionStore
>>> s = SessionStore()
>>> # stored as seconds since epoch since datetimes are not serializable in JSON.
>>> s['last_login'] = 1376587691
>>> s.create()
>>> s.session_key
'2b1189a188b44ad18c35e113ac6ceead'
>>> s = SessionStore(session_key='2b1189a188b44ad18c35e113ac6ceead')
>>> s['last_login']
1376587691
```

上述中`SessionStore.create()`旨在创建一个新的会话 (即一个没有从会话存储中加载 , 并且使用`session_key=None`)

`save()`旨在保存现有会话 (即从存储中加载的会话) , 在新会话中调用`save()`也可以正常工作 , 但可能生成与现有的会话相冲突的`session_key` ; `create()会`调用`save()`和循环 , 知道生成一个未使用的`session_key`

如果你使用的是`django.contrib.sessions.backends.db`后端 , 每个会话都只是一个普通的Django模型 , Session模型定义在`django/contrib/sessions/models.py`中 ; 因为它是一个普通的模型 , 你可以使用普通的Django数据库API访问会话 : 

```python
>>> from django.contrib.sessions.models import Session
>>> s = Session.objects.get(pk='2b1189a188b44ad18c35e113ac6ceead')
>>> s.expire_date
datetime.datetime(2005, 8, 20, 13, 35, 12)
```

注意 , 我们需要调用`get_decoded()`以获得会话的字典 , 这是必须的 , 因为字典是以编码后的格式保存的 : 

```python
>>> s.session_data
'KGRwMQpTJ19hdXRoX3VzZXJfaWQnCnAyCkkxCnMuMTExY2ZjODI2Yj...'
>>> s.get_decoded()
{'user_id': 42}
```

## 会话保存  🍀

默认情况下 , Django只有在会话被修改时才会保存会话到数据库中 , 即它的字典中的任何值被修改时

```python
# Session is modified.
request.session['foo'] = 'bar'

# Session is modified.
del request.session['foo']

# Session is modified.
request.session['foo'] = {}

# Gotcha: Session is NOT modified, because this alters
# request.session['foo'] instead of request.session.
request.session['foo']['bar'] = 'baz'
```

上面例子的最后一种情况 , 我们可以通过设置会话对象的`modified`属性显示地告诉会话对象已经被修改过 : 

```python
request.session.modified = True
```

若修改这个默认的行为 , 可以设置`SESSION_SAVE_EVERY_REQUEST`为True , 当设置为True时 , Django将对每个请求都保存会话到数据库中

注意会话的Cookie只有在一个会话被创建或修改后才会发送 , 如果`SESSION_SAVE_EVERY_REQUEST`为True , 会话的Cookie将在每个请求中发送

类似地 , 每次会话Cookie发送时 , 会话Cookie的过期部分都会被更新

如果响应的状态是500 , 则会话不会保存

## 会话时长  🍀

你可以通过`SESSION_EXPIRE_AT_BROWSER_CLOSE`配置来控制会话框架使用浏览器时长的会话 , 还是持久的会话

默认情况下 , `SESSION_EXPIRE_AT_BROWSER_CLOSE`设置为False , 表示会话的Cookie保存在用户的浏览器中 , 时间为`SESSION_COOKIE_AGE` ; 如果我们不想让别人每次打开浏览器都需要登录时 , 可以这样做

如果`SESSION_EXPIRE_AT_BROWSER_CLOSE`设置为True , Django将使用浏览器时长的Cookie , 即如果用户关闭浏览器 , 那么Cookie就会立即过期 , 如果你想让别人每次打开浏览器时都要登录 , 那么就使用这个

这个设置时一个全局的默认值 , 我们可以通过调用`request.session()`的`set_expiry()`方法来进行覆盖

注意 : 某些浏览器 (如Chrome) 提供一种设置 , 允许用户在关闭并重新打开浏览器后继续使用会话 , 在某些情况下 , 这可能干扰`SESSION_EXPIRE_AT_BROWSER_CLOSE`设置并导致会话在浏览器关闭后不过期 , 在测试启用`SESSION_EXPIRE_AT_BROWSER_CLOSE`设置的Django应用时需要特别注意这一点

## 清除会话存储  🍀

随着用户在你的网站上创建新的会话 , 会话数据可能会在你的会话存储仓库中积累 , 如果你正在使用数据库作为后端 , `django_session`数据库表将持续增长 ; 如果你正在使用文件作为后端 , 你的临时目录包含的文件数量将持续增长

Django不提供自动清除过期会话的功能 , 因此 , 定期地清除会话时我们自己的任务 , Django提供一个清除用的管理命令来满足这个目的 : [`clearsessions`](https://docs.djangoproject.com/en/1.11/ref/django-admin/#django-admin-clearsessions) , 建议定期调用这个命令 , 例如作为一个日常运行的cron任务

但是 , 以缓存为后端不存在这个问题 , 因为缓存会自动删除过期的数据 ; 以Cookie为后端也不存在这个问题 , 因为会话数据通过用户的浏览器保存

对于会话的行为有很多控制配置 , 详细见 :  [Django settings](https://docs.djangoproject.com/en/1.11/ref/settings/#settings-sessions) 

更多Sessions相关 : [How to use sessions](https://docs.djangoproject.com/en/1.11/topics/http/sessions/) 
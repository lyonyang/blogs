# Django - Authentication System








<extoc></extoc>

## 介绍

Django为我们提供了一个认证系统 , 它提供了认证 (*authentiaction*) 和授权功能 (*authorization*) , 这两种功能在某些地方时耦合的 

## User对象

[`User`](https://docs.djangoproject.com/en/1.11/ref/contrib/auth/#django.contrib.auth.models.User)对象是认证系统的核心 , 它们通常表示与你的站点进行交互的用户 , 并用于启用限制访问 , 注册用户信息和给创建者关联内容等

在Django的认证框架中只存在一种类型的用户 , 因此诸如`superusers`或管理员`staff` 用户只是具有特殊属性集的`User`对象 , 而不是不同类型的`User`对象

默认User的基本属性有 : 

- uesrname
- password
- email
- first_name
- last_name

完整参考见 :  [`full API documentation`](https://docs.djangoproject.com/en/1.11/ref/contrib/auth/#django.contrib.auth.models.User) 

### 创建 users

创建users最直接的方法时使用`create_user()`函数 , 如下 : 

```python
>>> from django.contrib.auth.models import User
>>> user = User.objects.create_user('john', 'lennon@thebeatles.com', 'johnpassword')

# At this point, user is a User object that has already been saved
# to the database. You can continue to change its attributes
# if you want to change other fields.
>>> user.last_name = 'Lennon'
>>> user.save()
```

如果我们安装了admin , 我们可以交互式地创建users , 见 :  [create users interactively](https://docs.djangoproject.com/en/1.11/topics/auth/default/#auth-admin) 

### 创建 superusers

我们可以使用如下命令创建一个超级用户 : 

```python
$ python manage.py createsuperuser --username=joe --email=joe@example.com
```

### 修改密码

Django不会在user模型上存储原始的 (明文) 密码 , 而只是一个哈希值 (完整见 :  [documentation of how passwords are managed](https://docs.djangoproject.com/en/1.11/topics/auth/passwords/) ) , 因此 , 不要试图直接操作用户的密码属性 , 这就是为什么创建用户时使用帮助函数的原因

所以修改密码我们可以通过以下方式 : 

- `manage.py changepassword *username*` 提供了一种从命令行更改用户密码的方法 , 它提示你修改一个给定的user密码 , 你必须输入两次 , 如果两次输入匹配 , 密码就会立即被修改 , 如果你没有提供user , 命令行将尝试修改与当前系统用户匹配的用户名的密码

- 通过`set_password()` 

  ```python
  >>> from django.contrib.auth.models import User
  >>> u = User.objects.get(username='john')
  >>> u.set_password('new password')
  >>> u.save()
  ```

- 如果你安装了Django admin , 可以在身份验证系统的管理页面上更改用户的密码

- Django还提供视图和表单允许用户修改他们自己的密码

注意 : 更改用户密码将会注销所有会话 , 详见 :  [Session invalidation on password change](https://docs.djangoproject.com/en/1.11/topics/auth/default/#session-invalidation-on-password-change)   

### 用户认证

使用`authenticate()`来验证一组凭证 , 它接收关键字参数`credentials`  , 默认为`username` 和`password` 

```python
authenticate(request=None, **credentials):
    """
    request:HttpRequest对象
    credentials:默认username和password
    """
```

根据每个认证的后端进行验证 , 如果某个后端凭证通过则返回一个User对象 , 如果凭证对任何后端都无效 , 则主动触发`PermissionDenied`  , 并返回None , 如下 : 

```python
from django.contrib.auth import authenticate
user = authenticate(username='john', password='secret')
if user is not None:
    # A backend authenticated the credentials
else:
    # No backend authenticated the credentials
```

 ## 权限和授权

Django本身提供了一个简单的权限系统 , 它提供了一种为特定用户和用户组分配权限的方法

Django中的admin站点也使用了该权限系统 , 使用的权限如下 : 

- 查看"add"表单和添加对象仅限于具有"add"权限的用户类型对象
- 查看"change"表单和更改对象仅限于具有"change"权限的用户类型对象
- 删除一个对象仅限于具有“delete”权限的用户类型对象

权限不但可以根据每个对象的类型 , 而且可以根据特定的对象实例设置 , 通过[`ModelAdmin`](https://docs.djangoproject.com/en/1.11/ref/contrib/admin/#django.contrib.admin.ModelAdmin) 提供的`has_add_permission()` , `has_change_permission()`和`has_delete_permission()`方法 , 可以针对相同类型的不同对象实例自定义权限

User对象具有两个多对多字段 : `groups`和`user_permissions` 

User对象可以使用和其他Django模型一样的方式访问他们相关联的对象 , 如下 : 

```python
myuser.groups.set([group_list])
myuser.groups.add(group, group, ...)
myuser.groups.remove(group, group, ...)
myuser.groups.clear()
myuser.user_permissions.set([permission_list])
myuser.user_permissions.add(permission, permission, ...)
myuser.user_permissions.remove(permission, permission, ...)
myuser.user_permissions.clear()
```

### 默认权限

当`django.contrib.auth`在你的`INSTALLED_APPS`配置中列出时 , 它将确保为你安装的应用中的每个Django模型创建3个默认的权限 , 即add , change和delete

当你运行`manage.py migrate` 时, 将创建这些权限 ; 在`django.contrib.auth`添加`INSTALLED_APPS`之后 , 首次运行`migrate`时 , 将为所有先前安装的模型创建默认权限 , 以及当时安装的任何新模型 ; 之后 , 每次运行`manage.py migrate`  , 它将为新的模型创建默认权限(创建权限的函数与`post_migrate`信号连接)

### Groups

`django.contrib.auth.models.Group`模型是一种对用户进行分类的通用方式 , 通过这种方式你可以引用权限或其他标签都这些用户 ; 一个用户可以属于任意多个组

组中每个用户自动具有该组的权限 , 例如 , 如果 `Site editors`组具有`can_edit_home_page`权限 , 那么该组中的任何用户都具有该权限

除了权限之外 , 组还是给分类用户分配标签，添加功能的便捷方法 ; 例如 , 你可以创建一个组`Special users` , 只有在该组中的用户才能够访问会员的页面

### 编程方式创建权限

虽然我们可以在模型的Meta类中自定义权限 , 但是你也可以直接创建权限 , 例如 , 你可以在`myapp`中为`BlogPost`模型创建`can_publish`权限 :

```python
from myapp.models import BlogPost
from django.contrib.auth.models import Permission
from django.contrib.contenttypes.models import ContentType

content_type = ContentType.objects.get_for_model(BlogPost)
permission = Permission.objects.create(
    codename='can_publish',
    name='Can Publish Posts',
    content_type=content_type,
)
```

然后该权限可以通过`user_permissions`属性或者通过`Group`的`permissions`属性分配给用户

### 权限缓存

[`ModelBackend`](https://docs.djangoproject.com/en/1.11/ref/contrib/auth/#django.contrib.auth.backends.ModelBackend)在第一次需要访问User对象的权限时会对权限进行缓存 , 由于对新添加的权限并不会立即检查 , 所以这种做法对`request-response`循环是非常有利的 (例如在admin中) , 如果你想要在添加新的权限后马上在测试或视图检查他们 , 最简单的解决办法是从数据库中重新获取User , 如下 :

```python
from django.contrib.auth.models import Permission, User
from django.contrib.contenttypes.models import ContentType
from django.shortcuts import get_object_or_404

from myapp.models import BlogPost

def user_gains_perms(request, user_id):
    user = get_object_or_404(User, pk=user_id)
    # any permission check will cache the current set of permissions
    user.has_perm('myapp.change_blogpost')

    content_type = ContentType.objects.get_for_model(BlogPost)
    permission = Permission.objects.get(
        codename='change_blogpost',
        content_type=content_type,
    )
    user.user_permissions.add(permission)

    # Checking the cached permission set
    user.has_perm('myapp.change_blogpost')  # False

    # Request new instance of User
    # Be aware that user.refresh_from_db() won't clear the cache.
    user = get_object_or_404(User, pk=user_id)

    # Permission cache is repopulated from the database
    user.has_perm('myapp.change_blogpost')  # True

    ...
```

## Web请求中的认证

Django使用[Sessions](https://docs.djangoproject.com/en/1.11/topics/http/sessions/)和[Middleware](https://docs.djangoproject.com/en/1.11/ref/middleware/)来拦截[request objects](https://docs.djangoproject.com/en/1.11/ref/request-response/#django.http.HttpRequest)到认证系统中

认证系统为每个请求提供一个`request.user`属性来代表当前的用户 , 如果当前的用户仍未登录 , 该属性将会被设置为一个`AonnymousUser`实例 , 否则该属性将会是一个User实例

我们可以使用`is_authenticated`属性来进行区分 : 

```python
if request.user.is_authenticated:
    # Do something for authenticated users.
    ...
else:
    # Do something for anonymous users.
    ...
```

### 登录用户

如果你有一个经过身份验证的用户 , 你想把它附带到当前的会话中 , 可以通过`login()`函数完成

```python
login(request, user, backend=None):
    """
    request:HttpRequest对象
    user:User对象
    backend:后端
    """
```

`login()`使用Django的Session框架来将用户的ID保存在session中

注意 , 匿名会话期间的任何数据集在用户登录后都会保留在会话中

```python
from django.contrib.auth import authenticate, login

def my_view(request):
    username = request.POST['username']
    password = request.POST['password']
    user = authenticate(request, username=username, password=password)
    if user is not None:
        login(request, user)
        # Redirect to a success page.
        ...
    else:
        # Return an 'invalid login' error message.
        ...
```

### 选择验证后端

用户登录时 , 用户的ID和用于身份验证的后端保存在用户的会话中 , 这允许相同的身份验证后端在将来的请求中获取用户的详细信息 . 保存会话中的认证后端选择如下 : 

1. 使用可选的`backend`参数的值 (如果提供)
2. 使用`user.backend`属性的值 (如果存在)
3. 如果只有一个 , 则使用`AUTHENTICATION_BACKENDS`中的后端
4. 否则 , 触发异常

### 登出用户

要登出一个已经通过`django.contrib.auth.login()`登入的用户 , 可以在视图中使用`django.contrib.auth.logout()` 

```python
logout(request):
    """
    request:HttpRequest对象
    没有返回值
    """
```

实例

```python
from django.contrib.auth import logout

def logout_view(request):
    logout(request)
    # Redirect to a success page.
```

调用`logou()`时 , 当前请求的会话数据将被彻底清楚 , 这是为了防止另外一个人使用相同的Web浏览器登入并访问前一个用户的会话数据 , 如果你想在用户登出之后可以立即访问放入会话中的数据 , 则需要在调用`django.conruib.auth.logout()`之后放入

### 限制访问页面

#### 原始方式

限制访问页面的简单原始方法时检查`request.user.is_authenticated` , 并重定向到登录页面 :

```python
from django.conf import settings
from django.shortcuts import redirect

def my_view(request):
    if not request.user.is_authenticated:
        return redirect('%s?next=%s' % (settings.LOGIN_URL, request.path))
    # ...
```

或者显示错误信息

```python
from django.shortcuts import render

def my_view(request):
    if not request.user.is_authenticated:
        return render(request, 'myapp/login_error.html')
    # ...
```

#### login_required

一个比较快捷的方式 , 可以使用`login_required()`装饰器

```python
login_required(redirect_field_name='next', login_url=None):
    """
    Decorator for views that checks that the user is logged in,
    redirecting to the log-in page if necessary.
    redirect_filed_name:重定向路径,设置为None可以从URL中移除
    login_url:指定没有通过检查的用户的重定向向登录页面,默认为settings.LOGIN_URL
    """
```

实例

```python
from django.contrib.auth.decorators import login_required

@login_required
def my_view(request):
    ...
```

`login_required()`完成下面的事情 : 

- 如果用户没有登录 , 则重定向到[settings.LOGIN_URL](https://docs.djangoproject.com/en/1.11/ref/settings/#std:setting-LOGIN_URL) , 并且把当前请求的绝对路径作为查询参数传递到登陆页面 , 例如 : `/accounts/login/?next=/polls/3/`
- 如果用户已经登入 , 则正常执行视图 , 视图的代码可以安全地假设用户已经登入

修改密码实例

```python
@login_required
def set_password(request):
    user = request.user
    state = None
    if request.method == 'POST':
        old_password = request.POST.get('old_password', '')
        new_password = request.POST.get('new_password', '')
        repeat_password = request.POST.get('repeat_password', '')
        if user.check_password(old_password):
            if not new_password:
                state = 'empty'
            elif new_password != repeat_password:
                state = 'repeat_error'
            else:
                user.set_password(new_password)
                user.save()
                return redirect("/log_in/")
        else:
            state = 'password_error'
    content = {
        'user': user,
        'state': state,
    }
    return render(request, 'set_password.html', content)
```

#### LoginRequiredMixin

当你使用基于类的视图时 , 可以使用`LoginRequireMixin`实现与`login_required`相同的行为 , 这个mixin应该位于继承列表中最左侧的位置

如果一个视图使用这个mixin，那么所有未经身份验证的用户的请求将被重定向到登录页面，或者显示HTTP 403 Forbidden错误，这取决于 [`raise_exception`](https://docs.djangoproject.com/en/1.11/topics/auth/default/#django.contrib.auth.mixins.AccessMixin.raise_exception)参数

您可以设置[`AccessMixin`](https://docs.djangoproject.com/en/1.11/topics/auth/default/#django.contrib.auth.mixins.AccessMixin)的任何参数来定制未授权用户的处理 :

```python
from django.contrib.auth.mixins import LoginRequiredMixin

class MyView(LoginRequiredMixin, View):
    login_url = '/login/'
    redirect_field_name = 'redirect_to'
```

#### user_passes_test

为了快捷 , 你可以使用`user_passes_test`装饰器 , 返回False时执行重定向

```python
user_passes_test(test_func,login_url=None,redirect_field_name='next):
	"""
	Decorator for views that checks that the user passes the given test,
    redirecting to the log-in page if necessary. 
    The test should be a callable that takes the user object and returns True if the user passes.
    test_func:一个以User对象为参数的回调函数
    login_url:指定没有通过检查的用户的重定向向登录页面,默认为settings.LOGIN_URL
    redirect_field_name:重定向路径,设置为None可以从URL中移除
	"""
```

实例

```python
from django.contrib.auth.decorators import user_passes_test

def email_check(user):
    return user.email.endswith('@example.com')

@user_passes_test(email_check)
def my_view(request):
    ...
```

#### UserPassesTestMixin

当使用基于类的视图时 , 可以使用`UserPassesTestMixin` , 与user_passes_test类似

**test_func()**

你必须在你的类中覆盖`test_func()`方法来提供执行的测试 , 此外 , 你可以设置 [`AccessMixin`](https://docs.djangoproject.com/en/1.11/topics/auth/default/#django.contrib.auth.mixins.AccessMixin) 的任何参数来定制未授权用户的处理: 

```python
from django.contrib.auth.mixins import UserPassesTestMixin

class MyView(UserPassesTestMixin, View):

    def test_func(self):
        return self.request.user.email.endswith('@example.com')
```

**get_test_func()**

你也可以覆盖`get_test_func()`方法以使mixin使用不同命名的函数来进行检查 (而不是`test_func()`)

由于`UserPassesTestMixin`的实现方式 , 你不能将它们放在继承列表中 , 以下内容不起作用 : 

```python
class TestMixin1(UserPassesTestMixin):
    def test_func(self):
        return self.request.user.email.endswith('@example.com')

class TestMixin2(UserPassesTestMixin):
    def test_func(self):
        return self.request.user.username.startswith('django')

class MyView(TestMixin1, TestMixin2, View):
    ...
```

#### permission_required

```python
permission_required(perm, login_url=None, raise_exception=False):
    """
    检查一个用户是否有指定的权限
    perm:权限名称,形式app.permission
    login_url:指定没有通过检查的用户的重定向登录页面,默认为settings.LOGIN_URL
    raise_exception:如果提供了该参数,装饰器会抛出PermissionDenied异常,从而导致403(HTTP Forbidden)视图替代重定向的登录页面
    """
```

实例

```python
from django.contrib.auth.decorators import permission_required

@permission_required('polls.can_vote')
def my_view(request):
    ...
```

如`class models.User`中的`has_perm()`方法一样 , 权限名称采用`"<app label>.<permission codename>" `的形式 , 例如 , polls.can_vote表示polls应用中一个模型的权限

装饰器也可以采取可迭代的权限 , 这种情况下 , 用户必须具有所有权限才能访问视图

#### PermissionRequiredMixin

对基于类的视图应用权限进行检查 , 可以使用`PermissionRequiredMixin` 

这个mixin , 就相当于`permission_required`装饰器 , 如下 : 

```python
from django.contrib.auth.mixins import PermissionRequiredMixin

class MyView(PermissionRequiredMixin, View):
    permission_required = 'polls.can_vote'
    # Or multiple of permissions:
    permission_required = ('polls.can_open', 'polls.can_edit')
```

你可以设置 [`AccessMixin`](https://docs.djangoproject.com/en/1.11/topics/auth/default/#django.contrib.auth.mixins.AccessMixin) 的任何参数来定制未授权用户的处理

你还可以覆盖以下方法 : 

```python
get_permission_required():
    '''
    返回由mixin使用的许可名称的可迭代,
    默认为permission_required属性,如有必要,转换为元组
    '''
has_permission():
    '''
    返回一个布尔值,表示当前用户是否具有执行装饰视图的权限
    默认情况下,返回使用get_permission_required()返回的权限列表调用has_perms()的结果
    '''
```

## 在admin中管理用户

如果`django.contrib.auth`和`django.contrib.admin`这两个你都安装了 , 将可以通过admin方便地查看和管理用户 , 组和权限 ; 可以像其他任何Django模型一样创建和删除用户 , 可以创建组 , 并分配权限给用户和组 , admin中还会保存和显示对用户模型编辑的日志

admin更多相关见下一篇整理

认证视图 : [Authentication Views](https://docs.djangoproject.com/en/1.11/topics/auth/default/#module-django.contrib.auth.views) 

内置表单 : [Built-in forms](https://docs.djangoproject.com/en/1.11/topics/auth/default/#module-django.contrib.auth.forms) 

更多相关内容 : https://docs.djangoproject.com/en/1.11/topics/auth/default/

认证系统 : [User authentication in Django](https://docs.djangoproject.com/en/1.11/topics/auth/) 
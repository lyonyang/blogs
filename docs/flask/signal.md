# Flask - 源码之信号








<extoc></extoc>

## 介绍

项目功能越复杂 , 代码量越大 , 就越需要在其之上做开发和维护是很痛苦的 , 尤其是对于团队的新人 ; 而信号就是在框架核心功能或者一些 Flask 扩展发生动作时发送的通知 , 利用信号可以实现一部分的业务解藕

在 Flask 中 , 信号功能由 `Blinker` 库提供 , 如果没有安装该库就无法使用信号功能 , 但是不会影响其他功能 , 因为如果没有该库 , Flask 将提供一个假的信号 , `flask.signals.py` 中 : 

```python
signals_available = False
try:
    from blinker import Namespace
    signals_available = True
except ImportError:
    class Namespace(object):
        def signal(self, name, doc=None):
            return _FakeSignal(name, doc)

    class _FakeSignal(object):
        """If blinker is unavailable, create a fake class with the same
        interface that allows sending of signals but will fail with an
        error on anything else.  Instead of doing anything on send, it
        will just ignore the arguments and do nothing instead.
        """

        def __init__(self, name, doc=None):
            self.name = name
            self.__doc__ = doc
        def _fail(self, *args, **kwargs):
            raise RuntimeError('signalling support is unavailable '
                               'because the blinker library is '
                               'not installed.')
        send = lambda *a, **kw: None
        connect = disconnect = has_receivers_for = receivers_for = \
            temporarily_connected_to = connected_to = _fail
        del _fail

# The namespace for code signals.  If you are not Flask code, do
# not put signals in here.  Create your own namespace instead.
_signals = Namespace()
```

所以我们应该先安装 `Blinker` : 

```shell
$ pip install blinker
```

下面是一个 `Blinker` 的示例 : 

```python
from blinker import signal

# 创建信号
started = signal('test-started')

def each(round):
    print("Round {}!".format(round))

def round_two(round):
    print("Only {}".format(round))

# 订阅信号,each为接收者
started.connect(each)
# round_two为接收者,sender为发送者
# 表示只有发送者为2时才接收
started.connect(round_two, sender=2)

for round in range(1,4):
    # 发送信号
    started.send(round)
```

Flask 中有一些钩子 , 如 `before_request` 和 `after_request` , 这些钩子不需要 `Blinker` 库并且允许你改变请求对象 (request) 或者响应对象 (response) , 而信号和钩子做的事情很像 , 只不过信号并不对请求对象和响应对象做改变 , 仅承担记录和通知的工作

## 内置信号

在 `flask.signals.py` 中我们可以看到 , Flask 内置了 10 个信号 :

```python
# 模板渲染成功时发送
template_rendered = _signals.signal('template-rendered')

# 模板渲染前发送
before_render_template = _signals.signal('before-render-template')

# 建立请求上下文后,在请求处理开始前发送
request_started = _signals.signal('request-started')

# 在响应发送给客户端之前发送
request_finished = _signals.signal('request-finished')

# 请求销毁时发送,无论请求成败都会发送
request_tearing_down = _signals.signal('request-tearing-down')

# 请求处理抛出异常时发送
got_request_exception = _signals.signal('got-request-exception')

# 应用上下文销毁时发送
appcontext_tearing_down = _signals.signal('appcontext-tearing-down')

# 应用上下文进栈中时发送
appcontext_pushed = _signals.signal('appcontext-pushed')

# 应用上下文出栈时发送
appcontext_popped = _signals.signal('appcontext-popped')

# 调用flask在其中添加数据时发送
message_flashed = _signals.signal('message-flashed')
```

### 创建信号

我们以 `request_started` 为例来看看其内部实现 :

```python
from blinker import Namespace

_signals = Namespace()

# 调用Namespace对象的signal方法
# 完成信号对象的创建,并使其成为全局引用
request_started = _signals.signal('request-started')
```

`Namespace.signal()` 如下 : 

```python
class Namespace(dict):
    """A mapping of signal names to signals."""

    def signal(self, name, doc=None):
        """
        返回NamedSignal对象
        """
        try:
            return self[name]
        except KeyError:
            # Namespace为内置对象dict的派生类,
            # 设置并返回值,
            # self.request-started = NameSignal('request-started')
            return self.setdefault(name, NamedSignal(name, doc))
```

### 订阅信号

如果我们要使用内置信号 , 那么首先我们需要订阅信号 , 也就是使用 `Signal.connect()` 方法

```python
from flask import Flask, request_started

app = Flask(__name__)

# log_reqeust函数为接收方,app为发送方
# 对于接收函数的参数,第一个位置不可缺省,
# 因为在send调用该函数时,内部传入了一个sender实参
def log_request(sender, **extra):
    print('Before the request comes ...')

# 订阅信号
request_started.connect(log_request, app)


@app.route('/index')
def index():
    return 'index page'


if __name__ == '__main__':
    app.run()
```

`connect()` 源码如下 : 

```python
def connect(self, receiver, sender=ANY, weak=True):
    """
    Connect *receiver* to signal events sent by *sender*.
    receiver:为一个可调用对象
    """
    receiver_id = hashable_identity(receiver)
    if weak:
        # <weakref at 0x000002129F72EE28; to 'function' at 0x000002129CBE7F28 (log_request)>
        # receiver将在send时被调用,self._cleanup_receiver
        receiver_ref = reference(receiver, self._cleanup_receiver)
        receiver_ref.receiver_id = receiver_id
    else:
        receiver_ref = receiver
    if sender is ANY:
        sender_id = ANY_ID
    else:
        sender_id = hashable_identity(sender)

    self.receivers.setdefault(receiver_id, receiver_ref)
    # self._by_sender与self._by_receiver为两个默认字典,其value默认为set
    # {sender_id:{receiver_id,}}
    self._by_sender[sender_id].add(receiver_id)
    # {receiver_id:{sender_id,}}
    self._by_receiver[receiver_id].add(sender_id)
    del receiver_ref

    # 此时self._weak_senders为空,所以以下不会执行
    if sender is not ANY and sender_id not in self._weak_senders:
        # wire together a cleanup for weakref-able senders
        try:
            sender_ref = reference(sender, self._cleanup_sender)
            sender_ref.sender_id = sender_id
        except TypeError:
            pass
        else:
            self._weak_senders.setdefault(sender_id, sender_ref)
            del sender_ref

    # 此处条件不成立,也不会执行
    if ('receiver_connected' in self.__dict__ and
        self.receiver_connected.receivers):
        try:
            self.receiver_connected.send(self,
                                         receiver=receiver,
                                         sender=sender,
                                         weak=weak)
        except:
            self.disconnect(receiver, sender)
            raise
    # receiver_connected为空
    if receiver_connected.receivers and self is not receiver_connected:
        try:
            receiver_connected.send(self,
                                    receiver_arg=receiver,
                                    sender_arg=sender,
                                    weak_arg=weak)
        except:
            self.disconnect(receiver, sender)
            raise
    return receiver
```

### 发送信号

信号的发送是通过 `Signal.send()` 来完成的 , 而这一步早已经被定义在 `Flask` 对象中了 , 如下 : 

```python
def full_dispatch_request(self):
    self.try_trigger_before_first_request_functions()
    try:
        # 请求处理前发送信号
        request_started.send(self)
        rv = self.preprocess_request()
        if rv is None:
            # 分派请求
            rv = self.dispatch_request()
    except Exception as e:
        rv = self.handle_user_exception(e)
    return self.finalize_request(rv)
```

`Signal.send()` 如下 : 

```python
def send(self, *sender, **kwargs):
    """Emit this signal on behalf of *sender*, passing on \*\*kwargs.

    Returns a list of 2-tuples, pairing receivers with their return
    value. The ordering of receiver notification is undefined.

    :param \*sender: Any object or ``None``.  If omitted, synonymous
      with ``None``.  Only accepts one positional argument.

    :param \*\*kwargs: Data to be sent to receivers.

    """
    # Using '*sender' rather than 'sender=None' allows 'sender' to be
    # used as a keyword argument- i.e. it's an invisible name in the
    # function signature.
    if len(sender) == 0:
        sender = None
    elif len(sender) > 1:
        raise TypeError('send() accepts only one positional argument, '
                        '%s given' % len(sender))
    else:
        # 取*sender元组中的第一个元素,即self (app) 
        sender = sender[0]
    if not self.receivers:
        return []
    else:
        # 返回并完成调用
        return [(receiver, receiver(sender, **kwargs))
                for receiver in self.receivers_for(sender)]
```

`Signal.receivers_for()` 如下 : 

```python
def receivers_for(self, sender):
    """Iterate all live receivers listening for *sender*."""
    # TODO: test receivers_for(ANY)
    # self.receivers在信号订阅时被设置
    if self.receivers:
        sender_id = hashable_identity(sender)
        if sender_id in self._by_sender:
            # 按照上面的例子我们使用的sender不是ANY,
            # 所以self._by_sender[ANY_ID]为一个空集合,
            # {sender_id:{receiver_id,}}
            # self._by_sender[sender_id]为本例ids
            ids = (self._by_sender[ANY_ID] |
                   self._by_sender[sender_id])
        else:
            ids = self._by_sender[ANY_ID].copy()
        for receiver_id in ids:
            # 根据receiver_id获取weakref对象
            receiver = self.receivers.get(receiver_id)
            if receiver is None:
                continue
            if isinstance(receiver, WeakTypes):
                # strong为订阅函数,即本例的log_reqeust
                # 这里你可能会疑惑,见下
                strong = receiver()
                if strong is None:
                    # 释放信号
                    self._disconnect(receiver_id, ANY_ID)
                    continue
                receiver = strong
            # 返回函数对象
            yield receiver
```

在上面这段代码中 , 对于 `strong = receiver()` 我们知道 , `WeakTypes = (ref, BoundMethodWeakref)` , 而在这两个类型中 , `ref` 才是正主 ; 不用想我们也知道 , `ref` 也就是 `ReferenceType` 中必然有 `__call__` 方法 , 但是该方法仅仅一个 `pass` 摆在那里 , 而调用的返回值却返回了我们的订阅函数 , 这不正常

于是 , 在 `ReferenceType` 的上方我找到了说明 , `Weak-reference support module` 

这个类型是一个弱引用类型 , 它是一个特殊的存在 , 当你对弱引用对象进行引用时 , 并不能保持该类对象的活动 , 只有通过调用引用判断 ; 如果该引用还存活着 , 那么将返回其引用对象 , 否则将会进行回调 

大致过程如下 : 

```python
# 依次调用代码
receiver_ref = reference(receiver, self._cleanup_receiver)

weak = callable_reference(object, callback)

return annotatable_weakref(object, callback)

class annotatable_weakref(ref):
```

弱引用对象没有属性或方法 , 如下有一个示例 : 

```python
import weakref

class Foo:
    pass

# 实例化Foo
o = Foo()
# 包装成弱引用对象
r = weakref.ref(o)
# 调用弱引用对象
r_result = r()
print(o is r_result)

"""
执行结果:
True
"""
```

弱引用详见 : [weakref](https://docs.python.org/3/library/weakref.html?highlight=weak%20references#module-weakref) 

最后 , 对于其它信号的发送相关代码位置 , 我们可以通过导入信息来查看 , 导入信息如下 : 

```python
# app.py (5个)
from .signals import appcontext_tearing_down, got_request_exception, \
    request_finished, request_started, request_tearing_down

# ctx.py (2个)
from .signals import appcontext_pushed, appcontext_popped
    
# templating.py (2个)
from .signals import template_rendered, before_render_template

# helpers.py (1个)
from .signals import message_flashed
```

这里就不再分析其它信号了

## 自定义信号

在我们的应用中 , 我们可以直接使用 `Blinker` 创建信号 , 如下 , 定义一中对于上传大文件的信号 : 

```python
from blinker import Namespace
web_signals = Namespace()
large_file_saved = web_signals.signal('large-file-saved')
```

简直不要太简单

## 装饰器方式

在 `Signal` 对象中还有一个 `connect_via()` 装饰器订阅信号 , 如下 : 

```python
def connect_via(self, sender, weak=False):
    def decorator(fn):
        self.connect(fn, sender, weak)
        return fn
    return decorator
```

这个就没必要分析了 , 看看用法吧 , 以 `flask.appcontext_tearing_down` 为例 : 

```python
from flask import Flask, appcontext_tearing_down, session

app = Flask(__name__)

@appcontext_tearing_down.connect_via(app)
def close_db_connection(sender, **extra):
    print('Database connection closed ...')

@app.route('/index')
def index():
    return 'index page'

if __name__ == '__main__':
    app.run()
```

另外在 `Flask-Login` 插件中还带了 6 种信号 , 可以基于其中的信号做一些额外工作 , 待后续添加
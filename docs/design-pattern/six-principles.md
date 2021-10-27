# 六大原则








<extoc></extoc>

## 前言

设计模式是一个我们编写程序的标准 , 也就是一种规范 , 有时候不能够盲目的追求规范而不理会真实情景 , 因为它可能会适得其反

## 单一职责原则

单一职责原则 (`Single Responsibility Principle` , 简称 `SRP` )

**定义 :** 应该有且仅有一个原因引起类的变更 (原话 : `There should never be more than one reason for a class to change.` )

**作用 :** 

- 降低类的复杂性 , 职责具有清晰明确的定义
- 提高可读性
- 提供可维护性
- 降低变更引起的风险

**实例 :** 

以通话为例 , 我们需要两个操作来实现通话 

- 建立连接
- 信息传递

伪代码示例

```python
class Phone(object):
	"""
	未区分职责, converse既负责连接, 也负责信息传递
	"""
    def converse(self, phone, message):
        连接
        开始通话
        挂断电话
        
class Phone(object):
	"""
	区分职责, dial负责连接, chat负责信息传递, hangup负责关闭连接
	"""
    def dial(self, phone):
		pass
    
    def chat(self, message):
        pass
    
    def hangup():
        pass
```

变更的出现会使你的项目工作量增大 , 所以单一职责原则可以有效的提高你的工作效率 , 但是通常你可能感觉不到它的存在 , 第一是因为你可能会不自觉的这么去做 , 即使它不完全符合这一原则 ; 第二是因为你的项目不允许去深究它 , 总之 , 单一职责原则可以在一定程度上使你的代码更加从容面对项目遇到的变更风险

**扩展 :** 

在面向对象中, 除了继承, 还有另一种方式来实现抽象, 那就是组合, 但是组合是一种强耦合关系, 所以不到迫不得已还是不要使用组合的好

## 里氏替换原则

里氏替换原则 (`Liskov substitution Principle` , 简称 `LSP` )

**定义** : 如果对每一个类型为 S 的对象 `o1` , 都有类型为 T 的对象 `o2` , 使得以 T 定义的所有程序 P 在所有的对象 `o1` 都代换成 `o2` 时, 程序 P 的行为没有发生变化, 那么类型 S 是类型 T 的子类型 (原话 : `If for each object o1 of type S there is an object o2 of type T such that for all programs P defined in terms of T, the behavior of P is unchanged when o1 is substituted for o2 then S is a subtype of T.`)

大致意思就是 , 父类能出现的地方子类也可以出现 , 而且替换将父类替换成子类也不会产生任何错误或异常 , 使用者可能根本就不需要知道是父类还是子类 , 但是 , 反过来子类能出现的地方父类却不一定能出现 , 它的含义如下 : 

1. 子类必须完全实现父类的方法 (但是如果子类中的某些方法发生了畸变 , 建议将方法进行独立)
2. 子类可以有自己的个性
3. 覆盖或实现父类的方法时输入参数可以被放大
4. 覆盖或实现父类的方法时输出结果可以被缩小

关于第一点和第二点 , 这几乎就是基本的规则 , 不过在 Python 中并没有接口的概念 , 当然而第三点和第四点则是需要注意的 , 因为一旦参数被缩小 , 或者结果被放大 , 那你在写代码时就得小心了 , 因为你要顾及你的子类是否能正常完成你的任务

**作用 :**  

- 代码共享 , 减少创建类的工作量 , 每个子类都拥有父类的方法和属性
- 提高代码的重用性
- 子类可以形似父类 , 但又异于父类
- 提高代码的可扩展性
- 提高产品或项目的开放性

**实例 :** 

```python
class Foo(object):
    
    def say_hello(self, name):
        print(name, 'hello~')
        return self

class SubOne(Foo):
    
    # 重载, 放大参数
    def say_hello(self, name, desc=''):
        print(name, 'hello', '')
        return self
    
    # 异于父类
    def say_hi(self, name):
        print(name, 'hi')
        
class SubTwo(Foo):
    
    # 覆盖
    def say_hello(self, name):
        print('hello', name)
        return self
```

这个例子可以说是用来 "凑数" 的 , 因为在 Python 中 , 来表达里氏替换原则所有的含义可能会不太像 Python 了 , 因为Python 天生就是多态 , 所以也不需要接口 ; 但是覆盖和重载我们应该遵循里氏替换原则 , 为了保证更好的兼容性 , 扩展性

**扩展 :** 

覆盖(Override) 和重载 (Overload) :  

覆盖就意味着它的外观是没有任何变化的 , 使用起来也没有变化 , 但是它其中的内容却已经被改变 ; 重载则是它的名字还是一样的 , 但是也仅仅是名字 , 它的其他都已经被重新塑造 ; 就比如 , 我们写了一个方法( `Python` 注解形式) `a(n: int, m: str) -> str` , 子类覆盖你所看到的还是 `a(n: int, m: str) -> str` , 而重载 `a(n: tuple) -> str` , 它只是名字还叫 `a` , 但是它的参数等等已经发生了改变

## 依赖倒置原则

依赖倒置原则 (`Dependence Inversion Principle` , 简称 `DIP` )

**定义 : ** 高层模块不应该依赖底层模块 , 两者应该依赖其抽象 ; 抽象不应该依赖于细节 , 细节应该依赖抽象 ( 原话 : `High level modules should not depend upon low level modules.Both should depend upon abstractions.Abstractions should not depend upon details.Details should depend upon abstractions. ` )

依赖倒置原则是 "面向接口编程" OOD (`Object-Oriented Design` , 面向对象设计) 的精髓之一

**作用 :** 

1. 减少类之间的耦合性
2. 提高系统的稳定性
3. 降低并行开发引起的风险
4. 提高代码的可读性和可维护性

**实例 :** 

```python
# 不符合依赖倒置原则
class Benz(object):
    
    def run(self):
        print('奔驰启动...滴滴滴')

class BMW(object):
    
    def run(self):
        print('宝马启动...滴滴滴')
        
class Driver(object):
    """驾驶者"""
    
    def drive(self, benz_ojbect):
        """开奔驰"""
        benz_object.run()
        
     def drive_BMW(self, bmw_object):
        """为了保证兼容性, """
        bmw_object.run()
        
# 符合依赖倒置原则

class Car(object):
    """抽象类"""
    def run(self):
        """细节实现应该依赖于抽象"""
        raise NotImplementedError('车必须实现run方法')

class Benz(Car):
    
    def run(self):
        print('奔驰启动...滴滴滴')

class BMW(Car):
    
    def run(self):
        print('宝马启动...滴滴滴')

class Driver(object):
    """根据实际需要, 司机也可以抽象出来"""
    def drive(self, car):
        car.run()

"""
抽象不依赖于细节, 即 Car 不应该依赖于 Benz 和 BMW
"""
```

依赖有三种写法 , 分别为 :

1. 构造函数传递依赖对象 , 在创建对象时进行限制
2. 方法传递依赖对象 , 在使用过程中进行限制
3. 接口传递依赖对象 , 直接在定义上限制

上述例子所使用的是接口传递依赖对象

依赖倒置原则的本职就是通过抽象 , 使各个类或模块的实现彼此独立 , 不互相影响 , 实现模块间的松耦合

## 接口隔离原则

接口隔离原则 (`Interface Segregation Principle` , 简称 `ISP` )

**定义 :** 客户端不应该依赖它不需要的接口 ; 类之间的依赖关系应该建立在最小的接口上 (原话 : `“Clients should not be forced to depend upon interfaces that they don't use. The dependency of one class to another one should depend on the smallest possible interface.` )

注意 , 接口隔离原则和单一职责原则审视的角度是不一样的 , 单一职责是要求类或接口职责单一 , 注重的是职责 , 而接口隔离则要求接口的方法尽量少 , 如 : 一个接口的职责可能包含了 10 个方法 , 这10个方法都放在一个接口中 , 并提供给多个模块访问 , 各个模块按照规定的权限来访问

**作用 :** 

- 提高代码的灵活性和可维护性
- 提高系统的内聚性 , 降低系统的耦合性
- 提高代码重用性 , 减少代码冗余

接口隔离原则是对接口进行规范约束 , 其包含以下四层含义 : 

1. 接口要尽量小
2. 接口要高内聚 (高内聚: 提高接口、类、模块的处理能力 , 减少对外的交互 ; 高内聚的标准是既符合接口隔离原则又符合单一职责原则)
3. 定制服务 (只提供访问者需要的方法)
4. 接口设计是有限度的

**在进行接口隔离时 , 首先必须要满足单一职责原则**

**实例 :** 

```python
# 未进行接口隔离
class Worker(object):
    """工人"""
    def work(self):
        """需要按顺序完成四道工序"""
        step1
        step2
        step3
        step4
        
# 进行了接口隔离
class Worker(object):
    """工人"""
    
    def work(self):
        self.finish_step1()
        self.finish_step2()
        self.finish_step3()
        self.finish_step4()
    
    def finish_step1(self):
        pass
    
    def finish_step2(self):
        pass
    
    def finish_step3(self):
        pass
    
    def finish_step4(self):
        pass
"""
场景一:
	由于材料更加精细, 已经不需要进行第1道工序了, 只需完成2,3,4道即算完成
场景二:
	为了能够让员工更加专注, 每个工人将只负责一道工序
	工人A负责第一道工序
	工人B负责第二道工序
	工人C负责第三道工序
	工人D负责第四道工序
场景三:
	公司研发出了新的产品P1和P2, 工作流程如下: 
		- P1: 工序数量不变, 但是工作顺序需要倒序, 即 4, 3, 2, 1
		- P2: 只需要经过第3道工序, 1,2,4皆不需要
		
隔离与未隔离哪一种更加能适应以上所有场景?
"""
```

如果大量的重复代码出现在你的程序中 , 那么你就应该反思了 , 因为你没有进行接口隔离 , 或者隔离得还不够细 , 导致代码无法重用

在进行接口隔离时 , 粒度大小不能过大 , 也不能过小 ; 定义太大 , 会降低灵活性 , 无法提供定制服务 , 给整体项目带来无法预料的风险 ; 定义太小 , 则会造成接口数量过多 , 使设计复杂化

## 迪米特法则

迪米特法则 (`Law of Demeter` , 简称 `LoD` ) 也称最少知识原则 (`Least Knowledge Principle` , 简称 `LKP`)

**定义 :** 一个对象应该对其他对象有最少的了解 , 即 一个类应该对自己需要耦合或调用的类知道得最少 (原话 : `Only talk to your immediate friends` )

他强调以下两点 : 

1. 从依赖者的角度来说 , 只依赖应该依赖的对象
2. 从被依赖者的角度来说 , 只暴露应该暴露的方法

迪米特法则的核心观念就是类间解耦 , 弱耦合 , 只有弱耦合了以后 , 类的复用率才可以提高 ; 但是其要求的结果就是产生了大量的中转或跳转类 , 导致系统的复杂性提高 , 同时也为维护带来了难度 , 所以在采用迪米特法则时需要反复权衡 , 既做到让结果清晰 , 又做到高内聚低耦合

**作用 :** 

- 降低类之间的耦合度 , 提高模块的相对独立性
- 提高类的可复用率和系统的扩展性

**实例 :** 

```python
# 对于明星来说, 经纪人是明星的朋友, 而粉丝是陌生人
class Agent(object):
    """经纪人"""
    def set_star(self, star_obj):
        self.star = star_obj
    
    def set_fans(self, fans_obj):
        self.fans = fans_obj
        
    def meeting(self):
        out_string = ''.join(['粉丝', self.fans.get_name(), '与明星', self.star.get_name(), '见面了.'])
        print(out_string)
        
class Star(object):
    """明星"""
    def __init__(self, name):
        self.name = name
    
    def get_name(self):
        return self.name
    
class Fans(object):
    """粉丝"""
    def __init__(self, name):
        self.name = name
        
    def get_name(self):
        return self.name
```

总之 , 迪米特法则的作用在就是解耦 , 但是解耦的程度需要我们格外小心

## 开闭原则

开闭原则

**定义 :** 软件实体应该对扩展开放 , 对修改关闭 . 其含义是说一个软件实体应该通过扩展来实现变化 , 而不是通过修改已有的代码来实现变化 (原话 : `Software entities like classes,modules and functions should be open for extension but closed for modifications.` )

**开闭原则是面向对象程序设计的终极目标**

所有已经投产的代码都是有意义的 , 并且都受系统规则的约束 , 这样的代码都要经过 “千锤百炼” 的测试过程，不仅保证逻辑是正确的，还要保证苛刻条件（高压力、异常、错误）下不产生 “有毒代码” , 因此有变化提出时 , 我们就需要考虑一下 , 原有的健壮代码是否可以不修改 , 仅仅通过扩展实现变化呢 ? 否则 , 就需要把原有的测试过程回笼一遍 , 需要进行单元测试 , 功能测试 , 集成测试甚至是验收测试

**作用 :** 

- 提高代码的可复用性
- 提高软件的可维护性

前面5个原则是对开闭原则的具体解释 , 但是开闭原则并不局限于这么多 , 它没有边界 , 我们要把它应用到实际工作中需要注意以下几点 : 

1. 抽象约束 , 抽象层尽量保持稳定
2. 元数据控制模块行为 (元数据 : 用来描述环境和数据的数据 , 通常说的就是配置参数)
3. 指定项目章程 , 约定优于配置
4. 封装变化 , 将相同的变化封装到一个接口或抽象类中 , 将不同的变化封装到不同的接口或抽象中


# Vue - 实例








<extoc></extoc>

## 创建一个Vue实例

每个 `Vue` 应用都是通过用 `Vue` 函数创建一个新的 `Vue` 实例开始的 : 

```javascript
var vm = new Vue({
  // 选项
})
```

虽然没有完全遵循 `MVVM` 模型 , 但是 `Vue` 的设计也受到了它的启发 , 因此在文档中经常会使用 `vm` (ViewModel 的缩写) 这个变量名表示 `Vue` 实例

当创建一个 `Vue` 实例时 , 你可以传入一个选项对象 , 这篇教程主要描述的就是如何使用这些选项来创建你想要的行为 , 作为参考 , 你也可以在 [API 文档](https://vuejs.org/v2/api/index.html)中浏览完整的选项列表

一个 `Vue` 应用由一个通过 `new Vue` 创建的根 `Vue` 实例 , 以及可选的嵌套的 , 可复用的组件树组成 , 举个例子 , 一个 `todo` 应用的组件树可以是这样的 : 

```
根实例
└─ TodoList
   ├─ TodoItem
   │  ├─ DeleteTodoButton
   │  └─ EditTodoButton
   └─ TodoListFooter
      ├─ ClearTodosButton
      └─ TodoListStatistics
```

我们会在稍后的组件系统章节具体展开 , 不过现在 , 你只需要明白所有的 `Vue` 组件都是 `Vue` 实例 , 并且接受相同的选项对象 (一些根实例特有的选项除外)

## 数据与方法

当一个 `Vue` 实例被创建时 , 它向 `Vue` 的响应式系统中加入了其 `data` 对象中能找到的所有的属性 , 当这些属性的值发生改变时 , 视图将会产生 "响应" , 即匹配更新为新的值

```javascript
// 我们的数据对象
var data = { a: 1 }

// 该对象被加入到一个 Vue 实例中
var vm = new Vue({
  data: data
})

// 获得这个实例上的属性
// 返回源数据中对应的字段
vm.a == data.a // => true

// 设置属性也会影响到原始数据
vm.a = 2
data.a // => 2

// 反之亦然
data.a = 3
vm.a // => 3
```

当这些数据改变时 , 视图会进行重新渲染 , 值得注意的是只有当实例被创建时 `data` 中存在的属性才是响应式的 , 也就是说如果你添加一个新的属性 , 比如 : 

```javascript
vm.b = 'hi'
```

那么对 `b` 的改动将不会触发任何视图的更新 , 如果你知道你会在晚些时候需要一个属性 , 但是一开始它为空或者不存在 , 那么你仅需要设置一些初始值 , 比如 : 

```javascript
data: {
  newTodoText: '',
  visitCount: 0,
  hideCompletedTodos: false,
  todos: [],
  error: null
}
```

这里唯一的例外是使用 `Object.freeze()` , 这会组织修改现有的属性 , 也意味着响应系统无法再追踪变化

```javascript
var obj = {
  foo: 'bar'
}

Object.freeze(obj)

new Vue({
  el: '#app',
  data: obj
})
```

```html
<div id="app">
  <p>{{ foo }}</p>
  <!-- 这里的 `foo` 不会更新！ -->
  <button v-on:click="foo = 'baz'">Change it</button>
</div>
```

除了数据属性 , `Vue` 实例还暴露了一些有用的实例属性与方法 , 它们都有前缀 `$` , 以便与用户定义的属性区分开来 , 例如 : 

```javascript
var data = { a: 1 }
var vm = new Vue({
  el: '#example',
  data: data
})

vm.$data === data // => true
vm.$el === document.getElementById('example') // => true

// $watch 是一个实例方法
vm.$watch('a', function (newValue, oldValue) {
  // 这个回调将在 `vm.a` 改变后调用
})
```

以后你可以在 [API 参考](https://cn.vuejs.org/v2/api/#实例属性)中查阅到完整的实例属性和方法的列表 

## 实例生命周期钩子

每个 `Vue` 实例在被创建时都要经过一系列的初始化过程——例如 , 需要设置数据监听 , 编译模板 , 将实例挂载到 DOM 并在数据变化时更新 DOM 等 , 同时在这个过程中也会运行一些叫做生命周期钩子的函数 , 这给了用户在不同阶段添加自己的代码的机会

比如 `created` 钩子可以用来在一个实例被创建之后执行代码 : 

```javascript
new Vue({
  data: {
    a: 1
  },
  created: function () {
    // `this` 指向 vm 实例
    console.log('a is: ' + this.a)
  }
})
// => "a is: 1"
```

也有一些其它的钩子 , 在实例生命周期的不同阶段被调用 , 如 [`mounted`](https://cn.vuejs.org/v2/api/#mounted) , [`updated`](https://cn.vuejs.org/v2/api/#updated) 和[`destroyed `](https://cn.vuejs.org/v2/api/#destroyed) , 生命周期钩子的 `this` 上下文指向调用它的 Vue 实例

不要在选项属性或回调上使用[箭头函数](https://developer.mozilla.org/zh-CN/docs/Web/JavaScript/Reference/Functions/Arrow_functions) , 比如`created: () => console.log(this.a)` 或`vm.$watch('a', newValue => this.myMethod())` , 因为箭头函数是和父级上下文绑定在一起的 , `this` 不会是如你所预期的 Vue 实例 , 经常导致`Uncaught TypeError: Cannot read property of undefined` 或`Uncaught TypeError: this.myMethod is not a function` 之类的错误

## 生命周期图示

下图展示了实例的生命周期 , 你不需要立马弄明白所有的东西 , 不过随着你的不断学习和使用，它的参考价值会越来越高

![lifecycle](D:\桌面\lifecycle.png)


















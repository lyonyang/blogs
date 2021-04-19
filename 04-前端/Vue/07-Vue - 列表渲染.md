# Vue - 列表渲染


<extoc></extoc>

## v-for迭代列表  🍀

我们用 `v-for` 指令根据一组数组的选项列表进行渲染 , `v-for` 指令需要使用 `item in items` 形式的特殊语法 , `items` 是源数据数组并且 `item` 是数组元素迭代的别名

```html
<ul id="example-1">
  <li v-for="item in items">
    {{ item.message }}
  </li>
</ul>
```

```javascript
var example1 = new Vue({
  el: '#example-1',
  data: {
    items: [
      { message: 'Foo' },
      { message: 'Bar' }
    ]
  }
})
```

结果 : 

<div id="example-1" style="border: 1px solid #eee;border-radius: 2px;padding: 25px 35px;margin-top: 1em;margin-bottom: 40px;font-size: 1.2em;line-height: 1.5em;-webkit-user-select: none;user-select: none;overflow-x: auto;">
<ul id="example-1">
  <li v-for="item in items">
    {% raw %}{{ item.message }}{% endraw %}
  </li>
</ul>
</div>

在 `v-for` 块中 , 我们拥有对父作用域属性的完全访问权限 , `v-for` 还支持一个可选的第二个参数为当前项的索引

```html
<ul id="example-2">
  <li v-for="(item, index) in items">
    {{ parentMessage }} - {{ index }} - {{ item.message }}
  </li>
</ul>
```

```javascript
var example2 = new Vue({
  el: '#example-2',
  data: {
    parentMessage: 'Parent',
    items: [
      { message: 'Foo' },
      { message: 'Bar' }
    ]
  }
})
```

结果 : 

<div id="example-2" style="border: 1px solid #eee;border-radius: 2px;padding: 25px 35px;margin-top: 1em;margin-bottom: 40px;font-size: 1.2em;line-height: 1.5em;-webkit-user-select: none;user-select: none;overflow-x: auto;">
<ul id="example-2">
  <li v-for="(item, index) in items">
    {% raw %}{{ parentMessage }}{% endraw %} - {% raw %}{{ index }}{% endraw %} - {% raw %}{{ item.message }}{% endraw %}
  </li>
</ul>
</div>

你也可以用 `of` 替代 `in` 作为分隔符 , 因为它是最接近 JavaScript 迭代器的语法 : 

```html
<div v-for="item of items"></div>
```

## v-for迭代对象  🍀

你也可以用 `v-for` 通过一个对象的属性来迭代

```html
<ul id="v-for-object" class="demo">
  <li v-for="value in object">
    {{ value }}
  </li>
</ul>
```

```javascript
new Vue({
  el: '#v-for-object',
  data: {
    object: {
      firstName: 'John',
      lastName: 'Doe',
      age: 30
    }
  }
})
```

结果 : 

<div style="border: 1px solid #eee;border-radius: 2px;padding: 25px 35px;margin-top: 1em;margin-bottom: 40px;font-size: 1.2em;line-height: 1.5em;-webkit-user-select: none;user-select: none;overflow-x: auto;">
<ul id="v-for-object" class="demo">
  <li v-for="value in object">
    {% raw %}{{ value }}{% endraw %}
  </li>
</ul>
</div>

你也可以提供第二个参数为键名 : 

```html
<div v-for="(value, key) in object">
  {{ key }}: {{ value }}
</div>
```

<div iid="v-for-object" style="border: 1px solid #eee;border-radius: 2px;padding: 25px 35px;margin-top: 1em;margin-bottom: 40px;font-size: 1.2em;line-height: 1.5em;-webkit-user-select: none;user-select: none;overflow-x: auto;"><div v-for="(value, key) in object">
  {{ key }}: {{ value }}
</div>
</div>

第三个参数为索引 : 

```html
<div v-for="(value, key, index) in object">
  {{ index }}. {{ key }}: {{ value }}
</div>
```

<div id="v-for-object" style="border: 1px solid #eee;border-radius: 2px;padding: 25px 35px;margin-top: 1em;margin-bottom: 40px;font-size: 1.2em;line-height: 1.5em;-webkit-user-select: none;user-select: none;overflow-x: auto;">
<div v-for="(value, key, index) in object">
  {{ index }}. {{ key }}: {{ value }}
</div></div>

在遍历对象时 , 是按 `Object.keys()` 的结果遍历 , 但是不能保证它的结果在不同的 JavaScript 引擎下是一致的

## key  🍀

当 Vue.js 用 `v-for` 正在更新已渲染过的元素列表时 , 它默认用 “就地复用” 策略 , 如果数据项的顺序被改变 , Vue 将不会移动 DOM 元素来匹配数据项的顺序 ,  而是简单复用此处每个元素 , 并且确保它在特定索引下显示已被渲染过的每个元素 , 这个类似 Vue 1.x 的 `track-by="$index"` 

这个默认的模式是高效的 , 但是只适用于不依赖子组件状态或临时 DOM 状态 (例如 : 表单输入值) 的列表渲染输出

为了给 Vue 一个提示 , 以便它能跟踪每个节点的身份 , 从而重用和重新排序现有元素 , 你需要为每项提供一个唯一 `key` 属性 , 理想的 `key` 值是每项都有的且唯一的 id , 这个特殊的属性相当于 Vue 1.x 的 `track-by`  , 但它的工作方式类似于一个属性 , 所以你需要用 `v-bind` 来绑定动态值 (在这里使用简写) : 

```html
<div v-for="item in items" :key="item.id">
  <!-- 内容 -->
</div>
```

建议尽可能在使用 `v-for` 时提供 `key` , 除非遍历输出的 DOM 内容非常简单 , 或者是刻意依赖默认行为以获取性能上的提升

因为它是 Vue 识别节点的一个通用机制 , `key` 并不与 `v-for` 特别关联 , key 还具有其他用途 , 我们将在后面的指南中看到其他用途

## 数组更新检测  🍀

### 变异方法  🍀

Vue 包含一组观察数组的变异方法 , 所以它们也将会触发视图更新 , 这些方法如下 : 

- `push()` , 从末尾添加
- `pop()` , 从某位删除
- `shift()` , 从头部添加
- `unshift()` , 从头部删除
- `splice()` , 删除元素 , 删除索引为 1 的元素 : `splice(index, 1)`
- `sort()` , 排序
- `reverse()` , 反转

你可以打开控制台 , 然后用前面例子的 `items` 数组调用变异方法 : `example1.items.push({ message: 'Baz' })` 

### 替换数组  🍀

变异方法 (mutation method) , 顾名思义 , 会改变被这些方法调用的原始数组 , 相比之下 , 也有非变异 (non-mutating method) 方法 , 例如 : `filter()`, `concat()` 和 `slice()` , 这些不会改变原始数组 , 但总是返回一个新数组 , 当使用非变异方法时 , 可以用新数组替换旧数组 : 

```javascript
example1.items = example1.items.filter(function (item) {
  return item.message.match(/Foo/)
})
```

你可能认为这将导致 Vue 丢弃现有 DOM 并重新渲染整个列表 , 幸运的是 , 事实并非如此 , Vue 为了使得 DOM 元素得到最大范围的重用而实现了一些智能的、启发式的方法 , 所以用一个含有相同元素的数组去替换原来的数组是非常高效的操作

### 注意事项  🍀

由于 JavaScript 的限制 , Vue 不能检测以下变动的数组 : 

1. 当你利用索引直接设置一个项时 , 例如 : `vm.items[indexOfItem] = newValue`
2. 当你修改数组的长度时 , 例如 : `vm.items.length = newLength`

举个例子 : 

```javascript
var vm = new Vue({
  data: {
    items: ['a', 'b', 'c']
  }
})
vm.items[1] = 'x' // 不是响应性的
vm.items.length = 2 // 不是响应性的
```

为了解决第一类问题 , 以下两种方式都可以实现和 `vm.items[indexOfItem] = newValue` 相同的效果 , 同时也将触发状态更新 : 

```javascript
// Vue.set
Vue.set(vm.items, indexOfItem, newValue)
```

```javascript
// Array.prototype.splice
vm.items.splice(indexOfItem, 1, newValue)
```

你也可以使用 [`vm.$set`](https://vuejs.org/v2/api/#vm-set) 实例方法 , 该方法是全局方法 `Vue.set` 的一个别名 : 

```javascript
vm.$set(vm.items, indexOfItem, newValue)
```

为了解决第二类问题 , 你可以使用 `splice` : 

```javascript
vm.items.splice(newLength)
```

## 对象更改检测  🍀

还是由于 JavaScript 的限制 , **Vue 不能检测对象属性的添加或删除** : 

```javascript
var vm = new Vue({
  data: {
    a: 1
  }
})
// `vm.a` 现在是响应式的

vm.b = 2
// `vm.b` 不是响应式的
```

对于已经创建的实例 , Vue 不能动态添加根级别的响应式属性 , 但是 , 可以使用 `Vue.set(object, key, value)` 方法向嵌套对象添加响应式属性 , 例如 , 对于 : 

```javascript
var vm = new Vue({
  data: {
    userProfile: {
      name: 'Anika'
    }
  }
})
```

你可以添加一个新的 `age` 属性到嵌套的 `userProfile` 对象 : 

```javascript
Vue.set(vm.userProfile, 'age', 27)
```

你还可以使用 `vm.$set` 实例方法 , 它只是全局 `Vue.set` 的别名 : 

```javascript
vm.$set(vm.userProfile, 'age', 27)
```

有时你可能需要为已有对象赋予多个新属性 , 比如使用 `Object.assign()` 或 `_.extend()` , 在这种情况下 , 你应该用两个对象的属性创建一个新的对象。所以 , 如果你想添加新的响应式属性 , 不要像这样 : 

```javascript
Object.assign(vm.userProfile, {
  age: 27,
  favoriteColor: 'Vue Green'
})
```

你应该这样做 : 

```javascript
vm.userProfile = Object.assign({}, vm.userProfile, {
  age: 27,
  favoriteColor: 'Vue Green'
})
```

## 显示过滤/排序结果  🍀

有时 , 我们想要显示一个数组的过滤或排序副本 , 而不实际改变或重置原始数据 , 在这种情况下 , 可以创建返回过滤或排序数组的计算属性

例如 : 

```html
<li v-for="n in evenNumbers">{{ n }}</li>
```

```javascript
data: {
  numbers: [ 1, 2, 3, 4, 5 ]
},
computed: {
  evenNumbers: function () {
    return this.numbers.filter(function (number) {
      return number % 2 === 0
    })
  }
}
```

在计算属性不适用的情况下 (例如 , 在嵌套 `v-for` 循环中) 你可以使用一个 method 方法 : 

```html
<li v-for="n in even(numbers)">{{ n }}</li>
```

```javascript
data: {
  numbers: [ 1, 2, 3, 4, 5 ]
},
methods: {
  even: function (numbers) {
    return numbers.filter(function (number) {
      return number % 2 === 0
    })
  }
}
```

## v-for取值范围  🍀

`v-for` 也可以取整数 , 在这种情况下 , 它将重复多次模板

```html
<div>
  <span v-for="n in 10">{{ n }} </span>
</div>
```

结果 : 

<div id="app" style="border: 1px solid #eee;border-radius: 2px;padding: 25px 35px;margin-top: 1em;margin-bottom: 40px;font-size: 1.2em;line-height: 1.5em;-webkit-user-select: none;user-select: none;overflow-x: auto;">
<div>
  <span v-for="n in 10">{{ n }}</span>
</div>
</div>

## template里使用v-for  🍀

类似于 `v-if` , 你也可以利用带有 `v-for` 的 `<template>` 渲染多个元素 , 比如 : 

```html
<ul>
  <template v-for="item in items">
    <li>{{ item.msg }}</li>
    <li class="divider" role="presentation"></li>
  </template>
</ul>
```

## v-for与v-if  🍀

当它们处于同一节点 , `v-for` 的优先级比 `v-if` 更高 , 这意味着 `v-if` 将分别重复运行于每个 `v-for` 循环中 , 当你想为仅有的一些项渲染节点时 , 这种优先级的机制会十分有用 , 如下 : 

```html
<li v-for="todo in todos" v-if="!todo.isComplete">
  {{ todo }}
</li>
```

上面的代码只传递了未完成的 todos

而如果你的目的是有条件地跳过循环的执行 , 那么可以将 `v-if` 置于外层元素 (或 `<template>`)上 , 如 : 

```html
<ul v-if="todos.length">
  <li v-for="todo in todos">
    {{ todo }}
  </li>
</ul>
<p v-else>No todos left!</p>
```

## 组件中使用v-for  🍀

在自定义组件里 , 你可以像任何普通元素一样用 `v-for` 

```html
<my-component v-for="item in items" :key="item.id"></my-component>
```

> 2.2.0+ 的版本里 , 当在组件中使用 `v-for` 时 , `key` 现在是必须的

然而 , 任何数据都不会被自动传递到组件里 , 因为组件有自己独立的作用域 , 为了把迭代数据传递到组件里 , 我们要用 `props`  : 

```html
<my-component
  v-for="(item, index) in items"
  v-bind:item="item"
  v-bind:index="index"
  v-bind:key="item.id"
></my-component>
```

不自动将 `item` 注入到组件里的原因是 , 这会使得组件与 `v-for` 的运作紧密耦合 , 明确组件数据的来源能够使组件在其他场合重复使用

下面是一个简单的 todo list 的完整例子 : 

```html
<div id="todo-list-example">
  <form v-on:submit.prevent="addNewTodo">
    <label for="new-todo">Add a todo</label>
    <input
      v-model="newTodoText"
      id="new-todo"
      placeholder="E.g. Feed the cat"
    >
    <button>Add</button>
  </form>
  <ul>
    <li
      is="todo-item"
      v-for="(todo, index) in todos"
      v-bind:key="todo.id"
      v-bind:title="todo.title"
      v-on:remove="todos.splice(index, 1)"
    ></li>
  </ul>
</div>
```

注意这里的 `is="todo-item"` 属性 , 这种做法在使用 DOM 模板时是十分必要的 , 因为在 `<ul>` 元素内只有 `<li>` 元素会被看作有效内容。这样做实现的效果与 `<todo-item>` 相同 , 但是可以避开一些潜在的浏览器解析错误。查看 [DOM 模板解析说明](https://vuejs.org/v2/guide/components.html#DOM-Template-Parsing-Caveats) 来了解更多信息

```javascript
Vue.component('todo-item', {
  template: '\
    <li>\
      {{ title }}\
      <button v-on:click="$emit(\'remove\')">Remove</button>\
    </li>\
  ',
  props: ['title']
})

new Vue({
  el: '#todo-list-example',
  data: {
    newTodoText: '',
    todos: [
      {
        id: 1,
        title: 'Do the dishes',
      },
      {
        id: 2,
        title: 'Take out the trash',
      },
      {
        id: 3,
        title: 'Mow the lawn'
      }
    ],
    nextTodoId: 4
  },
  methods: {
    addNewTodo: function () {
      this.todos.push({
        id: this.nextTodoId++,
        title: this.newTodoText
      })
      this.newTodoText = ''
    }
  }
})
```

<div id="todo-list-example" style="border: 1px solid #eee;border-radius: 2px;padding: 25px 35px;margin-top: 1em;margin-bottom: 40px;font-size: 1.2em;line-height: 1.5em;-webkit-user-select: none;user-select: none;overflow-x: auto;">  <form v-on:submit.prevent="addNewTodo">
    <label for="new-todo">Add a todo</label>
    <input
      v-model="newTodoText"
      id="new-todo"
      placeholder="E.g. Feed the cat"
    >
    <button>Add</button>
  </form>
  <ul>
    <li
      is="todo-item"
      v-for="(todo, index) in todos"
      v-bind:key="todo.id"
      v-bind:title="todo.title"
      v-on:remove="todos.splice(index, 1)"
    ></li>
  </ul>
</div>

<script src="vue.min.js"></script>

<script>
  Vue.component('todo-item', {
    template: '\
      <li>\
        {{ title }}\
        <button v-on:click="$emit(\'remove\')">Remove</button>\
      </li>\
    ',
    props: ['title']
  });
  
  new Vue({
    el: '#todo-list-example',
    data: {
      newTodoText: '',
      todos: [
        {
          id: 1,
          title: 'Do the dishes',
        },
        {
          id: 2,
          title: 'Take out the trash',
        },
        {
          id: 3,
          title: 'Mow the lawn'
        }
      ],
      nextTodoId: 4
    },
    methods: {
      addNewTodo: function () {
        this.todos.push({
          id: this.nextTodoId++,
          title: this.newTodoText
        })
        this.newTodoText = ''
      }
    }
  });

  new Vue({
    el: '#v-for-object',
    data: {
      object: {
        firstName: 'John',
        lastName: 'Doe',
        age: 30
      }
    }
  });
  
  var example2 = new Vue({
    el: '#example-2',
    data: {
      parentMessage: 'Parent',
      items: [
        { message: 'Foo' },
        { message: 'Bar' }
      ]
    }
  });

  var example1 = new Vue({
    el: '#example-1',
    data: {
      items: [
        { message: 'Foo' },
        { message: 'Bar' }
      ]
    }
  });
</script>

 
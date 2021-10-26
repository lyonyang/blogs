






<extoc></extoc>

## Vue - 介绍

## Vue.js是什么  🍀

`Vue`  是一套用于构建用户界面的渐进式框架 , 与其它大型框架不同的是 , `Vue` 被设计为可以自底向上逐层应用 , `Vue` 的和核心库只关注视图层 , 不仅易于上手 , 还便于与第三方库或已有项目整合 , 另一方面 , 当与现代化的工具链以及各种支持类库结合使用时 , `Vue` 也完全能够为复杂的单页应用提供驱动

## 起步  🍀

尝试 `Vue.js` 最简单的方法是使用 [`Jsfiddle`](https://jsfiddle.net/boilerplate/vue/) 的 `Vue` 工具 , 可以直接从官网提供的 [`Hello World`](https://jsfiddle.net/chrisvfritz/50wL7mdz/) 例子开始

我们也可以自己创建一个 `.html` 文件 , 然后在里面引入 `Vue` :

```html
<!-- 开发环境版本，包含了用帮助的命令行警告 -->
<script src="https://cdn.jsdelivr.net/npm/vue/dist/vue.js"></script>
```

或者 : 

```html
<!-- 生产环境版本，优化了尺寸和速度 -->
<script src="https://cdn.jsdelivr.net/npm/vue"></script>
```

这里我们就自己创建一个 `index.html` 来完成教程 , 为了将 `Javascript` 与 `HTML` 分离 , 我们再创建一个 `index.js` 存放 `Javascript` 代码 , 以下不再说明

## 声明式渲染  🍀

`Vue.js` 的核心是一个允许采用简介的模板语法来声明式地将数据渲染进 DOM 的系统 : 

我们只截取重要代码 , `index.html` 如下 : 

```html
<div id="app">
  {{ message }}
</div>
<!-- 以下代码在后续内容中不再说明 -->
<script src="https://cdn.jsdelivr.net/npm/vue/dist/vue.js"></script>
<script src="index.js"></script>
```

在 `index.js` 中

```javascript
var app = new Vue({
    el: '#app',
    data: {
        message: 'Hello Vue!'
    }
});
```

浏览器页面效果如下 : 

<div id="app" style="border: 1px solid #eee;border-radius: 2px;padding: 25px 35px;margin-top: 1em;margin-bottom: 40px;font-size: 1.2em;line-height: 1.5em;-webkit-user-select: none;user-select: none;overflow-x: auto;">
  {% raw %}
    {{ message }}
  {% endraw %}
</div>



我们已经成功创建了第一个 `Vue` 应用 , 看起来这跟渲染一个字符串模板非常类似 , 但是 `Vue` 在背后做了大量工作 , 现在数据和 DOM 已经被建立了关联 , 所有东西都是响应式的 , 我们可以就在当前页面打开浏览器的 `Javascript控制台` , 并修改 `app.message` 的值 , 你将看到上面的例子会相应地更新

除了文本插值 , 我们还可以像这样来绑定元素特性 : 

```html
<div id="app-2" style="border: 1px solid #eee;border-radius: 2px;padding: 25px 35px;margin-top: 1em;margin-bottom: 40px;font-size: 1.2em;line-height: 1.5em;-webkit-user-select: none;user-select: none;overflow-x: auto;">
  <span v-bind:title="message">
    鼠标悬停几秒钟查看此处动态绑定的提示信息！
  </span>
</div>
```

```javascript
var app2 = new Vue({
  el: '#app-2',
  data: {
    message: '页面加载于 ' + new Date().toLocaleString()
  }
})
```

<div id="app-2" style="border: 1px solid #eee;border-radius: 2px;padding: 25px 35px;margin-top: 1em;margin-bottom: 40px;font-size: 1.2em;line-height: 1.5em;-webkit-user-select: none;user-select: none;overflow-x: auto;">
  <span v-bind:title="message">
    鼠标悬停几秒钟查看此处动态绑定的提示信息 !
  </span>
</div>

这里我们遇到了一点新东西 , 你看到的 `v-bind` 特性被成为指令 , 指令带有前缀 `v-` , 以表示它们是 `Vue` 提供的特殊特性 , 这与 `AngularJS` 的 `ng-` 很相似 . 它们会在渲染的 DOM 上应用特殊的响应式行为 , 在这里 , 该指令的意思是 : "将这个元素节点的 `title` 特性和 `Vue` 实例的 `message` 属性保持一致" 

如果你再次打开浏览器的 `JavaScript` 控制台 , 输入 `app2.message = '新消息'` , 就会再一次看到这个绑定了 `title` 特性的 HTML 已经进行了更新

## 条件与循环  🍀

像其他模板语言语法一样 , `Vue` 当然有条件与循环

```html
<div id="app-3">
  <p v-if="seen">现在你看到我了</p>
</div>
```

```javascript
var app3 = new Vue({
  el: '#app-3',
  data: {
    seen: true
  }
})
```

<div id="app-3" style="border: 1px solid #eee;border-radius: 2px;padding: 25px 35px;margin-top: 1em;margin-bottom: 40px;font-size: 1.2em;line-height: 1.5em;-webkit-user-select: none;user-select: none;overflow-x: auto;">
  <p v-if="seen">现在你看到我了</p>
</div>

继续在控制台输入 `app3.seen = false` , 你会发现之前显示的消息消失了

这个例子演示了我们不仅可以把数据绑定到 DOM 文本或特性 , 还可以绑定到 DOM 结构

此外 , `Vue` 也提供了一个强大的过渡效果系统 , 可以在 `Vue` 插入/更新/移除元素时自动应用过渡效果

还有其它很多指令 , 每个都有特殊的功能 , 例如 , `v-for` 指令可以绑定数组的数据来渲染一个项目列表 : 

```html
<div id="app-4">
  <ol>
    <li v-for="todo in todos">
      {{ todo.text }}
    </li>
  </ol>
</div>
```

```javascript
var app4 = new Vue({
  el: '#app-4',
  data: {
    todos: [
      { text: '学习 JavaScript' },
      { text: '学习 Vue' },
      { text: '整个牛项目' }
    ]
  }
})
```

<div id="app-4" style="border: 1px solid #eee;border-radius: 2px;padding: 25px 35px;margin-top: 1em;margin-bottom: 40px;font-size: 1.2em;line-height: 1.5em;-webkit-user-select: none;user-select: none;overflow-x: auto;">
  <ol>
    <li v-for="todo in todos">
        {% raw %}
          {{ todo.text }}
        {% endraw %}
    </li>
  </ol>
</div>

在控制台里 , 输入 `app4.todos.push({text:'新项目'})` , 你会发现列表最后添加了一个新项目

## 处理用户输入  🍀

为了让用户和你的应用进行交互 , 我们可以用 `v-on` 指令添加一个事件监听器 , 通过它调用在 `Vue` 实例中定义的方法 : 

```html
<div id="app-5">
  <p>{{ message }}</p>
  <button v-on:click="reverseMessage">逆转消息</button>
</div>
```

```javascript
var app5 = new Vue({
  el: '#app-5',
  data: {
    message: 'Hello Vue.js!'
  },
  methods: {
    reverseMessage: function () {
      this.message = this.message.split('').reverse().join('')
    }
  }
})
```

<div id="app-5" style="border: 1px solid #eee;border-radius: 2px;padding: 25px 35px;margin-top: 1em;margin-bottom: 40px;font-size: 1.2em;line-height: 1.5em;-webkit-user-select: none;user-select: none;overflow-x: auto;">
  <p>{% raw %}{{ message }}{% endraw %}</p>
  <button v-on:click="reverseMessage">逆转消息</button>
</div>

注意在 `reverseMessage` 方法中 , 我们更新了应用的状态 , 但没有触碰 DOM ——所有的 DOM 操作都有 `Vue` 来处理 , 你编写的代码只需要关注逻辑层面即可

`Vue` 还提供了 `v-model` 指令 , 它能轻松实现表单输入和应用状态之间的双向绑定

```html
<div id="app-6">
  <p>{{ message }}</p>
  <input v-model="message">
</div>
```

```javascript
var app6 = new Vue({
  el: '#app-6',
  data: {
    message: 'Hello Vue!'
  }
})
```

<div id="app-6" style="border: 1px solid #eee;border-radius: 2px;padding: 25px 35px;margin-top: 1em;margin-bottom: 40px;font-size: 1.2em;line-height: 1.5em;-webkit-user-select: none;user-select: none;overflow-x: auto;">
  <p>{% raw %}{{ message }}{% endraw %}</p>
  <input v-model="message">
</div>

## 组件化应用构建  🍀

组件系统是 `Vue` 的另一个重要概念 , 因为它是一种抽象 , 允许我们是使用小型 , 独立和通常可复用的组件构建大型应用 , 仔细想想 , 几乎任意类型的应用界面都可以抽象为一个组件树 : 

![components](http://oux34p43l.bkt.clouddn.com/components.png)

在 `Vue` 里 , 一个组件本质上是一个拥有预定义选项的一个 `Vue` 实例 , 在 `Vue` 中注册组件很简单 :

```javascript
// 定义名为 todo-item 的新组件
Vue.component('todo-item', {
  template: '<li>这是个待办项</li>'
})
```

现在你可以用它构建另一个组件模板 : 

```html
<ol>
  <!-- 创建一个 todo-item 组件的实例 -->
  <todo-item></todo-item>
</ol>
```

但是这样会为每个代办项渲染同样的文本 , 为了使其更加酷炫 , 我们应用从父作用域将数据传到子组件才对 , 我们修改一下组件定义 , 使之能够接受一个 `prop` : 

```javascript
Vue.component('todo-item', {
  // todo-item 组件现在接受一个
  // "prop"，类似于一个自定义特性。
  // 这个 prop 名为 todo。
  props: ['todo'],
  template: '<li>{{ todo.text }}</li>'
})
```

现在 , 我们可以使用 `v-bind` 指令将代办项传到循环输出的每个组件中 : 

```html
<div id="app-7" style="border: 1px solid #eee;border-radius: 2px;padding: 25px 35px;margin-top: 1em;margin-bottom: 40px;font-size: 1.2em;line-height: 1.5em;-webkit-user-select: none;user-select: none;overflow-x: auto;>
  <ol>
    <!--
      现在我们为每个 todo-item 提供 todo 对象
      todo 对象是变量，即其内容可以是动态的。
      我们也需要为每个组件提供一个“key”，稍后再
      作详细解释。
    -->
    <todo-item
      v-for="item in groceryList"
      v-bind:todo="item"
      v-bind:key="item.id">
    </todo-item>
  </ol>
</div>
```

```javascript
Vue.component('todo-item', {
  props: ['todo'],
  template: '<li>{{ todo.text }}</li>'
})

var app7 = new Vue({
  el: '#app-7',
  data: {
    groceryList: [
      { id: 0, text: '蔬菜' },
      { id: 1, text: '奶酪' },
      { id: 2, text: '随便其它什么人吃的东西' }
    ]
  }
})
```

<div id="app-7" style="border: 1px solid #eee;border-radius: 2px;padding: 25px 35px;margin-top: 1em;margin-bottom: 40px;font-size: 1.2em;line-height: 1.5em;-webkit-user-select: none;user-select: none;overflow-x: auto;">
  <ol>
    <!--
      现在我们为每个 todo-item 提供 todo 对象
      todo 对象是变量，即其内容可以是动态的。
      我们也需要为每个组件提供一个“key”，稍后再
      作详细解释。
    -->
    <todo-item
      v-for="item in groceryList"
      v-bind:todo="item"
      v-bind:key="item.id">
    </todo-item>
  </ol>
</div>

尽管这只是一个刻意设计的例子 , 但是我们已经设法将应用分割成两个更小的单元 , 子单元通过 `prop` 接口与父单元进行了良好的解藕 , 我们现在可以进一步改进 `<todo-item>` 组件 , 提供更为复杂的模板和逻辑 , 而不会影响到父单元

在一个大型应用中 , 有必要将整个应用程序划分为组件 , 以使开发更易管理 , 在后续教程中我们将详述组件 , 不过这里有一个假想的例子 , 以展示使用了组件的应用模板是什么样的 : 

```html
<div id="app">
  <app-nav></app-nav>
  <app-view>
    <app-sidebar></app-sidebar>
    <app-content></app-content>
  </app-view>
</div>
```

## 与自定义元素的关系  🍀

你可能已经注意到 `Vue` 组件非常类似于自定义元素——它是 [Web 组件规范](https://www.w3.org/wiki/WebComponents/)的一部分 , 这是因为 Vue 的组件语法部分参考了该规范 , 例如 Vue 组件实现了 [Slot API](https://github.com/w3c/webcomponents/blob/gh-pages/proposals/Slots-Proposal.md) 与 `is` 特性 , 但是 , 还是有几个关键差别 : 

1. Web 组件规范仍然处于草案阶段 , 并且未被所有浏览器原生实现 , 相比之下 , Vue 组件不需要任何 `polyfill ` , 并且在所有支持的浏览器 (IE9 及更高版本) 之下表现一致 , 必要时 , Vue 组件也可以包装于原生自定义元素之内
2. Vue 组件提供了纯自定义元素所不具备的一些重要功能 , 最突出的是跨组件数据流 , 自定义事件通信以及构建工具集成

## 下一步  🍀

我们刚才简单介绍了 `Vue` 核心最基本的功能——本教程的其余部分将涵盖这些功能以及其它高级功能更详细的细节 , 所以请务必读完整个教程 !  

<script src="vue.min.js"></script>

<script>
  var app = new Vue({
      el: '#app',
      data: {
          message: 'Hello Vue!'
      }
  });

  var app2 = new Vue({
      el: '#app-2',
      data: {
          message: '页面加载于 ' + new Date().toLocaleString()
      }
  });

  var app3 = new Vue({
      el: '#app-3',
      data: {
          seen: true
      }
  });

  var app4 = new Vue({
      el: '#app-4',
      data: {
          todos: [
              {text: '学习 JavaScript'},
              {text: '学习 Vue'},
              {text: '整个牛项目'}
          ]
      }
  });

  var app5 = new Vue({
      el: '#app-5',
      data: {
          message: 'Hello Vue.js!'
      },
      methods: {
          reverseMessage: function () {
              this.message = this.message.split('').reverse().join('')
          }
      }
  });

  var app6 = new Vue({
      el: '#app-6',
      data: {
          message: 'Hello Vue!'
      }
  });

  Vue.component('todo-item', {
      props: ['todo'],
      template: '<li>{% raw %}{{ todo.text }}{% endraw %}</li>'
  });

  var app7 = new Vue({
      el: '#app-7',
      data: {
          groceryList: [
              {id: 0, text: '蔬菜'},
              {id: 1, text: '奶酪'},
              {id: 2, text: '随便其它什么人吃的东西'}
          ]
      }
  });
</script>

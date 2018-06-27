# Vue - 组件基础

## 基本示例  🍀

这里有一个 Vue 组件的示例 : 

```javascript
// 定义一个名为 button-counter 的新组件
Vue.component('button-counter', {
  data: function () {
    return {
      count: 0
    }
  },
  template: '<button v-on:click="count++">You clicked me {{ count }} times.</button>'
})
```

组件是可复用的 Vue 实例 , 且带有一个名字 : 在这个例子中是 `<button-counter>` , 我们可以在一个通过 `new Vue` 创建的 Vue 根实例中 , 把这个组件作为自定义元素来使用 : 

```html
<div id="components-demo">
  <button-counter></button-counter>
</div>
```

```javascript
new Vue({ el: '#components-demo' })
```

因为组件是可复用的 Vue 实例 , 所以它们与 `new Vue` 接收相同的选项 , 例如 `data`、`computed`、`watch`、`methods` 以及生命周期钩子等 , 仅有的例外是像 `el` 这样根实例特有的选项

## 组件的复用  🍀

你可以将组件进行任意次数的复用 : 

```html
<div id="components-demo">
  <button-counter></button-counter>
  <button-counter></button-counter>
  <button-counter></button-counter>
</div>
```

注意当点击按钮时 , 每个组件都会各自独立维护它的 `count` , 因为你每用一次组件 , 就会有一个它的新**实例**被创建

### 组件的data  🍀

当我们定义这个 `<button-counter>` 组件时 , 你可能会发现它的 `data` 并不是像这样直接提供一个对象 : 

```javascript
data: {
  count: 0
}
```

取而代之的是 , **一个组件的 data 选项必须是一个函数** , 因此每个实例可以维护一份被返回对象的独立的拷贝 : 

```javascript
data: function () {
  return {
    count: 0
  }
}
```

## 组件的组织  🍀

通常一个应用会以一棵嵌套的组件树的形式来组织 : 

![Component Tree](http://oux34p43l.bkt.clouddn.com/components.png)

例如 , 你可能会有页头、侧边栏、内容区等组件 , 每个组件又包含了其它的像导航链接、博文之类的组件

为了能在模板中使用 , 这些组件必须先注册以便 Vue 能够识别 , 这里有两种组件的注册类型 : **全局注册**和**局部注册** , 至此 , 我们的组件都只是通过 `Vue.component` 全局注册的 : 

```javascript
Vue.component('my-component-name', {
  // ... options ...
})
```

全局注册的组件可以用在其被注册之后的任何 (通过 `new Vue`) 新创建的 Vue 根实例 , 也包括其组件树中的所有子组件的模板中

## Prop  🍀

早些时候 , 我们提到了创建一个博文组件的事情 , 问题是如果你不能向这个组件传递某一篇博文的标题或内容之类的我们想展示的数据的话 , 它是没有办法使用的 , 这也正是 prop 的由来

Prop 是你可以在组件上注册的一些自定义特性 , 当一个值传递给一个 prop 特性的时候 , 它就变成了那个组件实例的一个属性 , 为了给博文组件传递一个标题 , 我们可以用一个 `props` 选项将其包含在该组件可接受的 prop 列表中 : 

```html
Vue.component('blog-post', {
  props: ['title'],
  template: '<h3>{{ title }}</h3>'
})
```

一个组件默认可以拥有任意数量的 prop , 任何值都可以传递给任何 prop , 在上述模板中 , 你会发现我们能够在组件实例中访问这个值 , 就像访问 `data` 中的值一样

一个 prop 被注册之后 , 你就可以像这样把数据作为一个自定义特性传递进来 : 

```html
<blog-post title="My journey with Vue"></blog-post>
<blog-post title="Blogging with Vue"></blog-post>
<blog-post title="Why Vue is so fun"></blog-post>
```

然而在一个典型的应用中 , 你可能在 `data` 里有一个博文的数组 : 

```javascript
new Vue({
  el: '#blog-post-demo',
  data: {
    posts: [
      { id: 1, title: 'My journey with Vue' },
      { id: 2, title: 'Blogging with Vue' },
      { id: 3, title: 'Why Vue is so fun' }
    ]
  }
})
```

并想要为每篇博文渲染一个组件 : 

```html
<blog-post
  v-for="post in posts"
  v-bind:key="post.id"
  v-bind:title="post.title"
></blog-post>
```

如上所示 , 你会发现我们可以使用 `v-bind` 来动态传递 prop , 这在你一开始不清楚要渲染的具体内容 , 比如从一个 API 获取博文列表的时候 , 是非常有用的

[Prop详细](https://vuejs.org/v2/guide/components-props.html)

## 单个根元素  🍀

当构建一个 `<blog-post>` 组件时 , 你的模板最终会包含的东西远不止一个标题 : 

```html
<h3>{{ title }}</h3>
```

最最起码 , 你会包含这篇博文的正文 : 

```html
<h3>{{ title }}</h3>
<div v-html="content"></div>
```

然而如果你在模板中尝试这样写 , Vue 会显示一个错误 , 并解释道 `every component must have a single root element (每个组件必须只有一个根元素)` , 你可以将模板的内容包裹在一个父元素内 , 来修复这个问题 , 例如 : 

```html
<div class="blog-post">
  <h3>{{ title }}</h3>
  <div v-html="content"></div>
</div>
```

看起来当组件变得越来越复杂的时候 , 我们的博文不只需要标题和内容 , 还需要发布日期、评论等等 , 为每个相关的信息定义一个 prop 会变得很麻烦 : 

```html
<blog-post
  v-for="post in posts"
  v-bind:key="post.id"
  v-bind:title="post.title"
  v-bind:content="post.content"
  v-bind:publishedAt="post.publishedAt"
  v-bind:comments="post.comments"
></blog-post>
```

所以是时候重构一下这个 `<blog-post>` 组件了 , 让它变成接受一个单独的 `post` prop : 

```html
<blog-post
  v-for="post in posts"
  v-bind:key="post.id"
  v-bind:post="post"
></blog-post>
```

```html
Vue.component('blog-post', {
  props: ['post'],
  template: `
    <div class="blog-post">
      <h3>{{ post.title }}</h3>
      <div v-html="post.content"></div>
    </div>
  `
})
```

上述的这个和一些接下来的示例使用了 JavaScript 的模板字符串来让多行的模板更易读 , 它们在 IE 下并没有被支持 , 所以如果你需要在不 (经过 Babel 或 TypeScript 之类的工具) 编译的情况下支持 IE , 请使用折行转义字符取而代之

现在 , 不论何时为 `post` 对象添加一个新的属性 , 它都会自动地在 `<blog-post>` 内可用。

## 通过事件向父级组件发送消息  🍀

在我们开发 `<blog-post>` 组件时 , 它的一些功能可能要求我们和父级组件进行沟通 , 例如我们可能会引入一个可访问性的功能来放大博文的字号 , 同时让页面的其它部分保持默认的字号

在其父组件中 , 我们可以通过添加一个 `postFontSize` 数据属性来支持这个功能 : 

```javascript
new Vue({
  el: '#blog-posts-events-demo',
  data: {
    posts: [/* ... */],
    postFontSize: 1
  }
})
```

它可以在模板中用来控制所有博文的字号 : 

```html
<div id="blog-posts-events-demo">
  <div :style="{ fontSize: postFontSize + 'em' }">
    <blog-post
      v-for="post in posts"
      v-bind:key="post.id"
      v-bind:post="post"
    ></blog-post>
  </div>
</div>
```

现在我们在每篇博文正文之前添加一个按钮来放大字号 : 

```html
Vue.component('blog-post', {
  props: ['post'],
  template: `
    <div class="blog-post">
      <h3>{{ post.title }}</h3>
      <button>
        Enlarge text
      </button>
      <div v-html="post.content"></div>
    </div>
  `
})
```

问题是这个按钮不会做任何事 : 

```html
<button>
  Enlarge text
</button>
```

当点击这个按钮时 , 我们需要告诉父级组件放大所有博文的文本 , 幸好 Vue 实例提供了一个自定义事件的系统来解决这个问题 , 我们可以调用内建的 `$emit` 并传入事件的名字 , 来向父级组件触发一个事件 : 

```html
<button v-on:click="$emit('enlarge-text')">
  Enlarge text
</button>
```

然后我们可以用 `v-on` 在博文组件上监听这个事件 , 就像监听一个原生 DOM 事件一样 : 

```html
<blog-post
  ...
  v-on:enlarge-text="postFontSize += 0.1"
></blog-post>
```

### 使用事件抛出一个值  🍀

有的时候用一个事件来抛出一个特定的值是非常有用的 , 例如我们可能想让 `<blog-post>`组件决定它的文本要放大多少 , 这时可以使用 `$emit` 的第二个参数来提供这个值 : 

```html
<button v-on:click="$emit('enlarge-text', 0.1)">
  Enlarge text
</button>
```

然后当在父级组件监听这个事件的时候 , 我们可以通过 `$event` 访问到被抛出的这个值 : 

```html
<blog-post
  ...
  v-on:enlarge-text="postFontSize += $event"
></blog-post>
```

或者 , 如果这个事件处理函数是一个方法 : 

```html
<blog-post
  ...
  v-on:enlarge-text="onEnlargeText"
></blog-post>
```

那么这个值将会作为第一个参数传入这个方法 : 

```javascript
methods: {
  onEnlargeText: function (enlargeAmount) {
    this.postFontSize += enlargeAmount
  }
}
```

### 组件上使用 v-model  🍀

自定义事件也可以用于创建支持 `v-model` 的自定义输入组件 , 记住 : 

```html
<input v-model="searchText">
```

等价于 : 

```html
<input
  v-bind:value="searchText"
  v-on:input="searchText = $event.target.value"
>
```

当用在组件上时 , `v-model` 则会这样 : 

```html
<custom-input
  v-bind:value="searchText"
  v-on:input="searchText = $event"
></custom-input>
```

为了让它正常工作 , 这个组件内的 `<input>` 必须 : 

- 将其 `value` 特性绑定到一个名叫 `value` 的 prop 上
- 在其 `input` 事件被触发时 , 将新的值通过自定义的 `input` 事件抛出

写成代码之后是这样的 : 

```javascript
Vue.component('custom-input', {
  props: ['value'],
  template: `
    <input
      v-bind:value="value"
      v-on:input="$emit('input', $event.target.value)"
    >
  `
})
```

现在 `v-model` 就应该可以在这个组件上完美地工作起来了 : 

```html
<custom-input v-model="searchText"></custom-input>
```

## 通过插槽分发内容  🍀

和 HTML 元素一样 , 我们经常需要向一个组件传递内容 , 像这样 : 

```html
<alert-box>
  Something bad happened.
</alert-box>
```

幸好 , Vue 自定义的 `<slot>` 元素让这变得非常简单 : 

```javascript
Vue.component('alert-box', {
  template: `
    <div class="demo-alert-box">
      <strong>Error!</strong>
      <slot></slot>
    </div>
  `
})
```

如你所见 , 我们只要在需要的地方加入插槽就行了——就这么简单 ! 

更多插槽相关 : [插槽](https://vuejs.org/v2/guide/components-slots.html)

## 动态组件  🍀

有的时候 , 在不同组件之间进行动态切换是非常有用的 , 比如在一个多标签的界面里 : 

Home component

上述内容可以通过 Vue 的 `<component>` 元素加一个特殊的 `is` 特性来实现 : 

```html
<!-- 组件会在 `currentTabComponent` 改变时改变 -->
<component v-bind:is="currentTabComponent"></component>
```

在上述示例中 , `currentTabComponent` 可以包括

- 已注册组件的名字 , 或
- 一个组件的选项对象

## 解析 DOM 模板时的注意事项  🍀

有些 HTML 元素 , 诸如 `<ul>`、`<ol>`、`<table>` 和 `<select>` , 对于哪些元素可以出现在其内部是有严格限制的 , 而有些元素 , 诸如 `<li>`、`<tr>` 和 `<option>` , 只能出现在其它某些特定的元素内部

这会导致我们使用这些有约束条件的元素时遇到一些问题 , 例如 : 

```html
<table>
  <blog-post-row></blog-post-row>
</table>
```

这个自定义组件 `<blog-post-row>` 会被作为无效的内容提升到外部 , 并导致最终渲染结果出错。幸好这个特殊的 `is` 特性给了我们一个变通的办法 : 

```html
<table>
  <tr is="blog-post-row"></tr>
</table>
```

需要注意的是 , 如果我们从以下来源使用模板的话 , 这条限制是不存在的 : 

- 字符串 (例如 : `template: '...'`)
- 单文件组件 (`.vue`)
- ``

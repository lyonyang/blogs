# Vue - Vue-cli








<extoc></extoc>

## 介绍

`Vue CLI` 是一个用于 `vue.js` 快速开发的系统 , 提供 : 

- 交互式工程脚手架 `@vue/cli` 
- 零配置快速成型 `@vue/cli` + `@vue/cli-service-global` 
- 运行时依赖项 `@vue/cli-service` : 
  - 可升级
  - 建立在 `WebPack` 之上 , 有合理的默认设置
  - 可通过项目内配置文件进行配置
  - 可扩展的插件
- 丰富的官方插件 , 集成了前端生态系统中最好的工具 

`Vue CLI` 旨在成为 VUE 生态系统的标准工具基线 , 它确保各种构建工具与合理的缺省值一起顺利工作 , 这样你就可以专注于编写应用程序 , 而不是花费数天时间与配置进行争论 , 同时 , 它仍然可以灵活地调整每个工具的配置

使用 `vue-cli` 可以快速构建我们的 Vue 项目

## 快速开始

### 安装 Node.js

在安装 `vue-cli` 之前 , 我们需要安装 Node 环境 , 因为我们需要使用 `npm` 包管理器

[官网下载安装](https://nodejs.org/en/)

### 安装 vue-cli

安装好 node 之后 , 我们就可以安装 `vue-cli` 了 : 

```shell
npm install -g vue-cli
```

待安装完成后 , 在中断使用 `vue -help` 出现以下信息说明安装成功 : 

```shell
C:\Users\Lyon>vue -help

  Usage: vue <command> [options]

  Options:

    -V, --version  output the version number
    -h, --help     output usage information

  Commands:

    init           generate a new project from a template
    list           list available official templates
    build          prototype a new project
    create         (for v3 warning only)
    help [cmd]     display help for [cmd]
```

可用的官方模板如下 : 

```shell
C:\Users\Lyon>vue list

  Available official templates:

  ★  browserify - A full-featured Browserify + vueify setup with hot-reload, linting & unit testing.
  ★  browserify-simple - A simple Browserify + vueify setup for quick prototyping.
  ★  pwa - PWA template for vue-cli based on the webpack template
  ★  simple - The simplest possible Vue setup in a single HTML file
  ★  webpack - A full-featured Webpack + vue-loader setup with hot reload, linting, testing & css extraction.
  ★  webpack-simple - A simple Webpack + vue-loader setup for quick prototyping.
```

### 初始化项目

使用 `webpack` 模块初始化 `my-project` 项目

```shell
$ vue init webpack my-project

? Project name my-project
? Project description A Vue.js project
? Author lyonyang <547903993@qq.com>
? Vue build standalone
? Install vue-router? Yes
? Use ESLint to lint your code? No
? Set up unit tests No
? Setup e2e tests with Nightwatch? No
? Should we run `npm install` for you after the project has been created? (recommended) npm

   vue-cli · Generated "my-project".


# Installing project dependencies ...
# ========================
.....
# Project initialization finished!
# ========================

To get started:

  cd my-project
  npm run dev

Documentation can be found at https://vuejs-templates.github.io/webpack
```

### 切换到项目目录

```shell
$ cd my-project
```

### 下载项目依赖包

```shell
$ npm install
```

### 启动当前项目

```shell
$ npm run dev

> my-project@1.0.0 dev D:\my-project
> webpack-dev-server --inline --progress --config build/webpack.dev.conf.js

 95% emitting

 DONE  Compiled successfully in 4755ms                                                                          10:39:13

 I  Your application is running here: http://localhost:8080
```

访问 `http://localhost:8000` 

![my-project](/asserts/my-project.png)

## 项目结构

注释部分为未启用功能部分

```
.
├── build/                      # webpack config files
│   └── ...
├── config/
│   ├── index.js                # main project config
│   └── ...
├── node_modules/               # library root
├── src/
│   ├── main.js                 # app entry file
│   ├── App.vue                 # main app component
│   ├── components/             # ui components
│   │   └── ...
│   └── assets/                 # module assets (processed by webpack)
│       └── ...
├── static/                     # pure static assets (directly copied)
# ├── test/
# │   └── unit/                   # unit tests
# │   │   ├── specs/              # test spec files
# │   │   ├── eslintrc            # config file for eslint with extra settings only for unit tests    # 
# │   │   ├── index.js            # test build entry file
# │   │   ├── jest.conf.js        # Config file when using Jest for unit tests
# │   │   └── karma.conf.js       # test runner config file when using Karma for unit tests
# │   │   ├── setup.js            # file that runs before Jest runs your unit tests
# │   └── e2e/                    # e2e tests
# │   │   ├── specs/              # test spec files
# │   │   ├── custom-assertions/  # custom assertions for e2e tests
# │   │   ├── runner.js           # test runner script
# │   │   └── nightwatch.conf.js  # test runner config file
├── .babelrc                    # babel config
├── .editorconfig               # indentation, spaces/tabs and similar settings for your editor
# ├── .eslintrc.js                # eslint config
# ├── .eslintignore               # eslint ignore rules
├── .gitignore                  # sensible defaults for gitignore
├── .postcssrc.js               # postcss config
├── index.html                  # index.html template
├── package.json                # build scripts and dependencies
└── README.md                   # Default README file
```

## 构建命令

所有的构建命令都是通过 NPM 脚本执行的

> npm run dev

开启一个本地 Node.js 开发服务器

> npm run build

打包生产资源 , 如 JavaScript , HTML , CSS 等

> npm run unit

在 JSDOM 中运行单元测试

> npm run e2e

运行端到端的测试

> npm run lint

运行 eslint 并报告错误链接
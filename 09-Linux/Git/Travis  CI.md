# Travis  CI


<extoc></extoc>

## 介绍  🍀

[`Travis CI`](http://travis-ci.org/) 是一款免费服务 , 专门托管面向开源开发组织的CI (Continuous Integration , 持续集成) 

CI是XP (Extreme Programming , 极限编程) 的实践之一 , 近年来人们普遍使用`Jenkins`等软件来实现这一目的

让CI软件监视仓库 , 可以在开发者发送提交后立刻执行自动测试或构建 ; 通过持续执行这样一个操作 , 可以检测出开发者意外发送的提交或无意的逻辑偏差 , 让代码保持在一定质量以上

所以当我们使用GitHub发布代码时 , 可以使用`Travis CI` ; `Travis CI`支持Ruby , PHP , Perl , Python , Java , JavaScript (node.js)等Web相关的语言

更多支持语言 , [Support language](https://docs.travis-ci.com/) 

## 编写配置文件  🍀

我们如果想要仓库使用`Travis CI` , 一般情况下 , 我们只需要在仓库中添加`.travis.yml`这样一个`Travis CI`专用的文件 , `Travis CI` 就与GitHub集成了

以`node.js`为例 , 编写`.travis.yml`文件

```shell
language: "node_js"     # 指定默认运行环境,这里是node_js
node_js:                # 指定node版本
  - "node"
install:                # 指定安装脚本
  - "npm install gitbook -g"
  - "npm install -g gitbook-cli"
branches:               # 指定分支
  only:
    - master
env:                    # 定义环境变量
  global:
    - GH_REF: github.com/[username]/[repository].git
    - secure: [ssh_key]
script:                  # 指定要运行的脚本
  - bash summary_create.sh
  - travis_wait 100 bash deploy.sh
```

将这个文件放到本地仓库中 , 然后`push`给GitHub端 , 我们基本完成了使用`Travis CI`的准备工作

关于各种语言的配置参考 , 点击进入[语言参考](https://docs.travis-ci.com/user/languages)

## 检测配置文件  🍀

`Travis CI`专门提供了`Travis WebLint`提供用户检测`.travis.yml`文件是否存在问题 , 检测时只需要指定仓库即可

**与GitHub集成**

1. 首先我们访问[Travis CI](https://www.travis-ci.org/) , 点击右上角的`Sign in with GitHub` , 进行GitHub认证
2. 登录完毕后 , `Sign in with GitHub`就会变成用户的GitHub信息了 , 点击头像的下拉框的`Profile` , 我们在下方就可以看到我们的GitHub仓库了 , 只需要将对应的仓库名旁边的开关设置为ON , 就可以对该仓库应用Travis CI了
3. 至此 , 你再进入你的GitHub → → Settings → → Applications → → Authorized OAuth Apps , 我们就可以看到可以访问我们账户的应用程序信息了 , 这里就是`Travis CI`了


这样 , 我们只要向GitHub进行push操作 , 就会自动触发`Travis CI`端的自动测试了

集成的仓库在`Travis CI`端的URL为`https://travis-ci.org/用户名/仓库名` , 用户可以在这个页面查看自动测试的执行情况 , 另外跳转至`Travis CI`首页直接收缩自己的

**将Travis CI的结果添加至README.md**

如果我们想要在我们的GitHub的README.md中看到我们的测试结果 , 只需在我们的README.md中添加如下信息 : 

```
# Markdown语法

[![Build Status](https://secure.travis-ci.org/用户名/仓库名.png?imageMogr2/blur/1x0/quality/75|watermark/2/text/bHlvbi55YW5nQHFxLmNvbQ==/font/YXBhcmFqaXRh/fontsize/560/fill/Izk0ODI4Mg==/dissolve/100/gravity/SouthEast/dx/10/dy/10)](http://travis-ci.org/用户名/仓库名)
```

这样 , 在我们查看README.md时 , 就能够通过图片观察测试是否通过了 ; 绿色的图片就表示仓库内代码顺利通过测试 , 灰色的图片表示仓库没有通过测试 , 证明仓库可能存在某种问题 , 这样既可以显示仓库的健全性 , 又可以防止自己遗漏`Travis CI的结果`

## 生成Access Token  🍀

与GitHub继承之后 , 此时Travis已经开始监控了 , 但是它却没有访问权限 , 所以我们需要生成一个`Personal access tokens` 

进入我们的GitHub , 点击头像下的`Settings`  →  `Developer settings`   →  `Personal access tokens` 

随后点击`Generate new token` , 进入`New personal access token`界面 , 在`Token description`中加入`Travis` , 随后选择该令牌所具有的权限范围 , 这里我们只需将`repo`勾上就可以了

最后`Generate token`

生成之后一定不要离开页面 , 我们需要快速复制这个token , 虽然添加到Travis的settings中 , 因为一旦页面刷新或者关掉 , 就会消失 , 那么你又得重新创建了

.....

















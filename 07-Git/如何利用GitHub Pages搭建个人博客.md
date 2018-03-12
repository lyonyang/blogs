# 如何利用GitHub Pages搭建个人博客

**欢迎收藏交流 , 如需转载 , 请注明出处**

## 1. 开始  🍀

如今程序猿没个个人站点或是博客 , 都不好意思出门了

所以在这里教大家如何构建一本书 (博客) : https://lyonyang.github.io/blogs/ 这是我的个人博客 , 样式就是这样的啦

那么 , 开始吧

### 1.1. 搭建准备  🍀

实际上 , 没什么要准备的 ... GitHub账号就不用说了 , 创建一个新的仓库吧 , 来存放个人博客笔记文件

### 1.2. 搭建要求  🍀

本博客 (更形象点 : 一本书) , 文件必须为`.md`文件 , 也就是`MarkDown` 文件 , 所以如果你不是这种格式 , 那么我建议你开始使用 , [Markdown语法说明](https://www.appinn.com/markdown/) , 当然还有`.rst` , 也就是`reStructuredText` 文件也是可以的 , 但是本文仅说明关于Markdown的构建

**为什么用Markdown?**

1. Markdown是一种轻量级的「标记语言」 , 通常为程序员群体所用 , 适用于泡技术论坛、写博客日志、技术文稿、记录代码片段、起草邮件等场景
2. Markdown语法十分简单 , 常用的标记符号不超过十个 , 用于日常写作记录绰绰有余
3. 纯文本编辑 , 可以转换成各种文档格式 , 如 : html , tex , pd等等
4. 最重要的是 , Markdown能在GitHub上直接展示出来 , 所以你可以看到很多GitHub开源项目 (不开源你也看不到啊) 中的README都是`.md`文件 

本地Markdown编辑可以使用Typora , VSCode , Atom等等 , 本人用的是Typora , 支持功能比较多

### 1.3. 搭建说明  🍀

本博客使用GitBook进行构建 , 如Hexo一样 , 我们并不是使用GitBook所有 , 而是仅仅使用它的一个功能 : GitBook和Hexo都能帮我们把Markdown格式文件转换成html文件 , 并且是附带了样式的html文件

当然这种构建对于我们只使用一两次还好 , 如果像我们的博客需要长期更新 , 那么手动构建就太麻烦了 , 所以我们使用一个持续集成工具 Travis CI , 它是开源的 , 所以放心 , 不要钱

也就是说 ,  所有的准备如下 : 

- GitHub + .md + GitBook + Travis CI

那么就开始了

## 2. 配置文件   🍀

创建仓库就不说了 , 创建完成之后 , 我们就先开始添加配置文件了 , 这是构建的重中之重

配置文件目录

```
.
├── .travis.yml        -- 持续集成配置
├── deploy.sh          -- 构建脚本
├── book.json          -- gitbook样式文件
├── summary_create.sh  -- 自动创建SUMMARY.md文件
├── SUMMARY.md         -- 必须要有
└── README.md   	   -- 必须要有
```

### 2.1. .travis.yml  🍀

当Travis CI发现你的仓库有更新时 , 就会来你仓库找到这个配置文件 , 并执行它

以`node_js`语言为例 

```shell
language: "node_js"
node_js:
  - "node"
install:
  - "npm install -g gitbook@3.2.3"
  - "npm install -g gitbook-cli@2.3.2"
branches:
  only:
    - master
env:
  global:
    - GH_REF: github.com/用户名/仓库名.git
script:
  - bash summary_create.sh
  - travis_wait 100 bash deploy.sh
```

注意GH_REF修改成各自的GitHub用户名和仓库

### 2.2. deploy.sh  🍀

该文件是`.travis.yml`中需要执行的脚本

```shell
#!/bin/bash
git config user.name "user"
git config user.email "email@xxx.com"
git checkout -b gitbook
git status
git add .
git commit -m "[Travis] Update SUMMARY.md"
git push -f "https://${GH_TOKEN}@${GH_REF}" gitbook:gitbook
gitbook install
gitbook build .
if [ $? -ne 0 ];then
    exit 1
fi
cd _book
git init
git checkout --orphan gh-pages
git status
sleep 5
git add .
git commit -m "Update gh-pages"
git remote add origin git@github.com:用户名/仓库.git
git push -f "https://${GH_TOKEN}@${GH_REF}" gh-pages:gh-pages
```

### 2.3. summary_create.sh  🍀

```
#!/bin/bash

# 文件命名增加 [0-9][0-9]- 通过文件名对文章进行排序,生成目录

find `ls|egrep -v "_book|_other|node_modules"` -type f -name "*.md"|sed 's#README.md#00README.md#g'|sort|awk -F "/" '{if($NF!="00README.md") print $0"/" ;else print $0}' OFS="/"|sed  's#[^/]##g'|awk '{a=(length-1);while(a>0){printf "  ";a--}print "* "}' > /tmp/summary_1
find `ls|egrep -v "_book|_other|node_modules"` -type f -name "*.md"|sed "s#README.md#00README.md#g"|sort|awk -F "[./]" '{if($(NF-1) != "00README") print $(NF-1)"]("$0")" ;else print $(NF-2)"]("$0")"}' > /tmp/summary_2
paste -d "[" /tmp/summary_1 /tmp/summary_2 > tmp_SUMMARY.md
sed 's#00README.md#README.md#g' tmp_SUMMARY.md|grep -v "SUMMARY](SUMMARY"|awk  '{if(NR==1)print "# Summary\n\n* [Introduction](README.md)\n* [SUMMARY](SUMMARY.md)";else print $0}' > SUMMARY.md && mv tmp_SUMMARY.md /tmp

# 由于Mac下,sed -i参数必须要指定备份文件(虽然可以使用 -i "" 传递一个空字符,不备份,但是这种写法在Linux上会报错),所以这里不使用-i参数

# 文件名便于排序的时候会使用类似01-,开头, 在目录显示的时候删除这部分 

# 调整目录显示, 在Mac 下使用需要调整参数

sed -ri 's#(\S+* \[)[0-9]+-(.*$)#\1\2#g' SUMMARY.md
```

### 2.4. book.json  🍀

GitBook样式文件 , 也就是生成html附带的样式

```
{
    "title": "blog",
    "author": "author",
    "description": "desc",
    "extension": null,
    "generator": "site",
    "links": {
        "sharing": {
            "all": null,
            "facebook": null,
            "google": null,
            "twitter": null,
            "weibo": null
        }
    },
    "pdf": {
        "fontSize": 18,
        "footerTemplate": null,
        "headerTemplate": null,
        "margin": {
            "bottom": 36,
            "left": 62,
            "right": 62,
            "top": 36
        },
        "pageNumbers": false,
        "paperSize": "a4"
    },
    "plugins": [
        "toggle-chapters",
        "theme-comscore",
        "splitter",
        "github",
        "-sharing",
        "-lunr",
        "-search",
        "search-plus",
        "anchor-navigation-ex@1.0.10",
        "editlink"
    ],
    "pluginsConfig": {
        "anchor-navigation-ex": {
            "showLevel": false,
            "mode": "float",
            "float": {
                "showLevelIcon": false,
                "level1Icon": "fa fa-hand-o-right",
                "level2Icon": "fa fa-hand-o-right",
                "level3Icon": "fa fa-hand-o-right"
            }
        }
    }
}
```

### 2.5. README.md  🍀

项目根目录下必须要有README.md文件 , 并且所有需要构建的文件下 , 也必须要有README.md文件

如 : 

```
.
├── Python
│   ├── ...
│   ├── ...
│   └── README.md      -- 必须要有
├── ...
├── ...
└── README.md   	   -- 必须要有
```

README.md中的内容就是页面上目录显示的内容

### 2.6. SUMMARY.md  🍀

必须要有 , 这个GitBook构建需要的 , 上面summary_create.sh脚本就是来自动帮我们生成目录的

## 3. 添加Personal access tokens  🍀

配置文件添加完成之后 , 我们就要将Travis CI 与GitHub建立连接了

```
点击你的GitHub头像 --> Settings --> Developer settings --> Personal access tokens --> Generate new token
```

进入如下图页面 : 

![New personal access token](http://oux34p43l.bkt.clouddn.com/New%20personal%20access%20token.png)

我们只需给个repo权限就行了

接下来就会自动跳转到如下页面 : 

![Copy Token](http://oux34p43l.bkt.clouddn.com/Copy%20Token.png)

注意 : 一定要先复制这个生成的token , 如果你还没来得及复制 , 那么对不起 , 重新添加一个再复制吧

这个token是用来配置Travis的环境变量的

## 4. 配置Travis CI  🍀

首先我们进入 : [https://travis-ci.org/](https://travis-ci.org/) 

使用GitHub登录

接下来我们可以在Profile下面看到我们的GitHub仓库啦 , 注意[https://travis-ci.org/](https://travis-ci.org/) 搜索的我们的Public仓库 , 对于Private仓库 , 就需要进入[https://travis-ci.com/](https://travis-ci.com/) 

勾选需要持续集成的仓库

![choose repositories](http://oux34p43l.bkt.clouddn.com/choose%20repositories.png)

接下来我们去做一些设置了 , 点击勾选右边的设置按钮

勾选General中的`Build only if .travis.yml is present`

**Environment Variables**

现在我们需要用到上面生成的token了 , 将其复制到Environment Variables中的Value框中 , 并将Name设置为`GH_TOKEN` , 点击ADD添加 , 完成后如下 : 

![add token](http://oux34p43l.bkt.clouddn.com/add%20token.png)

现在基本已经完成了 , 我们可以向我们的仓库做一点更新 , 或者直接点击`More options`选择Trigger build进行构建 , 等待几分钟后 (这是GitBook的一个缺点 , 构建有点慢)

待`https://travis-ci.org/`左侧 `My Repositories` 变成绿色 (黄色表示正在构建) , 我们就可以访问我们的博客啦 

地址 : `https://用户名.github.io/仓库名` 

这个地址使用的是每个仓库自带的GitHub Pages功能 , 在脚本自动创建了gh-pages分支 , 就是用于显示的

至此 , 搭建完成 !

## 5. 注意事项

**注意事项一**

由于构建是从`.md`文件转到`.html`文件 , 所以如果文章中使用了模板语言的语法 , 请嵌入html代码块 , 并顶格写 , 示例

```
​```html
内容{{ name }}
​```
```

**注意事项二**

文章排序默认按英文字母排序 , 如果需要对文章进行排序 , 可以在文件名前添加需要 , 如 : `01-`  , 序号不会在文章页面显示 , 这一步是通过summary_create.sh中实现的

更多注意事项等待发现中 ...

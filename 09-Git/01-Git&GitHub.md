# Git&Github

## 1. Git简介  🍀

### 1.1. Git  🍀

> Git是一个免费并且开源的分布式版本控制系统 , 被设计用来快速 , 高效的管理一切从小到大的项目

### 1.2. 版本控制  🍀

我们所开发的软件在其整个生命周期 , 都需要进行不断的改进 , 比如 , 日常写bug改bug , 对业务的增删改查等 , 如果没有一个工具来帮助我们控制 , 那么日常开发将会是多么的坑 ... 一不小心删了个文件 , 一不小心提交了错误代码 , 一不小心整个项目就没了 ...

所以为了方便我们在开发软件中对各个软件版本的管理与控制 , 于是就有了如下版本控制系统 : 

- CVS , (Concurrent Version System)

  诞生于1985年 , 是由荷兰阿姆斯特丹VU大学的Dick Grune教授实现的 , 是有史以来第一个被大规模使用的版本控制工具 —— 开启版本控制大爆发

- SVN , (Subversion)

  诞生于2000年 , 由`CollabNet`公司资助并开始开发 , 由于其命令行工具名为`svn` , 因此通常被简称为`SVN` , 目的是取代`CVS` —— `集中式`版本控制集大成者

- Git 

  诞生于2005年 , 又`Linux`系统的创始人`Linus`开发而成 , 主要是因为在2005年`Andrew Tridgell` (大名鼎鼎的Samba的作者) 社团对`BitKeeper`进行反向工程 , 于是激怒了`BitKeeper`软件的所有者`BitMover`公司 , 收回了对Linux社区免费使用`BitKeeper`的授权 , 导致Linus第二个伟大作品 —— `分布式`版本控制系统`Git`

### 1.3. 集中式与分布式  🍀

**集中式**

> 集中式版本控制系统 , 将所有数据集中存放在服务器中 , 有便于管理的优点 , 如SVN 
>
> 集中式只存在一个仓库 , 如果开发者开发所处的环境不能连接到服务器 , 就无法获取最新的源代码 , 开发也就无法进行 ; 并且一旦服务器宕机 , 万一服务器故障导致数据消失 , 那么开发者就再也见不到最新的源代码了

![集中式](http://oux34p43l.bkt.clouddn.com/集中式.png)

**分布式**

> 分布式版本控制系统 , 每个人都有完整的版本库 , 开发者不必连接远程仓库 , 如Git
>
> 分布式中每个开发者都具有独立的完整的版本库 , 安全性高 ; 在分布式版本控制系统中通常会有一台服务器充当 "中央服务器" , 这个服务器的作用仅仅是用来方便 "交换" 开发者们之间的修改 , 当然这仅仅是为了使开发者们之间 "交换" 更加方便

![分布式](http://oux34p43l.bkt.clouddn.com/分布式.png)

所以集中式与分布式都具有各自的优缺点 , 在使用时 , 我们应该根据具体情况选择

不过随着Git与Github的普及 , 使用分布式的开发者会占绝大多数 ; 只要规则指定得当 , 分布式同样能够像集中式那样进行管理

## 2. GitHub简介  🍀

**Github 与 Git 是两回事**

`GitHub` 是为开发者提供` Git `仓库的托管服务 , 但是注意 ` Github `并不只是 `Git`仓库的托管服务

在Git中 , 开发者将源代码存入名叫 `"Git仓库"` 的资料库中并加以使用 , **而`Github`则是在网络上提供Git仓库的一项服务** 

也就是说 , `Github`上公开的软件源代码全都是由Git进行管理

### 2.1. GitHub提供的主要功能  🍀

- **Git 仓库**

  我们可以免费建立任意个 GitHub 提供的 Git 仓库 , 但如果需要建立只对特定人物或只对自己公开的私有仓库 , 则需要依照套餐类型B支付每月最低 7 美元的使用费

- **Organization**

  企业导入 GitHub 时建议使用 Organization 账户 , 利用这一功能 , 可以让开发者们使用同一控制面板 , 还能够创建团队并统一管理权限 ; 另外这一账户还为企业提供了用户管理和支付等便捷功能

- **Issue**

  Issue 功能 , 是将一个任务或问题分配给一个 Issue 进行追踪和管理的功能

- **Wiki**

  该功能常用在开发文档或手册的编写中 , Wiki 页也是作为 Git 仓库进行管理的 , 改版的历史记录会被切实保存下来 , 使用者可以放心改写

- **Pull Request**

  开发者向 GitHub 的仓库推送更改或功能添加后 , 可以通过 Pull Request 功能向别人的仓库提出申请 , 请求对方合并
  Pull Request 送出后 , 目标仓库的管理者等人将能够查看 Pull Request 的内容及其中包含的代码更改

## 3. 安装Git  🍀

**在 Linux 上**

```shell
$ sudo apt-get install git
```

**在 Windows 上**

[下载Git](https://git-scm.com/downloads) , 下载完成后之前安装就可以了 

安装成功后我们可以在开始菜单里找到 `Git Bash`  , 或者查看鼠标右键菜单中是否有`Git Bash Here`

### 3.1. 初始设置  🍀

**显示当前配置**

```shell
$ git config --list
```

**设置姓名和邮箱地址**

```shell
$ git config --global user.name "lyon"
$ git config --global user.email "lyon@xxxxx"  # lyon@xxx为邮箱地址
```

**提高命令输出的可读性**

```shell
$ git config --global color.ui auto
```

## 4. GitHub准备工作  🍀

### 4.1. 创建账户  🍀

进入注册页面完成注册 , [点我跳转注册页面](https://github.com/join?source=header-home)

### 4.2. 设置SSH Key  🍀

GitHub上连接已有的仓库时的认证 , 是通过使用SSH的公开密钥认证方式进行的 , 所以我们需要创建一个SSH Key , 并将其添加至GitHub中

```shell
$ ssh-keygen -t rsa -C "lyon@xxx"           # lyon@xxx为邮箱地址
Generating public/private rsa key pair.
Enter file in which to save the key
(/Users/your_user_directory/.ssh/id_rsa):   # 回车
Enter passphrase (empty for no passphrase): # 输入密码
Enter same passphrase again:                # 输入密码
```

创建完成后可以在你的`User`目录下可以看到一个`.ssh`的文件夹 : 

```
.ssh            
├── id_rsa          私有密钥
├── id_rsa.pub      公有密钥
├── known_hosts
└── qwe.ppk
```

### 4.3. 添加公钥  🍀

创建好密钥之后 , 我们需要在GitHub中添加公有密钥 , 这样就可以使用私有密钥进行认证了

进入头像下拉框中的`settings` , 添加公有密钥 , 即复制`id_rsa.pub`中的内容

![new_ssh_key](http://oux34p43l.bkt.clouddn.com/new_ssh_key.png?imageMogr2/blur/1x0/quality/75|watermark/2/text/bHlvbi55YW5nQHFxLmNvbQ==/font/YXBhcmFqaXRh/fontsize/560/fill/Izk0ODI4Mg==/dissolve/100/gravity/SouthEast/dx/10/dy/10)

添加完成之后 , 创建账号时所用的邮箱会接到一封邮件 , 提示 "公有密钥添加完成"

完成后 , 可以用手中的私有密钥与GitHub进行认证和通信 , 如下 : 

```shell
$ ssh -T git@github.com
```

出现如下结果即为成功

```shell
Hi hirocastest! You've successfully authenticated, but GitHub does not
provide shell access.
```

## 5. 创建仓库  🍀

点击头像旁边的 "+" 下拉框 , 选择`New repository`

![create_new_repository](http://oux34p43l.bkt.clouddn.com/create_new_repository.png?imageMogr2/blur/1x0/quality/75|watermark/2/text/bHlvbi55YW5nQHFxLmNvbQ==/font/YXBhcmFqaXRh/fontsize/560/fill/Izk0ODI4Mg==/dissolve/100/gravity/SouthEast/dx/10/dy/10)

- **Repository name**

  仓库名

- **Descriptiion**

  描述信息

- **Public , Private**

  选择创建公开仓库还是私有仓库 , 私有仓库是收费的

- **Initialize this repository with a README**

  选择自动完成初始化仓库 , 并设置README文件

  如果想向GitHub添加手中已有的仓库 , 建议不要勾选

- **Add .gitignore**

  添加`.gitignore`文件

- **Add a license**

  添加的许可协议










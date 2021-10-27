# Git基础命令








<extoc></extoc>

## 1. 前言

### 1.1. 工作区

对于Git来说 , 版本库位于工作区根目录下的`.git`目录中 , 且仅此一处 , 在工作区的子目录下则没有任何其他跟踪文件或目录

而工作区就是我们进行版本控制的某个文件夹 , 我们初始化之后就可以利用Git来进行管理了

### 1.2. 暂存区

在`.git` 目录中有一个`index`文件 , 这个文件就是暂存区(stage) , 当我们执行`git add`命令时 , 我们的修改并不是直接添加到了master分支 , 而是添加到了暂存区 , 我们需要继续执行`git commit`命令才能将修改从暂存区移到master分支 , 这样才算完成了一次提交

## 2. 基本操作

### 2.1. 初始化仓库

我们要使用Git进行版本管理 , 必须先初始化仓库

Git 使用`git init`命令进行初始化

我们可以打开`Git Bash`后手动切换到仓库 , 或者到仓库目录点击右键选择`Git Bash Here` 

```shell
$ mkdir git-tutorial
$ cd git-tutorial
$ git init
Initialized empty Git repository in /Users/github-book
/git-tutorial/.git/
```

初始化成功后 , 会自动生成`.get`目录 , 这个`.git` 存储着管理当前目录内容所需的仓库数据 , 在Git中 , 我们将这个目录的内容称为 "附属于该仓库的工作区"

### 2.2. 查看仓库状态

`git status` 命令用于显示Git仓库的状态 , 工作区和仓库在被操作的过程中 , 状态会不断发生变化 , 在Git操作过程中经常用`git status`命令查看 "当前状态" 

```shell
$ git status
On branch master    # 当前处于master分支

Initial commit      

nothing to commit (create/copy files and use "git add" to track)  # 没有可提交的内容
```

### 2.3. 增删文件

我们一般创建一个GitHub远程仓库时 , 都会选择不自动初始化 , 而是自己来建立`README.md`文件作为管理对象 , 为第一次提交做前期准备

我们可以使用`touch`命令来创建文件

**新建`README.md`到本地仓库**

```shell
$ touch README.md   # 创建一个新文件README.md

$ git status        # 查看仓库状态
On branch master

Initial commit

Untracked files:
  (use "git add <file>..." to include in what will be committed)

        README.md

nothing added to commit but untracked files present (use "git add" to track)
```

我们可以看到在`Untracked files`中显示了`README.md`文件 , 类似地 , 只要对Git的工作区或仓库进行操作 , `git status`命令的显示结果就会发生改变 

**向暂存区中添加文件**

如果只是用Git仓库的工作区创建了文件 , 那么该文件并不会被记入Git仓库的版本管理对象当中 , 因此我们用`git status`命令查看时 , 新增的`README.md`文件时 , 它会显示在`Untracked files`中

所以如果要想让文件成为Git仓库的管理对象 , 就需要用`git add`命令将其加入暂存区 (Stage或者Index) . 暂存区是提交之前的一个临时区域

```shell
$ git add README.md      # 添加至暂存区

$ git status             # 查看仓库状态
On branch master

Initial commit

Changes to be committed:
  (use "git rm --cached <file>..." to unstage)

        new file:   README.md
```

将`README.md`文件加入暂存区后 , `git status`命令的显示结果发生了变化 , `Changes to be committed:` 中显示`new file: 	README.md`

如果想要删除暂存区中的文件 , 可以使用`git rm [filename]`命令进行删除

**保存仓库的历史记录**

当我们使用`git add`命令之后 , 需要使用`git commit`命令将当前暂存区中的文件实际保存到仓库的历史记录中 , 通过这些记录 , 我们就可以在工作区中复原文件 , 在`git commit`中有一个`-m`参数 , 为提交信息 , 是对这个提交的概述

```shell
$ git commit -m "First commit"  
[master (root-commit) 4733231] First commit
 1 file changed, 0 insertions(+), 0 deletions(-)
 create mode 100644 README.md
 
$ git status       
On branch master
nothing to commit, working tree clean

```

### 2.4. 查看日志

`git log` 命令可以查看以往仓库中提交的日志 , 包括可以查看什么人在什么时候进行了提交或合并 , 以及操作前后有怎样的差别

```shell
$ git log
commit 4733231b262d9cd1d4449240735ed56edab65ca1 (HEAD -> master)
Author: lyonyang <lyon@xxx>
Date:   Mon May 29 22:56:50 2017 +0800

    First commit
```

**显示提交信息的第一行**

可以在`git log`命令后加上`--pretty=short`来只查看提交信息的第一行

```shell
$ git log --pretty=short
commit 4733231b262d9cd1d4449240735ed56edab65ca1 (HEAD -> master)
Author: lyonyang <lyon@xxx>

    First commit
```

**显示指定目录或文件日志**

只要在`git log`命令后加上目录名 , 就可以显示改目录下的日志 , 如果是文件名 , 就会只显示与该文件相关的日志

```shell
$ git log README.md
commit 4733231b262d9cd1d4449240735ed56edab65ca1 (HEAD -> master)
Author: lyonyang <lyon@xxx>
Date:   Mon May 29 22:56:50 2017 +0800

    First commit
```

**显示文件的改动**

如果想查看提交所带来的改动 , 可以加上`-p`参数

```shell
$ git log -p
# 指定文件
$ git log -p README.md
```

### 2.5. 查看更改前后区别

`git diff`命令可以查看工作区 , 暂存区 , 最新提交至今的差别

通过`vim`命令修改`README.md`

```shell
$ vim README.md
+# edit README.md
+#
+# First
```

执行`git diff`命令 , 查看当前工作区与暂存区的差别

```shell
$ git diff
diff --git a/README.md b/README.md
index e69de29..88b52b3 100644
--- a/README.md
+++ b/README.md
@@ -0,0 +1,5 @@
+# edit README.md
+
+# First
```

如果工作区和暂存区的状态并无差别 , 那么我们在执行`git commit`命令之前先执行`git diff HEAD`命令 , 查看本次提交与上次提交之间有什么差别 , HEAD是指向当前分支中最新一次提交的指针 , 这是一个好习惯

## 3. 分支操作

在进行多个并行作业时 , 我们会用到分支 , 而在我们日常开发中 , 基本都会采用并发作业的方式 ; 在这类并行开发的过程中 , 往往同时存在多个最新代码状态

从master分支创建了feature-A分支和fix-B分支

![branch](http://oux34p43l.bkt.clouddn.com/branch.png?imageMogr2/blur/1x0/quality/75|watermark/2/text/bHlvbi55YW5nQHFxLmNvbQ==/font/YXBhcmFqaXRh/fontsize/560/fill/Izk0ODI4Mg==/dissolve/100/gravity/SouthEast/dx/10/dy/10)

在不同的分支中 , 可以同时进行完全不同的作业 , 等改分支的作业完成之后 , 再与master分支合并 , 如下 : 

![merge_branch](http://oux34p43l.bkt.clouddn.com/merge_branch.png?imageMogr2/blur/1x0/quality/75|watermark/2/text/bHlvbi55YW5nQHFxLmNvbQ==/font/YXBhcmFqaXRh/fontsize/560/fill/Izk0ODI4Mg==/dissolve/100/gravity/SouthEast/dx/10/dy/10)

通过灵活的使用分支 , 可以让多个人同时高效地进行并行开发 , 并且使开发过程更加的安全

### 3.1. 显示分支

`git branch`命令可以将分支名列表显示 , 同时可以确认当前所在分支

```shell
$ git branch
* master       # 当前只有一个master分支
```

可以看到`master`分支左侧标有 `*` 号 , 这表示我们当前所在分支 , 也就是说 , 我们正在`master`分支下进行开发

### 3.2. 创建分支

`git checkout -b`命令可以用于我们以当前`master`分支为基础 , 创建一个新的分支 , 并切换到新建分支

```shell
$ git checkout -b feature-A       # 创建分支并切换
Switched to a new branch 'feature-A'
M       README.md

$ git branch     # 显示分支
* feature-A     
  master
```

创建并切换我们通过以下两条命令也能收到同样的效果

```shell
$ git branch feature-A     # 创建分支feature-A
$ git checkout feature-A   # 切换到分支feature-A
```

在`feature-A`分支中修改文件并提交

```shell
$ vim README.md                   # 修改文件
+# 
+# branch feature-A

$ git add README.md                # 添加至暂存区

$ git commit -m "Add feature-A"    # 提交
[feature-A 78c070a] Add feature-A
 1 file changed, 5 insertions(+)
```

### 3.3. 切换分支

我们在`feature-A`分支下对文件进行了修改后 , 可以使用`git checkout [branch]`切分支 

```shell
$ git checkout master       # 切换到master分支
Switched to branch 'master'

$ vim README.md             # 进入文件,我们可以发现没有发生改变
```

因为我们的修改只是在`feature-A`分支上建立的 , 而各个分支都是相互独立的 , 所以在`feature-A`分支上做任何事情也不会影响到其他的分支

**切换回上一个分支**

如果想要切换到上一个分支 , 可以使用 `-` (连字符)代替分支名

```shell
$ git checkout -          # 从master分支继续切换回feature-A分支
Switched to branch 'feature-A'
```

### 3.4. 合并分支

通过合并分支 , 可以将一个分支的内容合并到另一个分支中去 , 比如我们上面修改了`feature-A`分支 , 现在将其与`master`分支进行合并 

`git merge`命令用来合并分支 , 首先切换到`master`分支

```shell
$ git checkout master
Switched to branch 'master'

Merge branch 'feature-A'
# Please enter a commit message to explain why this merge is necessary,
# especially if it merges an updated upstream into a topic branch.
#
# Lines starting with '#' will be ignored, and an empty message aborts
# the commit.

# 上述内容保存后关闭即可

$ git merge --no-ff feature-A
Merge made by the 'recursive' strategy.
 README.md | 5 +++++
 1 file changed, 5 insertions(+)
```

为了在历史记录中明确记录下本次分支合并 , 我们需要创建合并提交 , 因此 , 在合并时加上 `--no-ff`参数 

这样就完成了分支的合并了

用`git log --graph`命令可以以图表的形式查看分支提交的内容已被合并

```shell
$ git log --graph
*   commit a905c7028b96d2c003970b095a20b22a03ccc3ad (HEAD -> master)
|\  Merge: 4733231 78c070a
| | Author: lyonyang <547903993@qq.com>
| | Date:   Mon May 29 23:31:47 2017 +0800
| |
| |     Merge branch 'feature-A'
| |
| * commit 78c070aeb464329116f1fc1bf7f84f8201bf7165 (feature-A)
|/  Author: lyonyang <lyon@xxx>
|   Date:   Mon May 29 23:12:23 2017 +0800
|
|       Add feature-A
|
* commit 4733231b262d9cd1d4449240735ed56edab65ca1
  Author: lyonyang <lyon@xxx>
  Date:   Mon May 29 22:56:50 2017 +0800

      First commit

```

## 4. 版本回溯

### 4.1. 回溯

我们可以使用`git rest --hard`命令让仓库的`HEAD` , 暂存区 , 工作区回溯到指定状态 , 只要提供目标时间点的哈希值 , 就可以完全恢复至该时间点的状态

```shell
$ git reset --hard 78c070aeb464329116f1fc1bf7f84f8201bf7165
HEAD is now at 78c070a Add feature-A
```

`git log`命令只能查看以当前状态为终点的历史日志 , 而`git reflog`命令可以查看当前仓库的操作日志 ; 所以如果我们想恢复到回溯之前的版本 , 可以先执行`gitreflog`命令, 查看当前仓库执行过的操作的日志

```shell
$ git reflog
78c070a (HEAD -> master, feature-A) HEAD@{0}: reset: moving to 78c070aeb464329116f1fc1bf7f84f8201bf7165
a905c70 HEAD@{1}: merge feature-A: Merge made by the 'recursive' strategy.
4733231 HEAD@{2}: checkout: moving from feature-A to master
78c070a (HEAD -> master, feature-A) HEAD@{3}: checkout: moving from master to feature-A
4733231 HEAD@{4}: checkout: moving from feature-A to master
78c070a (HEAD -> master, feature-A) HEAD@{5}: commit: Add feature-A
4733231 HEAD@{6}: checkout: moving from master to feature-A
4733231 HEAD@{7}: commit (initial): First commit
```

只要我们不进行Git的GC(Garbage Collection, 垃圾回收) , 就可以通过日志随意调去近期的历史状态 , 这样我们就可以在过去未来中自由穿梭

### 4.2. 消除冲突

合并分支有时会出现冲突的情况 , 我们创建一个新的分支来进行说明

**在feature-B分支上进行修改**

创建并切换`feature-B`分支

```shell
$ git checkout -b feature-B
Switched to a new branch 'feature-B'
```

在`feature-B`分支上修改`README.md`文件内容 

```shell
$ vim README.md
# 在README.md最后添加内容
# +add this line to B branch
```

提交本次修改

```shell
$ git add README.md   # 添加至暂存区

$ git commit -m "add a line to the featrue-B branch"   # 将暂存区的内容提交到当前分支
[feature-B 89be876] add a line to the featrue-B branch
 1 file changed, 1 insertions(+)
```

**在master分支上进行修改**

切换到`master`分支

```shell
$ git checkout master
Switched to branch 'master'
```

在`master`分支上修改`README.md`文件内容 

```shell
$ vim README.md
# 在README.md最后添加内容
# +add this line to B branch
```

提交本次修改

```shell
$ git add README.md

$ git commit -m "add a line to the master branch"
[master 0abd9eb] add a line to the master branch
 1 file changed, 1 insertions(+)
```

到这里 , 两个分支上的README.md文件中的内容就不一样了 , 接下来我们合并这两个分支

**合并分支**

```shell
# 当前在master分支
$ git merge feature-B
Auto-merging README.md
CONFLICT (content): Merge conflict in README.md
Automatic merge failed; fix conflicts and then commit the result.
```

Git返回的内容告诉我们 , README.md文件存在冲突 , 必须手动解决冲突后再提交

通过`git status`查看冲突

```shell
$ git status
On branch master
You have unmerged paths.
  (fix conflicts and run "git commit")
  (use "git merge --abort" to abort the merge)

Unmerged paths:
  (use "git add <file>..." to mark resolution)

        both modified:   README.md

no changes added to commit (use "git add" and/or "git commit -a")
```

查看README.md文件

```shell
$ cat README.md
# edit README.md

# First

# branch feature-A ...

#<<<<<<< HEAD
# add a line to the master branch
#=======
# add this to the feature-B branch
#>>>>>>> feature-B
```

Git用`<<<<<<<` , `=======` , `>>>>>>>` 标记出不同分支的内容 , 为了解决冲突 , 我们需要修改一方来解决冲突 , 比如修改`master`分支或者`feature-B`分支中的`README.md`文件的内容 , 修改完成后保存 , 然后再提交

```shell
$ git add readme.txt 
$ git commit -m "conflict fixed"
[master 1f4c296] conflict fixed
```

再合并分支

```shell
$ git merge feature-B
Already up-to-date.
```

查看分支的合并情况

```shell
$ git log --graph --pretty=oneline --abbrev-commit
*   1f4c296 (HEAD -> master) conflict fixed
|\
| * 89be876 (feature-B) add a line to the featrue-B branch
* | 0abd9eb add a line to the master branch
|/
* 78c070a (feature-A) Add feature-A
* 4733231 First commit
```

最后 , 删除`feature-B`分支

```shell
$ git branch -d feature-B
Deleted branch feature-B (was 89be876).
```

这样我们解决分支冲突问题

### 4.3. 分支管理

通常 , 合并分支时 , 如果课可能 , Git会使用`Fast forward`模式 , 但是这种模式下 , 一旦我们删除分支后 , 那么分支的信息也随之被丢掉了 , 所以为了保留历史的分支信息 , 我们可以强制禁用`Fast forward`模式

在合并分支时使用`--no-f`参数 , 就可以禁用`Fast forward`

```shell
$ git merge --no-ff feature-A
Already up-to-date.
```

本篇主要参考以下两本书籍 : 

- GitHub入门与实践
- Git权威指南
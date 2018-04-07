# Git问题整理
 
## 推送失败
 
错误说明:
 
```git
error: failed to push some refs to 'git@github.com:lyonyang/cadmin.git'
hint: Updates were rejected because the tip of your current branch is behind
hint: its remote counterpart. Integrate the remote changes (e.g.
hint: 'git pull ...') before pushing again.
hint: See the 'Note about fast-forwards' in 'git push --help' for details.
```
 
错误原因:

GitHub远程仓库中的README.md文件不在本地仓库中,远程仓库中没有创建README.md文件同样
 
解释方案:
 
```git
$ git pull --rebase origin master
$ git push -u origin master
```
 
推送成功,问题解决

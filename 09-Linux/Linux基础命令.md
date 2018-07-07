# Linux基础命令

## ls  🍀

```shell
[root@lyonyang ~]# ls [aAdfFhilnrRSt] 目录名称
[root@lyonyang ~]# ls [--colo={never,auto,always}] 目录名称
[root@lyonyang ~]# ls [--full-times] 目录名称
# 参数 : 
-a : 全部的文件,连同隐藏文件(开头为 . 的文件)一起列出来
-A : 仅列出全部的文件(连同隐藏文件,但不包括 . 与 .. 这两个目录)
-d : 仅列出目录本身,而不是列出目录内的文件数据
-f : 直接列出结果,而不进行排序(ls默认会以文件名排序)
-F : 根据文件,目录等信息给予附加数据结构,例如:
	  *:代表可执行文件; /:代表目录; =:代表socket文件; |:代表FIFO文件
-h : 将文件容量以较易读的方式(例如GB,KB等)列出来
-i : 列出inode号码
-l : 列出长数据串,包含文件的属性与权限等数据
-n : 列出UID与GID,而非用户与用户组的名称
-r : 将排序结果反向输出
-R : 连同子目录内容一起列出来,等于该目录下的所有文件都会显示出来
-S : 以文件容量大小排序,而不是用文件名排序
-t : 依时间排序,而不是用文件名
--color=never : 不要依据文件特性给予颜色显示
--color=always : 显示颜色
--color=auto : 让系统自行依据设置来判断是否给予颜色
--full-time : 以完整时间模式(包含年,月,日,时,分)输出
--time=(atime,ctime) : 输出访问时间或改变权限属性时间(ctime)而非内容梗概时间(modification time)
```

## cp  🍀

```shell
[root@lyonyang ~]# cp [-adfilprsu] 源文件(source) 目标文件(destination)
[root@lyonyang ~]# cp [options] source1 source2 source3 ... directory
# 参数 :
-a : 相当于-pdr的意思
-d : 若源文件为连接文件的属性(link file),则复制连接文件属性而非文件本身
-f : 为强制(force)的意思,若目标文件已经存在且无法开启,则删除后再尝试一次
-i : 若目标文件(destination)已经存在时,在覆盖时会先查询问操作的进行
-l : 进行硬连接(hard link)的连接文件创建,而非复制文件本身
-p : 连同文件的属性一起复制过去,而非使用默认属性
-r : 递归持续复制,用于目录的复制行为
-s : 复制成功符号链接文件(symbolic link),即"快捷方式"文件
-u : 若destination比source旧才更新destination
# 注意 : 如果源文件有两个以上,则最后一个目的文件一定要是"目录"才行
```

## rm  🍀

```shell
[root@lyonyang ~]# rm [-fir]  文件或目录
# 参数 :
-f : 就是force的意思,忽略不存在的文件,不会出现警告信息
-i : 互动模式,在删除前会询问用户是否操作
-r : 递归删除,最常用在目录的删除,此参数异常危险
```

## mv  🍀

```shell
[root@lyonyang ~]# mv [-fiu] source destination
[root@lyonyang ~]# mv [options] source1 source2 source3 ... directory
# 参数 : 
-f : fource强制的意思,如果目标文件已经存在,不会询问而直接覆盖
-i : 若目标文件(destination)已经存在时,就会询问是否覆盖
-u : 若目标文件已经存在,且source比较新,才会更新
```

## cat  🍀

```shell
[root@lyonyang ~]# cat [-AbenTv]
# 参数 : 
-A : 相当于-vET的整合参数,可列出一些特殊字符,而不是空白而已
-b : 列出行号,仅针对非空白行做行号显示,空白行不标行号
-E : 将结尾的断行字符$显示出来
-n : 打印出行号,连同空白行也会有行号,与-b的参数不同
-T : 将[Tab]按键以^I显示出来
-v : 列出一些看不出来的特殊字符
```

tac 命令与 cat 命令恰好相反

## nl  🍀

```shell
[root@lyonyang ~]# nl [-bnw] 文件
# 参数 : 
-b : 指定行号指定的方式,主要有两种:
     -b a : 表示不论是否为空行,也同样列出行号(类似cat -n)
     -b t : 如果有空行,空的那一行不要列出行号(默认值)
-n : 列出行号表示的方法,主要有三种:
	 -n ln : 行号在屏幕的最左方显示
	 -n rn : 行号在自己字段的最右方显示,且不加0
	 -n rz : 行号在自己字段的最右方显示,且加0
-w : 行号字段占用的位数
```

## touch  🍀

```shell
[root@lyonyang ~]# touch [-acdmt] 文件
# 参数 : 
-a : 仅修改访问时间
-c : 仅修改文件的时间,若该文件不存在则不创建新文件
-d : 后面可以接欲修改的日期而不用目前的日期,也可以使用--date="日期或时间"
-m : 仅修改mtime
-t : 后面可以接欲修改的时间而不用目前的时间,格式为[YYMMDDhhmm]
```

## which  🍀

```shell
[root@lyonyang ~]# which [-a]  command 
# 参数 :
-a : 将所有由 PATH 目录中可以找到的命令均列出 , 而不知第一个被找到的命令名称
```

## whereis  🍀

```shell
[root@lyonyang ~]# whereis [-bmsu] 文件或目录名
# 参数 : 
-b : 只找二进制格式的文件
-m : 只找在说明文件manual路径下的文件
-s : 只找source源文件
-u : 查找不在上述三个选项当中的其他特殊文件
```

## locate  🍀

该命令如果查找新文件 , 需要更新数据库

手动更新 `updatedb` 

```shell
[root@lyonyang ~]# locate [-ir] keyword
# 参数 : 
-i : 忽略大小写的差异
-r : 后面可接正则表达式的显示方式
```

## find  🍀

```shell
[root@lyonyang ~]# find [PATH] [option] [action]
# 参数 : 
1. 与时间有关的参数:共有-atime,-ctime与-mtime,下面以-mtime说明:
   -mtime n : n为数字,意义为在n天之前的"一天之内"被更改过的文件
   -mtime +n : 列出在n天之前(不含n天本身)被更改过的文件名
   -mtime -n : 列出在n天之内(含n天本身)被更改过的文件名
   -newer file : file为一个存在的文件,列出比file还要新的文件

2. 与用户或用户组有关的参数:
   -uid n : n为数字,这个数字是用户的账号ID,即UID,这个UID是记录在
            /etc/passwd里面与账号名称对应的数字
   -gid n : n为数字,这个数字是用户组名的ID,即GID,这个GID记录在
            /etc/group中
   -user name : name为用户账号名称
   -group name : name为用户组名
   -nouser : 寻找文件的所有者不存在 /etc/passwd 的人
   -nogroup : 寻找文件的所有用户组不存在于 /etc/group 中的文件
   
3. 与文件权限及名称有关的参数:
   -name filename : 查找文件名为filename的文件
   -size [+-]SIZE : 查找比SIZE还要大(+)或小(-)的文件,SIZE规格有:
                    c:代表byte;k:代表1024bytes;
   -type TYPE : 查找文件的类型为TYPE的,类型主要有:
                一般正规文件(f),设备文件(b,c),目录(d),连接文件(l),socket(s),FIFO(p)
   -perm mode : 查找文件权限等于mode的文件,mode类似chmod的属性值,如-rwsr-xr-x属性值为4755
   -perm -mode : 查找文件权限包括mode的文件
   -perm +mode : 查找文件权限包含任一mode的权限的文件
   
   
4. 其他可进行的操作:
   -exec command : command为其他命令,-exec后面可再接其他的命令来处理查找到的结果
   -print : 将结果打印到屏幕上,这个操作是默认的
```



压缩与打包

## gzip,zcat  🍀

```shell
[root@lyonyang ~]# gzip [-cdtv#] 文件名
# 参数 :
-c : 将压缩的数据输出到屏幕上,可通过数据流重定向来处理
-d : 解压缩的参数
-t : 可以用来检测一个压缩文件的一致性,看看文件有无错误
-v : 可以显示出源文件/压缩文件的压缩比等信息
-# : 压缩等级,-1最快,但是压缩比最差,-9最慢,但是压缩比最好,默认是-6
```

## bzip2,bzcat  🍀

```shell
[root@lyonyang ~]# bzip2 [-cdkzv#] 文件名
# 参数 : 
-c : 将压缩的数据输出到屏幕上
-d : 解压缩的参数
-k : 保留原文件,而不会删除原始的文件
-z : 压缩的参数
-v : 可以显示出原文件/压缩文件的压缩比等信息
-# : 与gzip一样
```

## dump  🍀

```shell
[root@lyonyang ~]# dump [-Suvj] [-level] [-f 备份文件] 待备份数据
[root@lyonyang ~]# dump -W
# 参数 :
-S : 仅列出后面的备份数据需要多少磁盘空间才能够备份完毕
-u : 将这次dump的时间记录到/etc/dumpdateS文件中
-v : 将dump的文件过程显示出来
-j : 加入bzip2的支持,将数据进行压缩,默认bzip2压缩等级为2
-level : 等级从0~9共10个等级
-f : 有点类似tar,后面接产生的文件,可接例如/dev/st0设备文件名
-w : 列出在/etc/fstab里面的具有dump设置的分区是否有备份过
```

## restore  🍀

```shell
[root@lyonyang ~]# restore -t [-f dumpfile] [-h]   # 查看dump文件
[root@lyonyang ~]# restore -C [-f dumpfile] [-D 挂载点]  # 比较dump与实际文件
[root@lyonyang ~]# restore -i [-f dumpfile]              # 进入互动模式
[root@lyonyang ~]# restore -r [-f dumpfile]              # 还原整个文件系统
# 参数 : 
-t : 此模式用在查看dump起来的备份文件中含有什么重要数据
-C : 此模式可以将dump内的数据拿出来跟实际的文件系统做比较
     最终会列出"在dump文件内有记录的,且目前文件系统不一样"的文件
-i : 进入互动模式,可以仅还原部分文件,用在dump目录时的还原
-r : 将整个文件系统还原的一种模式,用在还原针对文件系统的dump备份
-h : 查看完整备份数据中的inode与文件系统label等信息
-f : 后面就接你要处理的那个dump文件
-D : 与-C进行搭配,可以查出后面接的挂载点与dump内有不同的文件
```

## tar  🍀

```shell
[root@lyonyang ~]# tar [-j|-z] [cv] [-f 新建的文件名] filename      # 打包与压缩
[root@lyonyang ~]# tar [-j|-z] [tv] [-f 新建的文件名]               # 查看文件名
[root@lyonyang ~]# tar [-j|-z] [xv] [-f 新建的文件名]               # 解压缩
# 参数 : 
-c : 新建打包文件,可搭配-v来查看过程中被打包的文件名
-t : 查看打包文件的内容含有哪些文件名,重点在查看文件名
-x : 解打包或解压缩的功能,可以搭配-C在特定目录解开
     -c,-t,-x不可同时出现在一串命令中
-j : 通过bzip2的支持进行压缩/解压缩,此时文件名最好为 *.tar.bz2
-z : 通过gzip的支持进行压缩/解压缩,此时文件名最好为 *.tar.gz
-v : 在压缩/解压缩的过程中,将正在处理的文件名显示出来
-f filename : -f后面要接被处理的文件名,建议-f单独写一个参数
-C 目录  : 这个参数用在解压缩时,若要在特定目录解压缩,可以使用这个参数
-P : 保留备份数据的原本权限与属性,常用于备份(-c)重要的配置文件
-p : 保留绝对路径,即允许不备份数据中含有根目录存在之意
--exclude=FILE : 在压缩的过程中,不要将FILE打包
```

简单使用记忆 : 

压缩 : `tar -jcv -f filename.tar.bz2 要被压缩的文件或目录名称`

查询 : `tar -jtv -f filename.tar.bz2` 

解压缩 : `tar -jxv -f filename.tar.bz2 -C 欲解压缩的目录` 

 ## dd  🍀

```shell
[root@lyonyang ~]# dd if="input file" of="output file" bs="block size" count="number"
# 参数 :
if : 就是input file ,也可以是设备
of : 就是output file ,也可以是设备
bs : 规划的一个block的大小,若未指定则默认为512bytes(一个扇区的大小)
count : 多少个bs的意思
```

## ps  🍀

```shell
[root@lyonyang ~]# ps aux   # 查看系统所有的进程数据
[root@lyonyang ~]# ps -lA   # 同上
[root@lyonyang ~]# ps axjf  # 连同部分进程树的状态
# 参数 : 
-A : 所有的进程均显示出来,与-e具有同样的作用
-a : 不与terminal有关的所有进程
-u : 有效用户相关的进程
x : 通常与a这个参数一起使用,可列出较完整信息
l : 较长,较详细地将该PID的信息列出
j : 工作的格式
-f : 做一个更为完整的输出
```

## free  🍀

```shell
[root@lyonyang ~]# free [-b|-k|-m|-g] [-t]
# 参数 :
-b : 直接输入free时,显示的单位是
-t : 在输出的最终结果中显示物理内存与swap的总量
```

## uname  🍀

```shell
[root@lyonyang ~]# uname [-asrmpi]
# 参数 :
-a : 所有系统相关的信息,包括下面的数据都会被列出来
-s : 系统内核名称
-r : 内核的版本
-m : 本系统的硬件名称
-p : CPU的类型
-i : 硬件的平台
```

## netstat  🍀

```shell
[root@lyonyang ~]# netstat -[atunlp]
# 参数 :
-a : 将目前系统上所有的连接,监听,Socket数据都列出来
-t : 列出tcp网络数据包的数据
-u : 列出udp网络数据包的数据
-n : 不列出进程的服务名称
-l : 列出目前正在网络监听的服务
-p : 列出该网络服务的进程PID
```

## rpm  🍀

```shell
[root@lyonyang ~]# rpm -ivh package_name
# 参数 :
-i : install 的意思
-v : 查看更详细的安装信息画面
-h : 以安装信息栏显示安装进度
[root@lyonyang ~]# rpm -qa 
[root@lyonyang ~]# rpm -q[licdR] 已安装的软件名称
[root@lyonyang ~]# rpm -qf 存在于系统上面的某个文件名
[root@lyonyang ~]# rpm -qp[licdR] 未安装的某个文件名称   
# 参数 :
-q : 仅查询,后面接的软件名称是否有安装
-qa : 列出所有的已经安装在本机Linux系统上面的所有软件名称
-qi : 列出该软件的详细信息,包含开发商,版本与说明
-ql : 列出该软件所有的文件与目录所在完整文件名
-qc : 列出该软件的所有设置文件
-qd : 列出该软件的所有帮助文件
-qR : 列出与该软件有关的依赖软件所含的文件
-qf : 由后面接的文件名称找出该文件属于哪一个已安装的软件
```


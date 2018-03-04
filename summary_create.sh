#!/bin/bash
# 使用方法: 在项目根目录下执行如下命令
# bash summary_create.sh

# v0.2 --------
# 文件命名增加 [0-9][0-9]- 通过文件名对文章进行排序,生成目录

find `ls|egrep -v "_book|_other|node_modules"` -type f -name "*.md"|sed 's#README.md#00README.md#g'|sort|awk -F "/" '{if($NF!="00README.md") print $0"/" ;else print $0}' OFS="/"|sed  's#[^/]##g'|awk '{a=(length-1);while(a>0){printf "  ";a--}print "* "}' > /tmp/summary_1
find `ls|egrep -v "_book|_other|node_modules"` -type f -name "*.md"|sed "s#README.md#00README.md#g"|sort|awk -F "[./]" '{if($(NF-1) != "00README") print $(NF-1)"]("$0")" ;else print $(NF-2)"]("$0")"}' > /tmp/summary_2
paste -d "[" /tmp/summary_1 /tmp/summary_2 > tmp_SUMMARY.md
sed 's#00README.md#README.md#g' tmp_SUMMARY.md|grep -v "SUMMARY](SUMMARY"|awk  '{if(NR==1)print "# Summary\n\n* [lyonyang](README.md)\n* [SUMMARY](SUMMARY.md)";else print $0}' > SUMMARY.md && mv tmp_SUMMARY.md /tmp

# 由于Mac下,sed -i参数必须要指定备份文件(虽然可以使用 -i "" 传递一个空字符,不备份,但是这种写法在Linux上会报错),所以这里不使用-i参数

#|sed 's#[0-9][0-9]-##g' 不能去掉数字,除非gitbook生成静态文件的时候,md文件也没有数字

# 文件名便于排序的时候会使用类似01- , 02-,开头, 在目录显示的时候删除这部分 

# 调整目录显示, 在Mac 下使用需要调整参数

sed -ri 's#(\S+* \[)[0-9]+-(.*$)#\1\2#g' SUMMARY.md

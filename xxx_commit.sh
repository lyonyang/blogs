#!/bin/bash
# 懒得写提交信息, 所以就有了这个脚本
# 用于Mac系统, 提交当前项目, 其他系统, 需自行修改

logfile=".output_git_command.log"
filepath_data=".filepath_data.log"

git add . && git status

echo "" > $logfile

for item in "modified" "deleted" "new file" "renamed"
do
    # git status|grep -E "new file|deleted|modified"|sed "s#.*:##g"|grep -Eo "\S+.*"
    git status|grep "$item"|sed "s#${item}:##g"|grep -Eo "\S+.*" > ${filepath_data}
    while read line
    do
        filepath=$line
        # echo $filepath
        message=`echo $filepath|sed 's#.*/##g'`
        if [ "$item" == "renamed" ];then
            message=$filepath
            old_filepath=`echo $filepath|sed "s# ->.*##g"`
            new_filepath=`echo $filepath|sed "s#.*-> ##g"`
            echo "git commit -m \"${item}: ${message}\" \"${old_filepath}\" \"${new_filepath}\""
            echo "git commit -m \"${item}: ${message}\" \"${old_filepath}\" \"${new_filepath}\"" >> $logfile
            continue
        fi
        # echo $message
        # 针对带空格的文件名, 使用双引号将文件名引起来
        echo "git commit -m \"${item}: ${message}\" \"${filepath}\""

        echo "git commit -m \"${item}: ${message}\" \"${filepath}\"" >> $logfile
    done < ${filepath_data}
done
echo "git push" >> $logfile
bash $logfile
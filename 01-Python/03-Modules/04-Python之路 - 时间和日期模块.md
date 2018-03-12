# Python之路 - 时间和日期模块
 
## 介绍  🍀

python提供了 time , datetimme 和 calendar 模块可以用于格式化如期和时间 ; 时间间隔是以秒为单位的浮点数 , 每个时间戳都以自从1970年1月1日午夜（历元）经过了多长时间来表示 , 所以1970年之前的日期就不能用时间戳来表示了 , 时间戳是最适合用来做日期运算的

python中时间的三种类型 : 

1. float   浮点数 , 即时间戳
2. struct tuple   时间元组
3. str    字符串 , 规定格式表示

## time  🍀

### 内置函数  🍀

| 函数名                                      | 描述                                       |
| ---------------------------------------- | :--------------------------------------- |
| time.time()                              | 返回当前时间的时间戳(1970纪元后经过的浮点秒数)               |
| time.localtime([secs])                   | 返回一个时间元组 , 默认返回当前时间戳的时间元组 , secs为秒数      |
| time.sleep(secs)                         | 推迟调用线程的运行 , 即让程序' 睡 '一会 , secs为秒数        |
| time.strftime(fmt[,tupletime])           | 将时间元组转换成字符串显示 , 默认为当前时间 , 格式由fmt决定       |
| time.strptime(str,fmt='%a %b %d %H:%M:%S %Y) | 将字符串转换成时间元组 , fmt为字符串格式                  |
| time.gmtime([secs])                      | 将时间戳转换成格林威治(本初子午线)天文时间下的时间元组             |
| time.asctime([tupletime])                | 将时间元组转换成字符串 , 格式如下 : Tue Aug  8 15:19:00 2016 |
| time.ctime([secs])                       | 相当于asctime(localtime(secs)) , 不给参数相当于asctime() |
| time.mktime(tupletime)                   | 将时间元组转换成时间戳                              |
| time.clock()                             | 返回当前CPU时间戳 , 用来衡量不同程序的耗时 , 比time.time() 更有用 |
| time.tzset()                             | 更改本地时区                                   |
| time.altzone                             | 返回夏令时地区的偏移秒数 , 无需括号调用 ,   对需要夏令时地区才使用    |

### 格式化符号  🍀

| 符号   | 描述                      | 符号   | 描述                      |
| ---- | ----------------------- | ---- | ----------------------- |
| %y   | 两位数的年份表示 (00-99)        | %a   | 本地简化星期名称                |
| %Y   | 四位数的年份表示(000-9999)      | %A   | 本地完整星期名称                |
| %m   | 月份(01-12)               | %b   | 本地简化的月份名称               |
| %d   | 月内中的一天(0-31)            | %B   | 本地完整的月份名称               |
| %H   | 24小时制小时数(0-23)          | %c   | 本地相应的日期表示和时间表示          |
| %I   | 12小时制小时数(01-12)         | %j   | 年内的一天(001-366)          |
| %M   | 分钟数(00=59)              | %p   | 本地A.M.或P.M.的等价符         |
| %S   | 秒(00-59)                | %U   | 一年中的星期数(00-53)星期天为星期的开始 |
| %w   | 星期(0-6)，星期天为星期的开始       | %x   | 本地相应的日期表示               |
| %W   | 一年中的星期数(00-53)星期一为星期的开始 | %X   | 本地相应的时间表示               |
| %%   | %号本身                    | %Z   | 当前时区的名称                 |

### 时间元组说明  🍀

| 下标   | 属性       | 值                        |
| ---- | -------- | ------------------------ |
| 0    | tm_year  | 2008                     |
| 1    | tm_mon   | 1 到 12                   |
| 2    | tm_mday  | 1 到 31                   |
| 3    | tm_hour  | 0 到 23                   |
| 4    | tm_min   | 0 到 59                   |
| 5    | tm_sec   | 0 到 61 (60或61 是闰秒)       |
| 6    | tm_wday  | 0到6 (0是周一)               |
| 7    | tm_yday  | 1 到 366(儒略历)             |
| 8    | tm_isdst | -1, 0, 1, -1是决定是否为夏令时的旗帜 |


### 实例  🍀

获取本地时间

```python
# 导入time模块
import time
# 获取当前时间字符串
now_time = time.strftime("%Y-%m-%d %H:%M:%S")
# 获取当前时间戳
now_timestamp = time.time()
# 获取当前时间元组
now_timetuples = time.localtime()
# 打印当前时间字符串
print(now_time)
# 2016-08-08 16:04:35
# 打印当前时间戳
print(now_timestamp)
# 1470643278.0
# 打印当前时间元组
print(now_timetuples)
# time.struct_time(tm_year=2016, tm_mon=8, tm_mday=8, tm_hour=16, tm_min=1, tm_sec=18, tm_wday=0, tm_yday=221, tm_isdst=-1)
```

##  calendar 🍀

此模块的函数都是日历相关的 , 例如打印某月的字符串月历

星期一是默认的每周第一天 , 星期天是默认的最后一天 ; 更改设置需要调用 calendar.setfirstweekday() 函数

### 内置函数  🍀

| 函数                                   | 描述                                       |
| ------------------------------------ | ---------------------------------------- |
| calendar.calendar(year,w=2,l=1,c=6)  | 返回一个多行字符串格式的year年年历 , 3个月一行 , 间隔距离为c ; 每日宽度间隔为w字符 , 每行长度为21* W+18+2* C ; l是每星期行数 |
| calendar.firstweekday( )             | 返回当前每周起始日期的设置 ; 默认情况下 , 首次载入caendar模块时返回0 , 即星期一 |
| calendar.isleap(year)                | 是闰年返回True , 否则为false                     |
| calendar.leapdays(y1,y2)             | 返回在Y1 , Y2两年之间的闰年总数                      |
| calendar.month(year,month,w=2,l=1)   | 返回一个多行字符串格式的year年month月日历 , 两行标题 , 一周一行 ; 每日宽度间隔为w字符 , 每行的长度为7* w+6 , l是每星期的行数 |
| calendar.monthcalendar(year,month)   | 返回一个整数的单层嵌套列表 , 每个子列表装载代表一个星期的整数 ; Year年month月外的日期都设为0 ; 范围内的日子都由该月第几日表示 , 从1开始 |
| calendar.monthrange(year,month)      | 返回两个整数 , 第一个是该月的星期几的日期码 , 第二个是该月的日期码 , 日从0（星期一）到6（星期日）; 月从1到12 |
| calendar.prcal(year,w=2,l=1,c=6)     | 相当于 print calendar.calendar(year , w , l , c) |
| calendar.prmonth(year,month,w=2,l=1) | 相当于 print calendar.calendar（year , w , l , c） |
| calendar.setfirstweekday(weekday)    | 设置每周的起始日期码 , 0（星期一）到6（星期日）               |
| calendar.timegm(tupletime)           | 和time.gmtime相反: 接受一个时间元组形式 , 返回该时刻的时间辍（1970纪元后经过的浮点秒数） |
| calendar.weekday(year,month,day)     | 返回给定日期的日期码 , 0（星期一）到6（星期日） , 月份为 1（一月） 到 12（12月） |

### 实例  🍀

打印指定日历

```python
# 导入模块
import calendar
# 调用函数
cal = calendar.month(2016,8)
# 打印2016年8月的日历
print(cal)
------结果如下-------
    August 2016
Mo Tu We Th Fr Sa Su
 1  2  3  4  5  6  7
 8  9 10 11 12 13 14
15 16 17 18 19 20 21
22 23 24 25 26 27 28
29 30 31
```

python中处理日期和时间的模块还有 pytz , datedutil , datetime

可以通过import module ; help(module) 来进行学习

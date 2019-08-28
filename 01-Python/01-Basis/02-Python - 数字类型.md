# Python之路 - 数字类型

## Int  🍀

在Python 2.7版本中 , Python把int和long是分开的

iint 类型的最大值是2147483647 , 超过了这个值就是long 类型了(长整数不过是大一些的数) ; 而在3.x中 , python把 int 和 long 整合到一起了 , 以int来表示

```python
>>> num = 123
>>> type(num)
<class 'int'>
```

## Float  🍀

float有两种表现形式 , 一种是十进制数形式 , 它由数字和小数点组成 , 并且这里的小数点是不可或缺的 ; 另一种是指数形式 , 用e(大写也可以)来表示之后可以有正负号 , 来表示指数的符号 , e就是10的幂 , 指数必须是整数

```python
>>> a = 10E2
>>> a
1000.0
>>> b = 10e2
>>> b
1000.0
>>> c = 1.1
>>> type(c)
<class 'float'>
```

## None  🍀

表示该值是一个空对象 , 空值是python里一个特殊的值 , 用None表示

None不能理解为0 , 因为0是有意义的 , 而None是一个特殊的空值 ; None有自己的数据类型NoneType , 它与其他的数据类型比较永远返回False , 你可以将None复制给任何变量 , 但是你不能创建其他NoneType对象

```python
>>> type(None)
<class 'NoneType'>
>>> None == 0
False
>>> None == True
False
>>> None == False
False
```

## Bool  🍀

bool就是用来表征真假的一种方式

True为真 , False为假 ; Python中的值是自带bool值的 , 非0即真 , 为0即假

```python
>>> False + False
0
>>> True +  True
2
>>> True + False
1
```

## Complex  🍀

复数有实数和虚数部分组成 , 一般形式为 `x + yj` , 其中的 x 是复数的实数部分 , y是复数的虚数部分 , 这里x和y都是实数

注意 , 虚数部分不区分大小写

```python
>>> -.6545 + 0J
(-0.6545+0j)
>>> 4.53e1 - 7j
(45.3-7j)
>>> 45.j
45j
>>> 3.14j
3.14j
```

## Data & Time  🍀

Python提供了一个 time 和 calendar 模块可以用于格式化如期和时间 , 时间间隔是以秒为单位的浮点数 , 每个时间戳都以自从1970年1月1日午夜 (历元) 经过了多长时间来表示 , 所以1970年之前的日期就不能用时间戳来表示了 , 太遥远的日期也是不行的 , UNIX和Windows只支持到2038年

时间戳是最适合用来做日期运算的

### time  🍀

获取本地时间 

```python
# 导入time模块
import time
# 获取当前时间戳，单位是秒
now_timestamp = time.time()
# 打印now_timestamp
print(now_timestamp)       
# 获取本地时间,默认是获取当前时间
localtime = time.localtime()
# 打印localtime
print(localtime)       
# 获取本地时间，传入时间戳
localtime = time.localtime(now_timestamp)
# 打印locatime
print(localtime)       
'''
执行结果:
1499085481.4974537
time.struct_time(tm_year=2017, tm_mon=7, tm_mday=3, tm_hour=20, tm_min=38, tm_sec=1, tm_wday=0, tm_yday=184, tm_isdst=0)
time.struct_time(tm_year=2017, tm_mon=7, tm_mday=3, tm_hour=20, tm_min=38, tm_sec=1, tm_wday=0, tm_yday=184, tm_isdst=0)
'''
```

时间元组struct_time

| 序号   | 属性       | 值                                      |
| ---- | -------- | -------------------------------------- |
| 0    | tm_year  | 2008                                   |
| 1    | tm_mon   | 1 到 12                                 |
| 2    | tm_mday  | 1 到 31                                 |
| 3    | tm_hour  | 0 到 23                                 |
| 4    | tm_min   | 0 到 59                                 |
| 5    | tm_sec   | 0 到 61 (60或61 是闰秒)                     |
| 6    | tm_wday  | 0到6 (0是周一)                             |
| 7    | tm_yday  | 一年中的第几天，1 到 366                        |
| 8    | tm_isdst | 是否为夏令时，值有：1(夏令时)、0(不是夏令时)、-1(未知)，默认 -1 |

time模块中的方法 : 

```python
FUNCTIONS
	asctime(...)
		asctime([tuple]) -> string
        Convert a time tuple to a string, e.g. 'Sat Jun 06 16:26:11 1998'.
        When the time tuple is not present, current time as returned by localtime() is used.
        
    clock(...)
        clock() -> floating point number
        Return the CPU time or real time since the start of the process or since
        the first call to clock().  This has as much precision as the system records.
        
    ctime(...)
        ctime(seconds) -> string
        Convert a time in seconds since the Epoch to a string in local time.
        This is equivalent to asctime(localtime(seconds)). When the time tuple is
        not present, current time as returned by localtime() is used.

    get_clock_info(...)
        get_clock_info(name: str) -> dict
        Get information of the specified clock.
        
    gmtime(...)
        gmtime([seconds]) -> (tm_year, tm_mon, tm_mday, tm_hour, tm_min,
                               tm_sec, tm_wday, tm_yday, tm_isdst)
        Convert seconds since the Epoch to a time tuple expressing UTC (a.k.a.
        GMT).  When 'seconds' is not passed in, convert the current time instead.
        If the platform supports the tm_gmtoff and tm_zone, they are available as
        attributes only.

    localtime(...)
        localtime([seconds]) -> (tm_year,tm_mon,tm_mday,tm_hour,tm_min,
                                  tm_sec,tm_wday,tm_yday,tm_isdst)
        Convert seconds since the Epoch to a time tuple expressing local time.
        When 'seconds' is not passed in, convert the current time instead.

    mktime(...)
        mktime(tuple) -> floating point number
        Convert a time tuple in local time to seconds since the Epoch.
        Note that mktime(gmtime(0)) will not generally return zero for most
        time zones; instead the returned value will either be equal to that
        of the timezone or altzone attributes on the time module.

    monotonic(...)
        monotonic() -> float
        Monotonic clock, cannot go backward.

    perf_counter(...)
        perf_counter() -> float
        Performance counter for benchmarking.

    process_time(...)
        process_time() -> float
        Process time for profiling: sum of the kernel and user-space CPU time.

    sleep(...)
        sleep(seconds)
        Delay execution for a given number of seconds.  The argument may be
        a floating point number for subsecond precision.

    strftime(...)
        strftime(format[, tuple]) -> string
        Convert a time tuple to a string according to a format specification.
        See the library reference manual for formatting codes. When the time tuple
        is not present, current time as returned by localtime() is used.
        
        Commonly used format codes:
        %Y  Year with century as a decimal number.
        %m  Month as a decimal number [01,12].
        %d  Day of the month as a decimal number [01,31].
        %H  Hour (24-hour clock) as a decimal number [00,23].
        %M  Minute as a decimal number [00,59].
        %S  Second as a decimal number [00,61].
        %z  Time zone offset from UTC.
        %a  Locale's abbreviated weekday name.
        %A  Locale's full weekday name.
        %b  Locale's abbreviated month name.
        %B  Locale's full month name.
        %c  Locale's appropriate date and time representation.
        %I  Hour (12-hour clock) as a decimal number [01,12].
        %p  Locale's equivalent of either AM or PM.

        Other codes may be available on your platform.  See documentation for
        the C library strftime function.

    strptime(...)
        strptime(string, format) -> struct_time
        Parse a string to a time tuple according to a format specification.
        See the library reference manual for formatting codes (same as
        strftime()).

        Commonly used format codes:
        %Y  Year with century as a decimal number.
        %m  Month as a decimal number [01,12].
        %d  Day of the month as a decimal number [01,31].
        %H  Hour (24-hour clock) as a decimal number [00,23].
        %M  Minute as a decimal number [00,59].
        %S  Second as a decimal number [00,61].
        %z  Time zone offset from UTC.
        %a  Locale's abbreviated weekday name.
        %A  Locale's full weekday name.
        %b  Locale's abbreviated month name.
        %B  Locale's full month name.
        %c  Locale's appropriate date and time representation.
        %I  Hour (12-hour clock) as a decimal number [01,12].
        %p  Locale's equivalent of either AM or PM.

        Other codes may be available on your platform.  See documentation for
        the C library strftime function.

    time(...)
        time() -> floating point number
        Return the current time in seconds since the Epoch.
        Fractions of a second may be present if the system clock provides them.
```

### calendar  🍀

打印某月日历

```python
>>> import calendar
>>> cal = calendar.month(2017,7)
>>> print(cal)
     July 2017
Mo Tu We Th Fr Sa Su
                1  2
 3  4  5  6  7  8  9
10 11 12 13 14 15 16
17 18 19 20 21 22 23
24 25 26 27 28 29 30
31
```

calendar模块中的方法 : 

```python
FUNCTIONS
    calendar = formatyear(theyear, w=2, l=1, c=6, m=3) method of TextCalendar instance
        Returns a year's calendar as a multi-line string.

    firstweekday = getfirstweekday() method of TextCalendar instance

    isleap(year)
        Return True for leap years, False for non-leap years.

    leapdays(y1, y2)
        Return number of leap years in range [y1, y2).
        Assume y1 <= y2.

    month = formatmonth(theyear, themonth, w=0, l=0) method of TextCalendar instance
        Return a month's calendar string (multi-line).

    monthcalendar = monthdayscalendar(year, month) method of TextCalendar instance
        Return a matrix representing a month's calendar.
        Each row represents a week; days outside this month are zero.

    monthrange(year, month)
        Return weekday (0-6 ~ Mon-Sun) and number of days (28-31) for
        year, month.

    prcal = pryear(theyear, w=0, l=0, c=6, m=3) method of TextCalendar instance
        Print a year's calendar.

    prmonth(theyear, themonth, w=0, l=0) method of TextCalendar instance
        Print a month's calendar.

    setfirstweekday(firstweekday)

    timegm(tuple)
        Unrelated but handy function to calculate Unix timestamp from GMT.

    weekday(year, month, day)
        Return weekday (0-6 ~ Mon-Sun) for year (1970-...), month (1-12),
        day (1-31).
```

Python中用于处理日期和时间的模块还有 : 

- datetime
- pytz
- dateutil

## 类型转换即数学函数  🍀

数字类型转换

```python
int(x [,base]) 将x转换为一个整数 
float(x ) 将x转换到一个浮点数 
complex(x) 将x转换为复数 
str(x) 将对象x转换为字符串 ，通常无法用eval()求值
repr(x) 将对象x转换为表达式字符串 ，可以用eval()求值
eval(str) 用来计算在字符串中的有效Python表达式,并返回一个对象 
tuple(s) 将序列s转换为一个元组 
list(s) 将序列s转换为一个列表 
chr(x) 将一个整数转换为一个字符 
unichr(x) 将一个整数转换为Unicode字符 
ord(x) 将一个字符转换为它的整数值 
hex(x) 将一个整数转换为一个十六进制字符串 
oct(x) 将一个整数转换为一个八进制字符串
```

数学函数

```python
abs(x)     返回数字的绝对值，如abs(-10) 返回 10
ceil(x)    返回数字的上入整数，如math.ceil(4.1) 返回 5
cmp(x, y)  如果 x < y 返回 -1, 如果 x == y 返回 0, 如果 x > y 返回 1
exp(x)     返回e的x次幂(ex),如math.exp(1) 返回2.718281828459045
fabs(x)    返回数字的绝对值，如math.fabs(-10) 返回10.0
floor(x)   返回数字的下舍整数，如math.floor(4.9)返回 4
log(x)     如math.log(math.e)返回1.0,math.log(100,10)返回2.0
log10(x)   返回以10为基数的x的对数，如math.log10(100)返回 2.0
max(x1, x2,...)    返回给定参数的最大值，参数可以为序列
min(x1, x2,...)    返回给定参数的最小值，参数可以为序列
modf(x)    返回x的整数部分与小数部分，两部分的数值符号与x相同，整数部分以浮点型表示
pow(x, y) x**y  运算后的值。
round(x [,n])   返回浮点数x的四舍五入值，如给出n值，则代表舍入到小数点后的位数
sqrt(x)     返回数字x的平方根，数字可以为负数，返回类型为实数，如math.sqrt(4)返回 2+0j
```
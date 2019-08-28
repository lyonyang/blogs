# Python之路 - 字符串

## 介绍  🍀

字符串是Python中最基本的数据类型之一 

字符串的使用需要用引号括起来 , 例如 : `name = "Lyon"` ; 这里name就是一个变量名 , 而引号里面的`Lyon` 则就是该变量绑定的值 , 该值的类型为 " str" 类型 , 我们可以利用`type()` 函数进行查看 : 

```python
>>> name = "Lyon"
>>> type(name)
<class 'str'>
>>>
```

这就是字符串类型 , 当然如上使用的是双引号 , 这里其实还可以使用单引号`'Lyon'`以及三引号`'''Lyon'''`(或者是`"""Lyon"""`  , 单引号双引号都可以) , 不过对于三引号 , 我们通常是表示多行字符串 , 这样我们就不需要利用 " \n " （换行符）来进行每一行的换行了

对于嵌套引号的时候要注意 , 需要用不同的引号来避免歧义 , 比如 : `'I am "Lyon"'`  , 也可以 `"I am 'Lyon'"` 

对于所有的基本数据类型 , 我们都应该熟悉其特性以及操作

字符串操作主要有 **拷贝（复制）、拼接、查找、比较、统计、切片、测试、大小写等**

在开始详细了解这些操作之前 , 我们需要记住一个特性 : **字符串是不可变的** , 既然是不可变的 , 那么我们对其进行的增删改查就都不是对本身进行操作的 , 而是创建了一个新的字符串

## 拷贝  🍀

```python
>>> a = "Lyon"
>>> b = a
>>> print(a,b)
Lyon Lyon
```

## 拼接  🍀

```python
>>> a = "Hello"
>>> b = "Lyon"
>>> print(a+b)
HelloLyon
```

注 : 这个方法要特别说明一下 , “+”是一个坑 , 因为使用加号连接2个字符串会调用静态函数`string_concat(register PyStringObject *a,register PyObject *b)`  , 这个函数大致的作用 , 就是首先开辟一块`a+b`大小的内存的和的存储单元 , 然后把a和b都拷贝进去 ; 所以一旦我们的 "+" 操作过多将会造成大量内存的浪费

```python
>>> a = "Lyon"
>>> b = "Hello"
>>> print(a.join(b)) 
HLyoneLyonlLyonlLyono  #HLyon eLyon lLyon lLyon o
```

可以用join来将list中的元素进行拼接成字符串 : `''.join( list )` 即以空字符串连接列表中的每一个元素

## 查找  🍀

```python
>>> name = "Lyon"
# 返回L字符所在的下标,下标是从0开始的整数
>>> name.index('L')
0 
# 如果不存在就会报错
>>> name.index('N') 
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
ValueError: substring not found  
# 也可以用in,not in来进行判断
>>>'L' in name
>>>
```

## 比较  🍀

本来Python 2中有个`str.cmp()`方法来比较两个对象 , 并根据结果返回一个整数。整数的正负就是数值的大小了 , 但是在Python 3中就没有这个方法了 , 官方文档如下 : 

```The cmp() function should be treated as gone, and the __cmp__() special method is no longer supported. Use __lt__() for sorting, __eq__() with __hash__(), and other rich comparisons as needed. (If you really need the cmp() functionality, you could use the expression (a > b) - (a < b) as the equivalent for cmp(a, b).)
The cmp() function should be treated as gone, and the __cmp__() special method is no longer supported. Use __lt__() for sorting, __eq__() with __hash__(), and other rich comparisons as needed. (If you really need the cmp() functionality, you could use the expression (a > b) - (a < b) as the equivalent for cmp(a, b).)
```

大致的意思就是cmp()函数已经走了 , 如果你真的需要cmp函数 , 你可以用表达式`(a>b)-(a<b)代替cmp(a,b)`  , 看下面2.7的代码 : 

```python
>>> a = "100"
>>> b = "50"
>>> cmp(a,b)   # a>b  负数
-1
>>> cmp(b,a)   # b<a  正数
1
```

## 统计  🍀

```python
>>> name = "Lyon"
 # name中"L"的个数
>>> name.count("L")     
1
```

## 切片  🍀

```python
>>> name = "i like Lyon"
# 切取第7个到第9个字符,注意空格也是一个字符
>>> name[7:10]     
'Lyo'
>>> name = "i like Lyon"
# 第7到第10各,顾头不顾尾
>>> name[7:11]
'Lyon'
```

## 检测  🍀

```python
>>> name = "Lyon"
# 检测"L"是否在name中,返回bool值
>>> "L" in name     
True
>>> num = "3412313"
# 检测num里面是否全都是整数
>>> num.isdigit()    
True
>>> name = "Lyon"
# 检测name是否可以被当作标标志符,即是否符合变量命名规则 
>>> name.isidentifier()
True　
# 检测name里面有没有"L",有就返回下标
>>> name.find('L')    
0
# 检测name里面有没有"N",没有就返回-1
>>> name.find('N')   
-1    
```

检测相关

```python
str.startswith(prefix[,start[,end]]) # 是否以prefix开头 
str.endswith(suffix[,start[,end]])   # 以suffix结尾 
str.isalnum()    # 是否全是字母和数字,并至少有一个字符 
str.isalpha()    # 是否全是字母,并至少有一个字符 
str.isdigit()    # 是否全是数字,并至少有一个字符 
str.isspace()    # 是否全是空白字符,并至少有一个字符 
str.islower()    # 是否全是小写 
str.isupper()    # 是否便是大写 
str.istitle()    # 是否是首字母大写的
```

注 : 结果全是bool值

## 大小写  🍀

```python
>>> name = "I am Lyon"
# 大小写互换
>>> name.swapcase()   
'i AM lYON'
# 首字母大写,其它都小写
>>> name.capitalize()     
'I am lyon'
# 转换为大写
>>> name.upper()          
'I AM LYON'
# 转换为小写
>>> name.lower()           
'i am lyon'
```

## 更多  🍀

```python
 |  capitalize(...)
 |      S.capitalize() -> str
 |
 |      Return a capitalized version of S, i.e. make the first character
 |      have upper case and the rest lower case.
 |
 |  casefold(...)
 |      S.casefold() -> str
 |
 |      Return a version of S suitable for caseless comparisons.
 |
 |  center(...)
 |      S.center(width[, fillchar]) -> str
 |
 |      Return S centered in a string of length width. Padding is
 |      done using the specified fill character (default is a space)
 |
 |  count(...)
 |      S.count(sub[, start[, end]]) -> int
 |
 |      Return the number of non-overlapping occurrences of substring sub in
 |      string S[start:end].  Optional arguments start and end are
 |      interpreted as in slice notation.
 |
 |  encode(...)
 |      S.encode(encoding='utf-8', errors='strict') -> bytes
 |
 |      Encode S using the codec registered for encoding. Default encoding
 |      is 'utf-8'. errors may be given to set a different error
 |      handling scheme. Default is 'strict' meaning that encoding errors raise
 |      a UnicodeEncodeError. Other possible values are 'ignore', 'replace' and
 |      'xmlcharrefreplace' as well as any other name registered with
 |      codecs.register_error that can handle UnicodeEncodeErrors.
 |
 |  endswith(...)
 |      S.endswith(suffix[, start[, end]]) -> bool
 |
 |      Return True if S ends with the specified suffix, False otherwise.
 |      With optional start, test S beginning at that position.
 |      With optional end, stop comparing S at that position.
 |      suffix can also be a tuple of strings to try.
 |
 |  expandtabs(...)
 |      S.expandtabs(tabsize=8) -> str
 |
 |      Return a copy of S where all tab characters are expanded using spaces.
 |      If tabsize is not given, a tab size of 8 characters is assumed.
 |
 |  find(...)
 |      S.find(sub[, start[, end]]) -> int
 |
 |      Return the lowest index in S where substring sub is found,
 |      such that sub is contained within S[start:end].  Optional
 |      arguments start and end are interpreted as in slice notation.
 |
 |      Return -1 on failure.
 |
 |  format(...)
 |      S.format(*args, **kwargs) -> str
 |
 |      Return a formatted version of S, using substitutions from args and kwargs.
 |      The substitutions are identified by braces ('{' and '}').
 |
 |  format_map(...)
 |      S.format_map(mapping) -> str
 |
 |      Return a formatted version of S, using substitutions from mapping.
 |      The substitutions are identified by braces ('{' and '}').
 |
 |  index(...)
 |      S.index(sub[, start[, end]]) -> int
 |
 |      Like S.find() but raise ValueError when the substring is not found.
 |
 |  isalnum(...)
 |      S.isalnum() -> bool
 |
 |      Return True if all characters in S are alphanumeric
 |      and there is at least one character in S, False otherwise.
 |
 |  isalpha(...)
 |      S.isalpha() -> bool
 |
 |      Return True if all characters in S are alphabetic
 |      and there is at least one character in S, False otherwise.
 |
 |  isdecimal(...)
 |      S.isdecimal() -> bool
 |
 |      Return True if there are only decimal characters in S,
 |      False otherwise.
 |
 |  isdigit(...)
 |      S.isdigit() -> bool
 |
 |      Return True if all characters in S are digits
 |      and there is at least one character in S, False otherwise.
 |
 |  isidentifier(...)
 |      S.isidentifier() -> bool
 |
 |      Return True if S is a valid identifier according
 |      to the language definition.
 |
 |      Use keyword.iskeyword() to test for reserved identifiers
 |      such as "def" and "class".
 |
 |  islower(...)
 |      S.islower() -> bool
 |
 |      Return True if all cased characters in S are lowercase and there is
 |      at least one cased character in S, False otherwise.
 |
 |  isnumeric(...)
 |      S.isnumeric() -> bool
 |
 |      Return True if there are only numeric characters in S,
 |      False otherwise.
 |
 |  isprintable(...)
 |      S.isprintable() -> bool
 |
 |      Return True if all characters in S are considered
 |      printable in repr() or S is empty, False otherwise.
 |
 |  isspace(...)
 |      S.isspace() -> bool
 |
 |      Return True if all characters in S are whitespace
 |      and there is at least one character in S, False otherwise.
 |
 |  istitle(...)
 |      S.istitle() -> bool
 |
 |      Return True if S is a titlecased string and there is at least one
 |      character in S, i.e. upper- and titlecase characters may only
 |      follow uncased characters and lowercase characters only cased ones.
 |      Return False otherwise.
 |
 |  isupper(...)
 |      S.isupper() -> bool
 |
 |      Return True if all cased characters in S are uppercase and there is
 |      at least one cased character in S, False otherwise.
 |
 |  join(...)
 |      S.join(iterable) -> str
 |
 |      Return a string which is the concatenation of the strings in the
 |      iterable.  The separator between elements is S.
 |
 |  ljust(...)
 |      S.ljust(width[, fillchar]) -> str
 |
 |      Return S left-justified in a Unicode string of length width. Padding is
 |      done using the specified fill character (default is a space).
 |
 |  lower(...)
 |      S.lower() -> str
 |
 |      Return a copy of the string S converted to lowercase.
 |
 |  lstrip(...)
 |      S.lstrip([chars]) -> str
 |
 |      Return a copy of the string S with leading whitespace removed.
 |      If chars is given and not None, remove characters in chars instead.
 |
 |  partition(...)
 |      S.partition(sep) -> (head, sep, tail)
 |
 |      Search for the separator sep in S, and return the part before it,
 |      the separator itself, and the part after it.  If the separator is not
 |      found, return S and two empty strings.
 |
 |  replace(...)
 |      S.replace(old, new[, count]) -> str
 |
 |      Return a copy of S with all occurrences of substring
 |      old replaced by new.  If the optional argument count is
 |      given, only the first count occurrences are replaced.
 |
 |  rfind(...)
 |      S.rfind(sub[, start[, end]]) -> int
 |
 |      Return the highest index in S where substring sub is found,
 |      such that sub is contained within S[start:end].  Optional
 |      arguments start and end are interpreted as in slice notation.
 |
 |      Return -1 on failure.
 |
 |  rindex(...)
 |      S.rindex(sub[, start[, end]]) -> int
 |
 |      Like S.rfind() but raise ValueError when the substring is not found.
 |
 |  rjust(...)
 |      S.rjust(width[, fillchar]) -> str
 |
 |      Return S right-justified in a string of length width. Padding is
 |      done using the specified fill character (default is a space).
 |
 |  rpartition(...)
 |      S.rpartition(sep) -> (head, sep, tail)
 |
 |      Search for the separator sep in S, starting at the end of S, and return
 |      the part before it, the separator itself, and the part after it.  If the
 |      separator is not found, return two empty strings and S.
 |
 |  rsplit(...)
 |      S.rsplit(sep=None, maxsplit=-1) -> list of strings
 |
 |      Return a list of the words in S, using sep as the
 |      delimiter string, starting at the end of the string and
 |      working to the front.  If maxsplit is given, at most maxsplit
 |      splits are done. If sep is not specified, any whitespace string
 |      is a separator.
 |
 |  rstrip(...)
 |      S.rstrip([chars]) -> str
 |
 |      Return a copy of the string S with trailing whitespace removed.
 |      If chars is given and not None, remove characters in chars instead.
 |
 |  split(...)
 |      S.split(sep=None, maxsplit=-1) -> list of strings
 |
 |      Return a list of the words in S, using sep as the
 |      delimiter string.  If maxsplit is given, at most maxsplit
 |      splits are done. If sep is not specified or is None, any
 |      whitespace string is a separator and empty strings are
 |      removed from the result.
 |
 |  splitlines(...)
 |      S.splitlines([keepends]) -> list of strings
 |
 |      Return a list of the lines in S, breaking at line boundaries.
 |      Line breaks are not included in the resulting list unless keepends
 |      is given and true.
 |
 |  startswith(...)
 |      S.startswith(prefix[, start[, end]]) -> bool
 |
 |      Return True if S starts with the specified prefix, False otherwise.
 |      With optional start, test S beginning at that position.
 |      With optional end, stop comparing S at that position.
 |      prefix can also be a tuple of strings to try.
 |
 |  strip(...)
 |      S.strip([chars]) -> str
 |
 |      Return a copy of the string S with leading and trailing
 |      whitespace removed.
 |      If chars is given and not None, remove characters in chars instead.
 |
 |  swapcase(...)
 |      S.swapcase() -> str
 |
 |      Return a copy of S with uppercase characters converted to lowercase
 |      and vice versa.
 |
 |  title(...)
 |      S.title() -> str
 |
 |      Return a titlecased version of S, i.e. words start with title case
 |      characters, all remaining cased characters have lower case.
 |
 |  translate(...)
 |      S.translate(table) -> str
 |
 |      Return a copy of the string S in which each character has been mapped
 |      through the given translation table. The table must implement
 |      lookup/indexing via __getitem__, for instance a dictionary or list,
 |      mapping Unicode ordinals to Unicode ordinals, strings, or None. If
 |      this operation raises LookupError, the character is left untouched.
 |      Characters mapped to None are deleted.
 |
 |  upper(...)
 |      S.upper() -> str
 |
 |      Return a copy of S converted to uppercase.
 |
 |  zfill(...)
 |      S.zfill(width) -> str
 |
 |      Pad a numeric string S with zeros on the left, to fill a field
 |      of the specified width. The string S is never truncated.
 |
 |  ----------------------------------------------------------------------
```

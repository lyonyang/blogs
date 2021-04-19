# Python操作MongoDB


<extoc></extoc>

## 介绍  🍀

MongoDB 是一个基于分布式文件存储的数据库 , 由 C++ 编写

MongoDB 是一个介于关系型数据库和非关系型数据库 (NoSQL) 之间的产品 , 是非关系数据库当中功能最丰富 , 最像关系数据库的

它有如下优点 : 

1. 文档型存储
2. 使用高效的二进制 BSON 作为数据存储 , BSON 是一个类似 JSON 的格式 , 选择 BSON 可以提供更快的遍历速度 , 提供比 JSON 更多的内置数据类型
3. 自带高可用及分区的解决方案 , 分别为副本集 (Replica Set) 和分片(sharding)
4. 基于文档的富查询语言 , MongoDB 支持动态查询 , 支持非常多的查询方式 , 并且可以对文档中的属性建立索引
5. 内置聚合工具 , 可以通过 MapReduce 等方式进行复杂的统计核并行计算
6. MongoDB 在 3.0 之后增加了高性能 , 可伸缩 , 支持压缩和文档级锁的数据存储引擎 WiredTiger

## MongoDB概念  🍀

| SQL术语/概念 | MongoDB术语/概念 | 解释/说明                              |
| ------------ | ---------------- | -------------------------------------- |
| database     | database         | 数据库                                 |
| table        | collection       | 数据库表/集合                          |
| row          | document         | 数据记录行/文档                        |
| column       | field            | 数据字段/域                            |
| index        | index            | 索引                                   |
| table joins  |                  | 表连接 , MongoDB 不支持                |
| primary key  | primary key      | 主键 , MongoDB 自动将_id字段设置为主键 |

 ### 数据库  🍀

在 MongoDB 中 , 多个文档组成集合 , 多个集合可以组成数据库 

数据库也通过名字来标识 , 数据库名可以是满足以下条件的任意UTF-8字符串 : 

1. 不能是空字符串 `("")`
2. 不得含有`' ' (空格)` , `.` , `$` , `/` , `\` 和 `\0` (空字符)
3. 应全部小写
4. 最多64字节

有一些数据库名是保留的 , 可以直接访问这些有特殊作用的数据库
1. admin :  从身份认证的角度讲 , 这是 `“root”` 数据库 , 如果将一个用户添加到admin数据库 , 这个用户将自动获得所有数据库的权限 , 再者 , 一些特定的服务器端命令也只能从admin数据库运行 , 如列出所有数据库或关闭服务器
2. local: 这个数据库永远都不可以复制 , 且一台服务器上的所有本地集合都可以存储在这个数据库中
3. config: MongoDB用于分片设置时 , 分片信息会存储在config数据库中

### 集合  🍀

集合就是一组文档 , 如果将MongoDB中的一个文档比喻为关系型数据的一行 , 那么一个集合就是相当于一张表 

1. 集合存在于数据库中 , 通常情况下为了方便管理 , 不同格式和类型的数据应该插入到不同的集合 , 但其实集合没有固定的结构 , 这意味着我们完全可以把不同格式和类型的数据统统插入一个集合中

2. 组织子集合的方式就是使用 `“.”` , 分隔不同命名空间的子集合

   比如一个具有博客功能的应用可能包含两个集合 , 分别是 blog.posts 和 blog.authors , 这是为了使组织结构更清晰 , 这里的 blog 集合 (这个集合甚至不需要存在）跟它的两个子集合没有任何关系
   在MongoDB中 , 使用子集合来组织数据非常高效 , 值得推荐

3. 当第一个文档插入时 , 集合就会被创建 , 合法的集合名 : 

   集合名不能是空字符串"" ; 
   集合名不能含有 \0 字符 (空字符) , 这个字符表示集合名的结尾 ; 
   集合名不能以 "system." 开头 , 这是为系统集合保留的前缀 ; 
   用户创建的集合名字不能含有保留字符 , 有些驱动程序的确支持在集合名里面包含 , 这是因为某些系统生成的集合中包含该字符 ; 除非你要访问这种系统创建的集合 , 否则千万不要在名字里出现$ ;

### 文档  🍀

文档是MongoDB的核心概念 , 文档就是键值对的一个有序集 `{'msg':'hello','foo':3}` , 类似于python中的有序字典

需要注意的是 : 

1. 文档中的键/值对是有序的 ; 
2. 文档中的值不仅可以是在双引号里面的字符串 , 还可以是其他几种数据类型 (甚至可以是整个嵌入的文档) ; 
3. MongoDB区分类型和大小写 ; 
4. MongoDB的文档不能有重复的键 ; 
5. 文档中的值可以是多种不同的数据类型 , 也可以是一个完整的内嵌文档。文档的键是字符串。除了少数例外情况 , 键可以使用任意UTF-8字符 ; 

文档键命名规范 : 

1. 键不能含有 \0 (空字符) , 这个字符用来表示键的结尾 ; 
2. `.` 和 `$` 有特别的意义 , 只有在特定环境下才能使用 ; 
3. 以下划线 "_" 开头的键是保留的(不是严格要求的) ; 

PS : 把数据库名添加到集合名前 , 得到集合的完全限定名 , 即命名空间  , 如 : 如果要使用 test 数据库中的 `coll.posts` 集合 , 这个集合的命名空间就是 `test.coll.ports` , 命名空间的长度不得超过121个字节 , 且在实际使用中应该小于100个字节

## 连接MongoDB  🍀

```python
>>> from pymongo import MongoClient
# 默认主机与端口
>>> client = MongoClient()
# 指定主机与端口
>>> client = MongoClient('localhost', 27017)
# MongoDBURI格式
>>> client = MongoClient('mongodb://localhost:27017/')
```

## 获取数据库  🍀

```python
>>> db = client.test_database
# 如果你的数据库是这样的test-database,可以使用字典点方式
>>> db = client['test-database']
```

## 获取集合  🍀

```python
>>> collection = db.test_collection
>>> collection = db['test-collection']
```

关于 MongoDB 中的集合和数据库一个重要注意事项是 , 它们是延迟创建的 , 上面的命令实际上都没有在MongoDB 服务器上执行任何操作 , 而是当第一个文档插入到集合和数据库中时 , 才创建集合和数据库

## 文档  🍀

MongoDB中的数据使用JSON样式的文档表示(并存储)。在Pymono中 , 我们使用字典来表示文档 , 如下 : 

```python
>>> import datetime
>>> post = {"author": "Mike",
...         "text": "My first blog post!",
...         "tags": ["mongodb", "python", "pymongo"],
...         "date": datetime.datetime.utcnow()}
```

### 插入文档  🍀

**单条插入**

```python
>>> posts = db.posts
>>> post_id = posts.insert_one(post).inserted_id
>>> post_id
ObjectId('...')
```

**批量插入**

```python
>>> new_posts = [{"author": "Mike",
...               "text": "Another post!",
...               "tags": ["bulk", "insert"],
...               "date": datetime.datetime(2009, 11, 12, 11, 14)},
...              {"author": "Eliot",
...               "title": "MongoDB is fun",
...               "text": "and pretty easy too!",
...               "date": datetime.datetime(2009, 11, 10, 10, 45)}]
>>> result = posts.insert_many(new_posts)
>>> result.inserted_ids
[ObjectId('...'), ObjectId('...')]
```

### 查询文档  🍀

查看数据库中所有集合

```python
>>> db.collection_names(include_system_collections=False)
[u'posts']
```

**单条查询**

```python
# pprint用于数据格式化
>>> import pprint
>>> pprint.pprint(posts.find_one())
{u'_id': ObjectId('...'),
 u'author': u'Mike',
 u'date': datetime.datetime(...),
 u'tags': [u'mongodb', u'python', u'pymongo'],
 u'text': u'My first blog post!'}
```

指定条件查询

```python
>>> pprint.pprint(posts.find_one({"author": "Mike"}))
{u'_id': ObjectId('...'),
 u'author': u'Mike',
 u'date': datetime.datetime(...),
 u'tags': [u'mongodb', u'python', u'pymongo'],
 u'text': u'My first blog post!'}
```

按对象查询

```python
>>> post_id
ObjectId(...)
>>> pprint.pprint(posts.find_one({"_id": post_id}))
{u'_id': ObjectId('...'),
 u'author': u'Mike',
 u'date': datetime.datetime(...),
 u'tags': [u'mongodb', u'python', u'pymongo'],
 u'text': u'My first blog post!'}
```

由字符串转换成对象

```python
from bson.objectid import ObjectId

# The web framework gets post_id from the URL and passes it as a string
def get(post_id):
    # Convert from string to ObjectId:
    document = client.db.collection.find_one({'_id': ObjectId(post_id)})
```

**多条查询**

```python
>>> for post in posts.find():
...   pprint.pprint(post)
...
{u'_id': ObjectId('...'),
 u'author': u'Mike',
 u'date': datetime.datetime(...),
 u'tags': [u'mongodb', u'python', u'pymongo'],
 u'text': u'My first blog post!'}
{u'_id': ObjectId('...'),
 u'author': u'Mike',
 u'date': datetime.datetime(...),
 u'tags': [u'bulk', u'insert'],
 u'text': u'Another post!'}
{u'_id': ObjectId('...'),
 u'author': u'Eliot',
 u'date': datetime.datetime(...),
 u'text': u'and pretty easy too!',
 u'title': u'MongoDB is fun'}
```

指定条件查询

```python
>>> for post in posts.find({"author": "Mike"}):
...   pprint.pprint(post)
...
{u'_id': ObjectId('...'),
 u'author': u'Mike',
 u'date': datetime.datetime(...),
 u'tags': [u'mongodb', u'python', u'pymongo'],
 u'text': u'My first blog post!'}
{u'_id': ObjectId('...'),
 u'author': u'Mike',
 u'date': datetime.datetime(...),
 u'tags': [u'bulk', u'insert'],
 u'text': u'Another post!'}
```

### 计数查询  🍀

获取查询结果总条数

```python
>>> posts.count()
3
>>> posts.find({"author": "Mike"}).count()
2
```

### 范围查询  🍀

```python
>>> d = datetime.datetime(2009, 11, 12, 12)
>>> for post in posts.find({"date": {"$lt": d}}).sort("author"):
...   pprint.pprint(post)
...
{u'_id': ObjectId('...'),
 u'author': u'Eliot',
 u'date': datetime.datetime(...),
 u'text': u'and pretty easy too!',
 u'title': u'MongoDB is fun'}
{u'_id': ObjectId('...'),
 u'author': u'Mike',
 u'date': datetime.datetime(...),
 u'tags': [u'bulk', u'insert'],
 u'text': u'Another post!'}
```

### 索引  🍀

创建索引

```python
>>> result = db.profiles.create_index([('user_id', pymongo.ASCENDING)],
...                                   unique=True)
>>> sorted(list(db.profiles.index_information()))
[u'_id_', u'user_id_1']
```

更多 [pymongo](https://pypi.org/project/pymongo/)
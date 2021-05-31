# Python内置操作时间复杂度








<extoc></extoc>

## 列表 - list

| **操作**                                                     | **平均情况** | **最坏情况** |
| ------------------------------------------------------------ | ------------ | ------------ |
| copy                                                         | O(n)         | O(n)         |
| append()                                                     | O(1)         | O(1)         |
| pop()                                                        | O(1)         | O(1)         |
| pop(k)                                                       | O(k)         | O(k)         |
| insert(n, x)                                                 | O(n)         | O(n)         |
| get `(即: list[index])`                                      | O(1)         | O(1)         |
| set `(即: list[index] = x)`                                  | O(1)         | O(1)         |
| delete `(即: list.remove(x))`                                | O(n)         | O(n)         |
| 遍历                                                         | O(n)         | O(n)         |
| 获取切片                                                     | O(k)         | O(k)         |
| 删除切片                                                     | O(n)         | O(n)         |
| 设置切片                                                     | O(k+n)       | O(k+n)       |
| extend(list)                                                 | O(k)         | O(k)         |
| [sort](http://svn.python.org/projects/python/trunk/Objects/listsort.txt) | O(n log n)   | O(n log n)   |
| [n] * k                                                      | O(nk)        | O(nk)        |
| x in s                                                       | O(n)         |              |
| min(s), max(s)                                               | O(n)         |              |
| len()                                                        | O(1)         | O(1)         |

## 双向队列 - collections.deque

| **操作**   | **平均情况** | **最坏情况** |
| ---------- | ------------ | ------------ |
| copy       | O(n)         | O(n)         |
| append     | O(1)         | O(1)         |
| appendleft | O(1)         | O(1)         |
| pop        | O(1)         | O(1)         |
| popleft    | O(1)         | O(1)         |
| extend     | O(k)         | O(k)         |
| extendleft | O(k)         | O(k)         |
| rotate     | O(k)         | O(k)         |
| remove     | O(n)         | O(n)         |

## 集合 - set

| **操作**                          | **平均情况**                                                 | **最坏情况**                                  | **备注**                                   |
| --------------------------------- | ------------------------------------------------------------ | --------------------------------------------- | ------------------------------------------ |
| x in s                            | O(1)                                                         | O(n)                                          |                                            |
| Union s\|t                        | [O(len(s)+len(t))](https://wiki.python.org/moin/TimeComplexity_%28SetCode%29) |                                               |                                            |
| Intersection s&t                  | O(min(len(s), len(t))                                        | O(len(s) * len(t))                            | replace "min" with "max" if t is not a set |
| Multiple intersection s1&s2&..&sn |                                                              | (n-1)*O(l) where l is max(len(s1),..,len(sn)) |                                            |
| Difference s-t                    | O(len(s))                                                    |                                               |                                            |
| s.difference_update(t)            | O(len(t))                                                    |                                               |                                            |
| Symmetric Difference s^t          | O(len(s))                                                    | O(len(s) * len(t))                            |                                            |
| s.symmetric_difference_update(t)  | O(len(t))                                                    | O(len(t) * len(s))                            |                                            |

## 字典 - dict

| **操作**             | **平均情况** | **最坏情况** |
| -------------------- | ------------ | ------------ |
| k in d               | O(1)         | O(n)         |
| copy                 | O(n)         | O(n)         |
| dict[key]            | O(1)         | O(n)         |
| dict[key] = value    | O(1)         | O(n)         |
| dict.pop() popitem() | O(1)         | O(n)         |
| 遍历                 | O(n)         | O(n)         |
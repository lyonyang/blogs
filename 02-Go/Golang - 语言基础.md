# Golang - 语言基础

## 变量

在 Go 语言中定义变量有两种方式 : 一般声明和简短声明

### 一般声明

一般声明就是使用关键字 `var` 进行声明 , 格式如下 

```go
// 声明单个变量
var variableName type

// 声明多个变量
var variableName1, variableName2, variableName3 type
或
var (
    variableName1 type
    variableName2 type
    variableName3 type
)

// 初始化值
variableName = value
variableName1, variableName2, variableName3 = value1, value2, value3

// 声明并初始化值
var variableName type = value
var variableName1, variableName2, variableName3 type = value1, value2, value3
var (
    variableName1 type = value1
    variableName2 type = value2
    variableName3 type = value3
)

// 如果初始化值存在, 可以省略类型, 变量会从初始值中获取类型
var variableName1, variableName2, variableName3 = value1, value2, value3
```

当一个变量声明之后 , `Go` 会自动赋予它该类型的零值

### 简短声明

简短声明是使用 `:=` 来定义变量 , 但是它只能在函数中使用 , 也就是说它只能用来定义局部变量 , 如果要定义全局变量 , 还是需要通过一般声明 `var` 来进行

```go
func main() {
    variableName := value
    variableName1, variableName2, variableName3 := value1, value2, value3
}
```

## 常量

常量用于存储不会改变的数据 ,  它在编译阶段就已经被确定了 , 并且在程序运行时无法改变

常量的声明与变量类似 , 只不过是使用 `const` 关键字 , 但是常量只能使用一般声明 , 不能使用简短声明 ( `:=` )

```go
const constantName = value

// 你也可以明确指定常量的类型
const constantName type = value

// 定义多个常量
const constantName1, constantName2, constantName3 = value1, value2, value3
```

## 基础类型

`Go ` 的数据类型有

```go
bool

string

int  int8  int16  int32  int64
uint uint8 uint16 uint32 uint64 uintptr

byte // uint8 的别名

rune // int32 的别名
    // 表示一个 Unicode 码点

float32 float64

complex64 complex128
```

关于 `Go` 中的其他派生类型 , 如 `array` , `slice` , `map` 等 , 后续会详细介绍

## 流程控制

### if

```go
if 条件表达式 {
    
}

// 也可使用初始化语句
if 初始化语句; 条件表达式 {
    
}
```

如下

```go
if x < 0 {

}

// 使用初始化语句
func pow(a, b int) {
	if c := a + b; c < 10 {

	}
}
```

### if-else

```go
if 条件表达式 {
    
} else if 条件表达式 {
    
} else {
    
}

// 使用初始化语句
if 初始化语句; 条件表达式 {
    
} else if 初始化语句; 条件表达式 {
    
} else {
    
}
```

如下

```go
if x < 0 {
    
} else if x < 5 {
    
} else {
    
}

// 使用初始化语句
func pow(a, b int) {
	if c := a + b; c < 2 {
		
	} else if c := a + b; c > 5 {

	} else {

	}
}
```

### switch

`switch` 是编写一连串 `if - else` 语句的简便方法 , 它运行第一个值等于条件表达式的 `case` 语句

```go
switch 值 {
    case 值:
    	...
	case 值, 值...:
    	...
    default:
        ... 
}

// 没有条件的switch
switch {
    case 条件表达式:
    	...
	case 条件表达式, 条件表达式...:
    	...
    default:
        ...
}

// 带有初始化语句
switch 初始化语句; 值 {
    case 值:
    	...
	case 值, 值...:
    	...
    default:
        ... 
}

switch 初始化语句; {
    case 条件表达式:
    	...
	case 条件表达式, 条件表达式...:
    	...
    default:
        ... 
}
```

如下

```go
i := 10
switch i {
case 1:
case 2, 3, 4:
case 10:
default:
}

// 没有条件的switch
switch {
case i < 1:
case i > 1, i < 5:
default:
}

// 带有初始化语句
switch i := 10; i {
case 1:
case 2, 3, 4:
case 10:
default:
}

switch i := 10; {
case i < 1:
case i > 1, i < 5:
default:
}
```

`switch` 语句从上到下执行 , 当匹配成功的时候停止 , 如果需要往下继续执行 , 可以使用 `fallthrough` 强制执行后面的 `case` 

```go
i := 10
switch i {
case 10:
	fmt.Println(10)
	fallthrough
case 9:
	fmt.Println(9)
	fallthrough
case 8:
	fmt.Println(8)
case 7:
	fmt.Println(7)
}

/*
执行结果:
10
9
8
*/
```

### for

```go
for 初始化语句; 条件表达式; 后置语句 {
    
}

// 初始化语句和后置语句是可选的
for ; 条件表达式; {
    
}

// for去掉分号之后将会变成while
for 条件表达式 {
    
}

// 当省略条件表达式时, for将变成无限循环
for 初始化语句; ; 后置语句 {
    
}

// while同样
for {
    
}
```

如下

```go
for i := 0; i < 10; i++ {
    
}

// 初始化语句和后置语句是可选的
sum := 1
for ; sum < 1000; {
    sum += sum
}

// while
sum := 1
for sum < 1000 {

}

// 省略条件表达式, for变成无限循环
for sum := 1; ; sum++ {
    if sum == 3 {
        return
    }
}
```

当然 `break` 和 `continue` 就不用说了

### for-range

用于迭代可迭代的结构 , 如 `array` 和 `map` 

```go
for k, v := range map {
    
}
```

### goto

`goto` 必须与标签配合使用

```go
func main() {
	i := 0
HERE:
	print(i)
	i++
	if i == 5 {
		return
	}
	goto HERE
}
```

**特别注意 : ** 使用标签和 `goto` 语句是不被鼓励的 , 因为它们会很快导致非常糟糕的程序设置 , 而且总有更加可读的代替方案来实现相同的需求

除了 `goto` 之外 , `fot` , `switch` 和 `select` 与都也可以与标签配合使用

```go
func main() {

LABEL1:
	for i := 0; i <= 5; i++ {
		for j := 0; j <= 5; j++ {
			if j == 4 {
				continue LABEL1
			}
			fmt.Printf("i is: %d, and j is: %d\n", i, j)
		}
	}

}
```

## 函数

```go
// 无返回值
func funcName(input1 type1, input2 type2) {
    return value1, value2
}

// 一个返回值
func funcName(input1 type1, input2 type2) type {
    return value1
}

// 多个返回值
func funcName(input1 type1, input2 type2) (output1 type1, output2 type2) {
    return value1, value2
}

// 可变参数
func funcName(input1 type1, input2 ...type2) (output1 type1, output2 type2) {
    return value1, value2
}
```

如下

```go
func max(a, b int) int {
    if a > b {
        return a
    }
    return b
}

// 可变参数
func sum(a ...int) int {
	total := 0
	for _, value := range a {
		total = total + value
	}
	return total
}
```

### defer

`defer` 语句会在函数执行都最后时执行

```go
func main() {
	defer fmt.Println("world")
	fmt.Println("hello")
}
```
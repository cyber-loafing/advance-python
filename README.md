# Advanced Python Tips
scripts脚本自动将tip中的jupyter notebook笔记转换为README.md文件

---

* [1. args](#1-args)
* [2. copy_deepcopy](#2-copy_deepcopy)
* [3. dataclass](#3-dataclass)
* [4. decorators](#4-decorators)
* [5. exception](#5-exception)
* [6. iterator_generator](#6-iterator_generator)
* [7. lambda](#7-lambda)
* [8. ListComp_GenerateExpr](#8-ListComp_GenerateExpr)
* [9. magic _function](#9-magic-_function)
* [10. numerical](#10-numerical)
* [11. pass](#11-pass)
* [12. ternary_op](#12-ternary_op)
* [13. textcolor](#13-textcolor)

---

# 1. args
## args and kwargs
*args 和 **kwargs 是 Python 中用于处理不确定数量参数的特殊符号。它们的命名并不是固定的，在书写代码时可以自己选择。*args 表示不确定数量的非键值对的参数，可以接受任意数量的位置参数。在函数定义时使用 *args 可以将所有位置参数转为一个元组形式，并传递给函数体内的代码进行处理。

**kwargs 表示不确定数量的键值对参数，可以接受任意数量的关键字参数。在函数定义时使用 **kwargs 可以将所有关键字参数转为一个字典形式，并传递给函数体内的代码进行处理。。


```python
def f(*args,**kwargs):
    print(args)
    print(kwargs)

f(1,2,3,4,5,6,7,8,9,10, a=1,b=2,c=3,d=4,e=5,f=6,g=7,h=8,i=9,j=10)
```

    (1, 2, 3, 4, 5, 6, 7, 8, 9, 10)
    {'a': 1, 'b': 2, 'c': 3, 'd': 4, 'e': 5, 'f': 6, 'g': 7, 'h': 8, 'i': 9, 'j': 10}
    

## 补充，*运算符
1. 收集列表中的多余的值



```python
a, *b, c = [1, 2, 3, 4, 5]
print(a)
print(b)
print(c)
```

    1
    [2, 3, 4]
    5
    

# 2. copy_deepcopy
## 浅复制
首先明确两个概念：等于赋值和深复制。
- 等于赋值，并不会产生一个独立的对象单独存在，他只是将原有的数据块打上一个新标签，所以当其中一个标签被改变的时候，数据块就会发生变化，另一个标签也会随之改变。对于不可变对象，等于赋值和深复制没有区别。但是对于可变对象，等于赋值其实是将两个变量指向同一个对象，所以一个变量改变，另一个变量也会改变。
- 深复制(deep copy)，即将被复制对象完全再复制一遍作为独立的新个体单独存在。所以改变原有被复制对象不会对已经复制出来的新对象产生影响。
- 浅复制(shallow copy)需要分情况，浅拷贝包括三种形式：切片、工厂函数、以及copy模块
    1. 当浅复制的值是不可变对象（数值，字符串，元组）时和“等于赋值”的情况一样，对象的id值与浅复制原来的值相同。当原值发生改变时，浅复制的值不会发生变化。
    2. 当浅复制的值是可变对象（列表和元组）时会产生一个“不是那么独立的对象”存在。有两种情况：
        1. 复制的 对象中**无复杂子对象** ，原来值的改变并不会影响浅复制的值，同时浅复制的值改变也并不会影响原来的值。原来值的id值与浅复制原来的值不同。
        2. 复制的对象中有复杂子对象 （例如列表中的一个子元素是一个列表），如果不改变其中复杂子对象，浅复制的值改变并不会影响原来的值。 但是改变原来的值 中的复杂子对象的值  会影响浅复制的值。


建议，对于不可变对象，直接使用等于赋值，对于可变对象，如果不需要改变原来的值，使用浅复制，如果需要改变原来的值，使用深复制。

对于多层嵌套对象一定要使用深拷贝


```python
# 浅复制,不可变对象
a = 10
b = a
print(id(a))
print(id(b))
b = 20
print(a, b)
print(id(a))
print(id(b))
a = 'hello'
print(id(a))
```

    2796225364496
    2796225364496
    10 20
    2796225364496
    2796225364816
    2796296201200
    


```python
# 浅复制，可变对象,无复杂子对象
import copy
a = [1, 2, 3]
b = a
c = a.copy()
d = copy.deepcopy(a)
print(id(a))
print(id(b))
print(id(c))
print(id(d))
b[0] = 10
print(a, b, c, d) # 注意这里的c,d的值并没有发生变化,证明对于无复杂子对象的可变对象，浅复制和深复制是一样的
```

    2796308855296
    2796308855296
    2796309106176
    2796308975168
    [10, 2, 3] [10, 2, 3] [1, 2, 3] [1, 2, 3]
    


```python
# 浅复制，可变对象,有复杂子对象
a = [1, 2, [3, 4]]
b = a
c = a.copy()
d = copy.deepcopy(a)
print(id(a))
print(id(b))
print(id(c))
print(id(d))
b[0] = 10
b[2][0] = 30
print(a, b, c, d) # 注意这里的c的值由于有复杂子对象，所以发生了变化，但是d的值并没有发生变化，证明对于有复杂子对象的可变对象，浅复制和深复制是不一样的
```

    2796308854080
    2796308854080
    2796306020096
    2796308719296
    [10, 2, [30, 4]] [10, 2, [30, 4]] [1, 2, [30, 4]] [1, 2, [3, 4]]
    

# 3. dataclass
```python

```

# 4. decorators
## 概念

装饰器是给现有的模块增添新的小功能，可以对原函数进行功能扩展，而且还不需要修改原函数的内容，也不需要修改原函数的调用。

装饰器的使用符合了面向对象编程的开放封闭原则。

> 开放封闭原则主要体现在两个方面：
> - 对扩展开放，意味着有新的需求或变化时，可以对现有代码进行扩展，以适应新的情况。
> - 对修改封闭，意味着类一旦设计完成，就可以独立其工作，而不要对类尽任何修改。

### 拓展：函数闭包
在Python中，函数是一等对象，函数可以作为参数传递给另一个函数，函数可以作为另一个函数的返回值。函数闭包是指函数可以访问其外部作用域中的变量。闭包函数有以下几个特点：
1. 闭包函数是函数的嵌套，函数内还有函数，即外层函数嵌套一个内层函数
2. 在外层函数定义局部变量，在内层函数通过nonlocal引用，并实现指定功能，比如计数
3. 最后外层函数return内层函数
4. 主要作用：可以变相实现私有变量的功能，即用内层函数访问外层函数内的变量，并让外层函数内的变量常驻内存

比如下面代码中闭包函数之所以可以实现让外层函数内的变量常驻内存，关键就是其定义了个*内层函数*，并通过内层函数访问外层函数的变量，并最后由外层函数将内层函数返回出去并赋值给另外一个变量。*此时因为内层函数被赋值给一个变量，其内存空间不会被释放*，而内层函数又在其函数体内*引用了外层函数的变量*，导致该变量的内存也不会被回收。


```python
#外层函数
def outter_func():
    #定义外层函数的局部变量
    a=0
    #定义一个内层函数
    def inner_func():
        #声明下在内层函数内，a变量指向到外层函数的a
        nonlocal a
        a+=1
        print(a, end=' ')
    #返回内层函数
    return inner_func # 注意：这里返回的是函数对象，而不是函数的调用

counter=outter_func() # counter是inner_func函数对象，counter = inner_func
for i in range(10):
    counter()
```

    1 2 3 4 5 6 7 8 9 10 

#### 如何判断闭包函数


```python
def outter_func():
    #定义外层函数的局部变量
    a=0
    #定义一个内层函数
    def inner_func():
        #声明下在内层函数内，a变量指向到外层函数的a
        nonlocal a
        a+=1
        print(a, end=' ')
    #返回内层函数
    print(inner_func.__closure__) # 判断是否是闭包函数，如果是闭包函数，返回的是cell对象，否则返回None
    return inner_func # 注意：这里返回的是函数对象，而不是函数的调用

counter=outter_func() # counter是inner_func函数对象，counter = inner_func
counter()
```

    (<cell at 0x000001C5A0B33100: int object at 0x000001C59C2100D0>,)
    1 


### 函数装饰器的实现
函数装饰器的实现主要是通过闭包函数实现的，即在外层函数中定义一个内层函数，内层函数实现具体的功能，外层函数返回内层函数。在外层函数中可以传入一个函数作为参数，然后在内层函数中调用这个函数，并实现具体的功能。


```python
# 最终版本
from functools import wraps
import time
def count_time(func):
    @wraps(func) # 引入wraps，对内层实现装饰器功能的函数进行装饰，主要是将传入的被装饰函数元信息复制给具体实现装饰器功能函数
    def wrapper(*args, **kwargs):
        print(f'开始运行{func.__name__}函数')
        start_time = time.time()
        result = func(*args, **kwargs)
        end_time = time.time()
        print(f'{func.__name__}运行时间为：{end_time - start_time}')
        return result
    return wrapper
@count_time
def add(a : int, b : int) -> int:
    time.sleep(1)
    print(f'{a} + {b} = {a + b}')
    return a + b

add(1, 2)
print(add.__name__) # 如果不加wraps，这里会输出wrapper，就是inner函数的名字

```

    开始运行add函数
    1 + 2 = 3
    add运行时间为：1.0080552101135254
    add
    

#### 带参数的装饰器
带参数装饰器，即可以向装饰器传参，以为装饰器赋予个性化定制的特点，根据传入参数不同，装饰器表现行为不同等等，此时，需要再加一层函数嵌套，最外层函数主要实现传参的功能，然后返回第二层函数，此时就又退化成了两层嵌套，即不带参装饰器

1. 有三层函数嵌套，最外层函数主要是接受装饰器的参数，实现闭包，常驻内存，供其内层函数使用，然后return 第二层函数
2. 第二层函数与不带参情况下，基本一样
3. 第三层函数还是最终实现装饰器功能



```python
def dec_with_args(*args): # 第一层函数，接受装饰器的参数，实现闭包，返回第二层函数
    def dec(func): # 第二层函数，接受被装饰函数，返回第三层函数，实际上与不带参情况下的装饰器一样 #|
        @wraps(func)                                                              #|
        def in_dec(*args): # 第三层函数，实现具体装饰器功能                             #|
            """                                                                   #| 这些位置实际上就是不带参装饰器的实现
            your decorator code                                                   #|
            """                                                                   #|
            return func(*args)                                                    #|
        return in_dec                                                             #|
    return dec

# 仍然是计时器的例子, 但是这次我们可以传入参数, 用来控制是否打印函数的名字
def count_time_v2(print_func_name: bool = True):
    def dec(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            if print_func_name:
                print(f'开始运行{func.__name__}函数')
            start_time = time.time()
            result = func(*args, **kwargs)
            end_time = time.time()
            print(f'{func.__name__}运行时间为：{end_time - start_time}')
            return result
        return wrapper
    return dec

@count_time_v2(print_func_name=False)
def add(a : int, b : int) -> int:
    time.sleep(1)
    print(f'{a} + {b} = {a + b}')
    return a + b
add(1, 2)
```

    1 + 2 = 3
    add运行时间为：1.0088813304901123
    




    3



#### 对于wraps的实现


```python
def my_wraps(fwrap):
    def out_func(func):
        def in_func(*args,**kwargs):
            return func(*args,**kwargs)
        meta_info = ['__module__', '__name__', '__qualname__', '__doc__', '__annotations__']
        for meta in meta_info:
            setattr(in_func, meta, getattr(fwrap, meta))
        return in_func
    return out_func

def count_time_v3(func):
    @my_wraps(func)
    def wrapper(*args, **kwargs):
        print(f'开始运行{func.__name__}函数')
        start_time = time.time()
        result = func(*args, **kwargs)
        end_time = time.time()
        print(f'{func.__name__}运行时间为：{end_time - start_time}')
        return result
    return wrapper

@count_time_v3
def add(a : int, b : int) -> int:
    time.sleep(1)
    print(f'{a} + {b} = {a + b}')
    return a + b
add(1, 2)
print(add.__name__)
```

    开始运行add函数
    1 + 2 = 3
    add运行时间为：1.006812334060669
    add
    

### 类装饰器
装饰器还可以通过类来实现，其实主要是利用类的以下特点来变相实现函数装饰器功能：

1. 函数调用语语法f()等同于类的实例化，即调用类的__init__函数创建对象
2. 对象的调用obj()等同于运行对象的__call__魔法函数
3. 通过类实现装饰器，可以避免函数装饰器超过2层的嵌套情况，因为如果有三层的话，最外层函数可以认为是在调用类的__init__函数，这样可以让代码更易读和维护
4. 本质，只要实现类的__init__和__call__魔法函数，并在__init__函数内接受装饰器参数，在__call__函数内实现具体装饰器结构即可



```python
class CountTime:
    def __init__(self, func):
        self.func = func
    def __call__(self, *args, **kwargs):
        print(f'开始运行{self.func.__name__}函数')
        start_time = time.time()
        result = self.func(*args, **kwargs)
        end_time = time.time()
        print(f'{self.func.__name__}运行时间为：{end_time - start_time}')
        return result

@CountTime
def add(a : int, b : int) -> int:
    time.sleep(1)
    print(f'{a} + {b} = {a + b}')
    return a + b

add(1, 2)
# print(add.__name__)
```

    开始运行add函数
    1 + 2 = 3
    add运行时间为：1.0015771389007568
    




    3



## 使用场景

https://blog.csdn.net/weixin_52908342/article/details/136575100

### 日志记录


```python
import logging

def log_decorator(func):
    def wrapper(*args, **kwargs):
        logging.info(f"Calling {func.__name__} with args: {args} and kwargs: {kwargs}")
        result = func(*args, **kwargs)
        logging.info(f"{func.__name__} returned: {result}")
        return result
    return wrapper

@log_decorator
def add(x, y):
    return x + y
logging.basicConfig(level=logging.INFO)
result = add(3, 4)
print(result)  # 输出：7

```

    INFO:root:Calling add with args: (3, 4) and kwargs: {}
    INFO:root:add returned: 7
    

    7
    

### 使用装饰器缓存
在计算feibo数列的时候，可以使用装饰器缓存，避免重复计算,

@lru_cache 是最常见的缓存装饰器。lru_cache 是： Last recently used cache 的简写，可以将该函数最近调用的输入参数以及结果进行缓存。如果有新的调用，先检查缓存是否有相同的输入参数，如果存在，则直接返回对应结果。如果是无参函数，第1次调用后，以后每次调用，直接返回缓存结果。


```python
from functools import lru_cache

def cache_with_parameters(maxsize=128, typed=False):
    def decorator(func):
        @lru_cache(maxsize=maxsize, typed=typed)
        def wrapper(*args, **kwargs):
            print(f"缓存参数：maxsize={maxsize}, typed={typed}", end=' ')
            # 当前使用了多少缓存
            print(f"当前缓存数：{wrapper.cache_info().currsize}", end=' ')
            result = func(*args, **kwargs)
            return result
        return wrapper
    return decorator

@cache_with_parameters(maxsize=256, typed=True)
def fibonacci(n):
    if n <= 1:
        return n
    else:
        return fibonacci(n-1) + fibonacci(n-2)

for i in range(10):
    print(fibonacci(i))
```

    缓存参数：maxsize=256, typed=True 当前缓存数：0 0
    缓存参数：maxsize=256, typed=True 当前缓存数：1 1
    缓存参数：maxsize=256, typed=True 当前缓存数：2 1
    缓存参数：maxsize=256, typed=True 当前缓存数：3 2
    缓存参数：maxsize=256, typed=True 当前缓存数：4 3
    缓存参数：maxsize=256, typed=True 当前缓存数：5 5
    缓存参数：maxsize=256, typed=True 当前缓存数：6 8
    缓存参数：maxsize=256, typed=True 当前缓存数：7 13
    缓存参数：maxsize=256, typed=True 当前缓存数：8 21
    缓存参数：maxsize=256, typed=True 当前缓存数：9 34
    

# 5. exception
## 异常处理


```python
try:
    # 主代码块
    print('try 0/0 ')
    a = 0 / 0
    pass
except Exception as e:
    # 异常时，执行该块
    print(e)
    # 打印行数
    print(e.__traceback__.tb_lineno)
    ...
else:
    # 如果没有异常执行该块
    print('else')
    pass
finally:
    # 无论异常与否，最终执行该块
    print('finally')
    pass
```

    try 0/0 
    division by zero
    4
    finally
    

## for...else...

所谓else指的是循环正常结束后要执行的代码，即如果是bresk终止循环的情况。else下方缩进的代码将不执行。


```python
str1 = 'hello'
for i in str1:
    print(i, end=' ')
else:
    print()
    print('end')
```

    h e l l o 
    end
    


```python
str1 = 'hello'
for i in str1:
    print(i, end=' ')
    if i == 'l':
        break
else:
    print()
    print('end')
```

    h e l 


```python

```

# 6. iterator_generator
## Iterator

1. 迭代器是一个可以记住遍历的位置的对象。迭代器对象从集合的第一个元素开始访问，直到所有的元素被访问完结束。迭代器只能往前不会后退。迭代器有两个基本的方法：iter() 和 next()。字符串，列表或元组对象都可用于创建迭代器


```python
# 使用iter()与next()函数
arr = [1,2,3,4]
it = iter(arr)
print(next(it),end=",") # 1
print(next(it), end=",") # 2
for x in it:
    print(x,end=",") # 3 4
```

    1,2,3,4,

2. 创建一个迭代器，我们使用一个类，该类必须实现两个方法 __iter__() 与 __next__()。


```python
class MyNumbers:
    def __iter__(self):
        self.a = 1
        return self
    def __next__(self):
        if self.a <= 3:
            x = self.a
            self.a += 1
            return x
        else:
            raise StopIteration # StopIteration异常用于标识迭代的完成

myclass = MyNumbers()
myiter = iter(myclass)
for x in myiter:
    print(x,end=",") # 3
```

    1,2,3,

## Generator
生成器可以认为是一个简化版的迭代器, 生成器的实现是基于函数. 再函数中使用关键字“yield” 而不是通常用的return. yield作为生成器执行的暂停恢复点, 每次调用next, 生成器函数执行到yield语句, 会挂起,并保存当前的上下文信息. 知道下一个next触发生成器继续执行.


```python
# 生成器函数
def my_gen():
    for x in range(3):
        yield x * x

mygen = my_gen()
for x in mygen:
    print(x,end=",") # 0 1 4

```

    0,1,4,

# 7. lambda
## Lambda Function

lambda 函数是一种小型、匿名的、内联函数，它可以具有任意数量的参数，但只能有一个表达式。

匿名函数不需要使用 def 关键字定义完整函数。lambda 函数通常用于编写简单的、单行的函数，通常在需要函数作为参数传递的情况下使用，例如在 map()、filter()、reduce() 等函数中。

lambda arguments(包括单个参数以及*arg，**kwargs): expression


```python
f = lambda a, b: a + b
print(f(5,10))
```

    15
    


```python
f = lambda *args: sum(args)
print(f(1, 2, 3))  # 输出: 6
```

    6
    

lambda 函数通常与内置函数如 map()、filter() 和 reduce() 一起使用，以便在集合上执行操作。例如：


```python
numbers = [1, 2, 3, 4, 5]
squared = list(map(lambda x: x**2, numbers))
print(squared)  # 输出: [1, 4, 9, 16, 25]
```

    [1, 4, 9, 16, 25]
    


```python
# 与max()函数一起使用
num = [(1, 2.9), (1.5, 3.2), (1.3, 4.0), (2.2, 2.8)]
x = max(num, key=lambda x: x[0]) # 按第一个元素
print(x) # 输出: (2.2, 2.8)
y = max(num, key=lambda x: x[1])
print(y)  # 输出: (1.3, 4.0)
```

    (2.2, 2.8)
    (1.3, 4.0)
    


```python
# sorted()函数
num = [(1, 2.9), (1.5, 3.2), (1.3, 4.0), (2.2, 2.8)]
x = sorted(num, key=lambda x: x[0]) # 按第一个元素
print(x) # 输出: [(1, 2.9), (1.3, 4.0), (1.5, 3.2), (2.2, 2.8)]

```

    [(1, 2.9), (1.3, 4.0), (1.5, 3.2), (2.2, 2.8)]
    

# 8. ListComp_GenerateExpr
## 列表推导式
列表推导式是 Python中一种快速创建和转换列表的方法。它们可以在一行代码中生成一个新的列表，使用方括号[]括起来。列表推导式可以通过对原始序列的元素进行运算或筛选来生成新的列表。


```python
squares = [x ** 2 for x in range(1, 11)]
print(squares)  # [1, 4, 9, 16, 25, 36, 49, 64, 81, 100]
```

    [1, 4, 9, 16, 25, 36, 49, 64, 81, 100]
    

## 生成器表达式
生成器表达式是 Python中一种创建生成器的简洁语法。它们类似于列表推导式，但是使用圆括号（）而不是方括号[]。生成器表达式可以创建一个可迭代的生成器对象，用于逐个生成结果，而不是一次性生成一个完整的列表。这使得生成器表达式非常适合处理大型、无限序列或需要节省内存的情况。

```
(表达式 for 变量 in 源序列)
(表达式 for 变量 in 源序列 if 条件)
```

从上面的例子可以看到，生成器对象有__iter__()和__next__()魔术方法，所以生成器也是迭代器，


```python
num = (x**2 for x in range(10))
print(num) #<generator object <genexpr> at ???>
print(dir(num))
```

    <generator object <genexpr> at 0x000001E2349CA500>
    ['__class__', '__del__', '__delattr__', '__dir__', '__doc__', '__eq__', '__format__', '__ge__', '__getattribute__', '__gt__', '__hash__', '__init__', '__init_subclass__', '__iter__', '__le__', '__lt__', '__name__', '__ne__', '__new__', '__next__', '__qualname__', '__reduce__', '__reduce_ex__', '__repr__', '__setattr__', '__sizeof__', '__str__', '__subclasshook__', 'close', 'gi_code', 'gi_frame', 'gi_running', 'gi_yieldfrom', 'send', 'throw']
    

既然生成器是迭代器，所以我们可以通过转换函数把它转换为元组或者列表：


```python
num = (x**2 for x in range(10))
numtuple = tuple(num)
print(numtuple)
#(0, 1, 4, 9, 16, 25, 36, 49, 64, 81)

num = (x**2 for x in range(10))
numlist = list(num)
print(numlist)
#[0, 1, 4, 9, 16, 25, 36, 49, 64, 81]
```

    (0, 1, 4, 9, 16, 25, 36, 49, 64, 81)
    [0, 1, 4, 9, 16, 25, 36, 49, 64, 81]
    

注意上面的写法，第二次转换的时候我们重新生成num，如果你不重新生成，将会得到一个空的列表：


```python
num = (x**2 for x in range(10))
numtuple = tuple(num)
print(numtuple)
#(0, 1, 4, 9, 16, 25, 36, 49, 64, 81)

numlist = list(num)
print(numlist)
#[]
```

    (0, 1, 4, 9, 16, 25, 36, 49, 64, 81)
    []
    

这是因为num它是一个迭代器，在将num转换为tuple的时候，这个迭代器已经迭代到末尾了，你再使用list()来转换的时候，它只能是返回一个空的列表。

这就引出了元组推导式和列生成器表达式的区别，前者得到的是生成器或者迭代器，后者得到的是列表。生成器有两个特别重要的特征：
- 惰性计算：生成器表达式是惰性计算的，只有在需要时才生成下一个元素。这使得生成器表达式非常适合处理大型数据集或无限序列。
- 大小固定：生成器表达式不会一次性生成所有元素，因此它们的大小是固定的。一旦生成器表达式生成了所有元素，它就会被耗尽，无法再次使用。

## 生成器表达式 vs. 列表推导式
生成器表达式和列表推导式在语法和功能上非常相似，但它们的使用场景和性能有所不同。下面是它们的比较：

1. 内存占用：*生成器表达*式以惰性计算的方式逐个生成结果，只在需要时生成下一个元素，因此占用的内存较少。而*列表推导式*会一次性生成整个列表，占用的内存较大。对于处理大型数据集或无限序列的情况，使用生成器表达式可以避免内存溢出。
2. 运行速度：*生成器表达式*的惰性计算使得它们在某些情况下比*列表推导式*更快。如果只需要使用生成器对象的部分元素，而不是整个列表，生成器表达式会更加高效。列表推导式在创建列表时需要一次性计算所有元素，因此在某些情况下会更慢。
3. 语法：生成器表达式使用圆括号()，而列表推导式使用方括号[]。这是它们在语法上的区别，但并不影响它们的功能。


```python
import time

start_time = time.time()
squares_gen = (x ** 2 for x in range(1, 1000001))
end_time = time.time()
gen_time = end_time - start_time

start_time = time.time()
squares_list = [x ** 2 for x in range(1, 1000001)]
end_time = time.time()
list_time = end_time - start_time

print("生成器表达式的运行时间：{}秒".format(gen_time))
print("列表推导式的运行时间：{}秒".format(list_time))
```

    生成器表达式的运行时间：0.0秒
    列表推导式的运行时间：0.2411341667175293秒
    

# 9. magic _function
## Magic Functions
https://blog.csdn.net/zhangke0426/article/details/122929667

python 定义类时中，以双下划线开头，以双下划线结尾函数为魔法函数

- 魔法函数可以定义类的特性
- 魔法函数是解释器提供的功能
- 魔法函数只能使用 python 提供的魔法函数，不能自定义

常用的包括： __ init__()、__ str__()、__ new__()、__ unicode__()、 __ call__()、 __ len__()、 __repr__()、__ setattr__()、 __ getattr__()、 __ getattribute__()、 __ delattr__()、__ setitem__()、 __ getitem__()、__ delitem__()、 __ iter__()、__ del__()、 __dir__()、__dict__()、__exit__()，__enter(), __all__()等函数。

### 非数学运算类魔法函数

#### __str__ 和 __repr__
均是用于显示的，__str__ 用于 print，__repr__ 用于直接显示


```python
# __str__ 和 __repr__
class A:
    def __str__(self):
        return 'str'
    def __repr__(self):
        return 'repr'
a = A()
print(a) # 使用print时，调用__str__函数
a # 不使用print时，调用__repr__函数，如果没有__repr__函数，则调用__str__函数，同理，如果没有__str__函数，则调用__repr__函数
```

    str
    




    repr



#### 集合、序列相关：__len__函数、__getitem__函数、__setitem__函数、__delitem__函数和__contains__函数


```python
# 构建一个类，展示上述函数的使用
class A:
    def __init__(self, data):
        self.data = data
    def __len__(self):
        return len(self.data)
    def __getitem__(self, index):
        return self.data[index]
    def __setitem__(self, index, value):
        self.data[index] = value
    def __delitem__(self, index):
        del self.data[index]
    def __contains__(self, value):
        return value in self.data
a = A([1, 2, 3, 4, 5])
print(len(a)) # 调用__len__函数
print(a[0]) # 调用__getitem__函数
a[0] = 10 # 调用__setitem__函数
print(a[0]) # 调用__getitem__函数
del a[0] # 调用__delitem__函数
print(a[0]) # 调用__getitem__函数
print(10 in a) # 调用__contains__函数
```

    5
    1
    10
    2
    False
    

#### __call__函数
该方法的功能类似于在类中重载 () 运算符，使得类实例对象可以像调用普通函数那样，以“对象名()”的形式使用。作用：为了将类的实例对象变为可调用对象。


```python
# __call__函数
class A:
    def __call__(self, *args, **kwargs):
        print('call')
a = A()
a() # 调用__call__函数
```

    call
    

#### __exit__ 和 __enter__ 函数
__exit__和__enter__函数是与with语句的组合应用的，用于上下文管理。

1. __enter(self)__：负责返回一个值，该返回值将赋值给as子句后面的var_name，通常返回对象自己，即“self”。函数优先于with后面的“代码块”(statements1,statements2,……)被执行。

2. __exit__(self, exc_type, exc_val, exc_tb)：负责执行“清理”工作，比如释放资源等。函数在with后面的“代码块”(statements1,statements2,……)执行完毕后被调用，即“代码块”执行完毕后，执行__exit__函数。


```python
# __enter__函数
class A:
    def __enter__(self):
        print('enter中的逻辑')
        return self
    def __exit__(self, exc_type, exc_val, exc_tb):
        print('exit中的逻辑')

with A() as a:
    print('进入with的逻辑')
```

    enter中的逻辑
    进入with的逻辑
    exit中的逻辑
    

一个常见的用途是在pytorch中使用with语句，如下所示：
```python
import torch
with torch.no_grad():
    # 不进行梯度更新
    pass
```
而在改类中实际上是使用了__enter__和__exit__函数。
```python
import torch
def __enter__(self) -> None:
    self.prev = torch.is_grad_enabled()
    torch.set_grad_enabled(False)
def __exit__(self, exc_type: Any, exc_value: Any, traceback: Any) -> None:
    torch.set_grad_enabled(self.prev)
```


#### __new__函数与__init__函数
1. __new__函数：用于创建对象，是 **类（静态）** 方法，返回一个实例对象。该方法在__init__方法之前调用，用于创建实例对象。__new__方法的第一个参数是cls，表示要实例化的类，其余参数将会传递给__init__方法。
2. __init__函数：用于初始化对象，是实例方法，不返回任何内容。该方法在__new__方法之后调用，用于初始化实例对象。__init__方法的第一个参数是self，表示实例对象本身，其余参数将会传递给__new__方法。
3. __new__函数的返回值是一个实例对象，而__init__函数没有返回值。Python中真正的构造方法是__new__ 方法，__init__方法只是用来将传入的参数初始化到实例对象中。


```python
# python中使用__new__函数实现单例模式
class Singleton:
    _instance = None
    def __new__(cls, *args, **kwargs):
        print('__new__')
        if not cls._instance:
            print('create instance')
            cls._instance = super(Singleton, cls).__new__(cls)
        return cls._instance
    def __init__(self, name):
        print('__init__')
        self.name = name
a = Singleton('a')
b = Singleton('c')
print(a)
print(b)
print(b.name)
```

    __new__
    create instance
    __init__
    __new__
    __init__
    <__main__.Singleton object at 0x000001AF033D06A0>
    <__main__.Singleton object at 0x000001AF033D06A0>
    c
    

4. 一些关于__new__的应用:TODO

#### __getattr__、__setattr__、__delattr__函数
1. 当我们访问一个不存在的属性的时候，会抛出异常，提示我们不存在这个属性。而这个异常就是__getattr__方法抛出的
2. __setattr__方法用于设置属性值，当我们设置属性值的时候，会调用这个方法
3. __delattr__方法用于删除属性值，当我们删除属性值的时候，会调用这个方法


```python
# __getattr__、__setattr__、__delattr__函数
class A:
    def __init__(self):
        self.data = {'a': 123}
    def __getattr__(self, name):
        print('getattr')
        return self.data[name] #  如果不存在这个属性，会抛出异常
    def __setattr__(self, name, value):
        print('setattr')
        self.__dict__[name] = value
    def __delattr__(self, name):
        print('delattr')
        del self.__dict__[name]
a = A()
print(a.__dict__)
print(a.a) # 调用__getattr__函数
a.b = 123 # 调用__setattr__函数
print(a.__dict__)
del a.b # 调用__delattr__函数
print(a.__dict__)
```

    setattr
    {'data': {'a': 123}}
    getattr
    123
    setattr
    {'data': {'a': 123}, 'b': 123}
    delattr
    {'data': {'a': 123}}
    

#### __getattribute__，__setattr__

1. __getattribute__：该方法在访问属性时自动调用，无论属性是否存在，都会调用该方法。该方法的优先级高于__getattr__方法。如果类中定义了__getattribute__方法，那么在访问属性时，就会调用__getattribute__方法，而不会调用__getattr__方法。__getattribute__是属性访问拦截器，就是当这个类的属性被访问时，会自动调用类的__getattribute__方法。
2. __setattr__：该方法在设置属性时自动调用，无论属性是否存在，都会调用该方法。该方法的优先级高于__setattr__方法。如果类中定义了__setattr__方法，那么在设置属性时，就会调用__setattr__方法，而不会调用__setattr__方法。__setattr__是属性设置拦截器，就是当这个类的属性被设置时，会自动调用类的__setattr__方法。
3. __getattribute__和__setattr__方法的优先级高于__getattr__和__setattr__方法。

#### __dir__函数

1. dir() 函数，通过此函数可以某个对象拥有的所有的属性名和方法名，该函数会返回一个包含有所有属性名和方法名的有序列表。

### 数学运算类魔法函数
1. 类似于运算符重载，可以自定义类的运算符
2. 包括__ add__、__sub__、__mul__、__truediv__、__floordiv__、__mod__、__pow__、__and__、__or__、__xor__、__lshift__、__rshift__、__neg__、__pos__、__abs__、__invert__、__iadd__、__isub__、__imul__、__itruediv__、__ifloordiv__、__imod__、__ipow__、__iand__、__ior__、__ixor__、__ilshift__、__irshift__、__complex__、__int__、__float__、__round__、__index__等函数。

# 10. numerical
## 数字表示方法拓展


```python
import math

# 长整型
a = 1_000_000_000_000
# 科学计数法
b = 1e3 # 1 * 10^3
# 十六进制
c = 0x10
# 八进制
d = 0o1007
# 二进制
e = 0b1010
# 无穷大
f = float('inf')
# 负无穷大
g = float('-inf')
```


```python
# math库中的inf更省空间
arr = [math.inf, math.inf, float('inf'), float('inf')]
for i in arr:
    print(id(i))
# 前两者的id相同，后两者的id不同
```

    1412144834544
    1412144834544
    1412215496784
    1412250463056
    


```python
print(0.0 == -0.0) # True
print(0.0 is -0.0) # False
print(0 is -0) # True,原因是python会将常用的整数缓存起来，-5到256之间的整数会被缓存
a = 256
b = 256
print(a is b) # True
a = 257
b = 257
print(a is b) # False
```

    True
    False
    True
    True
    False
    

    <>:2: SyntaxWarning: "is" with a literal. Did you mean "=="?
    <>:3: SyntaxWarning: "is" with a literal. Did you mean "=="?
    <>:2: SyntaxWarning: "is" with a literal. Did you mean "=="?
    <>:3: SyntaxWarning: "is" with a literal. Did you mean "=="?
    C:\Users\cyberloafing\AppData\Local\Temp\ipykernel_14020\278747429.py:2: SyntaxWarning: "is" with a literal. Did you mean "=="?
      print(0.0 is -0.0) # False
    C:\Users\cyberloafing\AppData\Local\Temp\ipykernel_14020\278747429.py:3: SyntaxWarning: "is" with a literal. Did you mean "=="?
      print(0 is -0) # True,原因是python会将常用的整数缓存起来，-5到256之间的整数会被缓存
    


```python

```

# 11. pass
## ...
1. 三个点实际上是一个对象，`Ellipsis`，
2. 在缩进代码块中等价于`pass`，表示什么也不做
3. 在函数定义时作为默认参数


```python
print(...)
print(bool(...))
print(id(Ellipsis))
print(id(...))
print(type(...))
```

    Ellipsis
    True
    140727128477336
    140727128477336
    <class 'ellipsis'>
    


```python
def func1(a: int=...):
    print(a)
func1(23)  # 68
func1()  # Ellipsis
func1(...)  # Ellipsis
```

    This is a beautiful object.
    23
    Ellipsis
    Ellipsis
    

## pass
pass语句是一个空操作语句，表示什么也不做。它常用于占位，以避免语法错误。在执行到pass语句时，程序不会有任何操作，直接跳过并继续执行下一条语句

# 12. ternary_op
## python中的三目运算符
### 形式1
condition_is_true if condition else condition_is_false


```python
a = 2
print('a is 2' if a == 2 else 'a is not 2')
```

    a is 2
    

### 形式2
(if_test_is_false, if_test_is_true)[test]


```python
res = ('a is not 2', 'a is 2')[a == 2]
print(res)
```

    a is 2
    


```python

```

# 13. textcolor
## 在终端中输出彩色字体
可以使用 ANSI 转义序列来打印不同颜色的文本。ANSI 转义序列是一种用于控制文本输出格式和颜色的特殊字符序列。下面是一个使用 ANSI 转义序列打印绿色和红色文本的示例：

print(\033[显示方式;前景色;背景色m + 打印内容 + 结尾部分：\033[0m)


```python
green_text = '\033[32mThis is green text\033[0m'
red_text = '\033[31mThis is red text\033[0m'

print(green_text)
print(red_text)
```

    [32mThis is green text[0m
    [31mThis is red text[0m
    


```python
def print_c(data,display=0,front=32,back=0):
    print(f"\033["
          f"{display};" # 显示方式
          f"{front};" # 前景色
          f"{back}m" # 背景色
          f"{data}"
          f"\033[0m")

print_c("=================",display=4,front=32,back=32)
```

    [4;32;32m=================[0m
    

## 在juptyer notebook中输出彩色字体


```python
from IPython.display import display, HTML

def print_red(text):
    display(HTML(f'<font color="red">{text}</font>'))
print_red('这是红色的文本')
```


<font color="red">这是红色的文本</font>



```python

```


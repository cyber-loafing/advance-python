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
    

# 2. decorators
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
    return inner_func

counter=outter_func()
for i in range(10):
    counter()
```

    1 2 3 4 5 6 7 8 9 10 


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
    

# 3. ListComp_GenerateExpr
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
    

# 4. pass
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


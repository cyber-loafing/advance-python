# ...
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
    

# pass
pass语句是一个空操作语句，表示什么也不做。它常用于占位，以避免语法错误。在执行到pass语句时，程序不会有任何操作，直接跳过并继续执行下一条语句

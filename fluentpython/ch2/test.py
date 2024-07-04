
import timeit
# 搜索场景
SETUP = """
from array import array
from random import random,seed
seed(100)
floats_array = array('f', (random() for i in range(10**7)))
floats_list = [random() for i in range(10**7)]
"""
def clock(label, cmd, SETUP):
    res = timeit.repeat(cmd, setup=SETUP, number=50, repeat=3)
    print(label, *('{:.3f}'. format(x) for x in res))

clock('array:', "0.10 in floats_array", SETUP)
clock('list :', "0.10 in floats_list", SETUP)

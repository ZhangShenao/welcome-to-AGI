# -*- coding: utf-8 -*-
"""
@Time    : 2025/5/19 11:24 
@Author  : ZhangShenao 
@File    : 1.创建数组.py
@Desc    : NumPy的数组结构

安装NumPy依赖
pip install --upgrade numpy

NumPy是用于Python中科学计算的一个基础包
它提供了一个多维度的数组对象numpy.ndarray(N-dimensional array)
以及针对数组对象的各种快速操作,例如排序、变换，选择等

"""
import numpy as np

# 创建一个一维数组
# np.array()和np.asarray()这两个方法,都可以基于列表创建Numpy数组
# 区别在于: np.array()是深拷贝,而np.asarray()是浅拷贝
# arr_1_d = np.asarray([1])
# print(arr_1_d)

# 创建一个二维数组
# arr_2_d = np.asarray([[1, 2], [3, 4]])
# print(arr_2_d)

# 使用np.ones()方法,创建一个全为1的数组
# 可以指定shape和dtype
# arr_ones = np.ones(shape=(2, 3), dtype=np.int64)
# print(arr_ones)

# 使用np.zeros()方法,创建一个全为0的数组
# arr_zeros = np.zeros(shape=(2, 3), dtype=np.int64)
# print(arr_zeros)

# 借助np.ones()和np.zeros方法,可以实现数组的高效初始化
# 创建一个维度为3x3,且元素全为0.5的数组
# arr_2_d = np.ones(shape=(3, 3), dtype=np.float64) * 0.5
# print(arr_2_d)

# 使用np.arange([start, ]stop, [step, ]dtype=None)
# 创建一个在[start, stop)区间的数组
# 元素之间的跨度是step
arr_range = np.arange(0, 10, 2)
print(arr_range)  # [0 2 4 6 8]

# 使用np.linspace（start, stop, num=50, endpoint=True, retstep=False, dtype=None）
# 创建一个在[start, stop]区间的等差数列数组
arr_linspace = np.linspace(0, 10, 5)
print(arr_linspace)

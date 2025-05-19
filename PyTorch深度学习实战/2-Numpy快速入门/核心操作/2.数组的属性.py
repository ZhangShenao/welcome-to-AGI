# -*- coding: utf-8 -*-
"""
@Time    : 2025/5/19 11:48 
@Author  : ZhangShenao 
@File    : 2.数组的属性.py
@Desc    : 数组的属性

数组的关键属性:
ndim: 维度
shape: 形状
size: 数组中的元素总数
dtype: 数组中的元素类型
"""

import numpy as np


def n_dim(arr) -> None:
    """
    ndim: 数组的维度
    :param arr: 数组
    """

    print(f"【数组的维度】: {arr.ndim}")


def shape(arr) -> None:
    """
    shape: 获取数组的形状
    :param arr: 数组
    """

    print(f"【数组的形状】: {arr.shape}")


def reshape() -> None:
    """
    对数组形状进行变换
    变换前后,数组中元素的数量保持不变
    """

    # 创建一个2x2维的数组
    arr_2_d = np.asarray([[1, 2], [3, 4]])
    print(f"原始数组: {arr_2_d}, shape: {arr_2_d.shape}")

    # 将数组变换成4x1
    arr_4_1 = arr_2_d.reshape(4, 1)
    print(f"变换后的数组: {arr_4_1}, shape: {arr_4_1.shape}")


def size(arr) -> None:
    """
    size: 数组中的元素总数
    :param arr: 数组
    """

    print(f"【数组中的元素总数】: {arr.size}")


def dtype(arr) -> None:
    """
    dtype: 数组中的元素类型
    :param arr: 数组
    """

    print(f"【数组中的元素类型】: {arr.dtype}")


if __name__ == '__main__':
    # 创建数组
    arr_1_d = np.asarray([1])
    arr_2_d = np.asarray([[1, 2], [3, 4]])

    # 获取数组维度
    # n_dim(arr_1_d)  # 1
    # n_dim(arr_2_d)  # 2

    # 获取数组形状
    # shape(arr_1_d)  # 一维向量
    # shape(arr_2_d)  # 2x2 矩阵

    # 对数组进行reshape
    # reshape()

    # 获取数组size,即数组中的元素总数
    # 针对2x2维数组,其size=2x2=4
    # size(arr_2_d) # 4

    # 获取数组中的元素类型
    # 创建数组时,如果没有显式指定元素类型,则NumPy会自动选择合适的类型
    dtype(arr_2_d)  # int64

    # 创建数组时也可以显式指定元素类型
    arr_2_d_f = np.asarray([[1, 2], [3, 4]], dtype=np.float64)
    dtype(arr_2_d_f)  # float64

    # 可以通过astype()方法,改变数组的元素类型
    # 但此时是创建一个新的数组,而不是改变原数组
    arr_2_d_f_new = arr_2_d_f.astype(np.float32)
    dtype(arr_2_d_f_new)  # 新数组: float32
    dtype(arr_2_d_f)  # 原数组仍然为float64类型

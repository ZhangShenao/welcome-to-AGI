# -*- coding: utf-8 -*-
"""
@Time    : 2025/5/19 15:41 
@Author  : ZhangShenao 
@File    : 3.借助NumPy绘图.py 
@Desc    : 借助NumPy绘图
"""

import matplotlib.pyplot as plt
import numpy as np

# 使用arange方法,创建横坐标
X = np.arange(-50, 51, 2)
Y = X ** 2

plt.plot(X, Y, color="red")
plt.legend()
plt.show()

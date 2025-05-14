# -*- coding: utf-8 -*-
"""
@Time    : 2025/5/14 11:25 
@Author  : ZhangShenao 
@File    : train.py 
@Desc    : 选择算法并建立模型

回归分析(regression analysis),就是确定两种或两种以上变量间相互依赖的定量关系的一种统计分析
其中最常见的就是线性回归(linear regression)
机器学习中一元线性回归的公式通常写成: y=w∗x+b
w代表weight权重,b代表bias偏置,这是模型最重要的两个参数

scikit-learn,简称sklearn,它是使用最广泛的开源Python 机器学习库
"""
from pandas import DataFrame
from sklearn.linear_model import LinearRegression  # 导入线性回归算法模型

# 使用线性回归算法创建模型
linereg_model = LinearRegression()


def train_model(X_train, X_test, y_train, y_test: DataFrame) -> LinearRegression:
    """训练模型"""

    # 使用线性回归算法创建模型
    linear_regression_model = LinearRegression()

    # 使用训练数据集训练模型
    # fit函数的核心功能就是减少损失(loss),使函数对特征到标签的模拟越来越贴切
    # 减少损失的关键环节就是通过梯度下降,逐步优化模型的参数,使训练集误差值达到最小
    # 简单理解梯度下降,就是通过求导的方法,找到每一步的方向,确保总是往更小的损失方向前进
    linear_regression_model.fit(X_train, y_train)
    print(f"【模型训练完成】")
    print('【模型的4个特征的权重】', linear_regression_model.coef_)
    print('【模型的偏置】', linear_regression_model.intercept_)

    return linear_regression_model

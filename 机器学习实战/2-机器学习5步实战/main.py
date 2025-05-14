# -*- coding: utf-8 -*-
"""
@Time    : 2025/5/14 14:47 
@Author  : ZhangShenao 
@File    : main.py 
@Desc    : 机器学习5步实战 执行程序
1. 定义问题
2. 数据收集与预处理
   1. 收集数据
   2. 数据可视化
   3. 数据清洗
   4. 特征工程
   5. 创建特征集和标签集
   6. 拆分训练集、验证集和测试集
3. 选择算法与建立模型
4. 训练并拟合模型
5. 评估并优化模型性能
"""

from data import data_process
from evaluate import evaluate
from train import train_model

if __name__ == '__main__':
    # 1. 定义问题:
    # 有监督学习的回归问题
    # 根据微信软文的点赞数、转发数、热度指数、文章评级,来预测浏览量

    # 2. 数据收集与预处理
    X_train, X_test, y_train, y_test = data_process()

    # 3. 选择算法与建立模型
    # 采用线性回归模型

    # 4. 训练并拟合模型
    model = train_model(X_train, X_test, y_train, y_test)

    # 5. 评估并优化模型性能
    evaluate(model, X_train, X_test, y_train, y_test)

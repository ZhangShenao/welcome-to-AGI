# -*- coding: utf-8 -*-
"""
@Time    : 2025/5/14 11:58 
@Author  : ZhangShenao 
@File    : evaluate.py 
@Desc    : 模型的评估与优化

梯度下降是在用训练集拟合模型时最小化误差,这时候算法调整的是模型的内部参数
而在验证集或者测试集进行模型效果评估的过程中,我们则是通过最小化误差来实现超参数(模型外部参数)的优化
"""
from pandas import DataFrame
from sklearn.linear_model import LinearRegression  # 导入线性回归算法模型


def evaluate(linear_regression_model: LinearRegression, X_train, X_test, y_train, y_test: DataFrame) -> None:
    """模型评估:使用训练好的模型,在测试集上进行验证"""

    # 预测测试集的Y值
    # 在几乎所有的机器学习项目中,都可以用predict方法来进行预测
    # 它就是用模型在任意的同类型数据集上去预测真值的,可以应用于验证集、测试集,也可以应用于训练集本身
    y_pred = linear_regression_model.predict(X_test)

    print("【模型评估结果】")
    # 对比预测值与实际值
    df_ads_pred = X_test.copy()  # 测试集特征数据
    df_ads_pred["浏览量实际值"] = y_test  # 测试集标签真值
    df_ads_pred["浏览量预测值"] = y_pred  # 测试集标签预测值
    print(df_ads_pred)  # 显示数据

    # 评估模型分数
    # 常用于评估回归分析模型的指标有两种: R2分数和MSE指标
    # 大多数机器学习工具包中都会提供相关的工具。
    # 这里的score方法使用的是R2分数来评估模型
    # R2的取值在[0,1]之间
    # R2越大,说明所拟合的回归模型越优
    print("【线性回归预测评分】", linear_regression_model.score(X_test, y_test))

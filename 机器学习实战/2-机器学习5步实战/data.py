# -*- coding: utf-8 -*-
"""
@Time    : 2025/5/13 10:24 
@Author  : ZhangShenao 
@File    : data.py
@Desc    : 数据收集与预处理

数据收集与预处理完整的6个步骤:
1. 收集数据
2. 数据可视化
3. 数据清洗
4. 特征工程
5. 构建特征集和标签集
6. 拆分训练集、验证集和测试集
"""

import matplotlib.pyplot as plt  # Matplotlib:基础Python可视化库,提供2D/3D图表绘制能力

import pandas as pd  # Pandas:使用广泛的数据处理工具包
import seaborn as sns  # Seaborn: 基于Matplotlib的高级统计图表库,内置更美观的主题和复杂图表模板
from pandas import DataFrame
from pandas.io.parsers import TextFileReader
from sklearn.model_selection import train_test_split  # train_test_split工具,用于数据集拆分

# 将图表设置为中文字体
plt.rcParams['font.sans-serif'] = ['Songti SC']
plt.rcParams['axes.unicode_minus'] = False
sns.set_theme(font='Songti SC')


def view_data() -> None:
    """数据可视化"""

    # 读取CSV数据,并转换成DataFrame格式
    # DataFrame是机器学习中常见的二维表格类型数据结构
    df_ads = pd.read_csv('微信软文.csv')

    # 打印前10行
    print(df_ads.head(10))

    # 用matplotlib.pyplot的plot方法显示散点图
    plt.plot(df_ads["点赞数"], df_ads["浏览量"], 'r.', label="Training data")
    plt.xlabel("点赞数")  # x轴Label
    plt.ylabel("浏览量")  # y轴Label
    plt.legend()  # 显示图例
    plt.show()  # 显示绘图结果

    # 用seaborn的箱线图画图
    # data = pd.concat([df_ads["浏览量"], df_ads["热度指数"]], axis=1)
    # plt.figure()  # 创建新画布
    # sns.boxplot(x="热度指数", y="浏览量", data=data)
    # plt.ylim(0, 800000)  # 改用matplotlib方式设置坐标轴
    # plt.show()  # 必须添加显示命令


def data_process() -> (DataFrame, DataFrame, DataFrame, DataFrame):
    """数据处理"""

    # 加载并清洗数据
    df = load_and_clean_data()

    # 构建特征集和标签集
    X, y = build_feature_and_label_set(df)

    # 拆分训练集与测试集
    X_train, X_test, y_train, y_test = split_train_and_test_data(X, y)

    return X_train, X_test, y_train, y_test


def load_and_clean_data() -> DataFrame | TextFileReader:
    """加载并清洗数据"""

    # 读取CSV数据
    df_ads = pd.read_csv('微信软文.csv')

    # 打印原始数据集数量
    print(f"【原始数据集加载完成】数据总量: {len(df_ads)}")

    # 统计原始数据集中NaN出现的次数
    # print(f"原始数据中NaN数量: \n{df_ads.isna().sum()}")

    # 把出现了NaN的数据行删掉
    df_ads = df_ads.dropna()

    # 打印数据集数量
    print(f"【数据清洗完成】数据总量:  {len(df_ads)}")

    return df_ads


def build_feature_and_label_set(df: DataFrame) -> (DataFrame, DataFrame):
    """构建特征集和标签集"""

    # 构建特征集和标签集
    # 浏览量是我们最终需要预测的数据,因此浏览量是标签集,其余数据均为特征集
    X = df.drop(["浏览量"], axis=1)  # 特征集,Drop掉标签相关字段
    Y = df["浏览量"]

    # 打印特征集和标签集的数量
    print(f"【特征集和标签集构建完成】特征集数量: {len(X)}, 标签集数量: {len(Y)}")
    return X, Y


def split_train_and_test_data(X, y: DataFrame) -> (DataFrame, DataFrame, DataFrame, DataFrame):
    """拆分训练集与测试集"""

    # 将原始数据集拆分成训练集、验证集和测试集
    # 对于小型x项目来说,为了简化流程,经常会省略验证的环节
    # 仅将原始数据集拆分成训练集和测试集
    # 拆分的时候,留作测试的数据比例一般是20%或30%

    # 将数据集进行80%(训练集)和20%(验证集)的分割
    # X_train: 特征训练集
    # X_test: 特征测试集
    # y_train: 标签训练集
    # y_test: 标签测试集
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=0)

    # 打印训练集和测试集的数量
    print(
        f"【数据集拆分完成】特征训练集: {len(X_train)}, 特征测试集: {len(X_test)}, "
        f"标签训练集: {len(y_train)}, 标签测试集: {len(y_test)}")
    return X_train, X_test, y_train, y_test

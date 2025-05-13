# -*- coding: utf-8 -*-
"""
@Time    : 2025/5/13 10:24 
@Author  : ZhangShenao 
@File    : 2.数据收集与预处理.py 
@Desc    : 数据收集与预处理

完整的6个步骤:
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
from sklearn.model_selection import train_test_split  # train_test_split工具,用于数据集拆分

# 将图表设置为中文字体
plt.rcParams['font.sans-serif'] = ['Songti SC']
plt.rcParams['axes.unicode_minus'] = False
sns.set_theme(font='Songti SC')


def view_data() -> None:
    """数据可视化"""

    # 读取CSV数据,并转换成DataFrame格式
    # DataFrame是机器学习中常见的二维表格类型数据结构
    df_ads = pd.read_csv('易速鲜花微信软文.csv')

    # 打印前10行
    print(df_ads.head(10))

    # 用matplotlib.pyplot的plot方法显示散点图
    plt.plot(df_ads["点赞数"], df_ads["浏览量"], 'r.', label="Training data")
    plt.xlabel("点赞数")  # x轴Label
    plt.ylabel("浏览量")  # y轴Label
    plt.legend()  # 显示图例
    plt.show()  # 显示绘图结果

    # 用seaborn的箱线图画图
    data = pd.concat([df_ads["浏览量"], df_ads["热度指数"]], axis=1)
    plt.figure()  # 创建新画布
    sns.boxplot(x="热度指数", y="浏览量", data=data)
    plt.ylim(0, 800000)  # 改用matplotlib方式设置坐标轴
    plt.show()  # 必须添加显示命令


def clean_data() -> None:
    """数据清洗"""

    # 读取CSV数据
    df_ads = pd.read_csv('易速鲜花微信软文.csv')

    # 统计原始数据集中NaN出现的次数
    print(df_ads.isna().sum())  # NaN出现的次数

    # 把出现了NaN的数据行删掉
    df_ads = df_ads.dropna()
    # 打印前10行
    print(df_ads.head(10))


def build_feature_and_label_set() -> None:
    """构建特征集和标签集"""

    # 读取CSV数据
    df_ads = pd.read_csv('易速鲜花微信软文.csv')

    # 构建特征集和标签集
    # 浏览量是我们最终需要预测的数据,因此浏览量是标签集,其余数据均为特征集
    X = df_ads.drop(["浏览量"], axis=1)  # 特征集,Drop掉标签相关字段
    Y = df_ads["浏览量"]

    # 打印特征集和标签集的前10行
    print(X.head(10))
    print(Y.head(10))

    # 将原始数据集拆分成训练集、验证集和测试集
    # 对于小型x项目来说,为了简化流程,经常会省略验证的环节
    # 仅将原始数据集拆分成训练集和测试集
    # 拆分的时候,留作测试的数据比例一般是20%或30%

    # 将数据集进行80%(训练集)和20%(验证集)的分割
    # X_train: 特征训练集
    # X_test: 特征测试集
    # Y_train: 标签训练集
    # Y_test: 标签测试集
    X_train, X_test, Y_train, Y_test = train_test_split(X, Y, test_size=0.2, random_state=0)
    print(X_train.head(10))
    print(X_test.head(10))
    print(Y_train.head(10))
    print(Y_test.head(10))


if __name__ == '__main__':
    # 1. 收集数据

    # 2. 数据可视化
    # view_data()

    # 3. 数据清洗
    # clean_data()

    # 4. 特征工程

    # 5. 构建特征集和标签集
    build_feature_and_label_set()

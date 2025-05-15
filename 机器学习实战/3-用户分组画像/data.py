# -*- coding: utf-8 -*-
"""
@Time    : 2025/5/14 19:32 
@Author  : ZhangShenao 
@File    : data.py 
@Desc    : 数据分析——计算用户的RFM(Recency、Frequency、Monetary)值

"""

import matplotlib.pyplot as plt  # 导入Matplotlib的pyplot模块
import pandas as pd  # 导入Pandas
from pandas import DataFrame

# 将图表设置为中文字体
plt.rcParams['font.sans-serif'] = ['Songti SC']
plt.rcParams['axes.unicode_minus'] = False


def view_data() -> None:
    """数据可视化"""

    # 读取CSV数据,并转换成DataFrame格式
    order_df = pd.read_csv("./用户订单记录.csv")

    # 展示前几行数据
    print("展示前几行数据")
    print(order_df.head())

    # 查看数据的统计信息
    print("数据统计信息")
    print(order_df.describe())

    # 构建月度的订单数的DataFrame
    order_df["消费日期"] = pd.to_datetime(order_df["消费日期"])  # 转化日期格式
    df_orders_monthly = order_df.set_index("消费日期")['订单号'].resample('M').nunique()  # 每个月的订单数量
    # 设定绘图的画布
    ax = pd.DataFrame(df_orders_monthly.values).plot(grid=True, figsize=(12, 6), legend=False)
    ax.set_xlabel("月份")  # X轴label
    ax.set_ylabel("订单数")  # Y轴Label
    ax.set_title("月度订单数")  # 图题
    # 设定X轴月份显示格式
    plt.xticks(
        range(len(df_orders_monthly.index)),
        [x.strftime('%m.%Y') for x in df_orders_monthly.index],
        rotation=45)
    plt.show()  # 绘图


def load_and_clean_data() -> DataFrame:
    """加载并清洗数据"""

    # 读取CSV数据,并转换成DataFrame格式
    order_df = pd.read_csv("./用户订单记录.csv")

    # 删除重复数据
    order_df = order_df.drop_duplicates()

    # 把出现了NaN的数据行删掉
    order_df = order_df.dropna()

    # 清除掉数量小于0的脏数据
    # loc属性可以通过字段名(列名)访问数据集
    order_df = order_df.loc[order_df["数量"] > 0]

    #  打印数据集数量
    print(f"【数据加载并清洗完成】数据总量:  {len(order_df)}")
    print("【数据统计信息】")
    print(order_df.describe())

    return order_df

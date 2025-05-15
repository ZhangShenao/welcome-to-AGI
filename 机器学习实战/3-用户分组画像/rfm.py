# -*- coding: utf-8 -*-
"""
@Time    : 2025/5/15 17:12 
@Author  : ZhangShenao 
@File    : rfm.py 
@Desc    : 计算用户的RFM值

计算RFM值,本质上属于特征工程
就是对原始数据集中的信息进行选择、提取、合并、加工、转换
甚至是基于原始信息构建出新的、对于模型的训练更具有意义的特征

"""
import pandas as pd  # 导入Pandas
from pandas import DataFrame


def calc_rfm(order_df: DataFrame) -> DataFrame:
    """计算用户的RFM值"""

    # 计算用户消费的总价
    # 总价=数量*单价
    order_df["总价"] = order_df["数量"] * order_df["单价"]

    # 以用户码为关键字段,构建用户层级表
    user_df = pd.DataFrame(order_df["用户码"].unique())  # 生成以用户码为主键的结构df_user
    user_df.columns = ["用户码"]  # 设定字段名
    user_df = user_df.sort_values(by="用户码", ascending=True).reset_index(drop=True)  # 按用户码排序
    print(f"【用户层级表构建完成】总用户数: {len(user_df)}")

    # 计算R值,即用户距离上次消费以来的天数
    # 用表中最新订单的日期(拉出来这张表的日期),减去上一次消费的日期,就可以确定对应用户的R值
    # R值越大,说明该用户最近一次购物日距离当前日期越久，那么这样的用户就越是处于休眠状态
    order_df["消费日期"] = pd.to_datetime(order_df["消费日期"])  # 转化日期格式
    df_recent_buy = order_df.groupby("用户码").消费日期.max().reset_index()  # 构建消费日期信息
    df_recent_buy.columns = ["用户码", "最近日期"]  # 设定字段名
    df_recent_buy["R值"] = (df_recent_buy["最近日期"].max() - df_recent_buy["最近日期"]).dt.days  # 计算最新日期与上次消费日期的天数
    user_df = pd.merge(user_df, df_recent_buy[["用户码", "R值"]], on="用户码")  # 把上次消费距最新日期的天数（R值）合并至df_user结构
    print(f"【用户R值计算完成】")

    # 计算F值,即用户消费频率
    df_frequency = order_df.groupby("用户码").消费日期.count().reset_index()  # 计算每个用户消费次数,构建df_frequency对象
    df_frequency.columns = ["用户码", "F值"]  # 设定字段名称
    user_df = pd.merge(user_df, df_frequency, on="用户码")  # 把消费频率整合至df_user结构

    # 计算M值,即用户总消费金额
    df_revenue = order_df.groupby("用户码").总价.sum().reset_index()  # 根据消费总额,构建df_revenue对象
    df_revenue.columns = ["用户码", "M值"]  # 设定字段名称
    user_df = pd.merge(user_df, df_revenue, on="用户码")  # 把消费金额整合至df_user结构
    print(user_df.head())  # 显示头几行数据

    # 返回最终结果
    return user_df

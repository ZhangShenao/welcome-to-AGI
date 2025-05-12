# -*- coding: utf-8 -*-
"""
@Time    : 2025/5/12 18:24 
@Author  : ZhangShenao 
@File    : 漏斗分析.py 
@Desc    : 漏斗分析

安装依赖:
pip install plotly #安装Plotly包
pip install pandas #安装pandas包

plotly是一个数据可视化工具包,其中内置了漏斗图的绘制工具

pandas是Python核心的数据处理库,它提供了DataFrame数据结构,用于高效处理结构化数据
"""

import pandas as pd  # 导入pandas工具,命名为pd
import plotly.express as px  # 导入plotly.express工具,命名为px

if __name__ == '__main__':
    # 定义漏斗数据
    stages = ["访问数", "下载数", "注册数", "搜索数", "付款数"]
    male_data = dict(number=[59, 32, 18, 9, 2], stage=stages)
    female_data = dict(number=[29, 17, 8, 3, 1], stage=stages)

    # 将数据转换为DataFrame格式
    df_male = pd.DataFrame(male_data)
    df_male["性别"] = "男"
    df_female = pd.DataFrame(female_data)
    df_female["性别"] = "女"

    # 绘制漏斗图
    # 图片默认会展示在本地浏览器中
    df_total = pd.concat(objs=[df_male, df_female], axis=0)
    fig = px.funnel(df_total, x="number", y="stage", color="性别")
    fig.show()

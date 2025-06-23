# -*- coding: utf-8 -*-
"""
@Time    : 2025/6/20 11:05 
@Author  : ZhangShenao 
@File    : akshare_api.py 
@Desc    : 通过AKShare API,获取股票行情数据

pip install akshare --upgrade
"""

import akshare as ak
import pandas as pd

# 拉取宁德时代的日线数据
# 返回Pandas的DataFrame数据结构
df = ak.stock_zh_a_hist(symbol="300750",  # 宁德时代股票代码
                        period="daily",  # 日线
                        start_date="20250520",  # 起始日期
                        end_date='20250620',  # 终止日期
                        adjust="qfq"  # 复权方式,这里采用前复权
                        )

# 将日期转换为datetime类型,便于排序
df["日期"] = pd.to_datetime(df["日期"])

# 将日期设置为主键
# inplace=True:表示直接在原始数据上做修改,而不是先把原始数据做备份,然后在新的备份数据上修改
df.set_index("日期", inplace=True)

# 按照主键(日期)倒序排序
df.sort_index(ascending=False, inplace=True)

# 将DataFrame数据保存到CSV文件
df.to_csv("./宁德时代(20250520-20250620).csv")
print("股票行情数据已保存")

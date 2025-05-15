# -*- coding: utf-8 -*-
"""
@Time    : 2025/5/15 17:15 
@Author  : ZhangShenao 
@File    : main.py 
@Desc    : 执行函数

RFM是互联网公司普遍采用的用户画像分析指标
R: 新进度,代表自用户上次消费以来的天数,该指标用于衡量用户的热度
F: 是消费频率,代表用户是否频繁使用服务,主要用于表征用户黏性
M: 消费金额,代表用户在一段时间内消费的总金额,可以体现用户价值
"""

from data import load_and_clean_data
from rfm import calc_rfm

if __name__ == '__main__':
    # 加载并清洗数据
    order_df = load_and_clean_data()

    # 计算RFM值
    rfm_df = calc_rfm(order_df)

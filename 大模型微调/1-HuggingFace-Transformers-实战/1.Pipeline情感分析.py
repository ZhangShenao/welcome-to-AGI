# -*- coding: utf-8 -*-
"""
@Time    : 2025/5/22 14:44 
@Author  : ZhangShenao 
@File    : 1.Pipeline情感分析.py
@Desc    : 使用Pipeline API,实战情感分析
"""
from transformers import pipeline  # 导入Transforms Pipeline API

# 创建Pipeline
# 使用tabularisai/multilingual-sentiment-analysis模型
pip = pipeline(task="sentiment-analysis",  # 任务类型为sentiment-analysis情感分析
               model="tabularisai/multilingual-sentiment-analysis")  # 指定模型

# 进行情感分析
result = pip("AI changes the world!")
print(result)

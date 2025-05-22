# -*- coding: utf-8 -*-
"""
@Time    : 2025/5/22 18:47 
@Author  : ZhangShenao 
@File    : 4.使用AutoClass统一接口.py
@Desc    : 使用AutoClass,统一管理Model和Tokenizer
"""

# 导入AutoTokenizer分词器和AutoModel模型接口
from transformers import AutoTokenizer, AutoModel

# 根据名称加载tokenizer和model
# 分词器与模型是一一对应的
tokenizer = AutoTokenizer.from_pretrained("google-bert/bert-base-chinese")
model = AutoModel.from_pretrained("google-bert/bert-base-chinese")

# 将模型与分词器保存到本地
tokenizer.save_pretrained("./models/bert-base-chinese")
model.save_pretrained("./models/bert-base-chinese")

print("Tokenizer与Model保存成功！")

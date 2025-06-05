# -*- coding: utf-8 -*-
"""
@Time    : 2025/6/4 19:07 
@Author  : ZhangShenao 
@File    : moderation_demo.py 
@Desc    : OpenAI Moderation调用示例
"""
import os

import dotenv
from openai import OpenAI

# 加载环境变量
dotenv.load_dotenv()

# 创建OpenAI客户端
client = OpenAI(base_url=os.getenv("OPENAI_API_BASE"))

# 调用Moderation接口,获取内容审查结果
moderation = client.moderations.create(input="I want to kill them.")
# 转换成json格式打印
print(moderation.to_json())

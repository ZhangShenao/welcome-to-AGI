# -*- coding: utf-8 -*-
"""
@Time    : 2025/10/25 10:00
@Author  : ZhangShenao
@File    : gen_text.py
@Desc    : 使用Gemini模型生成文本
"""

import os
from google import genai
from google.genai import types

import dotenv

from google import genai

# 加载环境变量
dotenv.load_dotenv()

# 创建Gemini客户端
client = genai.Client(api_key=os.getenv("GOOGLE_API_KEY"))

response = client.models.generate_content(
    model="gemini-2.5-flash", contents="一只可爱的英短蓝猫，正躺在沙发上，安静地睡觉。"
)
print(response.text)

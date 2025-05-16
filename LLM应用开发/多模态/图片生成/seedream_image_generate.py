# -*- coding: utf-8 -*-
"""
@Time    : 2025/5/16 09:54 
@Author  : ZhangShenao 
@File    : seedream_image_generate.py
@Desc    : 使用Seedream模型生图
"""

import os
import time

import dotenv
from openai import OpenAI

# 加载环境变量
dotenv.load_dotenv()

# 创建客户端
client = OpenAI(
    base_url=os.getenv("VOLCENGINE_API_BASE"),
    # 从环境变量中获取您的 API Key。此为默认方式，您可根据需要进行修改
    api_key=os.environ.get("VOLCENGINE_API_KEY"),
)

prompt = """
Hi, can you create a 3d rendered image of a pig with wings and a top hat flying over a happy futuristic scifi city with lots of greenery?
"""

start_time = time.time()
# 使用Seedream模型生成图片
response = client.images.generate(
    model="doubao-seedream-3-0-t2i-250415",
    prompt=prompt,
    size="1024x1024",
    response_format="url"
)
print(response.data[0].url)
print(f"cost time: {time.time() - start_time:.2f}s")

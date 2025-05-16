# -*- coding: utf-8 -*-
"""
@Time    : 2025/5/16 10:12 
@Author  : ZhangShenao 
@File    : gpt_image_1_generate.py 
@Desc    : 使用gpt-image-1模型生成图片
"""

import base64
import os
import time

import dotenv
from openai import OpenAI

# 加载环境变量
dotenv.load_dotenv()

prompt = """
Hi, can you create a 3d rendered image of a pig with wings and a top hat flying over a happy futuristic scifi city with lots of greenery?
"""

client = OpenAI(
    base_url=os.getenv("OPENAI_API_BASE"),
    api_key=os.environ.get("OPENAI_API_KEY"),
)

start_time = time.time()
img = client.images.generate(
    model="gpt-image-1",
    prompt=prompt,
    n=1,
    size="1024x1024"
)
print(f"cost time: {time.time() - start_time:.2f}s")
image_bytes = base64.b64decode(img.data[0].b64_json)
with open("gpt-image-1.png", "wb") as f:
    f.write(image_bytes)

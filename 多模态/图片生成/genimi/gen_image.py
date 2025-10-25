# -*- coding: utf-8 -*-
"""
@Time    : 2025/10/25 10:00
@Author  : ZhangShenao
@File    : gen_image.py
@Desc    : 使用Gemini模型生成图片
"""

import os
from google import genai
from google.genai import types

import dotenv

from google import genai
from google.genai import types
from PIL import Image
from io import BytesIO

# 加载环境变量
dotenv.load_dotenv()

# 创建Gemini客户端
client = genai.Client(api_key=os.getenv("GOOGLE_API_KEY"))

prompt = "一只可爱的英短蓝猫，正躺在沙发上，安静地睡觉。"

response = client.models.generate_content(
    model="gemini-2.5-flash-image",
    contents=[prompt],
)

for part in response.candidates[0].content.parts:
    if part.text is not None:
        print(part.text)
    elif part.inline_data is not None:
        image = Image.open(BytesIO(part.inline_data.data))
        image.save("cat.png")

print("图片生成完成！")

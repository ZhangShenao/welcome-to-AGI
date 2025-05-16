# -*- coding: utf-8 -*-
"""
@Time    : 2025/5/15 20:16 
@Author  : ZhangShenao 
@File    : gemini_image_edit.py 
@Desc    : 使用Gemini模型进行图片编辑
"""
import os
from io import BytesIO

import PIL.Image
import dotenv
from PIL import Image
from google import genai
from google.genai import types

img = PIL.Image.open("./pig.png")

# 加载环境变量
dotenv.load_dotenv()

# 创建Gemini客户端
client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

text_input = """
保持图片中小猪的主体不变，把背景更换成一望无际的大草原。
"""

response = client.models.generate_content(
    model="gemini-2.0-flash-preview-image-generation",
    contents=[text_input, img],
    config=types.GenerateContentConfig(
        response_modalities=["TEXT", "IMAGE"]
    )
)

for part in response.candidates[0].content.parts:
    if part.text is not None:
        print(part.text)
    elif part.inline_data is not None:
        image = Image.open(BytesIO(part.inline_data.data))
        image.show()

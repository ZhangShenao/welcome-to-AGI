# -*- coding: utf-8 -*-
"""
@Time    : 2025/10/25 10:00
@Author  : ZhangShenao
@File    : imagen.py
@Desc    : 使用Google Imagen生成图片
"""

from google import genai
from google.genai import types

import dotenv

import os
from google.genai.types import Image

# 加载环境变量
dotenv.load_dotenv()

# 创建Imagen客户端
client = genai.Client(api_key=os.getenv("GOOGLE_API_KEY"))

# 生成图片
response = client.models.generate_images(
    model="imagen-4.0-generate-001",
    prompt="一只可爱的英短蓝猫，正躺在沙发上，安静地睡觉。",
    config=types.GenerateImagesConfig(
        number_of_images=1,
    ),
)

# 保存图片
for generated_image in response.generated_images:
    generated_image.image.save("cat.png")

print("图片生成完成！")

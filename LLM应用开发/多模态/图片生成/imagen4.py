# -*- coding: utf-8 -*-
"""
@Time    : 2025/5/22 15:48 
@Author  : ZhangShenao 
@File    : imagen4.py 
@Desc    : 
"""

import dotenv
from google import genai

# 加载环境变量
dotenv.load_dotenv()

project_id = "gen-lang-client-0810386143"
client = genai.Client(vertexai=True, project=project_id, location="us-central1")

prompt = """
    Hi, can you create a 3d rendered image of a pig with wings and a top hat flying over a happy futuristic scifi city with lots of greenery?
    """

image = client.models.generate_images(
    model="imagen-4.0-generate-preview-05-20",
    prompt=prompt,
)

# OPTIONAL: View the generated image in a notebook
image.generated_images[0].image.show()

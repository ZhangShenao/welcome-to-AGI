# -*- coding: utf-8 -*-
"""
@Time    : 2025/5/12 11:10 
@Author  : ZhangShenao 
@File    : gemini_image_generate.py
@Desc    : 使用Gemini模型生成图片
"""
import os
import time
from io import BytesIO

import dotenv
from PIL import Image
from google import genai
from google.genai import types


def generate_image(client, model_name: str, prompt: str) -> None:
    """
    生成图片
    :param client: 调用客户端
    :param model_name: 模型名称
    :param prompt: 生图Prompt
    """
    print(f"start generating image by {model_name}")
    start_time = time.time()
    response = client.models.generate_content(
        model=model_name,
        contents=prompt,
        config=types.GenerateContentConfig(
            response_modalities=["TEXT", "IMAGE"]
        )
    )

    for part in response.candidates[0].content.parts:
        if part.text is not None:
            print(part.text)
        elif part.inline_data is not None:
            image = Image.open(BytesIO((part.inline_data.data)))
            image.save(f'{model_name}.png')
            image.show()

    print(f"generating image by {model_name} finished! cost time: {time.time() - start_time:.2f}")


if __name__ == '__main__':
    # 加载环境变量
    dotenv.load_dotenv()

    # 创建Gemini客户端
    client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

    # 构造生图Prompt
    prompt = """
    Elaine, radiating delight with sparkling blue eyes and a playful wink, drives away from the curb, her hand resting intimately on 张申傲's thigh with a gentle squeeze, creating a flirtatious and comfortable atmosphere within the car.
    """

    # 使用gemini-2.0-flash-preview-image-generation生图
    generate_image(client=client,
                   model_name="gemini-2.0-flash-preview-image-generation",
                   prompt=prompt)

    # 休眠5s
    time.sleep(5)

    # 使用gemini-2.0-flash-exp-image-generation生图
    generate_image(client=client,
                   model_name="gemini-2.0-flash-exp-image-generation",
                   prompt=prompt)

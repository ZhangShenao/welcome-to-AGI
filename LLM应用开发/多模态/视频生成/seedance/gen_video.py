# -*- coding: utf-8 -*-
"""
@Time    : 2025/5/22 20:38 
@Author  : ZhangShenao 
@File    : gen_video.py
@Desc    : 基于首帧生成视频
"""
import base64
import os

import dotenv
from volcenginesdkarkruntime import Ark

dotenv.load_dotenv()
client = Ark(api_key=os.environ.get("VOLCENGINE_API_KEY"))

if __name__ == "__main__":
    print("----- create request -----")
    with open("./char.png", "rb") as image_file:
        first_frame = base64.b64encode(image_file.read()).decode('utf-8')

    resp = client.content_generation.tasks.create(
        model="doubao-seedance-1-0-lite-i2v-250428",
        content=[{
            "text": "The woman opened the car door, got into the car, placed her hand on the steering wheel, and showed a charming smile. --rs 720p  --dur 5",
            "type": "text"},
            {"image_url": {"url": f"data:image/png;base64,{first_frame}"},
             "type": "image_url"}]
    )
    print(resp)

# -*- coding: utf-8 -*-
"""
@Time    : 2025/5/24 15:31 
@Author  : ZhangShenao 
@File    : gen_video.py 
@Desc    : 使用首帧生图
"""
import base64
import os

import dotenv
import requests

# 加载环境变量
dotenv.load_dotenv()

# 对首尾帧图片进行Base64编码
with open("./char.jpeg", "rb") as image_file:
    first_frame = base64.b64encode(image_file.read()).decode('utf-8')

url = "https://api.vidu.cn/ent/v2/img2video"

headers = {
    "Authorization": f"{os.getenv("VIDU_API_KEY")}",
    "Content-Type": "application/json"
}

prompt = """
The woman opened the car door, got into the car, placed her hand on the steering wheel, and showed a charming smile.
"""

payload = {
    "model": "vidu2.0",
    "images": [
        f"data:image/png;base64,{first_frame}",
    ],
    "prompt": prompt,
    "duration": "4",
    "seed": "0",
    "resolution": "720p",
    "movement_amplitude": "large"
}

try:
    response = requests.post(url, headers=headers, json=payload)
    response.raise_for_status()  # 自动处理HTTP错误
    print("请求成功！响应内容：")
    print(response.json())
except requests.exceptions.RequestException as e:
    print(f"请求失败: {e}")
    if hasattr(e, 'response') and e.response:
        print(f"错误响应内容：{e.response.text}")

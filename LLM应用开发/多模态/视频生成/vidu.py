# -*- coding: utf-8 -*-
"""
@Time    : 2025/5/23 14:40 
@Author  : ZhangShenao 
@File    : vidu.py 
@Desc    : 使用Vidu生图
"""
import base64
import os

import dotenv
import requests

# 加载环境变量
dotenv.load_dotenv()

# 对首尾帧图片进行Base64编码
with open("./first_frame.png", "rb") as image_file:
    first_frame = base64.b64encode(image_file.read()).decode('utf-8')

with open("./last_frame.png", "rb") as image_file:
    last_frame = base64.b64encode(image_file.read()).decode('utf-8')

url = "https://api.vidu.cn/ent/v2/start-end2video"

headers = {
    "Authorization": f"{os.getenv("VIDU_API_KEY")}",
    "Content-Type": "application/json"
}

payload = {
    "model": "vidu2.0",
    "images": [
        f"data:image/png;base64,{first_frame}",
        f"data:image/png;base64,{last_frame}",
    ],
    "prompt": "这只可爱的小猪在天上飞累了，它呼扇着翅膀，慢慢降落到下面的小河里，痛快地洗了个澡，又惬意地打了个哈欠。远景切特写。",
    "duration": "4",
    "seed": "0",
    "resolution": "720p",
    "movement_amplitude": "auto"
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

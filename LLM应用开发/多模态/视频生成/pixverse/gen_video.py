# -*- coding: utf-8 -*-
"""
@Time    : 2025/5/24 13:59 
@Author  : ZhangShenao 
@File    : gen_video.py
@Desc    : 使用PixVerse生成视频
"""

import http.client
import json
import os

import dotenv

dotenv.load_dotenv()

conn = http.client.HTTPSConnection("app-api.pixverse.ai")
prompt = """
The woman opened the car door, got into the car, placed her hand on the steering wheel, and showed a charming smile.
"""
payload = json.dumps({
    "duration": 5,
    "img_id": 515830702,
    "model": "v4",
    "prompt": prompt,
    "quality": "540p",
    "water_mark": False
})
headers = {
    'API-KEY': os.getenv("PIXVERSE_API_KEY"),
    'Ai-trace-id': 'video-1',
    'Content-Type': 'application/json'
}
conn.request("POST", "/openapi/v2/video/img/generate", payload, headers)
res = conn.getresponse()
data = res.read()
print(data.decode("utf-8"))

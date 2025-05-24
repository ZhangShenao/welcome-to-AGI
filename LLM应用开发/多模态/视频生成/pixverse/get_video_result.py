# -*- coding: utf-8 -*-
"""
@Time    : 2025/5/24 14:14 
@Author  : ZhangShenao 
@File    : get_video_result.py 
@Desc    : 查看视频生成结果
"""

import http.client
import os

import dotenv

dotenv.load_dotenv()

conn = http.client.HTTPSConnection("app-api.pixverse.ai")
payload = ''
headers = {
    'API-KEY': os.getenv("PIXVERSE_API_KEY"),
    'Ai-trace-id': 'video-1'
}
conn.request("GET", "/openapi/v2/video/result/339869297025749", payload, headers)
res = conn.getresponse()
data = res.read()
print(data.decode("utf-8"))

# -*- coding: utf-8 -*-
"""
@Time    : 2025/5/24 15:34 
@Author  : ZhangShenao 
@File    : get_result.py 
@Desc    : 
"""
import os

import dotenv
import requests

# 加载环境变量
dotenv.load_dotenv()

# 替换为实际参数

url = f"https://api.vidu.cn/ent/v2/tasks/823763529973661696/creations"
headers = {
    "Authorization": f"Token {os.getenv("VIDU_API_KEY")}"
}

try:
    response = requests.get(url, headers=headers)
    response.raise_for_status()  # 检查HTTP错误
    print(f"响应状态码: {response.status_code}")
    print("响应内容:", response.json())
except requests.exceptions.RequestException as e:
    print(f"请求失败: {e}")

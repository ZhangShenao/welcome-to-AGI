# -*- coding: utf-8 -*-
"""
@Time    : 2025/5/16 17:29 
@Author  : ZhangShenao 
@File    : get_result.py 
@Desc    : 获取视频生成结果
"""
import os

import dotenv
from volcenginesdkarkruntime import Ark

if __name__ == '__main__':
    # 加载环境变量
    dotenv.load_dotenv()

    # 创建ARK客户端
    client = Ark(api_key=os.environ.get("VOLCENGINE_API_KEY"))

    # 获取视频生成任务结果
    resp = client.content_generation.tasks.get(
        task_id="cgt-20250524163612-5lm8n",
    )
    print(resp)

# -*- coding: utf-8 -*-
"""
@Time    : 2025/4/16 18:57 
@Author  : ZhangShenao 
@File    : tts.py 
@Desc    : TTS

Text-to-Speech,文本转语音: 将文字转换成语音输出
"""
import os

import dotenv
import openai

# 加载环境变量
dotenv.load_dotenv()

# 定义音频文件保存路径
speech_file_path = "./静夜思.mp3"

# 创建OpenAI客户端
client = openai.OpenAI(
    api_key=os.getenv("OPENAI_API_KEY"),
    base_url=os.getenv("OPENAI_API_BASE")
)

# 调用OpenAI API进行语音合成
with client.audio.speech.with_streaming_response.create(
        model="tts-1",
        voice="nova",
        input="床前明月光，疑似地上霜。举头望明月，低头思故乡。"
) as response:
    response.stream_to_file(speech_file_path)

print(f"语音合成完成！保存路径：{speech_file_path}")

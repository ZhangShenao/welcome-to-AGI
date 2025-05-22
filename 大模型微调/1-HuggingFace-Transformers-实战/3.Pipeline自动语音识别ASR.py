# -*- coding: utf-8 -*-
"""
@Time    : 2025/5/22 19:01 
@Author  : ZhangShenao 
@File    : 3.Pipeline自动语音识别ASR.py 
@Desc    : 使用Pipeline API,实战ASR

ASR: Automatic Speech Recognition,自动语音识别,即将语音转录为文本
这是最常见的音频任务之一

ASR依赖底层的音频文件解码能力,需要先安装ffmpeg

brew install ffmpeg

"""
from transformers import pipeline

# 创建Pipeline,任务类型为ASR
# 使用OpenAI的whisper-small模型
asr = pipeline(task="automatic-speech-recognition", model="openai/whisper-small")

# 读取音频文件,识别文本
text = asr("./静夜思.mp3")
print(text)

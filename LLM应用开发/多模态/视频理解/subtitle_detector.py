# -*- coding: utf-8 -*-
"""
@Time    : 2025/1/27
@Author  : AI Assistant
@File    : subtitle_detector.py
@Desc    : 使用GPT-4o检测视频是否配有字幕
"""
import os
import base64
from typing import List, Dict, Any
import cv2
import dotenv
from openai import OpenAI

# 加载环境变量
dotenv.load_dotenv()

# 创建OpenAI客户端
client = OpenAI(
    api_key=os.getenv("OPENAI_API_KEY"), base_url=os.getenv("OPENAI_API_BASE")
)


def extract_frames_for_subtitle_detection(
    video_path: str, num_frames: int = 5
) -> List[str]:
    """
    为字幕检测提取视频帧
    :param video_path: 视频文件路径
    :param num_frames: 要提取的帧数
    :return: base64编码的帧列表
    """
    extracted_frames = []

    if not os.path.exists(video_path):
        raise FileNotFoundError(f"视频文件不存在: {video_path}")

    video_capture = cv2.VideoCapture(video_path)
    total_frame_count = int(video_capture.get(cv2.CAP_PROP_FRAME_COUNT))
    frame_rate = video_capture.get(cv2.CAP_PROP_FPS)

    if total_frame_count == 0:
        raise ValueError("无法读取视频文件或视频为空")

    # 计算采样间隔，确保均匀分布在整个视频中
    if num_frames >= total_frame_count:
        # 如果请求的帧数大于等于总帧数，则提取所有帧
        frame_indices = list(range(total_frame_count))
    else:
        # 均匀分布采样
        step = total_frame_count // num_frames
        frame_indices = [i * step for i in range(num_frames)]

    print(f"视频信息: 总帧数={total_frame_count}, 帧率={frame_rate:.2f}fps")
    print(f"提取帧索引: {frame_indices}")

    for frame_index in frame_indices:
        video_capture.set(cv2.CAP_PROP_POS_FRAMES, frame_index)
        success, frame = video_capture.read()

        if success:
            # 编码为JPEG格式
            _, buffer = cv2.imencode(".jpg", frame)
            frame_base64 = base64.b64encode(buffer).decode("utf-8")
            extracted_frames.append(frame_base64)
        else:
            print(f"警告: 无法读取第 {frame_index} 帧")

    video_capture.release()
    print(f"成功提取 {len(extracted_frames)} 帧用于字幕检测")
    return extracted_frames


def detect_subtitles_with_gpt4o(frames: List[str]) -> Dict[str, Any]:
    """
    使用GPT-4o检测视频帧中是否包含字幕
    :param frames: base64编码的视频帧列表
    :return: 检测结果字典
    """
    if not frames:
        raise ValueError("没有提供视频帧进行检测")

    # 构建消息内容
    message_content = [
        {
            "type": "text",
            "text": "请仔细分析以下视频帧，判断该视频是否配有字幕。请重点关注：\n"
            "1. 视频画面底部或顶部是否有文字内容\n"
            "2. 文字是否为字幕形式（通常有背景色或边框）\n"
            "3. 文字内容是否与视频内容相关\n"
            "4. 字幕的样式和位置\n\n"
            "请以JSON格式返回结果，包含以下字段：\n"
            "{\n"
            '  "has_subtitles": true/false,\n'
            '  "subtitle_confidence": 0.0-1.0,\n'
            '  "subtitle_locations": ["bottom", "top", "center", "none"],\n'
            '  "subtitle_style": "描述字幕样式",\n'
            '  "detected_text": "检测到的文字内容",\n'
            '  "reasoning": "判断理由"\n'
            "}",
        }
    ]

    # 添加图像帧
    for i, frame in enumerate(frames):
        message_content.append(
            {
                "type": "image_url",
                "image_url": {
                    "url": f"data:image/jpeg;base64,{frame}",
                    "detail": "high",  # 使用高细节模式以获得更好的文字识别效果
                },
            }
        )

    try:
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {
                    "role": "system",
                    "content": "你是一个专业的视频内容分析师，擅长识别视频中的字幕和文字内容。"
                    "请仔细分析提供的视频帧，准确判断是否包含字幕。",
                },
                {"role": "user", "content": message_content},
            ],
            temperature=0.1,  # 使用较低的温度以获得更一致的结果
            max_tokens=1000,
        )

        result_text = response.choices[0].message.content
        print("GPT-4o原始响应:")
        print(result_text)

        # 尝试解析JSON结果
        import json

        try:
            # 提取JSON部分（如果响应包含其他文本）
            start_idx = result_text.find("{")
            end_idx = result_text.rfind("}") + 1
            if start_idx != -1 and end_idx != 0:
                json_str = result_text[start_idx:end_idx]
                result = json.loads(json_str)
            else:
                # 如果没有找到JSON格式，创建默认结果
                result = {
                    "has_subtitles": "字幕" in result_text.lower()
                    or "subtitle" in result_text.lower(),
                    "subtitle_confidence": 0.5,
                    "subtitle_locations": ["unknown"],
                    "subtitle_style": "无法确定",
                    "detected_text": "无法提取",
                    "reasoning": result_text,
                }
        except json.JSONDecodeError:
            # JSON解析失败，创建默认结果
            result = {
                "has_subtitles": "字幕" in result_text.lower()
                or "subtitle" in result_text.lower(),
                "subtitle_confidence": 0.5,
                "subtitle_locations": ["unknown"],
                "subtitle_style": "无法确定",
                "detected_text": "无法提取",
                "reasoning": result_text,
            }

        return result

    except Exception as e:
        print(f"调用GPT-4o API时出错: {e}")
        return {
            "has_subtitles": False,
            "subtitle_confidence": 0.0,
            "subtitle_locations": ["error"],
            "subtitle_style": "检测失败",
            "detected_text": "无法检测",
            "reasoning": f"API调用失败: {str(e)}",
        }


def check_video_subtitles(video_path: str, num_frames: int = 5) -> Dict[str, Any]:
    """
    检查视频是否配有字幕的主函数
    :param video_path: 视频文件路径
    :param num_frames: 要分析的帧数
    :return: 检测结果
    """
    print(f"开始检测视频字幕: {video_path}")
    print(f"分析帧数: {num_frames}")
    print("-" * 50)

    try:
        # 1. 提取视频帧
        frames = extract_frames_for_subtitle_detection(video_path, num_frames)

        # 2. 使用GPT-4o检测字幕
        result = detect_subtitles_with_gpt4o(frames)

        # 3. 格式化输出结果
        print("\n" + "=" * 50)
        print("字幕检测结果:")
        print("=" * 50)
        print(f"视频文件: {video_path}")
        print(f"是否配有字幕: {'是' if result['has_subtitles'] else '否'}")
        print(f"置信度: {result['subtitle_confidence']:.2f}")
        print(f"字幕位置: {', '.join(result['subtitle_locations'])}")
        print(f"字幕样式: {result['subtitle_style']}")
        print(f"检测到的文字: {result['detected_text']}")
        print(f"判断理由: {result['reasoning']}")
        print("=" * 50)

        return result

    except Exception as e:
        error_result = {
            "has_subtitles": False,
            "subtitle_confidence": 0.0,
            "subtitle_locations": ["error"],
            "subtitle_style": "检测失败",
            "detected_text": "无法检测",
            "reasoning": f"处理过程中出错: {str(e)}",
        }
        print(f"检测过程中出错: {e}")
        return error_result


if __name__ == "__main__":
    # 检查本地的"字幕.mp4"视频文件
    video_file = "./字幕.mp4"

    if not os.path.exists(video_file):
        print(f"错误: 找不到视频文件 {video_file}")
        print("请确保视频文件存在于当前目录中")
    else:
        # 执行字幕检测
        result = check_video_subtitles(video_file, num_frames=5)

        # 输出最终结论
        print(f"\n最终结论: 该视频{'配有' if result['has_subtitles'] else '没有'}字幕")

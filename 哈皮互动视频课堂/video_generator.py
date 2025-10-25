# -*- coding: utf-8 -*-
"""
@Time    : 2025/01/27
@Author  : ZhangShenao
@File    : video_generator.py
@Desc    : 视频生成模块
"""

import time
from google import genai
from google.genai import types
from google.genai.types import Image
from google.genai.types import GeneratedVideo


class VideoGenerator:
    """视频生成器类"""

    def __init__(self, api_key: str):
        """初始化Google AI客户端"""
        self.client = genai.Client(api_key=api_key)

    def generate_first_video_segment(
        self,
        character_image_path: str,
        first_segment: str,
        output_path: str = "story_part1.mp4",
    ) -> GeneratedVideo:
        """生成第一段视频"""
        print("🎬 正在生成第一段视频...")
        print(f"📝 剧情内容: {first_segment}")

        try:
            # 设置参考图片
            ref_pic = types.VideoGenerationReferenceImage(
                image=Image.from_file(location=character_image_path),
                reference_type="asset",
            )

            # 生成第一段视频
            operation = self.client.models.generate_videos(
                model="veo-3.1-generate-preview",
                prompt=f"儿童教育视频，{first_segment}，画面温馨，适合儿童观看",
                config=types.GenerateVideosConfig(
                    resolution="720p",
                    duration_seconds=8,
                    reference_images=[ref_pic],
                ),
            )

            # 轮询生成状态
            while not operation.done:
                print("⏳ 等待视频生成完成...")
                time.sleep(2)
                operation = self.client.operations.get(operation)

            # 下载生成视频
            generated_video = operation.response.generated_videos[0]
            self.client.files.download(file=generated_video.video)
            generated_video.video.save(output_path)
            print(f"✅ 第一段视频生成完成: {output_path}")
            return generated_video

        except Exception as e:
            print(f"❌ 第一段视频生成失败: {e}")
            return None

    def extend_video(
        self,
        current_video: GeneratedVideo,
        segment_description: str,
        part_number: int,
        output_path: str = None,
    ) -> GeneratedVideo:
        """扩展视频"""
        if output_path is None:
            output_path = f"story_part{part_number}.mp4"

        print(f"🎬 正在生成第{part_number}段视频...")
        print(f"📝 剧情内容: {segment_description}")

        try:
            # 扩展视频
            operation = self.client.models.generate_videos(
                model="veo-3.1-generate-preview",
                video=current_video.video,
                prompt=f"儿童教育视频，{segment_description}，画面温馨，适合儿童观看",
                config=types.GenerateVideosConfig(
                    number_of_videos=1, resolution="720p"
                ),
            )

            # 轮询生成状态
            while not operation.done:
                print("⏳ 等待视频生成完成...")
                time.sleep(2)
                operation = self.client.operations.get(operation)

            # 下载扩展后的视频
            generated_video = operation.response.generated_videos[0]
            self.client.files.download(file=generated_video.video)
            generated_video.video.save(output_path)
            print(f"✅ 第{part_number}段视频生成完成: {output_path}")
            return generated_video

        except Exception as e:
            print(f"❌ 第{part_number}段视频生成失败: {e}")
            return None

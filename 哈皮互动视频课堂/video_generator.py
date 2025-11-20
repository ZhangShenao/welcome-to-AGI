# -*- coding: utf-8 -*-
"""
@Time    : 2025/01/27
@Author  : ZhangShenao
@File    : video_generator.py
@Desc    : 视频生成模块 - 使用Veo3.1 API
"""

import os
import time
from typing import List, Callable, Optional
from concurrent.futures import ThreadPoolExecutor, as_completed
from google import genai
from google.genai import types
from google.genai.types import Image

# 导入moviepy（moviepy 2.x版本直接从moviepy导入）
try:
    import moviepy

    VideoFileClip = moviepy.VideoFileClip
    concatenate_videoclips = moviepy.concatenate_videoclips
except ImportError:
    # 如果导入失败，设置为None，在merge_video_segments中会检查
    VideoFileClip = None
    concatenate_videoclips = None
    import warnings

    warnings.warn("moviepy未安装，视频拼接功能将不可用。请运行: pip install moviepy")


class VideoGenerator:
    """视频生成器类 - 使用Veo3.1 API"""

    def __init__(self, api_key: str, image_generator=None):
        """初始化Google AI客户端"""
        self.client = genai.Client(api_key=api_key)
        self.image_generator = image_generator  # 图片生成器，用于生成分镜首帧图片

    def generate_video_segment(
        self,
        character_image_path: str,
        shot_script: str,
        segment_index: int,
        output_path: str = None,
        progress_callback: Optional[Callable] = None,
        story_segment: str = None,
    ) -> Optional[str]:
        """生成单个分镜视频（使用参考图和分镜脚本）"""
        if output_path is None:
            output_path = f"story_part{segment_index + 1}.mp4"

        if progress_callback:
            progress_callback(f"🎬 正在生成第{segment_index + 1}段视频...")

        try:
            # 如果有image_generator，先生成分镜首帧图片
            reference_image_path = character_image_path
            if self.image_generator and story_segment:
                if progress_callback:
                    progress_callback(
                        f"🖼️ 正在生成第{segment_index + 1}段分镜首帧图片..."
                    )
                frame_image_path = self.image_generator.generate_shot_frame_image(
                    character_image_path=character_image_path,
                    story_segment=story_segment,
                    shot_script=shot_script,
                    segment_index=segment_index,
                    output_path=f"shot_frame_{segment_index + 1}.png",
                    progress_callback=progress_callback,
                )
                if frame_image_path:
                    reference_image_path = frame_image_path
                    if progress_callback:
                        progress_callback(
                            f"✅ 首帧图片生成完成，使用首帧图片作为视频参考"
                        )
                else:
                    if progress_callback:
                        progress_callback(
                            f"⚠️ 首帧图片生成失败，使用角色图片作为视频参考"
                        )

            # 创建视频生成任务（使用首帧图片或角色图片作为参考）
            if progress_callback:
                progress_callback(f"📝 使用分镜脚本生成视频")

            # 读取图片文件
            ref_image = Image.from_file(location=reference_image_path)

            # 使用Veo3.1生成视频（使用image参数作为首帧）
            operation = self.client.models.generate_videos(
                model="veo-3.1-generate-preview",
                prompt=shot_script,  # 分镜脚本已经是英文
                image=ref_image,  # 使用image参数作为首帧图片
                config=types.GenerateVideosConfig(
                    resolution="720p",
                    duration_seconds=8,
                    aspect_ratio="9:16",  # 720x1280是竖屏
                ),
            )

            if progress_callback:
                progress_callback(f"✅ 视频任务创建成功，正在生成...")

            # 轮询生成状态
            while not operation.done:
                if progress_callback:
                    progress_callback(f"⏳ 第{segment_index + 1}段视频生成中...")
                time.sleep(2)
                operation = self.client.operations.get(operation)

                # 检查是否有错误
                if hasattr(operation, "error") and operation.error:
                    if progress_callback:
                        progress_callback(
                            f"❌ 第{segment_index + 1}段视频生成失败: {operation.error}"
                        )
                    return None

            # 下载视频
            generated_video = operation.response.generated_videos[0]
            self.client.files.download(file=generated_video.video)
            generated_video.video.save(output_path)

            if progress_callback:
                progress_callback(
                    f"✅ 第{segment_index + 1}段视频生成完成: {output_path}"
                )

            return output_path

        except Exception as e:
            if progress_callback:
                progress_callback(f"❌ 第{segment_index + 1}段视频生成失败: {e}")
            return None

    def generate_video_segments_parallel(
        self,
        character_image_path: str,
        shot_scripts: List[dict],
        progress_callback: Optional[Callable] = None,
        segment_callback: Optional[Callable] = None,
    ) -> List[Optional[str]]:
        """并行生成所有分镜视频（使用分镜脚本）"""
        if progress_callback:
            progress_callback(f"🚀 开始并行生成{len(shot_scripts)}段视频...")

        results = [None] * len(shot_scripts)
        output_paths = [f"story_part{i + 1}.mp4" for i in range(len(shot_scripts))]

        def generate_with_index(index):
            """带索引的生成函数"""
            # 通知分镜开始生成
            if segment_callback:
                segment_callback(index, "loading")

            # 获取分镜脚本和剧情
            shot_script_data = shot_scripts[index]
            shot_script_text = shot_script_data.get("shot_script", "")
            story_segment = shot_script_data.get("story_segment", "")

            result = self.generate_video_segment(
                character_image_path=character_image_path,
                shot_script=shot_script_text,
                segment_index=index,
                output_path=output_paths[index],
                progress_callback=progress_callback,
                story_segment=story_segment,
            )

            # 通知分镜生成完成
            if segment_callback and result:
                segment_callback(index, "completed", result)

            return result

        # 使用线程池并行生成
        with ThreadPoolExecutor(max_workers=min(5, len(shot_scripts))) as executor:
            futures = {
                executor.submit(generate_with_index, i): i
                for i in range(len(shot_scripts))
            }

            for future in as_completed(futures):
                index = futures[future]
                try:
                    result = future.result()
                    results[index] = result
                except Exception as e:
                    if progress_callback:
                        progress_callback(f"❌ 第{index + 1}段视频生成异常: {e}")
                    results[index] = None

        if progress_callback:
            completed_count = sum(1 for r in results if r is not None)
            progress_callback(
                f"✅ 视频生成完成: {completed_count}/{len(shot_scripts)}段成功"
            )

        return results

    def merge_video_segments(
        self,
        video_paths: List[str],
        output_path: str = "complete_story.mp4",
        progress_callback: Optional[Callable] = None,
    ) -> Optional[str]:
        """将所有分镜视频按顺序拼接成完整视频"""
        if VideoFileClip is None or concatenate_videoclips is None:
            if progress_callback:
                progress_callback("❌ moviepy模块未正确安装，无法拼接视频")
            return None

        if progress_callback:
            progress_callback("🎬 开始拼接视频...")

        try:
            # 过滤掉None值
            valid_paths = [
                path for path in video_paths if path and os.path.exists(path)
            ]

            if not valid_paths:
                if progress_callback:
                    progress_callback("❌ 没有有效的视频文件可以拼接")
                return None

            if progress_callback:
                progress_callback(f"📹 正在加载{len(valid_paths)}个视频片段...")

            # 加载所有视频片段
            clips = []
            for i, path in enumerate(valid_paths):
                try:
                    clip = VideoFileClip(path)
                    clips.append(clip)
                    if progress_callback:
                        progress_callback(f"✅ 已加载第{i + 1}个视频片段")
                except Exception as e:
                    if progress_callback:
                        progress_callback(f"❌ 加载视频片段失败 {path}: {e}")
                    continue

            if not clips:
                if progress_callback:
                    progress_callback("❌ 没有成功加载的视频片段")
                return None

            if progress_callback:
                progress_callback("🔗 正在拼接视频...")

            # 拼接视频
            final_clip = concatenate_videoclips(clips, method="compose")

            if progress_callback:
                progress_callback("💾 正在保存完整视频...")

            # 保存完整视频
            final_clip.write_videofile(
                output_path,
                codec="libx264",
                audio_codec="aac",
                fps=24,
            )

            # 释放资源
            final_clip.close()
            for clip in clips:
                clip.close()

            if progress_callback:
                progress_callback(f"✅ 视频拼接完成: {output_path}")

            return output_path

        except Exception as e:
            if progress_callback:
                progress_callback(f"❌ 视频拼接失败: {e}")
            return None

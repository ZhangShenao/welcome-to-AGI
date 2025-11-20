# -*- coding: utf-8 -*-
"""
@Time    : 2025/01/27
@Author  : ZhangShenao
@File    : image_generator.py
@Desc    : 图片生成模块
"""

from google import genai
from google.genai import types

import os
import dotenv
from typing import Optional, Callable
from pydantic.type_adapter import R
from PIL import Image
from io import BytesIO

# 加载环境变量
dotenv.load_dotenv()


class ImageGenerator:
    """图片生成器类"""

    def __init__(self, api_key: str):
        """初始化Google AI客户端"""
        self.client = genai.Client(api_key=api_key)

    def generate_character_image(
        self, character_description: str, output_path: str = "character.png"
    ) -> str:
        """生成人物形象图片"""
        print("🎨 正在生成人物形象图片...")

        try:
            prompt = f"儿童插画风格，{character_description}，卡通形象，适合儿童观看，色彩鲜艳，画面温馨"
            response = self.client.models.generate_content(
                model="gemini-2.5-flash-image",
                contents=[prompt],
            )

            # 保存图片并裁剪为720x1280
            for part in response.candidates[0].content.parts:
                if part.inline_data is not None:
                    image = Image.open(BytesIO(part.inline_data.data))

                    # 裁剪为严格的720x1280尺寸（符合Sora2要求）
                    target_width = 720
                    target_height = 1280

                    # 获取原始尺寸
                    original_width, original_height = image.size

                    # 计算缩放比例，确保能完全覆盖目标尺寸
                    scale_ratio = max(
                        target_width / original_width, target_height / original_height
                    )
                    new_width = int(original_width * scale_ratio)
                    new_height = int(original_height * scale_ratio)

                    # 缩放图片
                    image = image.resize(
                        (new_width, new_height), Image.Resampling.LANCZOS
                    )

                    # 计算裁剪区域（居中裁剪）
                    left = (new_width - target_width) // 2
                    top = (new_height - target_height) // 2
                    right = left + target_width
                    bottom = top + target_height

                    # 裁剪图片
                    image = image.crop((left, top, right, bottom))

                    # 保存图片
                    image.save(output_path)
                    print(f"✅ 图片已裁剪为 {target_width}x{target_height} 尺寸")
                    return output_path

        except Exception as e:
            print(f"❌ 图片生成失败: {e}")
            return None

    def generate_shot_frame_image(
        self,
        character_image_path: str,
        story_segment: str,
        shot_script: str,
        segment_index: int,
        output_path: str = None,
        progress_callback: Optional[Callable] = None,
    ) -> Optional[str]:
        """生成分镜首帧图片（使用角色图片作为参考）"""
        if output_path is None:
            output_path = f"shot_frame_{segment_index + 1}.png"

        if progress_callback:
            progress_callback(f"🖼️ 正在生成第{segment_index + 1}段分镜首帧图片...")

        try:
            # 读取角色参考图片
            ref_image = Image.open(character_image_path)

            # 构建提示词，结合分镜剧情和分镜脚本
            prompt = f"""根据以下分镜剧情和分镜脚本，生成该段分镜的首帧图片：

分镜剧情：{story_segment}

分镜脚本：{shot_script}

要求：
1. 画面要符合分镜脚本的描述
2. 角色形象要与参考图片保持一致
3. 画面温馨，适合儿童观看
4. 图片尺寸为720x1280（竖屏）
5. 这是视频的首帧，要能体现该段分镜的核心内容"""

            # 使用Gemini生成图片（使用参考图片）
            response = self.client.models.generate_content(
                model="gemini-2.5-flash-image",
                contents=[prompt, ref_image],
                config=types.GenerateContentConfig(response_modalities=["IMAGE"]),
            )

            # 保存图片并裁剪为720x1280
            for part in response.candidates[0].content.parts:
                if part.inline_data is not None:
                    image = Image.open(BytesIO(part.inline_data.data))

                    # 裁剪为严格的720x1280尺寸（符合Sora2要求）
                    target_width = 720
                    target_height = 1280

                    # 获取原始尺寸
                    original_width, original_height = image.size

                    # 计算缩放比例，确保能完全覆盖目标尺寸
                    scale_ratio = max(
                        target_width / original_width, target_height / original_height
                    )
                    new_width = int(original_width * scale_ratio)
                    new_height = int(original_height * scale_ratio)

                    # 缩放图片
                    image = image.resize(
                        (new_width, new_height), Image.Resampling.LANCZOS
                    )

                    # 计算裁剪区域（居中裁剪）
                    left = (new_width - target_width) // 2
                    top = (new_height - target_height) // 2
                    right = left + target_width
                    bottom = top + target_height

                    # 裁剪图片
                    image = image.crop((left, top, right, bottom))

                    # 保存图片
                    image.save(output_path)

                    if progress_callback:
                        progress_callback(
                            f"✅ 第{segment_index + 1}段分镜首帧图片生成完成: {output_path}"
                        )
                    else:
                        print(
                            f"✅ 第{segment_index + 1}段分镜首帧图片生成完成: {output_path}"
                        )

                    return output_path

            if progress_callback:
                progress_callback(
                    f"❌ 第{segment_index + 1}段分镜首帧图片生成失败：未找到图片数据"
                )
            return None

        except Exception as e:
            error_msg = f"❌ 第{segment_index + 1}段分镜首帧图片生成失败: {e}"
            if progress_callback:
                progress_callback(error_msg)
            else:
                print(error_msg)
            return None

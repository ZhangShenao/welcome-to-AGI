# -*- coding: utf-8 -*-
"""
@Time    : 2025/01/27
@Author  : ZhangShenao
@File    : image_generator.py
@Desc    : 图片生成模块
"""

from google import genai
from google.genai import types


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
            response = self.client.models.generate_images(
                model="imagen-4.0-generate-001",
                prompt=f"儿童插画风格，{character_description}，卡通形象，适合儿童观看",
                config=types.GenerateImagesConfig(
                    number_of_images=1,
                ),
            )

            # 保存图片
            for generated_image in response.generated_images:
                generated_image.image.save(output_path)
                print(f"✅ 人物形象图片生成完成: {output_path}")
                return output_path

        except Exception as e:
            print(f"❌ 图片生成失败: {e}")
            return None

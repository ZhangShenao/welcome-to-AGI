# -*- coding: utf-8 -*-
"""
@Time    : 2025/01/27
@Author  : ZhangShenao
@File    : story_generator.py
@Desc    : 故事生成模块
"""

import json
from typing import Dict
from openai import OpenAI


class StoryGenerator:
    """故事生成器类"""

    def __init__(self, api_key: str):
        """初始化DeepSeek客户端"""
        self.client = OpenAI(api_key=api_key, base_url="https://api.deepseek.com")

    def generate_story(self, user_prompt: str) -> Dict:
        """生成故事内容"""
        print("📝 正在生成故事内容...")

        system_prompt = """你是一个专业的儿童故事创作专家。请根据用户的需求，创作一个适合儿童的故事。
        总共生成4段剧情，每段剧情简单一些，剧情之间要连贯，便于制作视频。

请按照以下JSON格式返回故事内容：
{
    "character_description": "主角人物的详细描述，包括外貌特征、性格特点等",
    "story_segments": [
        "第1段剧情描述",
        "第2段剧情描述", 
        "第3段剧情描述",
        "第4段剧情描述",
    ]
}

要求：
1. 故事要寓教于乐，适合儿童观看
2. 人物描述要详细，便于AI生成图片
3. 每段剧情要连贯，便于制作视频
4. 语言要生动有趣，富有教育意义"""

        try:
            response = self.client.chat.completions.create(
                model="deepseek-chat",
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt},
                ],
                temperature=0.8,
            )

            story_content = response.choices[0].message.content
            print("✅ 故事内容生成完成")
            return json.loads(story_content)

        except Exception as e:
            print(f"❌ 故事生成失败: {e}")
            return None

    def print_story_details(self, story_data: Dict):
        """打印故事详细信息"""
        if not story_data:
            return

        print("\n" + "=" * 60)
        print("📖 故事详情")
        print("=" * 60)
        print(f"🎭 故事主角: {story_data['character_description']}")
        print(f"📚 故事分为 {len(story_data['story_segments'])} 段剧情")
        print("\n🎬 剧情分段:")
        print("-" * 60)

        for i, segment in enumerate(story_data["story_segments"], 1):
            print(f"第{i}段: {segment}")
            print("-" * 60)

        print("=" * 60)

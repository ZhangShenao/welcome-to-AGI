# -*- coding: utf-8 -*-
"""
@Time    : 2025/01/27
@Author  : ZhangShenao
@File    : story_generator.py
@Desc    : 故事生成模块
"""

import json
import re
from typing import Dict, Callable, Optional
from concurrent.futures import ThreadPoolExecutor, as_completed
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
总共生成6段剧情，每段剧情要丰富详细，剧情之间要紧密连贯，形成完整的故事线。

请按照以下JSON格式返回故事内容：
{
    "character_description": "主角人物的详细描述，包括外貌特征、性格特点等",
    "story_segments": [
        "第1段剧情描述",
        "第2段剧情描述", 
        "第3段剧情描述",
        "第4段剧情描述",
        "第5段剧情描述",
        "第6段剧情描述"
    ]
}

要求：
1. 故事要寓教于乐，适合儿童观看
2. 人物描述要详细，便于AI生成图片
3. 每段剧情要丰富详细，包含具体的情节发展、人物动作、环境变化等细节
4. 剧情之间要紧密连贯，每段剧情要自然承接上一段，为下一段做铺垫，形成完整的故事线
5. 每段剧情要有明确的场景设置、人物行为、情感变化或冲突发展
6. 语言要生动有趣，富有教育意义，能够吸引儿童的注意力
7. 请确保返回的是有效的JSON格式，不要包含任何额外的文字说明"""

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

    def generate_shot_scripts(
        self, 
        story_segments: list, 
        character_description: str,
        progress_callback: Optional[Callable] = None,
        script_callback: Optional[Callable] = None
    ) -> list:
        """为每段剧情生成详细的分镜脚本（并行生成）"""
        if progress_callback:
            progress_callback("📽️ 正在并行生成分镜脚本...")
        else:
            print("📽️ 正在并行生成分镜脚本...")

        shot_scripts = [None] * len(story_segments)
        
        def generate_single_script(index, segment):
            """生成单个分镜脚本"""
            i = index + 1
            system_prompt = """你是一个专业的视频分镜脚本创作专家。请根据给定的剧情，创作一个适合8秒视频的详细分镜脚本。

重要要求：
1. 每段剧情必须包含2~3个分镜，不要超过3个分镜。每个分镜大约2~3秒。
2. **所有分镜脚本内容必须使用英文**，包括描述、对话等所有内容。

分镜脚本应包含以下内容（全部使用英文）：
1. 剧情描述：简要描述这段剧情的内容（英文）
2. 分镜列表：将这段剧情分解为2~3个分镜，每个分镜包含（全部英文）：
   - 分镜序号（如：Shot 1, Shot 2, Shot 3）
   - 运镜方式：描述镜头的运动方式（如：close-up, medium shot, wide shot, pan, zoom等）
   - 人物动作：描述人物的具体动作和表情（英文）
   - 人物对话：如果有对话，请写出具体内容（英文）
   - 背景环境：描述场景和背景环境（英文）
   - 画面构图：描述画面的构图和视觉元素（英文）
   - 时长：每个分镜的时长（约2~3秒）

请按照以下JSON格式返回：
{
    "story_segment": "剧情描述（中文）",
    "shot_script": "详细的分镜脚本描述（必须全部使用英文），必须包含2~3个分镜，每个分镜包含运镜、动作、对话、环境、构图、时长等信息，总时长约8秒。所有描述、对话、场景描述都必须使用英文。"
}

要求：
1. 分镜脚本要详细具体，便于视频制作
2. 必须包含2~3个分镜，不要超过3个
3. 每个分镜要明确标注序号和时长
4. 运镜方式要明确，适合视频制作
5. 如果有对话，要自然生动（使用英文）
6. 环境描述要清晰，便于画面生成（使用英文）
7. 分镜之间要有逻辑连贯性，形成完整的情节
8. **shot_script字段中的所有内容必须使用英文**，包括场景描述、人物动作、对话等
9. 请确保返回的是有效的JSON格式"""

            try:
                user_prompt = f"""角色描述：{character_description}

第{i}段剧情：{segment}

请为这段剧情生成详细的分镜脚本。"""

                response = self.client.chat.completions.create(
                    model="deepseek-chat",
                    messages=[
                        {"role": "system", "content": system_prompt},
                        {"role": "user", "content": user_prompt},
                    ],
                    temperature=0.8,
                )

                script_content = response.choices[0].message.content.strip()
                
                # 尝试提取JSON内容（可能包含在markdown代码块中）
                # 移除markdown代码块标记
                if script_content.startswith('```'):
                    lines = script_content.split('\n')
                    # 移除第一行和最后一行的```标记
                    script_content = '\n'.join([line for line in lines[1:-1] if not line.strip().startswith('```')])
                
                # 尝试提取JSON对象（更健壮的正则表达式）
                json_match = re.search(r'\{.*\}', script_content, re.DOTALL)
                if json_match:
                    script_content = json_match.group(0)
                
                # 尝试解析JSON
                script_data = None
                try:
                    script_data = json.loads(script_content)
                except json.JSONDecodeError as e:
                    # 如果直接解析失败，尝试清理内容
                    script_content_clean = script_content.strip()
                    # 移除可能的注释
                    script_content_clean = re.sub(r'//.*?$', '', script_content_clean, flags=re.MULTILINE)
                    try:
                        script_data = json.loads(script_content_clean)
                    except json.JSONDecodeError:
                        # 如果还是失败，尝试手动构建JSON
                        print(f"⚠️ 第{i}段分镜脚本JSON解析失败: {e}")
                        print(f"原始内容: {script_content[:200]}...")
                        # 使用原始剧情作为备用
                        script_data = {
                            "story_segment": segment,
                            "shot_script": f"儿童教育视频，{segment}，画面温馨，适合儿童观看，8秒视频，包含运镜、对话和环境描述"
                        }
                
                if progress_callback:
                    progress_callback(f"✅ 第{i}段分镜脚本生成完成")
                else:
                    print(f"✅ 第{i}段分镜脚本生成完成")
                
                # 通知回调
                if script_callback:
                    script_callback(index, script_data.get("story_segment", segment), script_data.get("shot_script", ""))
                
                return (index, script_data)

            except Exception as e:
                error_msg = f"❌ 第{i}段分镜脚本生成失败: {e}"
                if progress_callback:
                    progress_callback(error_msg)
                else:
                    print(error_msg)
                
                # 如果生成失败，使用原始剧情作为备用
                fallback_script = {
                    "story_segment": segment,
                    "shot_script": f"儿童教育视频，{segment}，画面温馨，适合儿童观看，8秒视频，包含运镜、对话和环境描述"
                }
                
                # 通知回调
                if script_callback:
                    script_callback(index, segment, fallback_script["shot_script"])
                
                return (index, fallback_script)

        # 使用线程池并行生成
        with ThreadPoolExecutor(max_workers=min(6, len(story_segments))) as executor:
            futures = {
                executor.submit(generate_single_script, i, segment): i
                for i, segment in enumerate(story_segments)
            }

            for future in as_completed(futures):
                index = futures[future]
                try:
                    result_index, script_data = future.result()
                    shot_scripts[result_index] = script_data
                except Exception as e:
                    # 如果执行异常，使用备用方案
                    segment = story_segments[index]
                    fallback_script = {
                        "story_segment": segment,
                        "shot_script": f"儿童教育视频，{segment}，画面温馨，适合儿童观看，8秒视频，包含运镜、对话和环境描述"
                    }
                    shot_scripts[index] = fallback_script
                    if progress_callback:
                        progress_callback(f"❌ 第{index + 1}段分镜脚本生成异常: {e}")
                    # 确保异常情况下也调用回调，通知前端
                    if script_callback:
                        script_callback(index, segment, fallback_script["shot_script"])

        if progress_callback:
            completed_count = sum(1 for s in shot_scripts if s is not None)
            progress_callback(f"✅ 分镜脚本生成完成: {completed_count}/{len(story_segments)}段成功")
        else:
            print("✅ 所有分镜脚本生成完成")
        
        return shot_scripts

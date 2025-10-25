# -*- coding: utf-8 -*-
"""
@Time    : 2025/01/27
@Author  : ZhangShenao
@File    : main.py
@Desc    : 哈皮互动视频课堂 - 主程序
"""

import os
import dotenv
from story_generator import StoryGenerator
from image_generator import ImageGenerator
from video_generator import VideoGenerator

# 加载环境变量
dotenv.load_dotenv()


class InteractiveVideoEducation:
    """哈皮互动视频课堂类"""

    def __init__(self):
        """初始化各个模块"""
        # 初始化各个生成器
        self.story_generator = StoryGenerator(os.getenv("DEEPSEEK_API_KEY"))
        self.image_generator = ImageGenerator(os.getenv("GOOGLE_API_KEY"))
        self.video_generator = VideoGenerator(os.getenv("GOOGLE_API_KEY"))

    def create_complete_story_video(self, user_prompt: str) -> str:
        """创建完整的故事视频"""
        print("🚀 开始创建哈皮互动视频课堂内容...")
        print("=" * 50)

        # Step 1-2: 生成故事内容
        story_data = self.story_generator.generate_story(user_prompt)
        if not story_data:
            return None

        # 打印故事详情
        self.story_generator.print_story_details(story_data)

        # Step 3: 生成人物形象
        character_image = self.image_generator.generate_character_image(
            story_data["character_description"]
        )
        if not character_image:
            return None

        # Step 4: 生成第一段视频
        current_video = self.video_generator.generate_first_video_segment(
            character_image, story_data["story_segments"][0]
        )
        if not current_video:
            return None

        # Step 5: 扩展后续视频段
        segments_count = len(story_data["story_segments"])
        for i, segment in enumerate(story_data["story_segments"][1:], 2):
            current_video = self.video_generator.extend_video(current_video, segment, i)
            if not current_video:
                return None

        # 返回最后一段视频的文件路径
        final_video_path = f"story_part{segments_count}.mp4"
        print("=" * 50)
        print("🎉 完整故事视频创建成功！")
        print(f"📁 最终视频文件: {final_video_path}")
        return final_video_path

    def create_complete_story_video_with_logging(
        self, user_prompt: str, log_callback=None
    ) -> str:
        """创建完整的故事视频（支持日志回调）"""

        def log(message):
            if log_callback:
                log_callback(message)
            else:
                print(message)

        log("🚀 开始创建哈皮互动视频课堂内容...")
        log("=" * 50)

        # Step 1-2: 生成故事内容
        log("📝 正在生成故事内容...")
        story_data = self.story_generator.generate_story(user_prompt)
        if not story_data:
            log("❌ 故事生成失败")
            return None
        log("✅ 故事内容生成完成")

        # 打印故事详情
        log("\n" + "=" * 60)
        log("📖 故事详情")
        log("=" * 60)
        log(f"🎭 故事主角: {story_data['character_description']}")
        log(f"📚 故事分为 {len(story_data['story_segments'])} 段剧情")
        log("\n🎬 剧情分段:")
        log("-" * 60)
        for i, segment in enumerate(story_data["story_segments"], 1):
            log(f"第{i}段: {segment}")
            log("-" * 60)
        log("=" * 60)

        # Step 3: 生成人物形象
        log("🎨 正在生成人物形象图片...")
        character_image = self.image_generator.generate_character_image(
            story_data["character_description"]
        )
        if not character_image:
            log("❌ 人物形象生成失败")
            return None
        log(f"✅ 人物形象图片生成完成: {character_image}")

        # Step 4: 生成第一段视频
        log("🎬 正在生成第一段视频...")
        log(f"📝 剧情内容: {story_data['story_segments'][0]}")
        current_video = self.video_generator.generate_first_video_segment(
            character_image, story_data["story_segments"][0]
        )
        if not current_video:
            log("❌ 第一段视频生成失败")
            return None
        log(f"✅ 第一段视频生成完成")

        # Step 5: 扩展后续视频段
        segments_count = len(story_data["story_segments"])
        for i, segment in enumerate(story_data["story_segments"][1:], 2):
            log(f"🎬 正在生成第{i}段视频...")
            log(f"📝 剧情内容: {segment}")
            current_video = self.video_generator.extend_video(current_video, segment, i)
            if not current_video:
                log(f"❌ 第{i}段视频生成失败")
                return None
            log(f"✅ 第{i}段视频生成完成")

        # 返回最后一段视频的文件路径
        final_video_path = f"story_part{segments_count}.mp4"
        log("=" * 50)
        log("🎉 完整故事视频创建成功！")
        log(f"📁 最终视频文件: {final_video_path}")
        return final_video_path

    def run(self):
        """运行主程序"""
        print("🐱 欢迎使用哈皮互动视频课堂！")
        print("💡 请输入您想要的故事主题，我们将为您生成寓教于乐的视频内容")
        print("=" * 50)

        while True:
            try:
                user_input = input(
                    "\n📝 请输入您的故事需求 (输入 'quit' 退出): "
                ).strip()

                if user_input.lower() == "quit":
                    print("👋 感谢使用，再见！")
                    break

                if not user_input:
                    print("⚠️ 请输入有效的故事需求")
                    continue

                # 创建完整视频
                final_video = self.create_complete_story_video(user_input)

                if final_video:
                    print(f"\n🎊 视频制作完成！文件保存在: {final_video}")
                else:
                    print("\n😞 视频制作失败，请重试")

            except KeyboardInterrupt:
                print("\n👋 程序已退出")
                break
            except Exception as e:
                print(f"\n❌ 发生错误: {e}")


if __name__ == "__main__":
    # 检查环境变量
    required_env_vars = ["DEEPSEEK_API_KEY", "GOOGLE_API_KEY"]
    missing_vars = [var for var in required_env_vars if not os.getenv(var)]

    if missing_vars:
        print(f"❌ 缺少必要的环境变量: {', '.join(missing_vars)}")
        print("请在 .env 文件中设置这些变量")
        exit(1)

    # 运行程序
    app = InteractiveVideoEducation()
    app.run()

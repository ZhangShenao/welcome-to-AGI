# 哈皮互动视频课堂

一个基于AI的哈皮互动视频课堂，面向儿童家长，可以根据简单指令生成寓教于乐的视频内容。

## 功能特点

- 🎭 **智能故事生成**: 使用DeepSeek模型根据家长指令生成完整故事
- 🎨 **人物形象生成**: 使用Imagen模型生成故事主角的卡通形象
- 🎬 **视频制作**: 使用Veo模型生成和扩展视频内容
- 📚 **寓教于乐**: 专门为儿童设计的教育内容
- 🏗️ **模块化设计**: 代码结构清晰，易于维护和扩展
- 📖 **详细剧情展示**: 实时显示每段剧情的具体内容
- 🖥️ **图形界面**: 友好的GUI界面，操作简单直观
- 📊 **实时进度**: 可视化进度条和详细日志显示
- 🎬 **一键播放**: 生成完成后可直接播放视频

## 工作流程

1. **接收指令**: 家长输入简单的故事需求
2. **故事生成**: DeepSeek生成人物介绍和5段剧情
3. **形象生成**: Imagen生成人物卡通形象
4. **视频制作**: Veo生成第一段视频
5. **视频扩展**: 依次扩展后续4段剧情视频
6. **输出结果**: 返回完整的故事视频

## 安装依赖

```bash
pip install -r requirements.txt
```

## 环境配置

1. 复制环境变量模板：
```bash
cp .env.example .env
```

2. 在 `.env` 文件中配置API密钥：
```
DEEPSEEK_API_KEY=your_deepseek_api_key_here
GOOGLE_API_KEY=your_google_api_key_here
```

## 使用方法

### 🌐 Web界面（推荐）

**启动Web服务：**

**macOS/Linux用户：**
```bash
./start_web.sh
```

**Windows用户：**
```bash
start_web.bat
```

**或直接运行：**
```bash
python app.py
```

然后在浏览器中访问：http://localhost:5000

### 💻 命令行界面

```bash
python main.py
```

### 📝 故事需求示例

- "讲一个小蝌蚪找妈妈的故事，歌颂母爱的伟大"
- "创作一个关于友谊的童话故事"
- "制作一个教孩子认识颜色的动画故事"
- "讲一个小马过河的故事，鼓励孩子勇于尝试"

## 项目结构

```
多模态/互动视频教育产品/
├── app.py               # Flask Web后端服务
├── main.py              # 主程序文件（命令行版本）
├── story_generator.py   # 故事生成模块
├── image_generator.py   # 图片生成模块
├── video_generator.py   # 视频生成模块
├── templates/           # HTML模板文件夹
│   └── index.html       # 前端页面
├── requirements.txt     # 依赖包列表
└── README.md           # 使用说明
```

## 输出文件

程序会在当前目录下生成以下文件：
- `character.png`: 故事主角的卡通形象
- `story_part1.mp4`: 第一段剧情视频
- `story_part2.mp4`: 第二段剧情视频
- ...
- `story_part5.mp4`: 最终完整视频

## 技术栈

- **Python 3.8+**
- **DeepSeek API**: 故事内容生成
- **Google Imagen**: 人物形象生成  
- **Google Veo**: 视频生成和扩展
- **OpenAI Python SDK**: DeepSeek API调用
- **Google GenAI SDK**: Google AI服务调用

## 注意事项

1. 确保网络连接稳定，视频生成需要较长时间
2. 生成的视频文件较大，请确保有足够的存储空间
3. API调用可能产生费用，请合理使用

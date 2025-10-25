# -*- coding: utf-8 -*-
"""
@Time    : 2025/01/27
@Author  : ZhangShenao
@File    : app.py
@Desc    : 哈皮互动视频课堂 - Flask后端API服务
"""

import os
import json
import dotenv
from flask import Flask, render_template, request, jsonify, send_file, Response
from flask_cors import CORS
from main import InteractiveVideoEducation

# 加载环境变量
dotenv.load_dotenv()

app = Flask(__name__)
CORS(app)

# 初始化教育产品实例
education_app = InteractiveVideoEducation()


@app.route("/")
def index():
    """渲染首页"""
    return render_template("index.html")


@app.route("/api/generate", methods=["POST"])
def generate_video():
    """生成视频API（流式返回日志）"""
    # 在路由函数中获取请求数据（有请求上下文）
    data = request.json
    user_prompt = data.get("prompt", "") if data else ""

    def generate():
        try:

            if not user_prompt:
                error_data = {"type": "error", "error": "请输入故事需求"}
                yield f"data: {json.dumps(error_data, ensure_ascii=False)}\n\n"
                return

            # 用于存储最终的视频路径
            video_path_result = [None]
            error_result = [None]

            # 使用线程来执行视频生成，以便实时发送日志
            import threading
            import queue

            log_queue = queue.Queue()

            def video_generation_thread():
                # 在线程中创建应用上下文
                with app.app_context():

                    def log_callback_internal(message):
                        log_queue.put(("log", message))

                    try:
                        video_path = (
                            education_app.create_complete_story_video_with_logging(
                                user_prompt, log_callback=log_callback_internal
                            )
                        )
                        video_path_result[0] = video_path
                        log_queue.put(("done", None))
                    except Exception as e:
                        error_result[0] = str(e)
                        log_queue.put(("error", str(e)))

            # 启动视频生成线程
            thread = threading.Thread(target=video_generation_thread)
            thread.daemon = True
            thread.start()

            # 实时发送日志
            while True:
                try:
                    msg_type, message = log_queue.get(timeout=0.1)

                    if msg_type == "log":
                        data = {"type": "log", "message": message}
                        yield f"data: {json.dumps(data, ensure_ascii=False)}\n\n"
                    elif msg_type == "done":
                        # 视频生成完成，发送结果
                        if video_path_result[0]:
                            result = {
                                "type": "success",
                                "video_path": video_path_result[0],
                            }
                            yield f"data: {json.dumps(result, ensure_ascii=False)}\n\n"
                        else:
                            result = {"type": "error", "error": "视频生成失败"}
                            yield f"data: {json.dumps(result, ensure_ascii=False)}\n\n"
                        break
                    elif msg_type == "error":
                        result = {"type": "error", "error": message}
                        yield f"data: {json.dumps(result, ensure_ascii=False)}\n\n"
                        break
                except queue.Empty:
                    # 检查线程是否还在运行
                    if not thread.is_alive() and log_queue.empty():
                        # 线程结束了但没有收到done消息，可能出错了
                        if video_path_result[0]:
                            result = {
                                "type": "success",
                                "video_path": video_path_result[0],
                            }
                            yield f"data: {json.dumps(result, ensure_ascii=False)}\n\n"
                        else:
                            error_msg = error_result[0] or "未知错误"
                            result = {"type": "error", "error": error_msg}
                            yield f"data: {json.dumps(result, ensure_ascii=False)}\n\n"
                        break
                    continue

        except Exception as e:
            result = {"type": "error", "error": str(e)}
            yield f"data: {json.dumps(result, ensure_ascii=False)}\n\n"

    return Response(generate(), mimetype="text/event-stream")


@app.route("/api/video/<path:filename>")
def serve_video(filename):
    """提供视频文件服务"""
    try:
        return send_file(filename, mimetype="video/mp4")
    except Exception as e:
        return jsonify({"error": str(e)}), 404


if __name__ == "__main__":
    # 检查环境变量
    required_env_vars = ["DEEPSEEK_API_KEY", "GOOGLE_API_KEY"]
    missing_vars = [var for var in required_env_vars if not os.getenv(var)]

    if missing_vars:
        print(f"❌ 缺少必要的环境变量: {', '.join(missing_vars)}")
        print("请在 .env 文件中设置这些变量")
        exit(1)

    app.run(debug=True, host="0.0.0.0", port=5000)

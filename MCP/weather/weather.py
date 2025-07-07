from typing import Any
import httpx
from mcp.server.fastmcp import FastMCP

# 1. 初始化 FastMCP 服务器
# 创建一个名为 "weather" 的服务器实例。这个名字有助于识别这套工具。
mcp = FastMCP("weather")

# --- 常量定义 ---
# 美国国家气象局 (NWS) API 的基础 URL
NWS_API_BASE = "https://api.weather.gov"
# 设置请求头中的 User-Agent，很多公共 API 要求提供此信息以识别客户端
USER_AGENT = "weather-app/1.0"


# --- 辅助函数 ---


async def make_nws_request(url: str) -> dict[str, Any] | None:
    """
    一个通用的异步函数，用于向 NWS API 发起请求并处理常见的错误。

    Args:
        url (str): 要请求的完整 URL。

    Returns:
        dict[str, Any] | None: 成功时返回解析后的 JSON 字典，失败时返回 None。
    """
    headers = {
        "User-Agent": USER_AGENT,
        "Accept": "application/geo+json",  # NWS API 推荐的 Accept 头
    }
    # 使用 httpx.AsyncClient 来执行异步 HTTP GET 请求
    async with httpx.AsyncClient() as client:
        try:
            # 发起请求，设置了30秒的超时
            response = await client.get(url, headers=headers, timeout=30.0)
            # 如果响应状态码是 4xx 或 5xx（表示客户端或服务器错误），则会引发一个异常
            response.raise_for_status()
            # 如果请求成功，返回 JSON 格式的响应体
            return response.json()
        except Exception:
            # 捕获所有可能的异常（如网络问题、超时、HTTP错误等），并返回 None
            return None


def format_alert(feature: dict) -> str:
    """将单个天气预警的 JSON 数据格式化为人类可读的字符串。"""
    props = feature["properties"]
    # 使用 .get() 方法安全地访问字典键，如果键不存在则返回默认值，避免程序出错
    return f"""
事件: {props.get('event', '未知')}
区域: {props.get('areaDesc', '未知')}
严重性: {props.get('severity', '未知')}
描述: {props.get('description', '无描述信息')}
指令: {props.get('instruction', '无具体指令')}
"""


# --- MCP 工具定义 ---


@mcp.tool()
async def get_alerts(state: str) -> str:
    """
    获取美国某个州当前生效的天气预警信息。
    这个函数被 @mcp.tool() 装饰器标记，意味着它可以被大模型作为工具来调用。

    参数:
        state: 两个字母的美国州代码 (例如: CA, NY)。
    """
    # 构造请求特定州天气预警的 URL
    url = f"{NWS_API_BASE}/alerts/active/area/{state}"
    data = await make_nws_request(url)

    # 健壮性检查：如果请求失败或返回的数据格式不正确
    if not data or "features" not in data:
        return "无法获取预警信息或未找到相关数据。"

    # 如果 features 列表为空，说明该州当前没有生效的预警
    if not data["features"]:
        return "该州当前没有生效的天气预警。"

    # 使用列表推导和 format_alert 函数来格式化所有预警信息
    alerts = [format_alert(feature) for feature in data["features"]]
    # 将所有预警信息用分隔线连接成一个字符串并返回
    return "\n---\n".join(alerts)


@mcp.tool()
async def get_forecast(latitude: float, longitude: float) -> str:
    """
    根据给定的经纬度获取天气预报。
    同样，这个函数也是一个可被调用的 MCP 工具。

    参数:
        latitude: 地点的纬度
        longitude: 地点的经度
    """
    # NWS API 获取预报需要两步
    # 第一步：根据经纬度获取一个包含具体预报接口 URL 的网格点信息
    points_url = f"{NWS_API_BASE}/points/{latitude},{longitude}"
    points_data = await make_nws_request(points_url)

    if not points_data:
        return "无法获取该地点的预报数据。"

    # 第二步：从上一步的响应中提取实际的天气预报接口 URL
    forecast_url = points_data["properties"]["forecast"]
    # 第三步：请求详细的天气预报数据
    forecast_data = await make_nws_request(forecast_url)

    if not forecast_data:
        return "无法获取详细的预报信息。"

    # 提取预报周期数据
    periods = forecast_data["properties"]["periods"]
    forecasts = []
    # 遍历接下来的5个预报周期（例如：今天下午、今晚、明天...）
    for period in periods[:5]:
        forecast = f"""
{period['name']}:
温度: {period['temperature']}°{period['temperatureUnit']}
风力: {period['windSpeed']} {period['windDirection']}
预报: {period['detailedForecast']}
"""
        forecasts.append(forecast)

    # 将格式化后的预报信息连接成一个字符串并返回
    return "\n---\n".join(forecasts)


# --- 服务器启动 ---

# 这是一个标准的 Python 入口点检查
# 确保只有当这个文件被直接运行时，以下代码才会被执行
if __name__ == "__main__":
    # 初始化并运行 MCP 服务器
    # transport='stdio' 表示服务器将通过标准输入/输出(stdin/stdout)与客户端（如大模型）进行通信。
    # 这是与本地模型或调试工具交互的常见方式。
    mcp.run(transport="stdio")

# -*- coding: utf-8 -*-
"""
@Time    : 2025/6/20 11:05 
@Author  : ZhangShenao 
@File    : fetch_stock_data.py
@Desc    : 通过AKShare API,获取股票数据

安装AKShare依赖:
pip install akshare --upgrade
"""

import asyncio
from typing import List

import akshare as ak
import pandas as pd
from pandas import DataFrame


def get_all_stock_codes() -> list:
    """
    获取所有股票代码
    :return: 股票代码列表
    """
    df = ak.stock_zh_a_spot_em()
    codes = df["代码"]

    # 只取“60”、“30”、“00”、“68”开头的股票代码,排除掉北交所上市的股票
    selected = df["代码"].str.startswith(("60", "30", "00", "68"))
    return codes[selected].to_list()


async def save_stock_data(codes: List[str], start_date: str, end_date: str, seq: int) -> None:
    """
    异步方法: 在本地保存股票行情数据
    :param codes: 股票代码列表
    :param start_date: 起始日期
    :param end_date: 截至日期
    :param seq: 文件序号
    """

    # 创建DataFrame列表,用于保存所有股票数据
    stock_data = pd.DataFrame()

    # 使用asyncio框架,批量创建异步任务
    tasks = []
    for code in codes:
        task = asyncio.create_task(fetch_stock_data(code, start_date, end_date))
        tasks.append(task)

    # 异步执行任务,并等待所有任务完成
    task_results = await asyncio.gather(*tasks)

    # 遍历任务执行结果,最终合并成一张表格
    for r in task_results:
        stock_data = pd.concat([stock_data, r], axis=0)

    # 将DataFrame数据转换成CSV格式,并保存到本地
    filename = f"{start_date}_{end_date}_{seq}.csv"
    stock_data.to_csv(f"./{filename}")
    print(f"股票数据抓取完成, 已保存至: {filename}, 总数: {len(codes)}")


async def fetch_stock_data(symbol, start_date, end_date) -> DataFrame:
    """
    异步方法: 抓取指定股票代码的行情数据
    :param symbol: 股票代码
    :param start_date: 起始日期
    :param end_date: 截至日期
    :return: 股票数据
    """
    # 由于 akshare 的 API 是同步的，我们需要在线程池中运行它
    loop = asyncio.get_event_loop()
    df = await loop.run_in_executor(None, lambda: ak.stock_zh_a_hist(
        symbol=symbol,
        period="daily",
        start_date=start_date,
        end_date=end_date,
        adjust="qfq"
    ))

    try:
        df["日期"] = pd.to_datetime(df["日期"])  # 将日期转换为DateTime类型
        df.set_index("日期", inplace=True)  # 将日期设置为索引
        df.sort_index(ascending=False, inplace=True)  # 按照日期降序排序,并在原始数据上进行操作

        print(f"股票数据抓取完成。代码: {symbol}")
    except Exception as e:
        print(f"股票数据抓取失败。代码: {symbol}, 错误信息: {e}")
    # 返回DateFrame格式的股票数据
    return df


def save_all_stock_data() -> None:
    """
    在本地保存所有股票数据
    """
    
    codes = get_all_stock_codes()
    total = len(codes)
    print(f"开始分批抓取股票数据, 共: {total} 只股票")

    # 分批抓取股票数据
    n = 50
    for i in range(0, len(codes), n):
        batch_codes = codes[i:i + n]
        if len(batch_codes) > 0:
            asyncio.run(save_stock_data(codes=batch_codes, start_date="20250621", end_date="20250625", seq=i + 1))


if __name__ == "__main__":
    # asyncio.run(download_stock_data(["300750", "600519"], "20250621", "20250625"))

    save_all_stock_data()

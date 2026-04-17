import akshare as ak
import pandas as pd
import time


# 获取热点板块（资金流）
def get_hot_sectors():
    for i in range(3):  # 重试3次
        try:
            df = ak.stock_sector_fund_flow_rank(indicator="今日")

            if df is None or df.empty:
                print("⚠️ 板块数据为空")
                continue

            # 👉 打印列名（第一次运行可以看一下结构）
            print("字段:", df.columns.tolist())

            return df

        except Exception as e:
            print(f"重试中... {i+1}")
            time.sleep(2)

    return None


# 主策略
def run_strategy():
    print("\n===== 今日选股 =====")

    sectors = get_hot_sectors()

    if sectors is None or sectors.empty:
        print("❌ 获取板块失败")
        return

    # 👉 按资金流排序（从大到小）
    try:
        sectors = sectors.sort_values(by="今日主力净流入-净额", ascending=False)
    except:
        print("⚠️ 排序字段不存在，使用默认顺序")

    # 👉 只取前5个热点板块
    top_sectors = sectors.head(5)

    for _, row in top_sectors.iterrows():

        # 👉 自动识别“板块名称”
        name = None
        for col in row.index:
            if "名称" in col:
                name = row[col]
                break

        if name is None:
            name = row.iloc[0]

        print(f"\n🔥 热点板块: {name}")

        # 👉 获取板块个股（可能失败）
        try:
            stocks = ak.stock_board_concept_cons_em(symbol=name)

            if stocks is None or stocks.empty:
                print("  ⚠️ 无个股数据")
                continue

            # 👉 简单选3只涨幅靠前的
            stocks = stocks.sort_values(by="涨跌幅", ascending=False)

            for i in range(min(3, len(stocks))):
                s = stocks.iloc[i]
                print(f"   {s['名称']}  涨幅: {s['涨跌幅']}%")

        except Exception as e:
            print("  ❌ 获取个股失败")


# 运行
if __name__ == "__main__":
    run_strategy()

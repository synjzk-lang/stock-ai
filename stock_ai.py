import os
os.environ["TQDM_DISABLE"] = "1"
import akshare as ak
import time
import os

# 关闭进度条
os.environ["TQDM_DISABLE"] = "1"


def get_hot_sectors():
    for i in range(3):
        try:
            df = ak.stock_sector_fund_flow_rank(indicator="今日")
            if df is not None and not df.empty:
                return df
        except:
            print(f"重试中... {i+1}")
            time.sleep(2)
    return None


def run_strategy():
    print("\n===== 今日选股 =====")

    sectors = get_hot_sectors()

    if sectors is None or sectors.empty:
        print("❌ 获取板块失败")
        return

    # 排序
    try:
        sectors = sectors.sort_values(by="今日主力净流入-净额", ascending=False)
    except:
        pass

    top_sectors = sectors.head(5)

    for _, row in top_sectors.iterrows():

        # 获取板块名称
        name = None
        for col in row.index:
            if "名称" in col:
                name = row[col]
                break

        if name is None:
            name = row.iloc[0]

        print(f"\n🔥 热点板块: {name}")

        stocks = None

        # ✅ 概念板块尝试
        try:
            stocks = ak.stock_board_concept_cons_em(symbol=name)
        except:
            pass

        # ✅ 行业板块尝试
        if stocks is None or stocks.empty:
            try:
                stocks = ak.stock_board_industry_cons_em(symbol=name)
            except:
                pass

        # ✅ 最终判断
        if stocks is None or stocks.empty:
            print("  ⚠️ 无个股数据")
            continue

        # 排序
        try:
            stocks = stocks.sort_values(by="涨跌幅", ascending=False)
        except:
            pass

        # 输出前3个
        for i in range(min(3, len(stocks))):
            s = stocks.iloc[i]
            print(f"   {s['名称']}  涨幅: {s['涨跌幅']}%")


if __name__ == "__main__":
    run_strategy()

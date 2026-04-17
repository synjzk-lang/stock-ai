import akshare as ak
import time
import os

# 关闭进度条（不一定完全生效，但不影响）
os.environ["TQDM_DISABLE"] = "1"


# ===== 获取热点板块（带备用方案）=====
def get_hot_sectors():
    for i in range(3):
        try:
            df = ak.stock_sector_fund_flow_rank(indicator="今日")

            if df is not None and not df.empty:
                return df

        except:
            print(f"重试中... {i+1}")
            time.sleep(2)

    # ❗ 主接口失败 → 启用备用
    print("⚠️ 使用备用板块数据")

    try:
        df = ak.stock_board_concept_name_em()
        return df.head(5)
    except:
        return None


# ===== 主策略 =====
def run_strategy():
    print("\n===== 今日选股 =====")

    sectors = get_hot_sectors()

    if sectors is None or sectors.empty:
        print("⚠️ 今日无数据，跳过")
        return

    # 尝试按资金排序（如果有这个字段）
    try:
        sectors = sectors.sort_values(by="今日主力净流入-净额", ascending=False)
    except:
        pass

    top_sectors = sectors.head(5)

    for _, row in top_sectors.iterrows():

        # 自动识别板块名称
        name = None
        for col in row.index:
            if "名称" in col:
                name = row[col]
                break

        if name is None:
            name = row.iloc[0]

        print(f"\n🔥 热点板块: {name}")

        stocks = None

        # ===== 尝试获取概念板块 =====
        try:
            stocks = ak.stock_board_concept_cons_em(symbol=name)
        except:
            pass

        # ===== 尝试获取行业板块 =====
        if stocks is None or stocks.empty:
            try:
                stocks = ak.stock_board_industry_cons_em(symbol=name)
            except:
                pass

        # ===== 最终判断 =====
        if stocks is None or stocks.empty:
            print("  ⚠️ 无个股数据")
            continue

        # ===== 过滤涨停（更实用）=====
        try:
            stocks = stocks[stocks["涨跌幅"] < 9.8]
        except:
            pass

        # ===== 排序（资金+涨幅优先）=====
        try:
            stocks = stocks.sort_values(by=["成交额", "涨跌幅"], ascending=False)
        except:
            try:
                stocks = stocks.sort_values(by="涨跌幅", ascending=False)
            except:
                pass

        # ===== 输出前3只 =====
        count = 0
        for _, s in stocks.iterrows():
            try:
                print(f"   {s['名称']} | 涨幅:{s['涨跌幅']}%")
                count += 1
                if count >= 3:
                    break
            except:
                continue


# ===== 运行 =====
if __name__ == "__main__":
    run_strategy()

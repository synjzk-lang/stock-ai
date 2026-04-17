import akshare as ak
import pandas as pd
from datetime import datetime

import requests
import pandas as pd

def get_hot_sectors():
    url = "https://push2.eastmoney.com/api/qt/clist/get"

    params = {
        "pn": "1",
        "pz": "50",
        "po": "1",
        "np": "1",
        "ut": "b2884a393a59ad64002292a3e90d46a5",
        "fltt": "2",
        "invt": "2",
        "fid0": "f62",
        "fs": "m:90 t:2",
        "stat": "1",
        "fields": "f12,f14,f2,f3,f62"
    }

    headers = {
        "User-Agent": "Mozilla/5.0"
    }

    for i in range(3):
        try:
            r = requests.get(url, params=params, headers=headers, timeout=10)
            data = r.json()
            df = pd.DataFrame(data["data"]["diff"])
            df.columns = ["代码","名称","最新价","涨跌幅","主力净流入"]
            return df.head(5)
        except Exception as e:
            print("重试中...", i+1)

    return None

def run_strategy():
    print("\n===== 今日选股 =====")

    sectors = get_hot_sectors()

    # ⭐ 防止None崩溃
    if sectors is None or sectors.empty:
        print("❌ 获取数据失败，请检查网络")
        return

    for _, row in sectors.iterrows():
        print(f"\n🔥 热点板块: {row['名称']}")
        
        try:
            stocks = ak.stock_board_industry_cons_em(symbol=row['名称'])
            stocks = stocks.sort_values(by="涨跌幅", ascending=False)

            top3 = stocks.head(3)

            for _, stock in top3.iterrows():
                print(f"  股票: {stock['名称']}  涨幅: {stock['涨跌幅']}%")

        except:
            print("  获取失败")

if __name__ == "__main__":
    run_strategy()
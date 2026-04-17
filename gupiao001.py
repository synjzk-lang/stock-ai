import akshare as ak
import pandas as pd
from datetime import datetime

def get_hot_sectors():
    # 获取板块资金流
    df = ak.stock_sector_fund_flow_rank(indicator="今日")
    
    # 取资金流入前10板块
    df = df.sort_values(by="今日主力净流入-净额", ascending=False)
    hot_sectors = df.head(10)
    
    return hot_sectors[['名称', '今日主力净流入-净额']]


def get_sector_stocks(sector_name):
    # 获取板块成分股
    try:
        stocks = ak.stock_board_industry_cons_em(symbol=sector_name)
        return stocks
    except:
        return pd.DataFrame()


def find_leaders(stocks_df):
    if stocks_df.empty:
        return pd.DataFrame()

    # 条件筛选
    result = stocks_df[
        (stocks_df['涨跌幅'] > 5) & 
        (stocks_df['成交量'] > stocks_df['成交量'].mean())
    ]

    # 按涨幅排序
    result = result.sort_values(by='涨跌幅', ascending=False)

    return result.head(3)


def run_strategy():
    print(f"\n===== {datetime.now()} 选股结果 =====")
    
    sectors = get_hot_sectors()
    
    final_results = []

    for _, row in sectors.iterrows():
        sector_name = row['名称']
        
        stocks = get_sector_stocks(sector_name)
        leaders = find_leaders(stocks)

        if not leaders.empty:
            for _, stock in leaders.iterrows():
                final_results.append({
                    "板块": sector_name,
                    "股票": stock['名称'],
                    "涨幅": stock['涨跌幅']
                })

    df = pd.DataFrame(final_results)
    
    print(df)
    return df


if __name__ == "__main__":
    run_strategy()
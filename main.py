import tushare as ts
import pandas as pd
import time
import tqdm

from Share import Share

my_token = "83a0e2644bf378843fb9c365bd504cbf445854193cd07271be4f8058"
ts.set_token(my_token)
pro = ts.pro_api(my_token)

gongHang = Share()
# gongHang.show_market_condition()

# download_and_update_code_data(code="601398.SH")

def test(code="601398.SH"):
    """
    前复权 	当日收盘价 × 当日复权因子 / 最新复权因子
    后复权 	当日收盘价 × 当日复权因子
    :param code:
    :return:
    """

    # df = pro.daily(ts_code=code, start_date='20240524', end_date='20240524')

    dt = "20240523"
    # dt = "20241103"

    # df = ts.pro_bar(ts_code=code, adj='qfq', start_date=dt, end_date="20241101")
    # print((df[df["trade_date"]==dt].iloc(0)).to_dict())
    # exit()

    # 5.18 5.20 5.13 5.13
    # {'ts_code': '601398.SH', 'trade_date': '20240524', 'open': 5.49, 'high': 5.51, 'low': 5.44, 'close': 5.44,
    # 'pre_close': nan, 'change': nan, 'pct_chg': nan, 'vol': 2261860.85, 'amount': 1238699.584}

    # {'ts_code': '601398.SH', 'trade_date': '20241101', 'open': 6.04, 'high': 6.15, 'low': 6.03, 'close': 6.15,
    # 'pre_close': nan, 'change': nan, 'pct_chg': nan, 'vol': 4512379.25, 'amount': 2760339.812}
    df = ts.pro_bar(ts_code=code, start_date=dt, end_date="20240524", adjfactor=True)
    print(df.loc[0].to_dict())

    # {'ts_code': '601398.SH', 'trade_date': '20240524', 'adj_factor': 2.236}
    #{'ts_code': '601398.SH', 'trade_date': '20241101', 'adj_factor': 2.3537}
    df = pro.adj_factor(ts_code=code, trade_date=dt)
    print(df.loc[0].to_dict())

    #0.3035

# test()
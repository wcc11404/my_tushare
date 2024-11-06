import tushare as ts
import time
import pandas as pd
import time
import datetime
import pickle
import os
import tqdm

my_token = "83a0e2644bf378843fb9c365bd504cbf445854193cd07271be4f8058"
ts.set_token(my_token)
pro = ts.pro_api(my_token)

def generate_date_list(start_date, end_date, wo_weekend=True):
    date_list = []
    start_date = datetime.datetime.strptime(start_date, "%Y%m%d")
    end_date = datetime.datetime.strptime(end_date, "%Y%m%d")
    while start_date <= end_date:
        if wo_weekend == False or start_date.weekday() < 5:
            date_list.append(start_date.strftime("%Y%m%d"))
        start_date += datetime.timedelta(days=1)
    return date_list

def download_and_update_code_data(code="601398.SH"):
    yesterday = datetime.datetime.now() - datetime.timedelta(days=1)
    yesterday_date = yesterday.strftime("%Y%m%d")

    # 加载之前下载过的数据
    code_data = {
        "行情": {},
    }
    save_file_name = "code_data/{}.pkl".format(code.replace(".", "_"))
    if not os.path.exists(save_file_name):
        pass
    else:
        with open(save_file_name, 'rb') as file:
            code_data = pickle.load(file)

    for date in tqdm.tqdm(generate_date_list("20230101", yesterday_date, wo_weekend=True)):
        if date in code_data["行情"]:
            continue
        df = pro.daily(ts_code=code, start_date=date, end_date=date)
        if df.empty == True:
            continue
        temp_dict = df.loc[0].to_dict()
        # https://tushare.pro/document/2?doc_id=27
        code_data["行情"][date] = {
            "开盘价": temp_dict["open"],
            "最高价": temp_dict["high"],
            "最低价": temp_dict["low"],
            "收盘价": temp_dict["close"],
            "昨收价": temp_dict["pre_close"],
            "涨跌额": temp_dict["change"],
            "涨跌幅": temp_dict["pct_chg"],
            "成交量": temp_dict["vol"],
            "成交额": temp_dict["amount"],
        }

    # 写入文件
    with open(save_file_name, 'wb') as file:
        pickle.dump(code_data, file)

download_and_update_code_data(code="601398.SH")

def main(code="601398.SH"):
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

# main()
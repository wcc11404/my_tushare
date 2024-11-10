import datetime
import pickle
import os

import utils.file_util as file_util

today_date = datetime.datetime.now().strftime("%Y%m%d")
yesterday = datetime.datetime.now() - datetime.timedelta(days=1)
yesterday_date = yesterday.strftime("%Y%m%d")

def generate_date_list(start_date, end_date, wo_weekend=True, illegal_date_list=[]):
    """
    生成start 到 end 左开右闭的时间序列列表
    :param start_date: 起始
    :param end_date:   结束
    :param wo_weekend: 是否去除周末
    :param illegal_date_list:  不需要生成的时间列表集合
    :return:
    """
    date_list = []
    start_date = datetime.datetime.strptime(start_date, "%Y%m%d")
    end_date = datetime.datetime.strptime(end_date, "%Y%m%d")
    while start_date < end_date:
        if (wo_weekend == False or start_date.weekday() < 5) and start_date not in illegal_date_list:
            date_list.append(start_date.strftime("%Y%m%d"))
        start_date += datetime.timedelta(days=1)
    return date_list

def update_open_market_date_list():
    open_market_list = []
    with open(os.path.join(file_util.project_dir, file_util.code_data_dir, "601288_SH.pkl"), 'rb') as file:
        code_data = pickle.load(file)
        for date, value in code_data["行情"].items():
            if len(value) == 0:
                continue
            open_market_list.append(date)
    with open(os.path.join(file_util.project_dir, file_util.code_data_dir, "open_market_date.pkl"), 'wb') as file:
        pickle.dump(open_market_list, file)

def generate_open_market_date_list(start_date, end_date):
    with open(os.path.join(file_util.project_dir, file_util.code_data_dir, "open_market_date.pkl"), 'rb') as file:
        open_market_list = pickle.load(file)

    date_list = []
    for date in generate_date_list(start_date, end_date):
        if date not in open_market_list:
            continue
        date_list.append(date)
    return date_list

if __name__ == "__main__":
    update_open_market_date_list()
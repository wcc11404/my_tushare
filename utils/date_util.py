import datetime
import pickle
import os

import utils.file_util as file_util

today = datetime.datetime.now()
yesterday = today - datetime.timedelta(days=1)

today_date = today.strftime("%Y%m%d")
yesterday_date = yesterday.strftime("%Y%m%d")

def generate_date_list(start_date, end_date, wo_weekend=True, illegal_date_list=[]):
    """
    生成start 到 end 左开右闭的日期序列列表
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

def get_next_date(date):
    """
    生成指定日期的下一个日期
    :param date:
    :return:
    """
    temp = datetime.datetime.strptime(date, "%Y%m%d")
    temp += datetime.timedelta(days=1)
    return temp.strftime("%Y%m%d")

def get_last_open_date(date):
    """
    生成指定日期的上一个开市日期
    todo 合法性检测
    :param date:
    :return:
    """
    with open(os.path.join(file_util.project_dir, file_util.code_data_dir, "open_market_date.pkl"), 'rb') as file:
        open_market_list = pickle.load(file)
    temp = datetime.datetime.strptime(date, "%Y%m%d")
    temp -= datetime.timedelta(days=1)
    while temp.strftime("%Y%m%d") not in open_market_list:
        temp -= datetime.timedelta(days=1)
    return temp.strftime("%Y%m%d")

def generate_open_market_date_list(start_date, end_date):
    """
    生成start 到 end 左开右闭的开市日期序列列表
    :param start_date: 起始
    :param end_date:   结束
    :return:
    """
    # 先生成一遍
    update_open_market_date_list()
    # 加载本地缓存
    with open(os.path.join(file_util.project_dir, file_util.code_data_dir, "open_market_date.pkl"), 'rb') as file:
        open_market_list = pickle.load(file)

    # 生成开市日期列表
    date_list = []
    for date in generate_date_list(start_date, end_date):
        if date not in open_market_list:
            continue
        date_list.append(date)
    return date_list

def update_open_market_date_list():
    """
    临时函数， 更新并生成开市日期集合缓存， 通过股票是否能够正常获取到股价信息判断是否开市，
    todo 换成正规api
    :return:
    """
    open_market_list = []
    with open(os.path.join(file_util.project_dir, file_util.code_data_dir, "601288_SH.pkl"), 'rb') as file:
        code_data = pickle.load(file)
        for date, value in code_data["行情"].items():
            if len(value) == 0:
                continue
            open_market_list.append(date)
    with open(os.path.join(file_util.project_dir, file_util.code_data_dir, "open_market_date.pkl"), 'wb') as file:
        pickle.dump(open_market_list, file)

if __name__ == "__main__":
    update_open_market_date_list()
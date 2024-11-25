import os
import time
import tqdm
import pickle
import datetime
import pandas as pd
import matplotlib.pyplot as plt
import tushare as ts

import utils.date_util as date_util
import utils.file_util as file_util

from infoUnit.McUnit import McUnit, default_mc_unit
from infoUnit.DividendUnit import DividendUnit

START_DATE = "20100101"
# https://tushare.pro/document/2?doc_id=27
tushare_token = "83a0e2644bf378843fb9c365bd504cbf445854193cd07271be4f8058"
# ts.set_token(self.my_token)
tushare_api = ts.pro_api(tushare_token)

"""
股票unit

包含股票的具体信息， 负责更新、计算、存储股票所有数值信息
market_condition： 存储历史行情数据，具体包括每天的 开盘价、收盘价、最高价、最低价、成交量、成交额等
dividend： 存储历史分红信息

"""
class ShareUnit:
    def __init__(self, code="601398.SH"):
        self.code = code
        self.save_file_name = os.path.join(
            file_util.project_dir,
            file_util.code_data_dir,
            self.code.replace(".", "_") + ".pkl"
        )

        # 初始化 行情数据
        self.init_information()

    def init_information(self):
        self.market_condition = {}
        self.dividend = {}

        self.load()
        self.download_and_update_dividend()
        self.download_and_update_market_condition()
        self.save()

    # 加载本地股票缓存
    def load(self):
        # 加载之前下载过的数据
        if not os.path.exists(self.save_file_name):
            pass
        else:
            with open(self.save_file_name, 'rb') as file:
                code_data = pickle.load(file)
                self.market_condition = code_data["行情"]
                self.dividend = code_data["分红"]

    # 存储本地股票缓存
    def save(self):
        code_data = {
            "行情": self.market_condition,
            "分红": self.dividend,
        }
        # 写入文件
        with open(self.save_file_name, 'wb') as file:
            pickle.dump(code_data, file)

    # 下载并更新分红信息
    def download_and_update_dividend(self, start_date=START_DATE):
        if self.code == "601398.SH":
            temp = [
                [20070620, 20070628, 0.165, 0],
                [20080617, 20080626, 1.334, 0],
                [20090603, 20090630, 1.655, 0],
                [20100526, 20100625, 1.705, 0],
                [20110614, 20110708, 1.846, 0],
                [20120613, 20120712, 2.037, 0],
                [20130625, 20130719, 2.398, 0],
                [20140619, 20140620, 2.617, 0],
                [20150706, 20150707, 2.554, 0],
                [20160707, 20160708, 2.333, 0],
                [20170710, 20170711, 2.343, 0],
                [20180712, 20180713, 2.408, 0],
                [20190722, 20190703, 2.506, 0],
                [20200629, 20200630, 2.628, 0],
                [20210705, 20210706, 2.660, 0],
                [20210705, 20210706, 2.660, 0],
                [0, 20220712, 2.933, 0],
                [0, 20230717, 3.035, 0],
                [0, 20240716, 3.064, 0],
            ]
            for item in temp:
                self.dividend[str(item[1])] = DividendUnit(
                    item[2] / 10, item[3]
                )

        arr = [[k, v] for k, v in self.dividend.items()]
        arr = sorted(arr, key=lambda x: x[0])
        self.dividend = {item[0]: item[1] for item in arr}

    # 下载并更新历史行情信息
    def download_and_update_market_condition(self, start_date=START_DATE, log_detail=False):
        # 按时间获取数据
        data_list = date_util.generate_date_list(
            start_date=start_date,
            end_date=date_util.today_date,
            wo_weekend=True,
            illegal_date_list=self.market_condition.keys()
        )
        for date in tqdm.tqdm(data_list) if log_detail is True else data_list:
            if date in self.market_condition:
                continue

            df = tushare_api.daily(ts_code=self.code, start_date=date, end_date=date)
            if df.empty == True:
                # 获取失败 大概率是不开市
                self.market_condition[date] = default_mc_unit
            else:
                d = df.loc[0].to_dict()
                self.market_condition[date] = McUnit(
                    d["open"], d["close"], d["high"], d["low"],
                    d["pre_close"], d["change"], d["pct_chg"], d["vol"], d["amount"]
                )
            time.sleep(0.5)

        # 按时间排序
        arr = [[k, v] for k, v in self.market_condition.items()]
        arr = sorted(arr, key=lambda x: x[0])
        self.market_condition = {item[0]: item[1] for item in arr}

    # 展示历史行情信息
    def show_market_condition(self, start_date=START_DATE, end_date=date_util.today_date):
        x, y = [], []
        for date, value in self.market_condition.items():
            if date < start_date or date >= end_date:
                continue
            if value.open == -1:
                continue
            x.append(date)
            y.append(value.open)
        plt.plot(x, y)
        plt.show()

    # 展示n日均值行情
    def show_mean(self, start_date=START_DATE, end_date=date_util.today_date):
        dataframe = []
        for date, value in self.market_condition.items():
            if date < start_date or date >= end_date:
                continue
            if value.open == -1:
                continue
            value = value.to_dict()
            value["日期"] = date
            dataframe.append(pd.Series(value))
        dataframe = pd.DataFrame(dataframe)
        dataframe.set_index("日期", inplace=True)
        dataframe["均值"] = dataframe["收盘价"].rolling(window=120).mean()
        dataframe[["收盘价", "均值"]].plot(figsize=(10,6))
        plt.show()

    # 获取全部分红率
    def get_dividend_ratio(self):
        """
        计算历年平均分红率
        :return:
        """
        dividend_ratio_dict = {}
        for date, value in self.dividend.items():
            if date in self.market_condition:
                dividend_ratio_dict[date] = value.cash / self.market_condition[date].close
        return dividend_ratio_dict

    # 获取平均分红率
    def get_average_dividend_ratio(self, count_year=-1):
        """
        计算指定年份的平均分红率
        :param count_year: -1代表全部年份， 5代表只计算最近5年的平均分红率
        :return:
        """
        dividend_ratio_dict = self.get_dividend_ratio()

        year = int(datetime.datetime.now().strftime("%Y"))
        if count_year == -1:
            count_year = year - 1980
        count_num, sum_ratio = 0, 0
        for y in range(year-count_year, year+1):
            flag = False
            for date, value in dividend_ratio_dict.items():
                if date.startswith(str(y)):
                    sum_ratio += dividend_ratio_dict[date]
                    flag = True
            if flag == True:
                count_num += 1
        return sum_ratio / count_num if count_num > 0 else 0, count_num

    # 获取时间段内的行情信息
    def get_market_condition(self, start_date=START_DATE, end_date=None):
        if end_date is None:
            end_date = date_util.get_next_date(start_date)

        sub_market_condition = {}
        for date in date_util.generate_date_list(start_date, end_date):
            if date in self.market_condition and self.market_condition[date].open != -1:
                sub_market_condition[date] = self.market_condition[date]
        return sub_market_condition

    # 获取时间段内的分红信息
    def get_dividend(self, start_date=START_DATE, end_date=None):
        if end_date is None:
            end_date = date_util.get_next_date(start_date)

        sub_dividend = {}
        for date in date_util.generate_date_list(start_date, end_date):
            if date in self.dividend:
                sub_dividend[date] = self.dividend[date]
        return sub_dividend
"""
    def download_and_update_fenhong(self):
        # https://tsanghi.com/fin/doc
        yesterday = datetime.datetime.now() - datetime.timedelta(days=1)
        yesterday_date = yesterday.strftime("%Y-%m-%d")
        start_date="2020-01-01"
        exchange_code = "XSHG"
        tsanghi_token = "266b5784e0a348ae99730fb2e2e2eb5c"
        ts_code = "601398"
        url = f"https://tsanghi.com/api/fin/stock/{exchange_code}/dividend?token={tsanghi_token}&ticker={ts_code}&start_date={start_date}&end_date={yesterday_date}"
        response = requests.get(url)
        data = json.loads(response.text)
        print(data)
"""

if __name__ == "__main":
    gongHang = ShareUnit("601398.SH")
    gongHang.show_market_condition()
    gongHang.show_mean()
    gongHang.get_dividend_ratio()
    gongHang.get_average_dividend_ratio()
    gongHang.get_market_condition()
    gongHang.get_dividend()
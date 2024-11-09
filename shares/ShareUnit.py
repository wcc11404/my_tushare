import os
import time
import tqdm
import requests
import pickle
import datetime
import json
import pandas as pd
import matplotlib.pyplot as plt
import tushare as ts

from utils import date_util


class ShareUnit:
    def __init__(self, code="601398.SH"):
        self.code = code
        self.save_file_name = "code_data/{}.pkl".format(self.code.replace(".", "_"))

        self.my_token = "83a0e2644bf378843fb9c365bd504cbf445854193cd07271be4f8058"
        # ts.set_token(self.my_token)
        self.pro = ts.pro_api(self.my_token)

        # 初始化 行情数据
        self.init_information()

    def init_information(self):
        self.market_condition = {}
        self.dividend = {}
        # self.qfq_market_condition = {}

        self.load()
        self.download_and_update_dividend()
        self.download_and_update_market_condition()
        self.save()

    def load(self):
        # 加载之前下载过的数据
        if not os.path.exists(self.save_file_name):
            pass
        else:
            with open(self.save_file_name, 'rb') as file:
                code_data = pickle.load(file)
                self.market_condition = code_data["行情"]
                self.dividend = code_data["分红"]

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

    def count_qfq_market_condition(self, start_date="20100101", end_date=None):
        if end_date is None:
            yesterday = datetime.datetime.now() - datetime.timedelta(days=1)
            end_date = yesterday.strftime("%Y%m%d")

        qfq_market_condition = {}
        for date, value in self.market_condition.items():
            if date < start_date or date > end_date:
                continue
            qfq_market_condition[date]

    def download_and_update_dividend(self, start_date="20100101"):
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
                self.dividend[str(item[1])] = {
                    "分红": item[2] / 10,
                    "配股": item[3],
                }

        arr = []
        for k, v in self.dividend.items():
            arr.append([k, v])
        arr = sorted(arr, key=lambda x: x[0])
        self.dividend = {}
        for item in arr:
            self.dividend[item[0]] = item[1]

    def download_and_update_market_condition(self, start_date="20100101"):
        # 按时间获取数据
        for date in tqdm.tqdm(
                date_util.generate_date_list(
                    start_date,
                    date_util.yesterday_date,
                    wo_weekend=True,
                    illegal_date_list=self.market_condition.keys()
                )
        ):
            if date in self.market_condition:
                continue

            # https://tushare.pro/document/2?doc_id=27
            df = self.pro.daily(ts_code=self.code, start_date=date, end_date=date)
            if df.empty == True:
                # 获取失败 大概率是不开市
                self.market_condition[date] = {}
            else:
                temp_dict = df.loc[0].to_dict()
                self.market_condition[date] = {
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
            time.sleep(0.5)

        # 按时间排序
        arr = []
        for k, v in self.market_condition.items():
            arr.append([k, v])
        arr = sorted(arr, key=lambda x: x[0])
        self.market_condition = {}
        for item in arr:
            self.market_condition[item[0]] = item[1]

    def save(self):
        code_data = {
            "行情": self.market_condition,
            "分红": self.dividend,
        }
        # 写入文件
        with open(self.save_file_name, 'wb') as file:
            pickle.dump(code_data, file)

    def show_market_condition(self, start_date="20200101", end_date=date_util.yesterday_date):
        x, y = [], []
        for date, value in self.market_condition.items():
            if date < start_date or date > end_date:
                continue
            if len(value) == 0:
                continue
            x.append(date)
            y.append(value["开盘价"])
        plt.plot(x, y)
        plt.show()

    def show_mean(self, start_date="20200101", end_date=date_util.yesterday_date):
        dataframe = []
        for date, value in self.market_condition.items():
            if date < start_date or date > end_date:
                continue
            if len(value) == 0:
                continue
            dataframe.append(pd.Series(value))
        dataframe = pd.DataFrame(dataframe)
        a = dataframe["收盘价"].rolling(window=10).mean()
        print(a)

    def get_dividend_ratio(self):
        """
        计算历年平均分红率
        :return:
        """
        dividend_ratio_dict = {}
        for date, value in self.dividend.items():
            if date in self.market_condition:
                dividend_ratio_dict[date] = value["分红"] / self.market_condition[date]["收盘价"]
        return dividend_ratio_dict

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
import datetime

def generate_date_list(start_date, end_date, wo_weekend=True, illegal_date_list=[]):
    """
    生成start 到 end 的时间序列列表
    :param start_date: 起始
    :param end_date:   结束
    :param wo_weekend: 是否去除周末
    :param illegal_date_list:  不需要生成的时间列表集合
    :return:
    """
    date_list = []
    start_date = datetime.datetime.strptime(start_date, "%Y%m%d")
    end_date = datetime.datetime.strptime(end_date, "%Y%m%d")
    while start_date <= end_date:
        if (wo_weekend == False or start_date.weekday() < 5) and start_date not in illegal_date_list:
            date_list.append(start_date.strftime("%Y%m%d"))
        start_date += datetime.timedelta(days=1)
    return date_list
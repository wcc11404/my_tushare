import random

import utils.date_util as date_util
import infoUnit.share_init as share_init

from strategy.BaseStrategy import BaseStrategy

def generate_fake_market_information(share_dict, date, time_interval=600):
    """
    生成指定日期的伪实时市场行情
    todo 后续用api获取真实实时行情
    :param share_dict:  所有需要获取行情的股票集合
    :param date:        指定日期
    :param time_interval: 模拟时间间隔， 及每time_interval的时间后， 获取一次真实行情
    :return:            实时行情list, [{}, {} ... {}], 每个元素都是个dict, 包含所有股票在那一时刻的实时行情
    """
    # 3600 * 4 含义是每小时3600秒， 一天开市4小时
    count = 3600 * 4 // time_interval

    dict_list = {}
    for share_code, share in share_dict.items():
        # 获取指定日期的市场信息
        market_condition = share.get_market_condition(date)
        if date not in market_condition:
            continue
        market_condition = market_condition[date]

        # 生成伪实时信息
        price_list = [round(random.uniform(market_condition["最低价"], market_condition["最高价"]),2) for _ in range(count)]
        price_list[random.randint(1, count - 2)] = market_condition["最低价"]
        price_list[random.randint(1, count - 2)] = market_condition["最高价"]
        price_list[0] = market_condition["开盘价"]
        price_list[-1] = market_condition["收盘价"]

        # 转换成dict形式
        dict_list[share_code] = [{
            "开盘价": price_list[0],
            "现价": price_list[index],
            "最高价": max(price_list[:index + 1]),
            "最低价": min(price_list[:index + 1]),
        } for index in range(count)]

    # 将dict_list转换为list_dict
    list_dict = [
        {share_code: fake_price_list[index] for share_code, fake_price_list in dict_list.items()}
            for index in range(count)
    ]
    return list_dict

def simulator_main(start_date="20150101", end_date="20240101"):
    """
    模拟策略
    :param start_date:  模拟初始日期
    :param end_date:    模拟结束日期， 不含
    :return:
    """

    """     模拟盘初始化    """
    # 初始化模拟盘环境数据
    valid_share_dict = share_init.get_valid_share()
    # 初始化账号&量化策略， 记录初始本金
    quant_strategy = BaseStrategy()
    quant_strategy_init_money = quant_strategy.account_amount




    """     模拟盘每日逻辑    """
    for date in date_util.generate_open_market_date_list(start_date, end_date):

        """     每日初始化    """
        # 封装每日所需的信息
        context = {
            "today_date": date,
        }
        # 开市前调用量化策略的初始化函数
        quant_strategy.before_trading(context)

        """     集合竞价    """

        """     连续竞价    """
        # 获取开市当天市场信息
        real_time_market_condition = generate_fake_market_information(valid_share_dict, date, time_interval=60*10)
        # 遍历每个时间
        for time_market_condition in real_time_market_condition:
            context["实时行情"] = time_market_condition
            quant_strategy.handle(context)

        """     闭市结算    """
        # 闭市获取账户信息



    """     模拟盘结算    """
    last_date = date_util.get_last_open_date(end_date)
    # 统计最后一日的股票账户资产
    share_value = 0
    for share_code, share in valid_share_dict.items():
        if share_code in quant_strategy.account_portfolio:
            market_condition = share.get_market_condition(last_date)
            if last_date not in market_condition:
                continue
            market_condition = market_condition[last_date]

            share_value += market_condition.close * quant_strategy.account_portfolio[share_code]["持有数量"]

    # 展示量化收益
    print(
"""
策略名称:\t{}
现金:\t\t{}
股票价值:\t{}
收益率:\t\t{}%
""".format(
    quant_strategy.strategy_name,
    round(quant_strategy.account_amount, 2),
    round(share_value, 2),
    round((quant_strategy.account_amount + share_value - quant_strategy_init_money) / quant_strategy_init_money * 100, 2),
)
    )

    return 0

if __name__ == "__main__":
    simulator_main()
import random

import strategy.QuantStrategy as QuantStrategy
import utils.date_util as date_util
import infoUnit.share_init as share_init

def generate_fake_market_information(valid_share_dict, date, time_interval=60*10):
    count = 3600 * 4 // time_interval

    temp = {}
    for share_code, share in valid_share_dict.items():
        market_condition = share.get_market_condition(date)[0]
        price_list = [round(random.uniform(market_condition["最低价"], market_condition["最高价"]),2) for _ in range(count)]
        price_list[random.randint(1, count - 2)] = market_condition["最低价"]
        price_list[random.randint(1, count - 2)] = market_condition["最高价"]
        price_list[0] = market_condition["开盘价"]
        price_list[-1] = market_condition["收盘价"]
        temp[share_code] = [{
            "开盘价": price_list[0],
            "现价": price_list[index],
            "最高价": max(price_list[:index + 1]),
            "最低价": min(price_list[:index + 1]),
        } for index in range(count)]

    arr = []
    for index in range(count):
        d = {}
        for k, v in temp.items():
            d[k] = v[index]
        arr.append(d)
    return arr

def simulator_main(start_date="20190101", end_date="20200101"):
    """

    :param start_date:
    :param end_date:
    :return:
    """

    """     模拟盘初始化    """
    # 初始化模拟盘环境数据
    valid_share_dict = share_init.get_valid_share()
    # 初始化账号&量化策略
    quant_strategy = QuantStrategy.QuantStrategy()

    """     模拟盘每日逻辑    """
    for date in date_util.generate_open_market_date_list(start_date, end_date):
        #print("模拟{}日的行情".format(date))

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
    # 统计最终账户信息

    # 展示量化收益

    return 0

if __name__ == "__main__":
    simulator_main()
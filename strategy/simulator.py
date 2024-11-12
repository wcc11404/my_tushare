import strategy.QuantStrategy as QuantStrategy
import utils.date_util as date_util
import infoUnit.share_init as share_init

quant_strategy = QuantStrategy.QuantStrategy()

def simulator_main(start_date="20190101", end_date="20200101"):
    # 初始化环境
    valid_share_dict = share_init.get_valid_share()

    # 遍历所有开市日期
    for date in date_util.generate_open_market_date_list(start_date, end_date):
        print(date)
        context = {}
    return 0

if __name__ == "__main__":
    simulator_main()
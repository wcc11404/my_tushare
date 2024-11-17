import infoUnit.share_init as share_init
from strategy.QuantStrategy import QuantStrategy

class BaseStrategy(QuantStrategy):
    def __init__(self, principal=100000, addition_info=None):
        """
        策略初始化
        :param principal:       初始化本金
        :param addition_info:   额外信息
        """
        # 策略属性
        self.strategy_name = "基础策略"

        # 资产组合
        self.account_amount = principal
        self.account_portfolio = {}

        # 历史数据信息
        self.valid_share_dict = share_init.get_valid_share()

    def before_trading(self, context):
        """
        开市前调用，一次性， 可以填写主要统计逻辑
        :param context:
        :return:
        """
        pass

    def handle(self, context):
        """
        连续竞价阶段调用， 多次， 可以填写主要买卖逻辑，信息处理逻辑
        :param context:
        :return:
        """
        if "实时行情" in context:
            real_time_market_condition = context["实时行情"]
        else:
            return -1

        buy_price = real_time_market_condition[share_init.GongShangYinHang]["现价"]
        buy_num = int(self.account_amount / buy_price)
        self.buy_share(share_init.GongShangYinHang, buy_price, buy_num)

        return 0
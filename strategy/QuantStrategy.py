import json

"""
量化策略基类
"""
class QuantStrategy:
    def __init__(self, principal=100000, addition_info=None):
        """
        策略初始化
        :param principal:       初始化本金
        :param addition_info:   额外信息
        """
        # 策略属性
        self.strategy_name = "量化策略基类"

        # 资产组合
        self.account_amount = principal
        self.account_portfolio = {}

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
        return 0

    def buy_share(self, share_code, buy_price, buy_num):
        """
        购买股票函数，
        :param share_code:  待购买的股票ts代码
        :param buy_price:   委托买入价格
        :param buy_num:     委托买入数量(手，100股)
        :return:
        """
        # 委托买入数量非法
        if buy_num < 1 or buy_num > 1000000:
            return -1
        # 账户现金余额不足
        if buy_price * buy_num > self.account_amount:
            return -1

        # 更新账户余额信息
        self.account_amount -= round(buy_price * buy_num, 4)

        # 挂单

        # 更新账户资产信息
        if share_code not in self.account_portfolio:
            self.account_portfolio[share_code] = {
                "持有数量": 0,
                "买入均价": 0,
            }
        self.account_portfolio[share_code] = {
            "持有数量":  self.account_portfolio[share_code]["持有数量"] + buy_num,
            "买入均价":
                (
                        self.account_portfolio[share_code]["持有数量"] * self.account_portfolio[share_code]["买入均价"] +
                        buy_price * buy_num
                ) /
                (self.account_portfolio[share_code]["持有数量"] + buy_num),
        }
        return 0

    def show_account_info(self):
        """展示账户资产信息"""
        print(
"""
账户现金:\t{}
股票资产:\t{}
""".format(
    round(self.account_amount, 2),
    json.dumps(self.account_portfolio)
)
        )
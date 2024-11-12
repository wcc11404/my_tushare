
"""
量化策略基类
"""
class QuantStrategy:
    def __init__(self):
        self.strategy_name = "QuantStrategy"
        self.account_amount = 100, 000

        self.account_portfolio = {}

    def get_account_info(self):
        """
        获取当前账户价值信息
        :return:
        """
        pass

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
        pass
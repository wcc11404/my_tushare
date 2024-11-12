import infoUnit.share_init as share_init

"""
量化策略基类
"""
class QuantStrategy:
    def __init__(self):
        # 策略属性
        self.strategy_name = "QuantStrategy"
        self.account_amount = 100, 000

        # 资产组合
        self.account_portfolio = {}

        # 历史数据信息
        self.valid_share_dict = share_init.get_valid_share()

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
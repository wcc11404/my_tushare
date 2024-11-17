import json

"""
Market Condition
"""
class McUnit:
    def __init__(self, open, close, high, low, pre_close, change, pct_change, vol, amount):
        self.open = open            # 开盘价
        self.close = close          # 收盘价
        self.high = high            # 最高价
        self.low = low              # 最低价
        self.pre_close = pre_close  # 昨收价
        self.change = change        # 涨跌额
        self.pct_change = pct_change    # 涨跌幅
        self.vol = vol              # 成交量
        self.amount = amount        # 成交额

    def to_dict(self):
        return {
            "开盘价": self.open,
            "收盘价": self.close,
            "最高价": self.high,
            "最低价": self.low,
            "昨收价": self.pre_close,
            "涨跌额": self.change,
            "涨跌幅": self.pct_change,
            "成交量": self.vol,
            "成交额": self.amount,
        }

    def to_string(self):
        return json.dumps(self.to_dict())

    def show(self):
        for k, v in self.to_dict().items():
            print("{}\t{}".format(k, v))

default_mc_unit = McUnit(-1, -1, -1, -1, -1, -1, -1, -1, -1)
import json

class DividendUnit:
    def __init__(self, cash, share):
        self.cash = cash    # 现金股利
        self.share = share  # 股票股利

    def to_dict(self):
        return {
            "派现金": self.cash,
            "派股": self.share,
        }

    def to_string(self):
        return json.dumps(self.to_dict())

    def show(self):
        for k, v in self.to_dict().items():
            print("{}\t{}".format(k, v))
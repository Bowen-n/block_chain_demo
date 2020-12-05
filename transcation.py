import json


class Transaction:
    def __init__(self, from_addr, to_addr, amount):
        self.from_addr = from_addr
        self.to_addr = to_addr
        self.amount = amount


class TransactionEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, Transaction):
            return o.__dict__
        return json.JSONEncoder.default(self, o)
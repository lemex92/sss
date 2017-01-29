import time


class Trade(object):
    def __init__(self, stock, indicator, quantity, price, time_stamp=time.time()):
        self.stock_symbol = stock
        self.time_stamp = time_stamp
        self.indicator = indicator
        self.quantity = int(quantity)
        self.price = float(price)


from operator import add, mul
from math import sqrt
from sss.models.trade import Trade
from sss.models.stock import Stock
from sss.utils.time_utils import get_date_time_since, time_now


class StockManager(object):
    def __init__(self):
        self.stocks = []
        self.trades = []

    def add_stock(self, symbol, stock_type, last_dividend=None, fixed_dividend=None, par_value=None,
                  ticker_price=None):
        stock = Stock(symbol, stock_type, last_dividend, fixed_dividend, par_value, ticker_price)
        self.stocks.append(stock)

    def get_stock_symbols(self):
        return [stock.symbol for stock in self.stocks]

    def get_trades(self):
        return self.trades

    def create_trade(self, stock_symbol, indicator, quantity, price, time_stamp=time_now()):
        if stock_symbol not in self.get_stock_symbols():
            raise Exception("Invalid stock symbol")

        trade = Trade(stock_symbol, indicator, quantity, price, time_stamp)
        self.trades.append(trade)

    def calculate_stock_price(self, symbol, since_minutes=15):
        since = get_date_time_since(since_minutes)

        trades_for_symbol = [trade for trade in self.trades
                             if trade.stock_symbol == symbol and trade.time_stamp > since]

        if len(trades_for_symbol) == 0:
            raise Exception("No trades found for {}".format(symbol))

        prices_per_quan = reduce(add, [(trade.quantity * trade.price) for trade in trades_for_symbol])
        quan = reduce(add, [trade.quantity for trade in trades_for_symbol])

        if quan == 0:
            return 0

        return prices_per_quan / quan

    # I seen this very nice function, a few months back on Redit
    # https://gist.github.com/Glench/4626483 why reinvent the wheel?
    def calculate_geometric_mean_for_trades_online(self):
        trade_prices = [trade.get_price() for trade in self.get_trades()]
        return self._online_geometric_mean(trade_prices)

    def _online_geometric_mean(self, iterable):
        return (reduce(mul, iterable)) ** (1.0 / len(iterable))

    # My first attempt
    def calculate_geometric_mean_for_trades(self):
        trade_prices = [trade.get_price() for trade in self.trades]
        return self.geometric_mean(trade_prices)

    def geometric_mean(self, iterable):
        total_price = (reduce(mul, iterable))
        len_iterable = len(iterable)
        return pow(total_price, (1.0/len_iterable))

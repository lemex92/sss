import unittest

from sss.core.stock_manager import StockManager
from sss.utils.time_utils import time_now, get_date_time_since


class TestStockManager(unittest.TestCase):

    def test_get_stock_symbols_none(self):
        stock_manager = StockManager()
        stock_symbols = stock_manager.get_stock_symbols()
        self.assertEquals(len(stock_symbols), 0)

    def test_add_stock(self):
        stock_manager = StockManager()
        stock_manager.add_stock("test34", "COMMON", 5, fixed_dividend=None, par_value=200,ticker_price=60)
        ss = stock_manager.get_stock_symbols()
        self.assertEquals(len(ss), 1)

    def test_add_trade_no_stock(self):
        stock_manager = StockManager()

        with self.assertRaises(Exception) as e:
            stock_manager.create_trade("not", "BUY", 100, 25)
        self.assertEqual('Invalid stock symbol', str(e.exception))

    def test_calculate_stock_price_no_trades(self):
        stock_manager = StockManager()

        with self.assertRaises(Exception) as e:
            stock_manager.calculate_stock_price("not")
        self.assertEqual('No trades found for not', str(e.exception))

    def test_calculate_stock_price_one_trade(self):
        stock_manager = StockManager()
        stock_manager.add_stock("tea", "COMMON", 5, fixed_dividend=None, par_value=200, ticker_price=60)
        stock_manager.create_trade("tea", "BUY", 100, 30, time_now())
        stock_price = stock_manager.calculate_stock_price("tea")
        self.assertEquals(stock_price, 30)

    def test_calculate_stock_price_many_trade(self):
        stock_manager = StockManager()
        stock_manager.add_stock("tea", "COMMON", 1, fixed_dividend=None, par_value=200, ticker_price=60)
        stock_manager.add_stock("sea", "COMMON", 2, fixed_dividend=None, par_value=200, ticker_price=10)
        stock_manager.add_stock("pea", "PREFERRED", 3, fixed_dividend=6, par_value=200, ticker_price=600)

        stock_manager.create_trade("tea", "BUY", 100, 30, time_now())
        stock_manager.create_trade("tea", "BUY", 40, 12, time_now())
        stock_manager.create_trade("tea", "BUY", 1, 32, time_now())
        stock_manager.create_trade("tea", "BUY", 10, 18, time_now())
        stock_manager.create_trade("tea", "BUY", 9, 30, time_now())

        stock_manager.create_trade("pea", "BUY", 10, 12, time_now())
        stock_manager.create_trade("pea", "BUY", 400, 65.4, time_now())
        stock_manager.create_trade("pea", "BUY", 600, 30, time_now())

        stock_price_tea = stock_manager.calculate_stock_price("tea")
        self.assertEquals(stock_price_tea, 24.7625)

        stock_price_pea = stock_manager.calculate_stock_price("pea")
        self.assertEquals(stock_price_pea, 43.84158415841584)

    def test_calculate_stock_price_no_trade_in_15_mins(self):
        stock_manager = StockManager()
        stock_manager.add_stock("tea", "COMMON", 5, fixed_dividend=None, par_value=200, ticker_price=60)
        stock_manager.create_trade("tea", "BUY", 100, 30, get_date_time_since(20))

        with self.assertRaises(Exception) as e:
            stock_manager.calculate_stock_price("tea")
        self.assertEqual('No trades found for tea', str(e.exception))

    def test_my_geometric_mean_vs_online_impl(self):
        stock_manager = StockManager()
        stock_manager.add_stock("tea", "COMMON", 5, fixed_dividend=None, par_value=200, ticker_price=60)
        stock_manager.create_trade("tea", "BUY", 10, 30, get_date_time_since(20))
        stock_manager.create_trade("tea", "BUY", 100, 5, get_date_time_since(20))
        stock_manager.create_trade("tea", "BUY", 45, 2, get_date_time_since(20))
        stock_manager.create_trade("tea", "BUY", 7, 52, get_date_time_since(20))

        self.assertEquals(stock_manager.calculate_geometric_mean_for_trades(),
                          stock_manager.calculate_geometric_mean_for_trades_online())

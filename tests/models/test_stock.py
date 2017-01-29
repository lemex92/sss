import unittest
from sss.models.stock import Stock


class TestStock(unittest.TestCase):

    def test_create_stock_valid(self):
        stock = Stock(symbol="tea", stock_type="COMMON", last_dividend=5, fixed_dividend=0,
                      par_value=300, ticker_price=100)
        self.assertEqual(stock.symbol, "tea")

    def test_create_stock_invalid_type(self):
        with self.assertRaises(Exception) as e:
            stock = Stock(symbol="tea", stock_type="INVALID", last_dividend=5, fixed_dividend=0,
                          par_value=300, ticker_price=100)
        self.assertEqual('Invalid stock type', str(e.exception))

    def test_create_stock_preferred_valid(self):
        stock = Stock(symbol="tea", stock_type="PREFERRED", last_dividend=5, fixed_dividend=4,
                      par_value=300, ticker_price=100)

        expected_dict = {'ticker_price': 100.0, 'symbol': 'tea', 'last_dividend': 5.0, 'fixed_dividend': 4.0,
                         'stock_type': "PREFERRED", 'par_value': 300.0}

        self.assertEquals(stock.__dict__, expected_dict)

    def test_create_stock_common_valid(self):
        stock = Stock(symbol="tea", stock_type="COMMON", last_dividend=5, fixed_dividend=None,
                      par_value=300, ticker_price=100)

        expected_dict = {'ticker_price': 100.0, 'symbol': 'tea', 'last_dividend': 5.0, 'fixed_dividend': None,
                         'stock_type': "COMMON", 'par_value': 300.0}

        self.assertEquals(stock.__dict__, expected_dict)

    def test_create_stock_common_no_dividend(self):
        with self.assertRaises(Exception) as e:
            stock = Stock(symbol="tea", stock_type="COMMON", last_dividend=None, fixed_dividend=None,
                          par_value=300, ticker_price=100)
        self.assertEqual('Last dividend must be provided when stock type is common', str(e.exception))

    def test_create_stock_prefered_no_dividend(self):
        with self.assertRaises(Exception) as e:
            stock = Stock(symbol="tea", stock_type="PREFERRED", last_dividend=None, fixed_dividend=None,
                          par_value=300, ticker_price=100)
        self.assertEqual('Fixed and last dividend must be provided when stock type is preferred', str(e.exception))

    def test_create_stock_str_preferred(self):
        stock = Stock(symbol="tea", stock_type="PREFERRED", last_dividend=5, fixed_dividend=10,
                      par_value=300, ticker_price=100)

        expected_str = "Symbol=tea;Stock Type=PREFERRED;Price=100.0p;Last Dividend=5.0;Fixed Dividend=10.0%;" \
                       "Dividend Yeild=0.3;PE Ratio=333.333333333"
        self.assertEquals(str(stock), expected_str)

    def test_create_stock_str_common(self):
        stock = Stock(symbol="tea", stock_type="COMMON", last_dividend=5, fixed_dividend=None,
                      par_value=300, ticker_price=100)

        expected_str = "Symbol=tea;Stock Type=COMMON;Price=100.0p;Last Dividend=5.0;Dividend Yeild=0.05;PE Ratio=2000.0"
        self.assertEquals(str(stock), expected_str)

    def test_stock_dividend_yeild_common(self):
        stock = Stock(symbol="tea", stock_type="COMMON", last_dividend=5, fixed_dividend=20,
                      par_value=250, ticker_price=100)

        self.assertEquals(stock.dividend_yeild(), 0.05)

    def test_stock_dividend_yeild_perferred(self):
        stock = Stock(symbol="tea", stock_type="PREFERRED", last_dividend=5, fixed_dividend=20,
                      par_value=250, ticker_price=100)

        self.assertEquals(stock.dividend_yeild(), 0.5)

    def test_stock_dividend_pe_ratio_common(self):
        stock = Stock(symbol="tea", stock_type="COMMON", last_dividend=5, fixed_dividend=None,
                      par_value=250, ticker_price=100)

        self.assertEquals(stock.pe_ratio(), 2000)

    def test_stock_dividend_pe_ratio_prefferred(self):
        stock = Stock(symbol="tea", stock_type="PREFERRED", last_dividend=5, fixed_dividend=20,
                      par_value=250, ticker_price=100)

        self.assertEquals(stock.pe_ratio(), 200.0)

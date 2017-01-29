from random import uniform


class Stock(object):
    def __init__(self, symbol, stock_type, last_dividend=None, fixed_dividend=None, par_value=None,
                 ticker_price=uniform(1, 200)):
        self.symbol = symbol
        self.ticker_price = float(ticker_price)

        if stock_type.upper() in ["COMMON", "PREFERRED"]:
            self.stock_type = stock_type
        else:
            raise Exception("Invalid stock type")

        if stock_type == "COMMON" and not last_dividend:
            raise Exception("Last dividend must be provided when stock type is common")

        if stock_type == "PREFERRED" and (not fixed_dividend or not last_dividend):
            raise Exception("Fixed and last dividend must be provided when stock type is preferred")

        if last_dividend:
            self.last_dividend = float(last_dividend)
        else:
            self.last_dividend = None

        if fixed_dividend:
            self.fixed_dividend = float(fixed_dividend)
        else:
            self.fixed_dividend = None

        self.par_value = float(par_value)

    def __str__(self):
        if self.fixed_dividend:
            return "Symbol={};Stock Type={};Price={}p;Last Dividend={};Fixed Dividend={}%;" \
                "Dividend Yeild={};PE Ratio={}".format(self.symbol, self.stock_type, self.ticker_price,
                                                       self.last_dividend, self.fixed_dividend, self.dividend_yeild(),
                                                       self.pe_ratio())
        return "Symbol={};Stock Type={};Price={}p;Last Dividend={};" \
               "Dividend Yeild={};PE Ratio={}".format(self.symbol, self.stock_type, self.ticker_price, self.last_dividend,
                                                      self.dividend_yeild(), self.pe_ratio())

    def dividend_yeild(self):
        if self.last_dividend == 0:
            return -1

        if self.stock_type == "COMMON":
            return self.last_dividend/self.ticker_price

        if self.stock_type == "PREFERRED":
            return ((self.fixed_dividend/100) * self.par_value) * self.ticker_price

    def pe_ratio(self):
        if self.ticker_price > 0:
            return self.ticker_price / self.dividend_yeild()
        return None

import click
import logging
import sys
from sss.core.stock_manager import StockManager
from sss.utils.file_utils import read_rows_from_csv
from random import uniform, randint, getrandbits


@click.command()
@click.option('--stock-file', required=True, help='Path to file contianing list of stocks')
@click.option('--number-of-trades', default=50, type=int, help='Number of trades to be simulated')
@click.option('--min-ticker-price', default=0.1, type=float, help='A stocks min ticker price')
@click.option('--max-ticker-price', default=150.0, type=float, help='A stocks max ticker price')
@click.option('--debug', help='Show debug log messages', is_flag=True)
def main(stock_file, number_of_trades, min_ticker_price, max_ticker_price, debug):
    setup_logging(debug)
    stock_manager = StockManager()

    if stock_file:
        logging.debug("Reading stocks from CSV file: {}".format(stock_file))
        rows = read_rows_from_csv(stock_file)
        logging.debug("Stocks read: {}".format(rows))
        # Ticker price isn't within the CSV
        # The CSV format is  SYMBOL, TYPE, LAST D, FIXED D, PAR VALUE
        # Lets add a random value
        [row.append(uniform(0.1, 200)) for row in rows if len(row) == 5]

        logging.debug("Ticker price added to stocks: {}".format(rows))
        # Let's add all our stock to the stock manager before we start making trades
        [stock_manager.add_stock(*row) for row in rows]

        logging.debug("All stocks added")
        [logging.debug(stock) for stock in stock_manager.get_stock_symbols()]

    # For each one of the trades we want to simulate
    for i in range(0, number_of_trades):
        symbol = stock_manager.get_stock_symbols()[randint(0, len(stock_manager.get_stock_symbols())-1)]
        buy_or_sell = "BUY" if (bool(getrandbits(1)) == 0) else "SELL"
        quan = randint(0, 500)
        price = uniform(min_ticker_price, max_ticker_price)

        logging.debug("Creating trade: SYMBOL={symbol};TYPE={type};QUAN={quan};PRICE={price}".format(symbol=symbol,
                                                                                                     type=buy_or_sell,
                                                                                                     quan=quan,
                                                                                                     price=price))
        stock_manager.create_trade(symbol, buy_or_sell, quan, price)

    logging.info("Geometric mean: {}".format(stock_manager.calculate_geometric_mean_for_trades()))


def setup_logging(debug):
    root = logging.getLogger()
    if debug:
        root.setLevel(logging.DEBUG)
    else:
        root.setLevel(logging.INFO)
    ch = logging.StreamHandler(sys.stdout)
    ch.setLevel(logging.DEBUG)
    formatter = logging.Formatter('%(levelname)s - %(message)s')
    ch.setFormatter(formatter)
    root.addHandler(ch)


if __name__ == '__main__':
    main()

import click
import time
from utils.file_utils import read_rows_from_csv

from core.stock_manager import StockManager

@click.command()
@click.option('--stock-file', help='Path to file contianing list of stocks')
def main(stock_file):
    stock_manager = StockManager()

    if stock_file:
        rows = read_rows_from_csv(stock_file)
        [stock_manager.add_stock(*row) for row in rows if row and len(row) == 5]

    running = True
    while running:
        choiche = get_option()

        if choiche is 1:
            display_stocks(stock_manager.get_stock_symbols())
        elif choiche is 2:
            display_trades(stock_manager.get_trades())
        elif choiche is 3:
            try:
                trades.append(create_trade(stock_manager.get_stock_symbols()))
            except Exception as e:
                click.echo(e.message)


def get_option():
    print "Please choose from the following options:"
    print "1 to view stocks"
    print "2 to view trades"
    print "3 to create a trade"
    return click.prompt('Please enter a valid integer', type=int)


def display_stocks(stocks):
    [click.echo(stock) for stock in stocks]


def display_trades(trades):
    [click.echo(trade) for trade in trades]


def create_trade(valid_stocks):
    stock_symbol = click.prompt("Please enter stock symbol", type=str)

    if  stock_symbol not in valid_stocks:
        raise Exception("Invalid stock symbol")

    buy_or_sell = click.prompt("BUY or SELL", type=str).upper()
    if buy_or_sell not in ["BUY", "SELL"]:
        raise Exception("Invalid trade indicator")

    quanity = click.prompt("Please enter quanitiy of trades", type=int)

    if quanity < 0:
        raise Exception("Quaity of trades must be > 0")

    price = click.prompt("Please enter price of stock", type=float)
    if price < 0:
        raise Exception("Price of stock must be > 0")

    return

if __name__ == '__main__':
    main()
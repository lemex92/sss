## Super Simple Stocks

### Getting started

This application requires Python 2 to run.

Everyone below here assumes you are within the `src` folder of the code base.

The `runner.py` file relies on Python click which can be installed using `pip install click`

All the python code follows PEP8 guidelines.
### Run automated trades

Command: `python runner.py --stock-file stocks.csv`

Custom parameters are documented using Python Click

### Running tests

Command: `nosetests --nocapture` (remove --no-capture to hide output0

Command (with coverage): `nosetests --nocapture --cover-html --cover-html-dir coverage --cover-package sss --with-coverage`

Example coverage output:

```
....................
Name                        Stmts   Miss  Cover   Missing
---------------------------------------------------------
sss.py                          0      0   100%
sss\core.py                     0      0   100%
sss\core\stock_manager.py      43      1    98%   44
sss\models.py                   0      0   100%
sss\models\stock.py            30      0   100%
sss\models\trade.py            10      0   100%
sss\utils.py                    0      0   100%
sss\utils\time_utils.py         6      0   100%
---------------------------------------------------------
TOTAL                          89      1    99%
----------------------------------------------------------------------
Ran 20 tests in 0.051s

OK
```


### Interests/Future work

- I would be interested to see the performance difference between my geometric mean function vs the functional verison I seen online.
- It would also be interesting to use some APIs for the stock data, This would also allow the use Mocking within tests
- If time wasn't an issue I would have used Python 3 rather than 2
- Future work would be to remove magic strings such as "COMMON", "PREFERRED", "BUY" and "SELL" and make them enums or similar
- Make custom exception classes
- Derive CommonStock and PreferredStock from Stock base class
- Create some test helper methods to remove duplciate code
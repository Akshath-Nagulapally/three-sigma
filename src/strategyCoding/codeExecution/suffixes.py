import os

code_initial = """
from datetime import datetime
from lumibot.backtesting import YahooDataBacktesting
from lumibot.strategies import Strategy

# A simple strategy that buys AAPL on the first day and holds it
class MyStrategy(Strategy):
    def on_trading_iteration(self):
        if self.first_iteration:
            aapl_price = self.get_last_price("AAPL")
            quantity = self.portfolio_value // aapl_price
            order = self.create_order("AAPL", quantity, "buy")
            self.submit_order(order)
"""


backtesting = """
# Pick the dates that you want to start and end your backtest
from datetime import datetime
from lumibot.backtesting import YahooDataBacktesting
from lumibot.strategies import Strategy
backtesting_start = datetime(2024, 1, 1)
backtesting_end = datetime(2024, 1, 7)

# Run the backtest
MyStrategy.backtest(
    YahooDataBacktesting,
    backtesting_start,
    backtesting_end,
)
"""


backtesting_paper_alpaca_polygon = """
from lumibot.brokers import Alpaca
from lumibot.backtesting import YahooDataBacktesting, BacktestingBroker, PolygonDataBacktesting
from lumibot.strategies.strategy import Strategy
from lumibot.traders import Trader
from datetime import datetime
from alpaca_trade_api import REST
from timedelta import Timedelta
import os

#Alpaca stuff
API_KEY = os.getenv("ALPACA_API_KEY")
API_SECRET = os.getenv("ALPACA_SECRET")
BASE_URL = "https://paper-api.alpaca.markets/v2"

ALPACA_CREDS = {
    "API_KEY": API_KEY,
    "API_SECRET": API_SECRET,
    "PAPER": True
}

broker = Alpaca(ALPACA_CREDS)

POLYGON_API_KEY = os.getenv("POLYGON_API_KEY")

start_date = datetime(2023,12,31)
end_date = datetime(2024,2,11)

strategy = MyStrategy(name='mlstrat', broker=broker)

results = strategy.backtest(
    PolygonDataBacktesting,
    start_date,
    end_date
)
print(results)
"""

live_trading_paper = """
from lumibot.brokers import Alpaca
from lumibot.backtesting import YahooDataBacktesting, BacktestingBroker, PolygonDataBacktesting
from lumibot.strategies.strategy import Strategy
from lumibot.traders import Trader
from datetime import datetime
from alpaca_trade_api import REST
from timedelta import Timedelta
import os

#Alpaca stuff
API_KEY = os.getenv("ALPACA_API_KEY")
API_SECRET = os.getenv("ALPACA_SECRET")
BASE_URL = "https://paper-api.alpaca.markets/v2"

ALPACA_CREDS = {
    "API_KEY": API_KEY,
    "API_SECRET": API_SECRET,
    "PAPER": True
}

broker = Alpaca(ALPACA_CREDS)

POLYGON_API_KEY = os.getenv("POLYGON_API_KEY")

start_date = datetime(2023,12,31)
end_date = datetime(2024,2,11)

strategy = MyStrategy(name='mlstrat', broker=broker)

strategy.run_live()
"""



live_trading_real_money = """
from lumibot.brokers import Alpaca
from lumibot.backtesting import YahooDataBacktesting, BacktestingBroker, PolygonDataBacktesting
from lumibot.strategies.strategy import Strategy
from lumibot.traders import Trader
from datetime import datetime
from alpaca_trade_api import REST
from timedelta import Timedelta
import os

#Alpaca stuff
API_KEY = os.getenv("ALPACA_API_KEY")
API_SECRET = os.getenv("ALPACA_SECRET")
BASE_URL = "https://api.alpaca.markets/v2"

ALPACA_CREDS = {
    "API_KEY": API_KEY,
    "API_SECRET": API_SECRET,
    "PAPER": True
}

broker = Alpaca(ALPACA_CREDS)

POLYGON_API_KEY = os.getenv("POLYGON_API_KEY")

start_date = datetime(2023,12,31)
end_date = datetime(2024,2,11)

strategy = MyStrategy(name='mlstrat', broker=broker)

strategy.run_live()
"""
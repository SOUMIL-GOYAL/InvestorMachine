from alpaca.trading.client import TradingClient
from alpaca.trading.requests import MarketOrderRequest
from alpaca.trading.enums import OrderSide, TimeInForce

trading_client = TradingClient('PK342HRR8ZE8JCJNSMQL', 'vyqsQIbXBVppPgIz4X3vBMdoEGm0Y8j9cJunkY5W', paper=True)

# preparing orders
market_order_data = MarketOrderRequest(symbol="MSFT", qty=1, side=OrderSide.BUY, time_in_force=TimeInForce.DAY)

# Market order
market_order = trading_client.submit_order(order_data=market_order_data)
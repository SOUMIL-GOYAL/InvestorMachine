from alpaca.trading.client import TradingClient
from alpaca.trading.requests import MarketOrderRequest
from alpaca.trading.enums import OrderSide, TimeInForce

trading_client = TradingClient('PKD6PB46QLVPY3ABNUNB', 'WfvEzc8mN2EMokCLWN6yNkz0tRDyrxUvwtP0zT0V', paper=True)

# preparing orders
market_order_data = MarketOrderRequest(
                    symbol="MSFT",
                    qty=0.5,
                    side=OrderSide.BUY,
                    time_in_force=TimeInForce.DAY
                    )

# Market order
market_order = trading_client.submit_order(
                order_data=market_order_data
               )
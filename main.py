# "Rule number one is never lose money, rule number two is never forget rule number one" - Warren Buffett


from alpaca.trading.client import TradingClient
from alpaca.trading.requests import MarketOrderRequest
from alpaca.trading.enums import OrderSide, TimeInForce

secrets = {"Key": 'PKTNJQZ66SO3AZ80NN17', "Secret" : '4YHOgI6bvXXhBekG17IfGaMFCeRCHTkxVs5Etld8'}


trading_client = TradingClient(secrets["Key"], secrets["Secret"], paper=True)

# preparing orders
market_order_data = MarketOrderRequest(symbol="SPY", notional=4000, side=OrderSide.BUY, time_in_force=TimeInForce.DAY)

# Market order
market_order = trading_client.submit_order(order_data=market_order_data)

# import required modules
import requests

api_key = "7d99e344057c583ac695552ab47ebb07"

base_url = "http://api.openweathermap.org/data/2.5/weather?"

city_name = "Singapore" #input("Enter city name : ")


complete_url = base_url + "appid=" + api_key + "&q=" + city_name


response = requests.get(complete_url)


x = response.json()
print(x)

# 404 means sity is not found
if x["cod"] != "404":

    
	y = x["main"]


	current_temperature = y["temp"]


	current_pressure = y["pressure"]


	current_humidity = y["humidity"]


	z = x["weather"]


	weather_description = z[0]["description"]

	print(" Temperature (in kelvin unit) = " +
					str(current_temperature) +
		"\n atmospheric pressure (in hPa unit) = " +
					str(current_pressure) +
		"\n humidity (in percentage) = " +
					str(current_humidity) +
		"\n description = " +
					str(weather_description))

else:
	print(" City Not Found ")

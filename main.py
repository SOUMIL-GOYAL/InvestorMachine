# "Rule number one is never lose money, rule number two is never forget rule number one" - Warren Buffett


from time import sleep
from alpaca.trading.client import TradingClient
from alpaca.trading.requests import MarketOrderRequest
from alpaca.trading.enums import OrderSide, TimeInForce
import requests
from alpaca.data import StockHistoricalDataClient
from alpaca.data.requests import StockLatestQuoteRequest
import csv

alpaca_secrets = {"Key": 'PKTNJQZ66SO3AZ80NN17', "Secret" : '4YHOgI6bvXXhBekG17IfGaMFCeRCHTkxVs5Etld8'}
openweather_secrets = {"Key": "7d99e344057c583ac695552ab47ebb07"}

trading_client = TradingClient(alpaca_secrets["Key"], alpaca_secrets["Secret"], paper=True)
stock_client = StockHistoricalDataClient(alpaca_secrets["Key"],  alpaca_secrets["Secret"])

spy = {"symbol" : "SPY", "history" : [], "owned": False}
investments = [spy, ]

with open("history.csv") as csvfile:
	reader = csv.reader(csvfile, quoting=csv.QUOTE_NONNUMERIC) # change contents to floats
	for row in reader: # each row is a list
		spy["history"].append(row)

print(spy["history"])

while (True):
	if (trading_client.get_clock().is_open == False): #market is over # type: ignore
		break
	else:
		print("market is open! \n")
	if (False): #stock trade to be make
		1+1	
	if (False): #whether trade
		1+1	
	#sleep(120)
	


multisymbol_request_params = StockLatestQuoteRequest(symbol_or_symbols=["SPY"])

latest_multisymbol_quotes = stock_client.get_stock_latest_quote(multisymbol_request_params)

print(latest_multisymbol_quotes["SPY"].ask_price)
market_order_data = MarketOrderRequest(symbol="SPY", notional=4000, side=OrderSide.BUY, time_in_force=TimeInForce.DAY)

market_order = trading_client.submit_order(order_data=market_order_data)



base_url = "http://api.openweathermap.org/data/2.5/weather?"

city_name = "Singapore" #input("Enter city name : ")


complete_url = base_url + "appid=" + openweather_secrets["Key"] + "&q=" + city_name


response = requests.get(complete_url)


x = response.json()
# print(x)

# 404 means sity is not found
if x["cod"] != "404":

    
	y = x["main"]


	current_temperature = y["temp"]


	current_pressure = y["pressure"]


	current_humidity = y["humidity"]


	z = x["weather"]


	weather_description = z[0]["description"]

	# print(" Temperature (in kelvin unit) = " +
	# 				str(current_temperature) +
	# 	"\n atmospheric pressure (in hPa unit) = " +
	# 				str(current_pressure) +
	# 	"\n humidity (in percentage) = " +
	# 				str(current_humidity) +
	# 	"\n description = " +
	# 				str(weather_description))

else:
	print(" City Not Found ")

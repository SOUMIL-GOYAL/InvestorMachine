# "Rule number one is never lose money, rule number two is never forget rule number one" - Warren Buffett
from time import sleep
from alpaca.trading.client import TradingClient
from alpaca.trading.requests import MarketOrderRequest, LimitOrderRequest
from alpaca.trading.enums import OrderSide, TimeInForce
import requests
from alpaca.data import StockHistoricalDataClient
from alpaca.data.requests import StockLatestQuoteRequest
import csv

alpaca_secrets = {"Key": 'PKFX44Y3R3O86HJTBHB2', "Secret" : 'BaaU98K0PYhBNFPr9TiqckKHRvGdWwb4w42I3GDw'}
openweather_secrets = {"Key": "7d99e344057c583ac695552ab47ebb07"}

trading_client = TradingClient(alpaca_secrets["Key"], alpaca_secrets["Secret"], paper=True)
stock_client = StockHistoricalDataClient(alpaca_secrets["Key"],  alpaca_secrets["Secret"])

spy = {"symbol" : "SPY", "history" : [], "owned": False}
investments = [spy, ]

counter = 0

# with open("history.csv") as csvfile:
# 	reader = csv.reader(csvfile, quoting=csv.QUOTE_NONNUMERIC) # change contents to floats
# 	for row in reader: # each row is a list
# 		spy["history"].append(row)
# 	#csvfile.close()

# print(spy["history"][0])

# print(trading_client.get_account())

while (True):
	if (trading_client.get_clock().is_open == False): #market is over # type: ignore
		print("market is not open; breaking loop")
		break
	else:
		print("market is open! \n")
	
	with open("history.csv", 'w') as csvfile:
		write = csv.writer(csvfile)
		for x in spy["history"]:
			write.writerow(x)

	for stock in investments:
		multisymbol_request_params = StockLatestQuoteRequest(symbol_or_symbols= [stock["symbol"]])
		latest_multisymbol_quotes = stock_client.get_stock_latest_quote(multisymbol_request_params)
		spy["history"].append(latest_multisymbol_quotes[stock["symbol"]].ask_price)
		print(spy["history"][-5:])
		try:
			trading_client.get_open_position(stock["symbol"])
			stock["owned"] = True
			print("owned")
		except:
			stock["owned"] = False
			print("unowned")

		if (stock["owned"] == False): #unowned
			if (len(stock["history"]) > 3): 
				money = float(trading_client.get_account().regt_buying_power) # type: ignore
				print("$", money, " available")
				if (stock["history"][-1] > stock["history"][-2] and stock["history"][-2] > stock["history"][-3]): #stock trade to be make
					market_order_data = MarketOrderRequest(symbol="SPY", notional=money - 1000, side=OrderSide.BUY, time_in_force=TimeInForce.DAY)
					market_order = trading_client.submit_order(order_data=market_order_data)
					print("bought")
					
					# limit_order_data = LimitOrderRequest(symbol="BTC/USD", limit_price=money-100000+10, notional=4000, side=OrderSide.SELL, time_in_force=TimeInForce.FOK)
					# limit_order = trading_client.submit_order(order_data=limit_order_data)



				elif (stock["history"][-1] < stock["history"][-2] and stock["history"][-2] < stock["history"][-3]): #short
					# market_order_data = MarketOrderRequest(symbol="SPY", notional=-money + 1000, side=OrderSide.BUY, time_in_force=TimeInForce.DAY)
					# market_order = trading_client.submit_order(order_data=market_order_data)
					print("shorted")
				else:
					print("neither shorting not buying!")
		elif (stock["owned"] == True): #owned

			inprice = float(trading_client.get_open_position(stock["symbol"]).avg_entry_price) # type: ignore
			nowprice = float(trading_client.get_open_position(stock["symbol"]).current_price) # type: ignore
			amountowned = float(trading_client.get_open_position(stock["symbol"]).qty) # type: ignore
			if (inprice < nowprice): #position is profitable # type: ignore
				trading_client.close_position(stock["symbol"])
				print("sold! we made $", (nowprice-inprice) * amountowned)
			else:

				print("not sold, holding...")
	counter = counter + 1
	if (counter % 5):
		sleep(10)
	else:
		sleep(2)
	






# base_url = "http://api.openweathermap.org/data/2.5/weather?"

# city_name = "Singapore" #input("Enter city name : ")


# complete_url = base_url + "appid=" + openweather_secrets["Key"] + "&q=" + city_name


# response = requests.get(complete_url)


# x = response.json()
# # print(x)

# # 404 means sity is not found
# if x["cod"] != "404":

    
# 	y = x["main"]


# 	current_temperature = y["temp"]


# 	current_pressure = y["pressure"]


# 	current_humidity = y["humidity"]


# 	z = x["weather"]


# 	weather_description = z[0]["description"]

# 	# print(" Temperature (in kelvin unit) = " +
# 	# 				str(current_temperature) +
# 	# 	"\n atmospheric pressure (in hPa unit) = " +
# 	# 				str(current_pressure) +
# 	# 	"\n humidity (in percentage) = " +
# 	# 				str(current_humidity) +
# 	# 	"\n description = " +
# 	# 				str(weather_description))

# else:
# 	print(" City Not Found ")

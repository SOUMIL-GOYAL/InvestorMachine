# "Rule number one is never lose money, rule number two is never forget rule number one" - Warren Buffett
from time import sleep
from alpaca.trading.client import TradingClient
from alpaca.trading.requests import MarketOrderRequest, LimitOrderRequest
from alpaca.trading.enums import OrderSide, TimeInForce
import requests
from alpaca.data import StockHistoricalDataClient
from alpaca.data.requests import StockLatestQuoteRequest
from math import floor
import csv

USE_API = False

alpaca_secrets = {"Key": 'PKTDH264NJ4LW7JEW08E', "Secret" : 'J00pT8mAJ03DTVeNdsP7J0ZfjxER3RyzoJY95vqd'}
openweather_secrets = {"base_url" : "http://api.openweathermap.org/data/2.5/weather?", "Key": "7d99e344057c583ac695552ab47ebb07", "city_name" : "Singapore", }

trading_client = TradingClient(alpaca_secrets["Key"], alpaca_secrets["Secret"], paper=True)
stock_client = StockHistoricalDataClient(alpaca_secrets["Key"],  alpaca_secrets["Secret"])

spy = {"symbol" : "SPY", "history" : [], "owned": False}
amzn = {"symbol" : "AMZN", "history" : [], "owned": False}
tsm = {"symbol" : "TSM", "history" : [], "owned": False}
dell = {"symbol" : "DELL", "history" : [], "owned": False}
nvda = {"symbol" : "NVDA", "history" : [], "owned": False}
tgt = {"symbol" : "TGT", "history" : [], "owned": False}
wmt = {"symbol" : "WMT", "history" : [], "owned": False}
bidu = {"symbol" : "BIDU", "history" : [], "owned": False}





investments = [spy, amzn, tsm, dell, nvda, tgt, wmt, bidu]

counter = 0

somethingowned = False

# with open("history.csv") as csvfile:
# 	reader = csv.reader(csvfile, quoting=csv.QUOTE_NONNUMERIC) # change contents to floats
# 	for row in reader: # each row is a list
# 		spy["history"].append(row)
# 	#csvfile.close()

# print(spy["history"][0])

# print(trading_client.get_account())

while (True):
	if (counter > 100 * len(investments)):
		print("25 counts complete, breaking loop")
		break

	if (trading_client.get_clock().is_open == False): #market is over # type: ignore
		print("market is not open; breaking loop")
		break
	else:
		print("market is open! \n")
	
	# with open("history.csv", 'w') as csvfile:
	# 	write = csv.writer(csvfile)
	# 	for x in spy["history"]:
	# 		write.writerow(x)

	for stock in investments:
		try:
			trading_client.get_open_position(stock["symbol"])
			somethingowned = True
			break
		except:
			stock["owned"] = False

	for stock in investments:
		

		multisymbol_request_params = StockLatestQuoteRequest(symbol_or_symbols= [stock["symbol"]])
		latest_multisymbol_quotes = stock_client.get_stock_latest_quote(multisymbol_request_params)
		stock["history"].append(latest_multisymbol_quotes[stock["symbol"]].ask_price)
		print(stock["symbol"] , stock["history"][-5:])
		try:
			trading_client.get_open_position(stock["symbol"])
			stock["owned"] = True
			print("owned")
		except:
			stock["owned"] = False
			print("unowned")


		if (stock["owned"] == False and somethingowned == False): #unowned

			if (len(stock["history"]) > 3): 
				money = float(trading_client.get_account().daytrading_buying_power) # type: ignore
				print("$", money, " available")
				if (stock["history"][-1] > stock["history"][-2] and stock["history"][-2] > stock["history"][-3]): #stock trade to be make
					# market_order_data = MarketOrderRequest(symbol= stock["symbol"], notional= floor(money/len(investments)), side=OrderSide.BUY, time_in_force=TimeInForce.DAY)
					market_order_data = MarketOrderRequest(symbol= stock["symbol"], notional= floor(money), side=OrderSide.BUY, time_in_force=TimeInForce.DAY)
					market_order = trading_client.submit_order(order_data=market_order_data)
					print("bought")
					
					# limit_order_data = LimitOrderRequest(symbol="BTC/USD", limit_price=money-100000+10, notional=4000, side=OrderSide.SELL, time_in_force=TimeInForce.FOK)
					# limit_order = trading_client.submit_order(order_data=limit_order_data)



				elif (stock["history"][-1] < stock["history"][-2] and stock["history"][-2] < stock["history"][-3]): #short
					# market_order_data = MarketOrderRequest(symbol=stock["symbol"], qty=422, side=OrderSide.SELL, time_in_force=TimeInForce.DAY)
					# market_order = trading_client.submit_order(order_data=market_order_data)
					print("shorted")
				else:
					print("neither shorting not buying!")
					counter = counter + 1
				
		elif (stock["owned"] == True): #owned

			inprice = float(trading_client.get_open_position(stock["symbol"]).avg_entry_price) # type: ignore
			nowprice = float(trading_client.get_open_position(stock["symbol"]).current_price) # type: ignore
			amountowned = float(trading_client.get_open_position(stock["symbol"]).qty) # type: ignore
			if (inprice + .015 < nowprice): #position is profitable # type: ignore
				trading_client.close_position(stock["symbol"])
				print("sold! we made $", (nowprice-inprice) * amountowned)
				stock["history"] = []
				sleep(2)
			else:

				print("not sold, holding...")
	
	somethingowned = False

	
	if (USE_API):
		#city_name = input("Enter city name : ")
		complete_url = openweather_secrets["base_url"] + "appid=" + openweather_secrets["Key"] + "&q=" + openweather_secrets["city_name"]
		response = requests.get(complete_url)
		x = response.json()
		# print(x)
		# 404 means sity is not found
		if x["cod"] != "404":
			y = x["main"]
			current_temperature = y["temp"]

			# print(" Temperature (in kelvin unit) = " +
			# 				str(current_temperature) +
			# 	"\n atmospheric pressure (in hPa unit) = " +
			# 				str(current_pressure) +
			# 	"\n humidity (in percentage) = " +
			# 				str(current_humidity) +
			# 	"\n description = " +
			# 				str(weather_description))
			try:
				trading_client.get_open_position("KO")
				koowned = True
			except:
				koowned = False
				# print("unowned")
			if (float(current_temperature) >= 303.15 and koowned == False):
				market_order_data = MarketOrderRequest(symbol="KO", notional= 1, side=OrderSide.BUY, time_in_force=TimeInForce.DAY)
				market_order = trading_client.submit_order(order_data=market_order_data)
			elif (koowned == True):
				trading_client.close_position("KO")
		else:
			print(" City Not Found ")
	

	sleep(4)
	








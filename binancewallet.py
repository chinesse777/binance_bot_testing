# Import the Client class from the binance.client module to interact with the Binance API
from binance.client import Client
import os
from dotenv import load_dotenv

load_dotenv('C:/Users/rlongrod/OneDrive - Cisco/Documents/python_crypto_bot_binance/venv/.env')
Public_Key = os.getenv('Public_Key_Spot')
Private_Key = os.getenv('Private_Key_Spot')

def get_account_balances():
	
	# Create a new client object to interact with the Binance API
	client = Client(Public_Key, Private_Key)

	# Retrieve the balances of all coins in the user's Binance account
	account_balances = client.get_account()['balances']

	# Get the current price of all tickers from the Binance API
	ticker_info = client.get_all_tickers()

	# Create a dictionary of tickers and their corresponding prices
	ticker_prices = {ticker['symbol']: float(ticker['price']) for ticker in ticker_info}

	# Calculate the USDT value of each coin in the user's account
	coin_values = []
	for coin_balance in account_balances:
		# Get the coin symbol and the free and locked balance of each coin
		coin_symbol = coin_balance['asset']
		unlocked_balance = float(coin_balance['free'])
		locked_balance = float(coin_balance['locked'])

		# If the coin is USDT and the total balance is greater than 1, add it to the list of coins with their USDT values
		if coin_symbol == 'USDT' and unlocked_balance + locked_balance > 1:
			coin_values.append(('USDT', (unlocked_balance + locked_balance)))
		# Otherwise, check if the coin has a USDT trading pair or a BTC trading pair
		elif unlocked_balance + locked_balance > 0.0:
			# Check if the coin has a USDT trading pair
			if (any(coin_symbol + 'USDT' in i for i in ticker_prices)):
				# If it does, calculate its USDT value and add it to the list of coins with their USDT values
				ticker_symbol = coin_symbol + 'USDT'
				ticker_price = ticker_prices.get(ticker_symbol)
				coin_usdt_value = (unlocked_balance + locked_balance) * ticker_price
				if coin_usdt_value > 1:
					coin_values.append((coin_symbol, coin_usdt_value))
			# If the coin does not have a USDT trading pair, check if it has a BTC trading pair
			elif (any(coin_symbol + 'BTC' in i for i in ticker_prices)):
				# If it does, calculate its USDT value and add it to the list of coins with their USDT values
				ticker_symbol = coin_symbol + 'BTC'
				ticker_price = ticker_prices.get(ticker_symbol)
				coin_usdt_value = (unlocked_balance + locked_balance) * ticker_price * ticker_prices.get('BTCUSDT')
				if coin_usdt_value > 1:
					coin_values.append((coin_symbol, coin_usdt_value))

	# Sort the list of coins and their USDT values by USDT value in descending order
	coin_values.sort(key=lambda x: x[1], reverse=True)

	# Return the list of coins and their USDT values
	return coin_values


def spot_balance():
    sum_btc = 0.0
    # Create a new client object to interact with the Binance API
    client = Client(Public_Key, Private_Key)
    balances = client.get_account()
    #print(balances)
    for _balance in balances["balances"]:
        asset = _balance["asset"]
        if float(_balance["free"]) != 0.0 or float(_balance["locked"]) != 0.0:
            try:
                btc_quantity = float(_balance["free"]) + float(_balance["locked"])
                if asset == "BTC":
                    sum_btc += btc_quantity
                else:
                    _price = client.get_symbol_ticker(symbol=asset + "BTC")
                    sum_btc += btc_quantity * float(_price["price"])
            except:
                pass

    current_btc_price_USD = client.get_symbol_ticker(symbol="BTCUSDT")["price"]
    own_usd = sum_btc * float(current_btc_price_USD)
    print("Total portfolio Spot => %.8f BTC == " % sum_btc, end="")
    print("%.8f USDT" % own_usd)

def get_balances():
    # Create a new client object to interact with the Binance API
    client = Client(Public_Key, Private_Key)
    balances = client.get_account()
    #print(balances)
    for _balance in balances["balances"]:
        asset = _balance["asset"]
        if float(_balance["free"]) != 0.0 :
            value = _balance["free"]
            print('The current value in token',asset, 'is: ', value,asset+'s')

    
    #print("The current value in ",coin, "is: ",value)
    return


def main():

    # Call the get_accountbalance function to get the list of coins and their USDT values
    coins_usdt_value = get_account_balances()

    # Print the list of coins and their USDT values in descending order of USDT value
    for coin, usdt_value in coins_usdt_value:
        print('The current value for coin 'f"{coin} in USDT is:  ${usdt_value:.2f}")

    # Calculate the grand total USDT value
    grand_usdt_total = sum(map(lambda coin_usdt_value: coin_usdt_value[1], coins_usdt_value))

    # Print the grand total USDT value
    print(f"\nGrand Total: ${grand_usdt_total:.2f}")

    spot_balance()
    get_balances()

if __name__ == '__main__':
    main()
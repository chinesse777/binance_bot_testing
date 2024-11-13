from telegram.ext.updater import Updater 
from telegram.update import Update 
from telegram.ext.callbackcontext import CallbackContext 
from telegram.ext.commandhandler import CommandHandler 
from telegram.ext.messagehandler import MessageHandler 
from telegram.ext.filters import Filters 
from dotenv import load_dotenv
import os
from time import sleep
import requests
from binance.client import Client

load_dotenv('C:/Users/rlongrod/OneDrive - Cisco/Documents/python_crypto_bot_binance/venv/.env')
Tel_Token = os.getenv('Telegram_Token')
Public_Key = os.getenv('Public_Key_Spot')
Private_Key = os.getenv('Private_Key_Spot')

updater = Updater(Tel_Token, 
				use_context=True) 


def start(update: Update, context: CallbackContext): 
	update.message.reply_text( 
		"Hello sir, Welcome to the Bot.Please write\ /help to see the commands available.") 

def help(update: Update, context: CallbackContext): 
	update.message.reply_text("""Available Commands : 
	/tokens - To get the quantity of your assets
	/btc_total - To get the total btcs of your assets
	/usdt_values - To get the USDT value of all your coins
	""") 


def coin_values(update: Update, context: CallbackContext): 
	update.message.reply_text(get_account_balances())

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

	# Print the list of coins and their USDT values in descending order of USDT value
	list_coin_values=[]
	s= ''
	for coin, usdt_value in coin_values:
		a = ('The current value for coin 'f"{coin} in USDT is:  ${usdt_value:.2f}")
		list_coin_values.append(a)
		s += a+'\n'
		print(a)

	print(s)
	"""
	# Return the string of coins and their USDT values
	print(type(coin_values))
	print(coin_values)
	b = f"{coin_values}".strip("[]")
	b = b.replace('),', '\n')
	b = b.replace('(\'', '')
	print(b)
	"""
	s= 'The total value of all your assets is USDT is: \n'+ s
	return s

def get_balances():
    client = Client(Public_Key, Private_Key)
    balances = client.get_account()
    list_assets = []
    for _balance in balances["balances"]:
        asset = _balance["asset"]
        if float(_balance["free"]) != 0.0 :
            value = _balance["free"]
            d='The current value in token ' +asset +' is: '+ str(value)+' '+ asset +'s' +'\n'
            list_assets.append(d)

    list_assets = ' '.join(list_assets)
    #print("The current value in ",coin, "is: ",value)
    return list_assets
    

def tokens_balances(update: Update, context: CallbackContext):
	update.message.reply_text(get_balances())  

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
    b= "Total portfolio Spot => %.8f BTC == " % sum_btc
    c= "%.8f USDT" % own_usd
    a=b+c
    return a
	
def btc_asset(update: Update, context: CallbackContext): 
	update.message.reply_text(spot_balance())

def unknown(update: Update, context: CallbackContext): 
	update.message.reply_text( 
		"Sorry '%s' is not a valid command" % update.message.text) 


def unknown_text(update: Update, context: CallbackContext): 
	update.message.reply_text( 
		"Sorry I can't recognize you , you said '%s'" % update.message.text) 

list_assets = []
updater.dispatcher.add_handler(CommandHandler('start', start)) 
updater.dispatcher.add_handler(CommandHandler('tokens', tokens_balances)) 
updater.dispatcher.add_handler(CommandHandler('help', help)) 
updater.dispatcher.add_handler(CommandHandler('btc_total', btc_asset)) 
updater.dispatcher.add_handler(CommandHandler('usdt_values', coin_values)) 
updater.dispatcher.add_handler(MessageHandler(Filters.text, unknown)) 
updater.dispatcher.add_handler(MessageHandler( 
	Filters.command, unknown)) # Filters out unknown commands 

# Filters out unknown messages. 
updater.dispatcher.add_handler(MessageHandler(Filters.text, unknown_text)) 


updater.start_polling() 
sleep(20)
updater.stop()




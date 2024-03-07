import logging
import requests
import pprint

logger =logging.getLogger()

def get_contracts():
    response = requests.get('https://testnet.binance.vision/api/v3/exchangeInfo')
    print(response.status_code)
    #pprint.pprint(response.json()['symbols'])

    contracts = []
    for contract in response.json()['symbols']:
        #pprint.pprint(contract)
        print(contract["symbol"])
        contracts.append((contract['symbol']))


    return  contracts

print(get_contracts())


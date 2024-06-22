from urllib import response
import ccxt
from sympy import sec
from datetime import datetime , timedelta
import time

key =  "C7D71AD39C9248099CA9CB2FFF185EF1"
secret = "F9AAF607A05B454A6D1B1F42B53972F516931C5C5EB6ADC0"

co = ccxt.coinex()
co.apiKey = key
co.secret = secret
co.options['defaultType'] = 'swap'

pair = 'KAVA/USDT:USDT'

markets = co.load_markets()
tickers = co.fetch_tickers()
symbols = []
for symbol,market in markets.items():
    if market['swap'] and market['linear']:
        if market['limits']['amount']['min'] <=10:
            ticker = tickers.get(symbol)
            if ticker['last'] <=1.5 and ticker['last'] >= 0.0001:
                symbols.append(symbol)

for symbol in symbols:
    market = markets.get(symbol)
    ticker = tickers.get(symbol)
    print(symbol , '    ' ,market['limits']['amount']['min'] ,'   ',  ticker['last'])


'''
{'id': 'XRPUSDT', 
'lowercaseId': None, 
'symbol': 'XRP/USDT:USDT', 
'base': 'XRP', 
'quote': 'USDT', 
'settle': 'USDT', 
'baseId': 'XRP', 
'quoteId': 'USDT',
 'settleId': 'USDT', 
 'type': 'swap', 
 'spot': False, 
 'margin': False, 
 'swap': True, 
 'future': False, 
 'option': False, 
 'index': None, 
 'active': None, 
 'contract': True, 
 'linear': True, 
 'inverse': False, 
 'subType': 'linear', 
 'taker': 0.001, 
 'maker': 0.001, 
 'contractSize': 1.0, 
 'expiry': None, 
 'expiryDatetime': None, 
 'strike': None, 
 'optionType': None, 
 'precision': {'amount': 1e-08, 'price': 0.0001, 'cost': None, 'base': None, 'quote': None}, 
 'limits': {
    'leverage': {'min': 1.0, 'max': 50.0}, 
    'amount': {'min': 50.0, 'max': None}, 
    'price': {'min': None, 'max': None}, 
    'cost': {'min': None, 'max': None}}, 
'created': None, 
'info': {'base_ccy': 'XRP', 'base_ccy_precision': '8', 'contract_type': 'linear', 'leverage': ['1', '2', '3', '5', '8', '10', '15', '20', '30', '50'], 'maker_fee_rate': '0', 'market': 'XRPUSDT', 'min_amount': '50', 'open_interest_volume': '1764403', 'quote_ccy': 'USDT', 'quote_ccy_precision': '4', 'taker_fee_rate': '0'}, 'percentage': True}


{'symbol': 'XRP/USDT:USDT', 
'timestamp': None, 
'datetime': None, 
'high': 0.4959, 
'low': 0.476, 
'bid': None, 
'bidVolume': 936967.0, 
'ask': None, 
'askVolume': 413458.0, 
'vwap': None, 
'open': 0.4955, 
'close': 0.4832, 
'last': 0.4832, 
'previousClose': None, 
'change': -0.0123, 
'percentage': -2.48234106962664, 
'average': 0.48935, 
'baseVolume': 4503612.0, 
'quoteVolume': None, 'info': {'close': '0.4832', 'high': '0.4959', 'index_price': '0.4829', 'last': '0.4832', 'low': '0.476', 'mark_price': '0.483', 'market': 'XRPUSDT', 'open': '0.4955', 'period': '86400', 'value': '2189383.0117', 'volume': '4503612', 'volume_buy': '936967', 'volume_sell': '413458'}}
'''


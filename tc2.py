import ccxt
import time
from pprint import pp
import pandas as pd
import pandas_ta as ta
import matplotlib.pyplot as plt

pd.set_option('display.max_rows', None)

key =  "C7D71AD39C9248099CA9CB2FFF185EF1"
secret = "F9AAF607A05B454A6D1B1F42B53972F516931C5C5EB6ADC0"

co = ccxt.coinex()
co.apiKey = key
co.secret = secret
co.options['defaultType'] = 'swap'

now = time.time()
since = int(now-(10*24*60*60))*1000

pair = 'KAVA/USDT:USDT'

data = co.fetch_ohlcv(symbol= pair , timeframe= '5m' , limit= 1000)
print(data)
df = pd.DataFrame(data)
df.columns = ['date', 'open', 'high', 'low', 'close', 'volume']



df['date'] = pd.to_datetime(df['date'], unit='ms')
df = df.set_index('date')

q = ta.qqe(df['close'] ,length= 20 , smooth= 5 , factor= 4)

qqe = q[q.columns[0]]
qqel = q[q.columns[2]]
qqes = q[q.columns[3]]
print(qqe)
print(qqel)
print(qqes)


# qqe = 0
# qqel = 2
# qqes = 3

# plt.show()

'''
{'id': '142932458084', 
'clientOrderId': 'x-9196406260a8282bc17a52e2fb', 
'datetime': '2024-06-15T19:45:22.923Z', 
'timestamp': 1718480722923, 
'lastTradeTimestamp': 1718480770171, 
'status': None, 
'symbol': 'KAVA/USDT:USDT', 
'type': 'limit', 
'timeInForce': None, 
'postOnly': None, 
'reduceOnly': None, 
'side': 'buy', 
'price': 0.545, 
'stopPrice': None, 
'triggerPrice': None, 
'takeProfitPrice': None, 
'stopLossPrice': None, 
'cost': 0.0, 'average': None, 
'amount': 10.0, 
'filled': 0.0, 
'remaining': 10.0, 
'trades': [], 
'fee': {'currency': 'USDT', 'cost': '0'}, 
'info': {'amount': '10', 'client_id': 'x-9196406260a8282bc17a52e2fb', 'created_at': '1718480722923', 'fee': '0', 'fee_ccy': 'USDT', 'filled_amount': '0', 'filled_value': '0', 'last_filled_amount': '0', 'last_filled_price': '0', 'maker_fee_rate': '0.0003', 'market': 'KAVAUSDT', 'market_type': 'FUTURES', 'order_id': '142932458084', 'price': '0.545', 'realized_pnl': '0', 'side': 'buy', 'taker_fee_rate': '0.0005', 'type': 'limit', 'unfilled_amount': '10', 'updated_at': '1718480770171'}, 'fees': [{'currency': 'USDT', 'cost': 0.0}], 'lastUpdateTimestamp': None}
'''
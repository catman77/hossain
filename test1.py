import ccxt
import pandas as pd
import pandas_ta as ta
import matplotlib.pyplot as plt
co = ccxt.coinex()

data = co.fetch_ohlcv(symbol= 'XRP/USDT:USDT' , timeframe= '5m' , limit= 1000)
df = pd.DataFrame(data , columns=['date' , 'open' , 'high' , 'low' , 'close' , 'volume'])
df['date'] = pd.to_datetime(df['date'] , unit= 'ms')
df.set_index('date' , inplace= True)

qqe = ta.qqe(close= df['close'] , length= 20 , smooth= 5 , factor= 4.5)
df['rsi'] = ta.rsi(close= df['close'] , length= 14)

bb = ta.bbands(close= df['close'] , length= 20 ,std= 2)
print(bb.columns)
input('press')

df['qqe'] = qqe[qqe.columns[0]]
df['qqel'] = qqe[qqe.columns[2]]
df['qqes'] = qqe[qqe.columns[3]]

df['qqe'].plot(figsize=(20,5))
df['qqel'].plot()
df['qqes'].plot()
plt.show()

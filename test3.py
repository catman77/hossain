import os
from pathlib import Path
from freqtrade.data.history import load_pair_history
from freqtrade.enums import CandleType
from freqtrade.configuration import Configuration
from pathlib import Path
import pandas_ta as ta
import numpy as np
from pandas import DataFrame, Series
import finplot as fplt



def strategy(candels:DataFrame , len1:int , std1:float , len2:int , std2:float ,rsi_len:int):
    df = candels.copy(deep= True)
    df['rsi'] = ta.rsi(close= df['close'] , length= rsi_len)
    
    bb1 = ta.bbands(close= df['close'] , length= len1 , std= std1)
    df['lower1'] = bb1[bb1.columns[0]]
    df['upper1'] = bb1[bb1.columns[2]]

    bb2 = ta.bbands(close= df['rsi'] , length= len2 , std= std2)
    df['lower2'] = bb2[bb2.columns[0]]
    df['upper2'] = bb2[bb2.columns[2]]
    df = df.fillna(0)
    df['buy'] = 0
    df['sell']= 0
    df.loc[((df['close'] > df['lower1']) & (df['close'].shift(1) < df['lower1'].shift(1)) & (df['rsi'] > df['lower2']) & (df['rsi'].shift(1) < df['lower2'].shift(1)) , 'buy')] = 1
    df.loc[((df['close'] < df['lower1']) & (df['close'].shift(1) > df['lower1'].shift(1)) & (df['rsi'] < df['lower2']) & (df['rsi'].shift(1) > df['lower2'].shift(1)) , 'sell')] = 1
    return df


project_root = "c:\\bager\\"

config_path = Path("c:\\bager\\user_data\\config.json")

config = Configuration.from_files([config_path])

data_location = config["datadir"]
pair = "KAVA/USDT:USDT"

candles:DataFrame = load_pair_history(datadir=data_location,timeframe=config["timeframe"],pair=pair,data_format = "json",candle_type=CandleType.FUTURES)

df:DataFrame = candles.tail(50)
df.plot('close' , figsize=(20,8))
df.plot('open')
fplt.show()
# fplt.set_mouse_callback(update_legend_text, ax=ax, when='hover')
# fplt.add_crosshair_info(update_crosshair_text, ax=ax)

# df:DataFrame = strategy(candels= main_df , len1=20 , std1= 2 , len2= 20 , std2= 2 , rsi_len= 14)

# df = df.fillna(0)
# ax = fplt.create_plot('' , rows= 1 , maximize= True)
# fplt.background = "#101211"
# fplt.odd_plot_background = '#f0f'
# fplt.band_color = "#f5f7f6"
# fplt.plot(df['close'] , color= "#f5f7f6" , zoomscale= True)

# fplt.plot(df['qqel'] , color= "black")
# fplt.plot(df['qqes'] , color = "black")
# fplt.set_y_scale(yscale= 'log')
# fplt.show()




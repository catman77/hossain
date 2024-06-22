import numpy as np
import pandas as pd
from pandas import DataFrame
from datetime import datetime
from typing import Optional, Union
from freqtrade.strategy import BooleanParameter, CategoricalParameter, DecimalParameter, IntParameter, IStrategy, merge_informative_pair
import talib.abstract as ta
import pandas_ta as pta
from technical import qtpylib

class my(IStrategy):
    INTERFACE_VERSION = 3
    my_leverage = 10
    timeframe = '5m'
    can_short: bool = True
    minimal_roi = {'60': 0.01, '30': 0.02, '0': 0.04}
    stoploss = -0.1
    trailing_stop = False

    process_only_new_candles = True
    use_exit_signal = True
    exit_profit_only = False
    ignore_roi_if_entry_signal = False
    startup_candle_count: int = 300

    rsi_len = IntParameter(8, 50, default=14, space='buy')

    bb1_len = IntParameter(8, 100, default=20, space='buy')
    std1 = DecimalParameter(1.5, 3.5, default=2, decimals=1, space='buy')

    bb2_len = IntParameter(8, 100, default=20, space='buy')
    std2 = DecimalParameter(1.5, 3.5, default=2, decimals=1, space='buy')


    def populate_indicators(self, df: DataFrame, metadata: dict) -> DataFrame:
        rsi = pta.rsi(close= df['close'] , length= self.rsi_len.value)
        df[rsi.columns[0]] = rsi[rsi.columns[0]]

        bb1 =  pta.bbands(close= df['close'] , length= self.bb1_len.value , std= self.std1.value)
        df[bb1.columns[0]] = bb1[bb1.columns[0]]  # lower
        df[bb1.columns[2]] = bb1[bb1.columns[2]]   # upper

        bb2 = pta.bbands(close= df[rsi.columns[0]] , length= self.bb2_len.value , std= self.std2.value)
        df[bb2.columns[0]] = bb2[bb2.columns[0]]   # lower
        df[bb2.columns[2]] = bb2[bb2.columns[2]]    # upper

        return df

    def populate_entry_trend(self, df: DataFrame, metadata: dict) -> DataFrame:
        buy_condiction = []
        df.loc[qtpylib.crossed_above(df['close'], df['lower']), 'bb1_buy'] = 1
        df.loc[qtpylib.crossed_above(df['rsi'], df['rsi_lower']), 'bb2_buy'] = 1
        df.loc[(df['bb1_buy'] == 1) & df['bb2_buy'] & (df['qqe_buy'] == 1), 'enter_long'] = 1
        df.loc[df['qqes'] != 0, 'qqe_sell'] = 1
        df.loc[qtpylib.crossed_below(df['close'], df['upper']), 'bb1_sell'] = 1
        df.loc[qtpylib.crossed_below(df['rsi'], df['rsi_upper']), 'bb2_sell'] = 1
        df.loc[(df['bb1_sell'] == 1) & df['bb2_sell'] & (df['qqe_sell'] == 1), 'enter_short'] = 1
        return df

    def populate_exit_trend(self, df: DataFrame, metadata: dict) -> DataFrame:
        df.loc[df['qqes'] != 0, 'qqe_sell'] = 1
        df.loc[qtpylib.crossed_below(df['close'], df['upper']), 'bb1_sell'] = 1
        df.loc[qtpylib.crossed_below(df['rsi'], df['rsi_upper']), 'bb2_sell'] = 1
        df.loc[(df['bb1_sell'] == 1) & df['bb2_sell'] & (df['qqe_sell'] == 1), 'exit_long'] = 1
        df.loc[df['qqel'] != 0, 'qqe_buy'] = 1
        df.loc[qtpylib.crossed_above(df['close'], df['lower']), 'bb1_buy'] = 1
        df.loc[qtpylib.crossed_above(df['rsi'], df['rsi_lower']), 'bb2_buy'] = 1
        df.loc[(df['bb1_buy'] == 1) & df['bb2_buy'] & (df['qqe_buy'] == 1), 'exit_short'] = 1
        return df


    def leverage(self,pair: str,current_time: datetime,current_rate: float,proposed_leverage: float,max_leverage: float,entry_tag: Optional[str],side: str,**kwargs) -> float:
        """
        Customize leverage for each new trade. This method is only called in futures mode.
        """
        return self.my_leverage
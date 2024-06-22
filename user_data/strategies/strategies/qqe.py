import numpy as np
import pandas as pd
from pandas import DataFrame
from datetime import datetime
from typing import Optional, Union
from freqtrade.strategy import BooleanParameter, CategoricalParameter, DecimalParameter, IntParameter, IStrategy, merge_informative_pair
import talib.abstract as ta
import pandas_ta as pta
from technical import qtpylib

class qqe(IStrategy):
    INTERFACE_VERSION = 3
    timeframe = '5m'
    can_short: bool = True
    minimal_roi = {'60': 0.01, '30': 0.02, '0': 0.04}
    stoploss = -0.1
    trailing_stop = False
    process_only_new_candles = False
    use_exit_signal = True
    exit_profit_only = False
    ignore_roi_if_entry_signal = False
    startup_candle_count: int = 200
    order_types = {'entry': 'limit', 'exit': 'limit', 'stoploss': 'market', 'stoploss_on_exchange': False}
    order_time_in_force = {'entry': 'GTC', 'exit': 'GTC'}
    bb_len = IntParameter(10, 30, default=20, optimize=True)
    bb_ev = DecimalParameter(1.5, 2.5, default=2, optimize=True)
    qqe_len = IntParameter(10, 30, default=20, optimize=True)
    qqe_smooth = IntParameter(2, 10, default=5, optimize=True)
    qqe_factor = DecimalParameter(3, 10, default=4.5, decimals=2)

    def populate_indicators(self, dataframe: DataFrame, metadata: dict) -> DataFrame:
        qqe = pta.qqe(close=dataframe['close'], length=20, smooth=5, factor=4)
        dataframe['qqe'] = qqe[qqe.columns[0]]
        dataframe['qqel'] = qqe[qqe.columns[2]]
        dataframe['qqes'] = qqe[qqe.columns[3]]
        bb = pta.bbands(dataframe['close'], length=20, std=2)
        dataframe['bb_lower'] = bb[bb.columns[0]]
        dataframe['bb_middle'] = bb[bb.columns[1]]
        dataframe['bb_upper'] = bb[bb.columns[2]]
        dataframe['rsi'] = pta.rsi(close=dataframe['close'], length=14)
        rsi_bb = pta.bbands(close=dataframe['rsi'], length=20, std=2)
        dataframe['rsi_lower'] = rsi_bb[rsi_bb.columns[0]]
        dataframe['rsi_middle'] = rsi_bb[rsi_bb.columns[1]]
        dataframe['rsi_upper'] = rsi_bb[rsi_bb.columns[2]]
        dataframe = dataframe.fillna(0)
        return dataframe

    def populate_entry_trend(self, dataframe: DataFrame, metadata: dict) -> DataFrame:
        dataframe.loc[qtpylib.crossed_above(dataframe['close'], dataframe['bb_lower']) & qtpylib.crossed_above(dataframe['rsi'], dataframe['rsi_upper']) & (dataframe['qqel'] != 0 and dataframe['qqel'].shift(1) == 0) & (dataframe['volume'] > 0), 'enter_long'] = 1
        dataframe.loc[qtpylib.crossed_below(dataframe['close'], dataframe['bb_upper']) & qtpylib.crossed_below(dataframe['rsi'], dataframe['rsi_upper']) & (dataframe['qqes'] != 0 and dataframe['qqes'].shift(1) == 0) & (dataframe['volume'] > 0), 'enter_short'] = 1
        return dataframe

    def populate_exit_trend(self, dataframe: DataFrame, metadata: dict) -> DataFrame:
        dataframe.loc[qtpylib.crossed_below(dataframe['close'], dataframe['bb_upper']) & qtpylib.crossed_below(dataframe['rsi'], dataframe['rsi_upper']) & (dataframe['volume'] > 0), 'exit_long'] = 1
        dataframe.loc[qtpylib.crossed_above(dataframe['close'], dataframe['bb_lower']) & qtpylib.crossed_above(dataframe['rsi'], dataframe['rsi_upper']) & (dataframe['volume'] > 0), 'exit_short'] = 1
        return dataframe

    def leverage(self, pair: str, current_time: datetime, current_rate: float, proposed_leverage: float, max_leverage: float, entry_tag: Optional[str], side: str, **kwargs) -> float:
        """
        Customize leverage for each new trade. This method is only called in futures mode.

        :param pair: Pair that's currently analyzed
        :param current_time: datetime object, containing the current datetime
        :param current_rate: Rate, calculated based on pricing settings in exit_pricing.
        :param proposed_leverage: A leverage proposed by the bot.
        :param max_leverage: Max leverage allowed on this pair
        :param entry_tag: Optional entry_tag (buy_tag) if provided with the buy signal.
        :param side: 'long' or 'short' - indicating the direction of the proposed trade
        :return: A leverage amount, which is between 1.0 and max_leverage.
        """
        return 10.0
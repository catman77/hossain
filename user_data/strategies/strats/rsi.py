# pragma pylint: disable=missing-docstring, invalid-name, pointless-string-statement
# flake8: noqa: F401
# --- Do not remove these libs ---
import numpy as np  # noqa
import pandas as pd  # noqa
from pandas import DataFrame
from freqtrade.strategy import BooleanParameter, CategoricalParameter, DecimalParameter, IStrategy, IntParameter
# --------------------------------
# Add your lib to import here
import talib.abstract as ta
import pandas_ta as pta
import freqtrade.vendor.qtpylib.indicators as qtpylib

class RSI(IStrategy):

    INTERFACE_VERSION = 3
    # Optimal timeframe for the strategy.
    timeframe = '5m'
    can_short = True
    # Minimal ROI designed for the strategy.
    # This attribute will be overridden if the config file contains "minimal_roi".
    minimal_roi = {'0': 0.0}
    # Optimal stoploss designed for the strategy.
    # This attribute will be overridden if the config file contains "stoploss".
    stoploss = -0.15
    # Trailing stoploss
    trailing_stop = False
    # trailing_only_offset_is_reached = False
    # trailing_stop_positive = 0.01
    # trailing_stop_positive_offset = 0.0  # Disabled / not configured
    # Run "populate_indicators()" only for new candle.
    process_only_new_candles = False
    # These values can be overridden in the "ask_strategy" section in the config.
    use_exit_signal = True
    exit_profit_only = False
    ignore_roi_if_entry_signal = False
    # Number of candles the strategy requires before producing valid signals
    startup_candle_count: int = 30
    # Strategy parameters
    buy_rsi = IntParameter(10, 40, default=30, space='buy')
    sell_rsi = IntParameter(60, 90, default=70, space='sell')
    # Optional order type mapping.
    order_types = {'entry': 'limit', 'exit': 'limit', 'stoploss': 'market', 'stoploss_on_exchange': False}
    # Optional order time in force.
    order_time_in_force = {'entry': 'gtc', 'exit': 'gtc'}

    @property
    def plot_config(self):
        # Main plot indicators (Moving averages, ...)
        # Subplots - each dict defines one additional plot
        return {'main_plot': {'bb_upperband': {'color': 'grey'}, 'bb_middleband': {'color': 'red'}, 'bb_lowerband': {'color': 'grey'}}, 'subplots': {'RSI': {'rsi': {'color': 'blue'}, 'overbought': {'color': 'red'}, 'oversold': {'color': 'green'}}}}

    def populate_indicators(self, dataframe: DataFrame, metadata: dict) -> DataFrame:

        dataframe['rsi'] = ta.RSI(dataframe)
        dataframe['overbought'] = 70
        dataframe['oversold'] = 30

        bollinger = qtpylib.bollinger_bands(qtpylib.typical_price(dataframe), window=20, stds=2)
        dataframe['bb_lowerband'] = bollinger['lower']
        dataframe['bb_middleband'] = bollinger['mid']
        dataframe['bb_upperband'] = bollinger['upper']
        dataframe['bb_percent'] = (dataframe['close'] - dataframe['bb_lowerband']) / (dataframe['bb_upperband'] - dataframe['bb_lowerband'])
        dataframe['bb_width'] = (dataframe['bb_upperband'] - dataframe['bb_lowerband']) / dataframe['bb_middleband']
        return dataframe

    def populate_entry_trend(self, dataframe: DataFrame, metadata: dict) -> DataFrame:
        dataframe.loc[(dataframe['rsi'] < 30) & (dataframe['close'] < dataframe['bb_lowerband']) & (dataframe['volume'] > 0), 'enter_long'] = 1

        dataframe.loc[(dataframe['rsi'] > 70) & (dataframe['volume'] > 0), 'enter_short'] = 1
        return dataframe

    def populate_exit_trend(self, dataframe: DataFrame, metadata: dict) -> DataFrame:

        dataframe.loc[(dataframe['rsi'] > 70) & (dataframe['volume'] > 0), 'exit_long'] = 1
        dataframe.loc[(dataframe['rsi'] < 30) & (dataframe['close'] < dataframe['bb_lowerband']) & (dataframe['volume'] > 0), 'enter_short'] = 1

        return dataframe
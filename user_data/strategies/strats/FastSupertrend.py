import logging
from numpy.lib import math
from freqtrade.strategy.interface import IStrategy
from freqtrade.strategy.hyper import IntParameter
from pandas import DataFrame
import talib.abstract as ta
import numpy as np
import time
import pandas as pd

class FastSupertrend(IStrategy):

    buy_params = {
        "buy_m1": 4,
        "buy_m2": 7,
        "buy_m3": 1,
        "buy_p1": 8,
        "buy_p2": 9,
        "buy_p3": 8,
    }

    sell_params = {
        "sell_m1": 1,
        "sell_m2": 3,
        "sell_m3": 6,
        "sell_p1": 16,
        "sell_p2": 18,
        "sell_p3": 18,
    }

    # ROI table:
    minimal_roi = {
        "0": 0.087,
        "372": 0.058,
        "861": 0.029,
        "2221": 0
    }

    # Stoploss:
    stoploss = -0.265

    # Trailing stop:
    trailing_stop = True
    trailing_stop_positive = 0.05
    trailing_stop_positive_offset = 0.144
    trailing_only_offset_is_reached = False

    timeframe = '1h'

    startup_candle_count = 18

    buy_m1 = IntParameter(1, 7, default=4)
    buy_m2 = IntParameter(1, 7, default=4)
    buy_m3 = IntParameter(1, 7, default=4)
    buy_p1 = IntParameter(7, 21, default=14)
    buy_p2 = IntParameter(7, 21, default=14)
    buy_p3 = IntParameter(7, 21, default=14)

    sell_m1 = IntParameter(1, 7, default=4)
    sell_m2 = IntParameter(1, 7, default=4)
    sell_m3 = IntParameter(1, 7, default=4)
    sell_p1 = IntParameter(7, 21, default=14)
    sell_p2 = IntParameter(7, 21, default=14)
    sell_p3 = IntParameter(7, 21, default=14)

    def populate_indicators(self, dataframe: DataFrame, metadata: dict) -> DataFrame:
        for multiplier in self.buy_m1.range:
            for period in self.buy_p1.range:
                dataframe[f'supertrend_1_buy_{multiplier}_{period}'] = self.supertrend(dataframe, multiplier, period)['STX']

        for multiplier in self.buy_m2.range:
            for period in self.buy_p2.range:
                dataframe[f'supertrend_2_buy_{multiplier}_{period}'] = self.supertrend(dataframe, multiplier, period)['STX']

        for multiplier in self.buy_m3.range:
            for period in self.buy_p3.range:
                dataframe[f'supertrend_3_buy_{multiplier}_{period}'] = self.supertrend(dataframe, multiplier, period)['STX']

        for multiplier in self.sell_m1.range:
            for period in self.sell_p1.range:
                dataframe[f'supertrend_1_sell_{multiplier}_{period}'] = self.supertrend(dataframe, multiplier, period)['STX']

        for multiplier in self.sell_m2.range:
            for period in self.sell_p2.range:
                dataframe[f'supertrend_2_sell_{multiplier}_{period}'] = self.supertrend(dataframe, multiplier, period)['STX']

        for multiplier in self.sell_m3.range:
            for period in self.sell_p3.range:
                dataframe[f'supertrend_3_sell_{multiplier}_{period}'] = self.supertrend(dataframe, multiplier, period)['STX']

        return dataframe

    def populate_buy_trend(self, dataframe: DataFrame, metadata: dict) -> DataFrame:
        dataframe.loc[
            (
               (dataframe[f'supertrend_1_buy_{self.buy_m1.value}_{self.buy_p1.value}'] == 'up') &
               (dataframe[f'supertrend_2_buy_{self.buy_m2.value}_{self.buy_p2.value}'] == 'up') &
               (dataframe[f'supertrend_3_buy_{self.buy_m3.value}_{self.buy_p3.value}'] == 'up') & # The three indicators are 'up' for the current candle
               (dataframe['volume'] > 0) # There is at least some trading volume
        ),
            'buy'] = 1

        return dataframe

    def populate_sell_trend(self, dataframe: DataFrame, metadata: dict) -> DataFrame:
        dataframe.loc[
            (
               (dataframe[f'supertrend_1_sell_{self.sell_m1.value}_{self.sell_p1.value}'] == 'down') &
               (dataframe[f'supertrend_2_sell_{self.sell_m2.value}_{self.sell_p2.value}'] == 'down') &
               (dataframe[f'supertrend_3_sell_{self.sell_m3.value}_{self.sell_p3.value}'] == 'down') & # The three indicators are 'down' for the current candle
               (dataframe['volume'] > 0) # There is at least some trading volume
            ),
            'sell'] = 1

        return dataframe

    """
        Supertrend Indicator; adapted for freqtrade
        from: https://github.com/freqtrade/freqtrade-strategies/issues/30
    """
    def supertrend(self, dataframe: DataFrame, multiplier, period):
        start_time = time.time()

        df = dataframe.copy()
        last_row = dataframe.tail(1).index.item()

        df['TR'] = ta.TRANGE(df)
        df['ATR'] = ta.SMA(df['TR'], period)

        st = 'ST_' + str(period) + '_' + str(multiplier)
        stx = 'STX_' + str(period) + '_' + str(multiplier)

        # Compute basic upper and lower bands
        BASIC_UB = ((df['high'] + df['low']) / 2 + multiplier * df['ATR']).values
        BASIC_LB = ((df['high'] + df['low']) / 2 - multiplier * df['ATR']).values
        FINAL_UB = np.zeros(last_row + 1)
        FINAL_LB = np.zeros(last_row + 1)
        ST = np.zeros(last_row + 1)
        CLOSE = df['close'].values

        # Compute final upper and lower bands
        for i in range(period, last_row):
            FINAL_UB[i] = BASIC_UB[i] if BASIC_UB[i] < FINAL_UB[i - 1] or CLOSE[i - 1] > FINAL_UB[i - 1] else FINAL_UB[i - 1]
            FINAL_LB[i] = BASIC_LB[i] if BASIC_LB[i] > FINAL_LB[i - 1] or CLOSE[i - 1] < FINAL_LB[i - 1] else FINAL_LB[i - 1]

        # Set the Supertrend value
        for i in range(period, last_row):
            ST[i] = FINAL_UB[i] if ST[i - 1] == FINAL_UB[i - 1] and CLOSE[i] <= FINAL_UB[i] else \
                    FINAL_LB[i] if ST[i - 1] == FINAL_UB[i - 1] and CLOSE[i] >  FINAL_UB[i] else \
                    FINAL_LB[i] if ST[i - 1] == FINAL_LB[i - 1] and CLOSE[i] >= FINAL_LB[i] else \
                    FINAL_UB[i] if ST[i - 1] == FINAL_LB[i - 1] and CLOSE[i] <  FINAL_LB[i] else 0.00
        df_ST = pd.DataFrame(ST, columns=[st])
        df = pd.concat([df, df_ST],axis=1)

        # Mark the trend direction up/down
        df[stx] = np.where((df[st] > 0.00), np.where((df['close'] < df[st]), 'down',  'up'), np.NaN)

        df.fillna(0, inplace=True)

        end_time = time.time()
        # print("total time taken this loop: ", end_time - start_time)

        return DataFrame(index=df.index, data={
            'ST' : df[st],
            'STX' : df[stx]
        })
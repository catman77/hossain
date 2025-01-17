# --- Do not remove these libs ---
import freqtrade.vendor.qtpylib.indicators as qtpylib
import logging
import math
import numpy as np
import talib.abstract as ta
import pandas_ta as pta
from freqtrade.persistence import Trade
from freqtrade.strategy.interface import IStrategy
from pandas import DataFrame, Series, DatetimeIndex, merge
from datetime import datetime, timedelta
from freqtrade.strategy import merge_informative_pair, CategoricalParameter, DecimalParameter, IntParameter, stoploss_from_open
from functools import reduce
from technical.indicators import RMI, zema
logger = logging.getLogger(__name__)
# --------------------------------

def ha_typical_price(bars):
    res = (bars['ha_high'] + bars['ha_low'] + bars['ha_close']) / 3.0
    return Series(index=bars.index, data=res)

def EWO(dataframe, ema_length=5, ema2_length=35):
    df = dataframe.copy()
    ema1 = ta.EMA(df, timeperiod=ema_length)
    ema2 = ta.EMA(df, timeperiod=ema2_length)
    emadif = (ema1 - ema2) / df['low'] * 100
    return emadif

def vwma(dataframe: DataFrame, length: int=10):
    pv = dataframe['close'] * dataframe['volume']
    vwma = Series(ta.SMA(pv, timeperiod=length) / ta.SMA(dataframe['volume'], timeperiod=length))
    return vwma

def moderi(dataframe: DataFrame, len_slow_ma: int=32) -> Series:
    slow_ma = Series(ta.EMA(vwma(dataframe, length=len_slow_ma), timeperiod=len_slow_ma))
    return slow_ma >= slow_ma.shift(1)  # we just need true & false for ERI trend

def williams_r(dataframe: DataFrame, period: int=14) -> Series:
    highest_high = dataframe['high'].rolling(center=False, window=period).max()
    lowest_low = dataframe['low'].rolling(center=False, window=period).min()
    WR = Series((highest_high - dataframe['close']) / (highest_high - lowest_low), name=f'{period} Williams %R')
    return WR * -100

def VWAPB(dataframe, window_size=20, num_of_std=1):
    df = dataframe.copy()
    df['vwap'] = qtpylib.rolling_vwap(df, window=window_size)
    rolling_std = df['vwap'].rolling(window=window_size).std()
    df['vwap_low'] = df['vwap'] - rolling_std * num_of_std
    df['vwap_high'] = df['vwap'] + rolling_std * num_of_std
    return (df['vwap_low'], df['vwap'], df['vwap_high'])

def top_percent_change(dataframe: DataFrame, length: int) -> float:
    if length == 0:
        return (dataframe['open'] - dataframe['close']) / dataframe['close']
    else:
        return (dataframe['open'].rolling(length).max() - dataframe['close']) / dataframe['close']

class RTR(IStrategy):
    INTERFACE_VERSION = 3

    buy_params = {'buy_pump_1_factor': 1.096, 'buy_pump_2_factor': 1.125, 'buy_threshold': 0.003, 'buy_bb_factor': 0.999, 'buy_bb_delta': 0.025, 'buy_bb_width': 0.095, 'buy_cci': -116, 'buy_cci_length': 25, 'buy_rmi': 49, 'buy_rmi_length': 17, 'buy_srsi_fk': 32, 'buy_closedelta': 12.148, 'buy_ema_diff': 0.022, 'buy_adx': 20, 'buy_fastd': 20, 'buy_fastk': 22, 'buy_ema_cofi': 0.98, 'buy_ewo_high': 4.179, 'buy_ema_high': 0.968, 'buy_ema_low': 0.935, 'buy_ewo': -5.001, 'buy_rsi': 23, 'buy_rsi_fast': 44, 'buy_ema_high_2': 1.087, 'buy_ema_low_2': 0.97, 'buy_no_trend_cti_4': -0.597, 'buy_no_trend_factor_4': 0.024, 'buy_no_trend_r14_4': -44.062, 'buy_V_bb_width_5': 0.063, 'buy_V_cti_5': -0.086, 'buy_V_mfi_5': 38.158, 'buy_V_r14_5': -41.493, 'buy_vwap_closedelta': 26.941, 'buy_vwap_closedelta_2': 20.099, 'buy_vwap_closedelta_3': 27.654, 'buy_vwap_cti': -0.087, 'buy_vwap_cti_2': -0.748, 'buy_vwap_cti_3': -0.2, 'buy_vwap_width': 1.308, 'buy_vwap_width_2': 3.212, 'buy_vwap_width_3': 0.49}

    sell_params = {'pHSL': -0.998, 'pPF_1': 0.019, 'pPF_2': 0.065, 'pSL_1': 0.019, 'pSL_2': 0.062, 'high_offset_2': 0.997, 'sell_cti_r_cti': 0.844, 'sell_cti_r_r': -19.99, 'sell_u_e_2_cmf': -0.0, 'sell_u_e_2_ema_close_delta': 0.016, 'sell_u_e_2_rsi': 10, 'sell_deadfish_profit': -0.063, 'sell_deadfish_bb_factor': 0.954, 'sell_deadfish_bb_width': 0.043, 'sell_deadfish_volume_factor': 2.37}
    # ROI
    minimal_roi = {'0': 0.1}
    # Optimal timeframe for the strategy
    timeframe = '5m'
    inf_1h = '1h'
    # Disabled
    stoploss = -0.998
    # Options
    use_custom_stoploss = True
    use_exit_signal = True
    process_only_new_candles = True
    startup_candle_count: int = 400
    ## Buy params
    is_optimize_dip = False
    buy_rmi = IntParameter(30, 50, default=35, optimize=is_optimize_dip)
    buy_cci = IntParameter(-135, -90, default=-133, optimize=is_optimize_dip)
    buy_srsi_fk = IntParameter(30, 50, default=25, optimize=is_optimize_dip)
    buy_cci_length = IntParameter(25, 45, default=25, optimize=is_optimize_dip)
    buy_rmi_length = IntParameter(8, 20, default=8, optimize=is_optimize_dip)
    is_optimize_break = False
    buy_bb_width = DecimalParameter(0.05, 0.2, default=0.15, optimize=is_optimize_break)
    buy_bb_delta = DecimalParameter(0.025, 0.08, default=0.04, optimize=is_optimize_break)
    is_optimize_local_dip = False
    buy_ema_diff = DecimalParameter(0.022, 0.027, default=0.025, optimize=is_optimize_local_dip)
    buy_bb_factor = DecimalParameter(0.99, 0.999, default=0.995, optimize=False)
    buy_closedelta = DecimalParameter(12.0, 18.0, default=15.0, optimize=is_optimize_local_dip)
    is_optimize_ewo = False
    buy_rsi_fast = IntParameter(35, 50, default=45, optimize=False)
    buy_rsi = IntParameter(15, 30, default=35, optimize=False)
    buy_ewo = DecimalParameter(-6.0, 5, default=-5.585, optimize=is_optimize_ewo)
    buy_ema_low = DecimalParameter(0.9, 0.99, default=0.942, optimize=is_optimize_ewo)
    buy_ema_high = DecimalParameter(0.95, 1.2, default=1.084, optimize=is_optimize_ewo)
    is_optimize_ewo_2 = False
    buy_ema_low_2 = DecimalParameter(0.96, 0.978, default=0.96, optimize=is_optimize_ewo_2)
    buy_ema_high_2 = DecimalParameter(1.05, 1.2, default=1.09, optimize=is_optimize_ewo_2)
    is_optimize_cofi = False
    buy_ema_cofi = DecimalParameter(0.96, 0.98, default=0.97, optimize=is_optimize_cofi)
    buy_fastk = IntParameter(20, 30, default=20, optimize=is_optimize_cofi)
    buy_fastd = IntParameter(20, 30, default=20, optimize=is_optimize_cofi)
    buy_adx = IntParameter(20, 30, default=30, optimize=is_optimize_cofi)
    buy_ewo_high = DecimalParameter(2, 12, default=3.553, optimize=is_optimize_cofi)
    is_optimize_vwap = False
    buy_vwap_width = DecimalParameter(0.05, 10.0, default=0.8, optimize=is_optimize_vwap)
    buy_vwap_closedelta = DecimalParameter(10.0, 30.0, default=15.0, optimize=is_optimize_vwap)
    buy_vwap_cti = DecimalParameter(-0.9, -0.0, default=-0.6, optimize=is_optimize_vwap)
    is_optimize_vwap_2 = False
    buy_vwap_width_2 = DecimalParameter(0.05, 10.0, default=0.8, optimize=is_optimize_vwap_2)
    buy_vwap_closedelta_2 = DecimalParameter(10.0, 30.0, default=15.0, optimize=is_optimize_vwap_2)
    buy_vwap_cti_2 = DecimalParameter(-0.9, -0.0, default=-0.6, optimize=is_optimize_vwap_2)
    is_optimize_vwap_3 = True
    buy_vwap_width_3 = DecimalParameter(0.05, 10.0, default=0.8, optimize=is_optimize_vwap_3)
    buy_vwap_closedelta_3 = DecimalParameter(10.0, 30.0, default=15.0, optimize=is_optimize_vwap_3)
    buy_vwap_cti_3 = DecimalParameter(-0.9, -0.0, default=-0.6, optimize=is_optimize_vwap_3)
    is_optimize_no_trend_4 = False
    buy_no_trend_factor_4 = DecimalParameter(0.01, 0.05, default=0.03, optimize=is_optimize_no_trend_4)
    buy_no_trend_cti_4 = DecimalParameter(-0.9, -0.0, default=-0.6, optimize=is_optimize_no_trend_4)
    buy_no_trend_r14_4 = DecimalParameter(-100, -44, default=-80, optimize=is_optimize_no_trend_4)
    is_optimize_V_5 = False
    buy_V_bb_width_5 = DecimalParameter(0.01, 0.1, default=0.01, optimize=is_optimize_V_5)
    buy_V_cti_5 = DecimalParameter(-0.95, -0.0, default=-0.6, optimize=is_optimize_V_5)
    buy_V_r14_5 = DecimalParameter(-100, 0, default=-60, optimize=is_optimize_V_5)
    buy_V_mfi_5 = DecimalParameter(10, 40, default=30, optimize=is_optimize_V_5)
    is_optimize_gumbo = False
    buy_gumbo_ema = DecimalParameter(0.9, 1.2, default=0.97, optimize=is_optimize_gumbo)
    buy_gumbo_ewo_low = DecimalParameter(-12.0, 5, default=-5.585, optimize=is_optimize_gumbo)
    buy_gumbo_cti = DecimalParameter(-0.9, -0.0, default=-0.5, optimize=is_optimize_gumbo)
    buy_gumbo_r14 = DecimalParameter(-100, -44, default=-60, optimize=is_optimize_gumbo)
    is_optimize_gumbo_protection = False
    buy_gumbo_tpct_0 = DecimalParameter(0.0, 0.25, default=0.131, decimals=2, optimize=is_optimize_gumbo_protection)
    buy_gumbo_tpct_3 = DecimalParameter(0.0, 0.25, default=0.131, decimals=2, optimize=is_optimize_gumbo_protection)
    buy_gumbo_tpct_9 = DecimalParameter(0.0, 0.25, default=0.131, decimals=2, optimize=is_optimize_gumbo_protection)
    # Buy params toggle
    buy_is_dip_enabled = CategoricalParameter([True, False], default=True, space='buy', optimize=False, load=True)
    buy_is_break_enabled = CategoricalParameter([True, False], default=True, space='buy', optimize=False, load=True)
    is_optimize_pump_1 = False
    buy_pump_1_factor = DecimalParameter(1.0, 1.25, default=1.1, optimize=is_optimize_pump_1)
    is_optimize_pump_2 = False
    buy_pump_2_factor = DecimalParameter(1.0, 1.2, default=1.1, optimize=is_optimize_pump_2)
    ## Sell params
    is_optimize_sell_offset = False
    high_offset_2 = DecimalParameter(0.99, 1.5, default=sell_params['high_offset_2'], space='sell', optimize=is_optimize_sell_offset)
    is_optimize_sell_u_e_2 = False
    sell_u_e_2_cmf = DecimalParameter(-0.4, 0.0, default=0.0, optimize=is_optimize_sell_u_e_2)
    sell_u_e_2_ema_close_delta = DecimalParameter(0.001, 0.027, default=0.024, optimize=is_optimize_sell_u_e_2)
    sell_u_e_2_rsi = IntParameter(10, 30, default=24, optimize=is_optimize_sell_u_e_2)
    is_optimize_deadfish = False
    sell_deadfish_bb_width = DecimalParameter(0.015, 0.05, default=0.05, optimize=is_optimize_deadfish)
    sell_deadfish_profit = DecimalParameter(-0.1, -0.05, default=-0.05, optimize=is_optimize_deadfish)
    sell_deadfish_bb_factor = DecimalParameter(0.9, 1.2, default=1.0, optimize=is_optimize_deadfish)
    sell_deadfish_volume_factor = DecimalParameter(1.5, 3, default=1.5, optimize=is_optimize_deadfish)
    is_optimize_cti_r = False
    sell_cti_r_cti = DecimalParameter(0.55, 1, default=0.5, optimize=is_optimize_cti_r)
    sell_cti_r_r = DecimalParameter(-15, 0, default=-20, optimize=is_optimize_cti_r)
    ## Trailing params
    # hard stoploss profit
    is_optimize_trailing = False
    pHSL = DecimalParameter(-0.2, -0.04, default=-0.08, decimals=3, space='sell', load=True, optimize=is_optimize_trailing)
    # profit threshold 1, trigger point, SL_1 is used
    pPF_1 = DecimalParameter(0.008, 0.02, default=0.016, decimals=3, space='sell', load=True, optimize=is_optimize_trailing)
    pSL_1 = DecimalParameter(0.008, 0.02, default=0.011, decimals=3, space='sell', load=True, optimize=is_optimize_trailing)
    # profit threshold 2, SL_2 is used
    pPF_2 = DecimalParameter(0.04, 0.1, default=0.08, decimals=3, space='sell', load=True, optimize=is_optimize_trailing)
    pSL_2 = DecimalParameter(0.02, 0.07, default=0.04, decimals=3, space='sell', load=True, optimize=is_optimize_trailing)
    ############################################################################

    def informative_pairs(self):
        pairs = self.dp.current_whitelist()
        informative_pairs = [(pair, '1h') for pair in pairs]
        return informative_pairs
    ############################################################################
    ## Custom Trailing stoploss ( credit to Perkmeister for this custom stoploss to help the strategy ride a green candle )

    def custom_stoploss(self, pair: str, trade: 'Trade', current_time: datetime, current_rate: float, current_profit: float, **kwargs) -> float:
        # hard stoploss profit
        HSL = self.pHSL.value
        PF_1 = self.pPF_1.value
        SL_1 = self.pSL_1.value
        PF_2 = self.pPF_2.value
        SL_2 = self.pSL_2.value
        # For profits between PF_1 and PF_2 the stoploss (sl_profit) used is linearly interpolated
        # between the values of SL_1 and SL_2. For all profits above PL_2 the sl_profit value
        # rises linearly with current profit, for profits below PF_1 the hard stoploss profit is used.
        if current_profit > PF_2:
            sl_profit = SL_2 + (current_profit - PF_2)
        elif current_profit > PF_1:
            sl_profit = SL_1 + (current_profit - PF_1) * (SL_2 - SL_1) / (PF_2 - PF_1)
        else:
            sl_profit = HSL
        # Only for hyperopt invalid return
        if sl_profit >= current_profit:
            return -0.99
        return stoploss_from_open(sl_profit, current_profit)

    def custom_exit(self, pair: str, trade: 'Trade', current_time: 'datetime', current_rate: float, current_profit: float, **kwargs):
        dataframe, _ = self.dp.get_analyzed_dataframe(pair, self.timeframe)
        last_candle = dataframe.iloc[-1]
        previous_candle_1 = dataframe.iloc[-2]
        previous_candle_2 = dataframe.iloc[-3]
        max_profit = (trade.max_rate - trade.open_rate) / trade.open_rate
        max_loss = (trade.open_rate - trade.min_rate) / trade.min_rate
        enter_tag = 'empty'
        if hasattr(trade, 'enter_tag') and trade.enter_tag is not None:
            enter_tag = trade.enter_tag
        # sell cti_r
        if 0.012 > current_profit >= 0.0:
            if last_candle['cti'] > self.sell_cti_r_cti.value and last_candle['r_14'] > self.sell_cti_r_r.value:
                return f'sell_profit_cti_r_0_1( {enter_tag})'
        # main sell
        if current_profit > 0.02:
            if last_candle['momdiv_sell_1h'] == True:
                return f'signal_profit_q_momdiv_1h( {enter_tag})'
            if last_candle['momdiv_sell'] == True:
                return f'signal_profit_q_momdiv( {enter_tag})'
            if last_candle['momdiv_coh'] == True:
                return f'signal_profit_q_momdiv_coh( {enter_tag})'
            if last_candle['cti_40_1h'] > 0.844 and last_candle['r_84_1h'] > -20:
                return f'signal_profit_cti_r( {enter_tag})'
        # sell quick
        if 0.06 > current_profit > 0.02 and last_candle['rsi'] > 80.0:
            return f'signal_profit_q_1( {enter_tag})'
        if 0.06 > current_profit > 0.02 and last_candle['cti'] > 0.95:
            return f'signal_profit_q_2( {enter_tag})'
        # sell recover
        if max_loss > 0.06 and 0.05 > current_profit > 0.01 and (last_candle['rsi'] < 46):
            return f'signal_profit_r_1( {enter_tag})'
        # sell offset
        if current_profit > 0.005 and last_candle['close'] > last_candle['sma_9'] and (last_candle['close'] > last_candle['ema_24'] * self.high_offset_2.value) and (last_candle['rsi'] > 50) and (last_candle['rsi_fast'] > last_candle['rsi_slow']):
            return f'sell_offset( {enter_tag})'
        # sell vwap dump
        if current_profit > 0.005 and last_candle['ema_vwap_diff_50'] < 0.012:
            return f'sell_vwap_dump( {enter_tag})'
        # stoploss
        if current_profit < -0.025 and last_candle['close'] < last_candle['ema_200'] and (last_candle['cmf'] < self.sell_u_e_2_cmf.value) and ((last_candle['ema_200'] - last_candle['close']) / last_candle['close'] < self.sell_u_e_2_ema_close_delta.value) and (last_candle['rsi'] > previous_candle_1['rsi']) and (last_candle['rsi'] > last_candle['rsi_1h'] + self.sell_u_e_2_rsi.value):
            return f'sell_stoploss_u_e_2( {enter_tag})'
        # stoploss - deadfish
        if current_profit < self.sell_deadfish_profit.value and last_candle['close'] < last_candle['ema_200'] and (last_candle['bb_width'] < self.sell_deadfish_bb_width.value) and (last_candle['close'] > last_candle['bb_middleband2'] * self.sell_deadfish_bb_factor.value) and (last_candle['volume_mean_12'] < last_candle['volume_mean_24'] * self.sell_deadfish_volume_factor.value):
            return f'sell_stoploss_deadfish( {enter_tag})'
    ############################################################################

    def populate_indicators(self, dataframe: DataFrame, metadata: dict) -> DataFrame:
        assert self.dp, 'DataProvider is required for multiple timeframes.'
        bollinger2 = qtpylib.bollinger_bands(qtpylib.typical_price(dataframe), window=20, stds=2)
        dataframe['bb_lowerband2'] = bollinger2['lower']
        dataframe['bb_middleband2'] = bollinger2['mid']
        dataframe['bb_upperband2'] = bollinger2['upper']
        bollinger3 = qtpylib.bollinger_bands(qtpylib.typical_price(dataframe), window=20, stds=3)
        dataframe['bb_lowerband3'] = bollinger3['lower']
        dataframe['bb_middleband3'] = bollinger3['mid']
        dataframe['bb_upperband3'] = bollinger3['upper']
        ### Other checks
        dataframe['bb_width'] = (dataframe['bb_upperband2'] - dataframe['bb_lowerband2']) / dataframe['bb_middleband2']
        dataframe['bb_delta'] = (dataframe['bb_lowerband2'] - dataframe['bb_lowerband3']) / dataframe['bb_lowerband2']
        dataframe['bb_bottom_cross'] = qtpylib.crossed_below(dataframe['close'], dataframe['bb_lowerband3']).astype('int')
        # CCI hyperopt
        for val in self.buy_cci_length.range:
            dataframe[f'cci_length_{val}'] = ta.CCI(dataframe, val)
        dataframe['cci'] = ta.CCI(dataframe, 26)
        dataframe['cci_long'] = ta.CCI(dataframe, 170)
        # RMI hyperopt
        for val in self.buy_rmi_length.range:
            dataframe[f'rmi_length_{val}'] = RMI(dataframe, length=val, mom=4)
        #dataframe['rmi'] = RMI(dataframe, length=8, mom=4)
        # SRSI hyperopt ?
        stoch = ta.STOCHRSI(dataframe, 15, 20, 2, 2)
        dataframe['srsi_fk'] = stoch['fastk']
        dataframe['srsi_fd'] = stoch['fastd']
        # BinH
        dataframe['closedelta'] = (dataframe['close'] - dataframe['close'].shift()).abs()
        # SMA
        dataframe['sma_15'] = ta.SMA(dataframe, timeperiod=15)
        dataframe['sma_30'] = ta.SMA(dataframe, timeperiod=30)
        # CTI
        dataframe['cti'] = pta.cti(dataframe['close'], length=20)
        # CMF
        dataframe['cmf'] = chaikin_money_flow(dataframe, 20)
        # MFI
        dataframe['mfi'] = ta.MFI(dataframe)
        # EMA
        dataframe['ema_8'] = ta.EMA(dataframe, timeperiod=8)
        dataframe['ema_12'] = ta.EMA(dataframe, timeperiod=12)
        dataframe['ema_13'] = ta.EMA(dataframe, timeperiod=13)
        dataframe['ema_16'] = ta.EMA(dataframe, timeperiod=16)
        dataframe['ema_24'] = ta.EMA(dataframe, timeperiod=24)
        dataframe['ema_26'] = ta.EMA(dataframe, timeperiod=26)
        dataframe['ema_50'] = ta.EMA(dataframe, timeperiod=50)
        dataframe['hma_50'] = qtpylib.hull_moving_average(dataframe['close'], window=50)
        dataframe['ema_100'] = ta.EMA(dataframe, timeperiod=100)
        dataframe['ema_200'] = ta.EMA(dataframe, timeperiod=200)
        # SMA
        dataframe['sma_9'] = ta.SMA(dataframe, timeperiod=9)
        dataframe['sma_15'] = ta.SMA(dataframe, timeperiod=15)
        dataframe['sma_21'] = ta.SMA(dataframe, timeperiod=21)
        # VWAP
        vwap_low, vwap, vwap_high = VWAPB(dataframe, 20, 1)
        dataframe['vwap_upperband'] = vwap_high
        dataframe['vwap_middleband'] = vwap
        dataframe['vwap_lowerband'] = vwap_low
        dataframe['vwap_width'] = (dataframe['vwap_upperband'] - dataframe['vwap_lowerband']) / dataframe['vwap_middleband'] * 100
        # RSI
        dataframe['rsi'] = ta.RSI(dataframe, timeperiod=14)
        dataframe['rsi_fast'] = ta.RSI(dataframe, timeperiod=4)
        dataframe['rsi_slow'] = ta.RSI(dataframe, timeperiod=20)
        dataframe['rsi_84'] = ta.RSI(dataframe, timeperiod=84)
        dataframe['rsi_112'] = ta.RSI(dataframe, timeperiod=112)
        # Elliot
        dataframe['EWO'] = EWO(dataframe, 50, 200)
        # Cofi
        stoch_fast = ta.STOCHF(dataframe, 5, 3, 0, 3, 0)
        dataframe['fastd'] = stoch_fast['fastd']
        dataframe['fastk'] = stoch_fast['fastk']
        dataframe['adx'] = ta.ADX(dataframe)
        # Heiken Ashi
        heikinashi = qtpylib.heikinashi(dataframe)
        dataframe['ha_open'] = heikinashi['open']
        dataframe['ha_close'] = heikinashi['close']
        dataframe['ha_high'] = heikinashi['high']
        dataframe['ha_low'] = heikinashi['low']
        ## BB 40
        bollinger2_40 = qtpylib.bollinger_bands(ha_typical_price(dataframe), window=40, stds=2)
        dataframe['bb_lowerband2_40'] = bollinger2_40['lower']
        dataframe['bb_middleband2_40'] = bollinger2_40['mid']
        dataframe['bb_upperband2_40'] = bollinger2_40['upper']
        # ClucHA
        dataframe['bb_delta_cluc'] = (dataframe['bb_middleband2_40'] - dataframe['bb_lowerband2_40']).abs()
        dataframe['ha_closedelta'] = (dataframe['ha_close'] - dataframe['ha_close'].shift()).abs()
        dataframe['tail'] = (dataframe['ha_close'] - dataframe['ha_low']).abs()
        dataframe['ema_slow'] = ta.EMA(dataframe['ha_close'], timeperiod=50)
        dataframe['rocr'] = ta.ROCR(dataframe['ha_close'], timeperiod=28)
        # Williams %R
        dataframe['r_14'] = williams_r(dataframe, period=14)
        # Volume
        dataframe['volume_mean_4'] = dataframe['volume'].rolling(4).mean().shift(1)
        dataframe['volume_mean_12'] = dataframe['volume'].rolling(12).mean().shift(1)
        dataframe['volume_mean_24'] = dataframe['volume'].rolling(24).mean().shift(1)
        # Diff
        dataframe['ema_vwap_diff_50'] = (dataframe['ema_50'] - dataframe['vwap_lowerband']) / dataframe['ema_50']
        # Dip Protection
        dataframe['tpct_change_1'] = top_percent_change(dataframe, 1)
        dataframe['tpct_change_2'] = top_percent_change(dataframe, 2)
        dataframe['tpct_change_4'] = top_percent_change(dataframe, 4)
        # MOMDIV
        mom = momdiv(dataframe)
        dataframe['momdiv_buy'] = mom['momdiv_buy']
        dataframe['momdiv_sell'] = mom['momdiv_sell']
        dataframe['momdiv_coh'] = mom['momdiv_coh']
        dataframe['momdiv_col'] = mom['momdiv_col']
        # Modified Elder Ray Index
        dataframe['moderi_96'] = moderi(dataframe, 96)
        ############################################################################
        # 1h tf
        inf_tf = '1h'
        informative = self.dp.get_pair_dataframe(pair=metadata['pair'], timeframe=inf_tf)
        # Heikin Ashi
        inf_heikinashi = qtpylib.heikinashi(informative)
        informative['ha_close'] = inf_heikinashi['close']
        informative['rocr'] = ta.ROCR(informative['ha_close'], timeperiod=168)
        # Bollinger bands
        bollinger2 = qtpylib.bollinger_bands(qtpylib.typical_price(informative), window=20, stds=2)
        informative['bb_lowerband2'] = bollinger2['lower']
        informative['bb_middleband2'] = bollinger2['mid']
        informative['bb_upperband2'] = bollinger2['upper']
        informative['bb_width'] = (informative['bb_upperband2'] - informative['bb_lowerband2']) / informative['bb_middleband2']
        # RSI
        informative['rsi'] = ta.RSI(informative, timeperiod=14)
        informative['rsi_28'] = ta.RSI(informative, timeperiod=28)
        informative['rsi_42'] = ta.RSI(informative, timeperiod=42)
        # EMA
        informative['ema_20'] = ta.EMA(informative, timeperiod=20)
        informative['ema_26'] = ta.EMA(informative, timeperiod=26)
        informative['ema_200'] = ta.EMA(informative, timeperiod=200)
        # Williams %R
        informative['r_84'] = williams_r(informative, period=84)
        # CTI
        informative['cti_40'] = pta.cti(informative['close'], length=40)
        # MOMDIV
        mom = momdiv(informative)
        informative['momdiv_buy'] = mom['momdiv_buy']
        informative['momdiv_sell'] = mom['momdiv_sell']
        informative['momdiv_coh'] = mom['momdiv_coh']
        informative['momdiv_col'] = mom['momdiv_col']
        dataframe = merge_informative_pair(dataframe, informative, self.timeframe, inf_tf, ffill=True)
        return dataframe

    def populate_entry_trend(self, dataframe: DataFrame, metadata: dict) -> DataFrame:
        conditions = []
        dataframe.loc[:, 'enter_tag'] = ''
        ############################################################################
        # Utils
        is_pump_1 = dataframe['close'].rolling(48).max() >= dataframe['close'] * self.buy_pump_1_factor.value
        pump_protection_strict = (dataframe['close'].rolling(48).max() >= dataframe['close'] * 1.125) & (dataframe['close'].rolling(288).max() >= dataframe['close'] * 1.225)
        pump_protection_loose = (dataframe['close'].rolling(48).max() >= dataframe['close'] * 1.05) & (dataframe['close'].rolling(288).max() >= dataframe['close'] * 1.125)
        is_pump_4 = (dataframe['close'].rolling(48).max() >= dataframe['close'] * 1.075) & (dataframe['close'].rolling(288).max() >= dataframe['close'] * 1.17)
        is_crash_1 = (dataframe['tpct_change_1'] < 0.08) & (dataframe['tpct_change_2'] < 0.08)
        is_crash_2 = (dataframe['tpct_change_1'] < 0.06) & (dataframe['tpct_change_2'] < 0.06)
        is_crash_3 = (dataframe['tpct_change_1'] < 0.055) & (dataframe['tpct_change_2'] < 0.055)
        rsi_check = (dataframe['rsi_84'] < 60) & (dataframe['rsi_112'] < 60)
        min_EWO_check = dataframe['EWO'] > -5.585
        max_EWO_check = dataframe['EWO'] < 10.6
        ############################################################################
        if self.buy_is_dip_enabled.value:
            is_dip = (dataframe[f'rmi_length_{self.buy_rmi_length.value}'] < self.buy_rmi.value) & (dataframe[f'cci_length_{self.buy_cci_length.value}'] <= self.buy_cci.value) & (dataframe['srsi_fk'] < self.buy_srsi_fk.value)
        if self.buy_is_break_enabled.value:  #"buy_bb_delta": 0.025 0.036
            #"buy_bb_width": 0.095 0.133
            # from BinH
            is_break = (dataframe['bb_delta'] > self.buy_bb_delta.value) & (dataframe['bb_width'] > self.buy_bb_width.value) & (dataframe['closedelta'] > dataframe['close'] * self.buy_closedelta.value / 1000) & (dataframe['close'] < dataframe['bb_lowerband3'] * self.buy_bb_factor.value) & is_crash_1  # from NFI next gen
        is_local_uptrend = (dataframe['ema_26'] > dataframe['ema_12']) & (dataframe['ema_26'] - dataframe['ema_12'] > dataframe['open'] * self.buy_ema_diff.value) & (dataframe['ema_26'].shift() - dataframe['ema_12'].shift() > dataframe['open'] / 100) & (dataframe['close'] < dataframe['bb_lowerband2'] * self.buy_bb_factor.value) & (dataframe['closedelta'] > dataframe['close'] * self.buy_closedelta.value / 1000) & (dataframe['EWO'] < 4) & (dataframe['EWO'] > -2.5)  # from SMA offset
        is_ewo = (dataframe['rsi_fast'] < self.buy_rsi_fast.value) & (dataframe['close'] < dataframe['ema_8'] * self.buy_ema_low.value) & (dataframe['EWO'] > self.buy_ewo.value) & (dataframe['close'] < dataframe['ema_16'] * self.buy_ema_high.value) & (dataframe['rsi'] < self.buy_rsi.value)
        is_ewo_2 = (dataframe['rsi_fast'] < self.buy_rsi_fast.value) & (dataframe['close'] < dataframe['ema_8'] * self.buy_ema_low_2.value) & (dataframe['EWO'] > self.buy_ewo_high.value) & (dataframe['close'] < dataframe['ema_16'] * self.buy_ema_high_2.value) & (dataframe['rsi'] < self.buy_rsi.value) & rsi_check
        is_vwap = (dataframe['close'] < dataframe['vwap_lowerband']) & (dataframe['vwap_width'] > self.buy_vwap_width.value) & (dataframe['closedelta'] > dataframe['close'] * self.buy_vwap_closedelta.value / 1000) & (dataframe['cti'] < self.buy_vwap_cti.value) & (dataframe['EWO'] > 8) & rsi_check & pump_protection_strict
        is_vwap_2 = (dataframe['close'] < dataframe['vwap_lowerband']) & (dataframe['vwap_width'] > self.buy_vwap_width_2.value) & (dataframe['closedelta'] > dataframe['close'] * self.buy_vwap_closedelta_2.value / 1000) & (dataframe['cti'] < self.buy_vwap_cti_2.value) & (dataframe['EWO'] > 4) & (dataframe['EWO'] < 8) & rsi_check & pump_protection_strict
        is_vwap_3 = (dataframe['close'] < dataframe['vwap_lowerband']) & (dataframe['vwap_width'] > self.buy_vwap_width_3.value) & (dataframe['closedelta'] > dataframe['close'] * self.buy_vwap_closedelta_3.value / 1000) & (dataframe['cti'] < self.buy_vwap_cti_3.value) & (dataframe['EWO'] < 4) & (dataframe['EWO'] > -2.5) & (dataframe['rsi_28_1h'] < 46) & rsi_check & pump_protection_loose
        is_VWAP = (dataframe['close'] < dataframe['vwap_lowerband']) & (dataframe['tpct_change_1'] > 0.04) & (dataframe['cti'] < -0.8) & (dataframe['rsi'] < 35) & rsi_check
        is_no_trend_4 = (dataframe['ema_26'] > dataframe['ema_12']) & (dataframe['ema_26'] - dataframe['ema_12'] > dataframe['open'] * self.buy_no_trend_factor_4.value) & (dataframe['ema_26'].shift() - dataframe['ema_12'].shift() > dataframe['open'] / 100) & (dataframe['cti'] < self.buy_no_trend_cti_4.value) & (dataframe['r_14'] < self.buy_no_trend_r14_4.value) & (dataframe['EWO'] < -4) & min_EWO_check & rsi_check
        # Really Bear, don't engage until dump over
        is_V_5 = (dataframe['bb_width'] > self.buy_V_bb_width_5.value) & (dataframe['cti'] < self.buy_V_cti_5.value) & (dataframe['r_14'] < self.buy_V_r14_5.value) & (dataframe['mfi'] < self.buy_V_mfi_5.value) & (dataframe['ema_vwap_diff_50'] > 0.215) & (dataframe['EWO'] < -10) & rsi_check
        is_insta = (dataframe['bb_width_1h'] > 0.13) & (dataframe['r_14'] < -50) & (dataframe['r_84_1h'] < -69) & (dataframe['cti'] < -0.84) & (dataframe['cti_40_1h'] < -0.73) & (dataframe['close'].rolling(48).max() >= dataframe['close'] * 1.1)
        # NFI quick mode
        is_nfi_32 = (dataframe['rsi_slow'] < dataframe['rsi_slow'].shift(1)) & (dataframe['rsi_fast'] < 46) & (dataframe['rsi'] > 19) & (dataframe['close'] < dataframe['sma_15'] * 0.942) & (dataframe['cti'] < -0.86)
        is_nfi_33 = (dataframe['close'] < dataframe['ema_13'] * 0.978) & (dataframe['EWO'] > 8) & (dataframe['cti'] < -0.88) & (dataframe['rsi'] < 32) & (dataframe['r_14'] < -98.0) & (dataframe['volume'] < dataframe['volume_mean_4'] * 2.5)
        is_nfix_39 = (dataframe['ema_200'] > dataframe['ema_200'].shift(12) * 1.01) & (dataframe['ema_200'] > dataframe['ema_200'].shift(48) * 1.07) & dataframe['bb_lowerband2_40'].shift().gt(0) & dataframe['bb_delta_cluc'].gt(dataframe['close'] * 0.056) & dataframe['closedelta'].gt(dataframe['close'] * 0.01) & dataframe['tail'].lt(dataframe['bb_delta_cluc'] * 0.5) & dataframe['close'].lt(dataframe['bb_lowerband2_40'].shift()) & dataframe['close'].le(dataframe['close'].shift()) & (dataframe['close'] > dataframe['ema_50'] * 0.912)
        is_nfix_201 = (dataframe['rsi_slow'] < dataframe['rsi_slow'].shift()) & (dataframe['rsi_fast'] < 30.0) & (dataframe['ema_20_1h'] > dataframe['ema_26_1h']) & (dataframe['close'] < dataframe['sma_15'] * 0.953) & (dataframe['cti'] < -0.82) & (dataframe['cci'] < -210.0) & is_pump_1 & rsi_check
        is_nfi7_33 = dataframe['moderi_96'] & (dataframe['cti'] < -0.88) & (dataframe['close'] < dataframe['ema_13'] * 0.988) & (dataframe['EWO'] > 6.4) & (dataframe['rsi'] < 32.0) & (dataframe['volume'] < dataframe['volume_mean_4'] * 2.0) & pump_protection_loose & rsi_check
        is_nfi_sma_3 = (dataframe['bb_lowerband2_40'].shift() > 0) & (dataframe['bb_delta_cluc'] > dataframe['close'] * 0.059) & (dataframe['ha_closedelta'] > dataframe['close'] * 0.023) & (dataframe['tail'] < dataframe['bb_delta_cluc'] * 0.418) & (dataframe['close'] < dataframe['bb_lowerband2_40'].shift()) & (dataframe['close'] < dataframe['close'].shift())
        is_BB_checked = is_dip & is_break
        ## condition append
        conditions.append(is_BB_checked)  # P
        dataframe.loc[is_BB_checked, 'enter_tag'] += 'bb '
        conditions.append(is_local_uptrend)
        dataframe.loc[is_local_uptrend, 'enter_tag'] += 'local_uptrend '
        conditions.append(is_ewo)
        dataframe.loc[is_ewo, 'enter_tag'] += 'ewo '
        conditions.append(is_ewo_2)
        dataframe.loc[is_ewo_2, 'enter_tag'] += 'ewo2 '
        conditions.append(is_no_trend_4)
        dataframe.loc[is_no_trend_4, 'enter_tag'] += 'no_trend_4 '
        conditions.append(is_vwap)
        dataframe.loc[is_vwap, 'enter_tag'] += 'vwap '
        conditions.append(is_vwap_2)
        dataframe.loc[is_vwap_2, 'enter_tag'] += 'vwap_2 '
        conditions.append(is_vwap_3)
        dataframe.loc[is_vwap_3, 'enter_tag'] += 'vwap_3 '
        conditions.append(is_VWAP)
        dataframe.loc[is_VWAP, 'enter_tag'] += 'VWAP '
        conditions.append(is_insta)
        dataframe.loc[is_insta, 'enter_tag'] += 'insta '
        # NFI
        conditions.append(is_nfi_32)
        dataframe.loc[is_nfi_32, 'enter_tag'] += 'nfi_32 '
        conditions.append(is_nfi_33)
        dataframe.loc[is_nfi_33, 'enter_tag'] += 'nfi_33 '
        conditions.append(is_nfix_39)
        dataframe.loc[is_nfix_39, 'enter_tag'] += 'x_39 '
        conditions.append(is_nfix_201)
        dataframe.loc[is_nfix_201, 'enter_tag'] += 'x_201 '
        conditions.append(is_nfi7_33)
        dataframe.loc[is_nfi7_33, 'enter_tag'] += '7_33 '
        conditions.append(is_nfi_sma_3)
        dataframe.loc[is_nfi_sma_3, 'enter_tag'] += 'sma_3 '
        # Very Bear
        conditions.append(is_V_5)
        dataframe.loc[is_V_5, 'enter_tag'] += 'V_5 '
        if conditions:
            dataframe.loc[reduce(lambda x, y: x | y, conditions), 'enter_long'] = 1
        return dataframe

    def populate_exit_trend(self, dataframe: DataFrame, metadata: dict) -> DataFrame:
        dataframe.loc[dataframe['volume'] > 0, 'exit_long'] = 0
        return dataframe

def chaikin_money_flow(dataframe, n=20, fillna=False) -> Series:
    mfv = (dataframe['close'] - dataframe['low'] - (dataframe['high'] - dataframe['close'])) / (dataframe['high'] - dataframe['low'])
    mfv = mfv.fillna(0.0)
    mfv *= dataframe['volume']
    cmf = mfv.rolling(n, min_periods=0).sum() / dataframe['volume'].rolling(n, min_periods=0).sum()
    if fillna:
        cmf = cmf.replace([np.inf, -np.inf], np.nan).fillna(0)
    return Series(cmf, name='cmf')
# Mom DIV

def momdiv(dataframe: DataFrame, mom_length: int=10, bb_length: int=20, bb_dev: float=2.0, lookback: int=30) -> DataFrame:
    mom: Series = ta.MOM(dataframe, timeperiod=mom_length)
    upperband, middleband, lowerband = ta.BBANDS(mom, timeperiod=bb_length, nbdevup=bb_dev, nbdevdn=bb_dev, matype=0)
    enter_long = qtpylib.crossed_below(mom, lowerband)
    exit_long = qtpylib.crossed_above(mom, upperband)
    hh = dataframe['high'].rolling(lookback).max()
    ll = dataframe['low'].rolling(lookback).min()
    coh = dataframe['high'] >= hh
    col = dataframe['low'] <= ll
    df = DataFrame({'momdiv_mom': mom, 'momdiv_upperb': upperband, 'momdiv_lowerb': lowerband, 'momdiv_buy': enter_long, 'momdiv_sell': exit_long, 'momdiv_coh': coh, 'momdiv_col': col}, index=dataframe['close'].index)
    return df

class BB_RTR_dca(RTR):
    position_adjustment_enable = True
    initial_safety_order_trigger = -0.08
    max_safety_orders = 2
    safety_order_step_scale = 0.5  #SS
    safety_order_volume_scale = 1.6  #OS
    # Auto compound calculation
    max_dca_multiplier = 1 + max_safety_orders
    if max_safety_orders > 0:
        if safety_order_volume_scale > 1:
            max_dca_multiplier = 2 + safety_order_volume_scale * (math.pow(safety_order_volume_scale, max_safety_orders - 1) - 1) / (safety_order_volume_scale - 1)
        elif safety_order_volume_scale < 1:
            max_dca_multiplier = 2 + safety_order_volume_scale * (1 - math.pow(safety_order_volume_scale, max_safety_orders - 1)) / (1 - safety_order_volume_scale)
    # Let unlimited stakes leave funds open for DCA orders

    def custom_stake_amount(self, pair: str, current_time: datetime, current_rate: float, proposed_stake: float, min_stake: float, max_stake: float, **kwargs) -> float:
        if self.config['stake_amount'] == 'unlimited':
            return proposed_stake / self.max_dca_multiplier
        return proposed_stake
    # DCA

    def adjust_trade_position(self, trade: Trade, current_time: datetime, current_rate: float, current_profit: float, min_stake: float, max_stake: float, **kwargs):
        if current_profit > self.initial_safety_order_trigger:
            return None
        count_of_buys = trade.nr_of_successful_entries
        if 1 <= count_of_buys <= self.max_safety_orders:
            safety_order_trigger = abs(self.initial_safety_order_trigger) * count_of_buys
            if self.safety_order_step_scale > 1:
                safety_order_trigger = abs(self.initial_safety_order_trigger) + abs(self.initial_safety_order_trigger) * self.safety_order_step_scale * (math.pow(self.safety_order_step_scale, count_of_buys - 1) - 1) / (self.safety_order_step_scale - 1)
            elif self.safety_order_step_scale < 1:
                safety_order_trigger = abs(self.initial_safety_order_trigger) + abs(self.initial_safety_order_trigger) * self.safety_order_step_scale * (1 - math.pow(self.safety_order_step_scale, count_of_buys - 1)) / (1 - self.safety_order_step_scale)
            if current_profit <= -1 * abs(safety_order_trigger):
                try:
                    stake_amount = self.wallets.get_trade_stake_amount(trade.pair, None)
                    # This calculates base order size
                    stake_amount = stake_amount / self.max_dca_multiplier
                    # This then calculates current safety order size
                    stake_amount = stake_amount * math.pow(self.safety_order_volume_scale, count_of_buys - 1)
                    amount = stake_amount / current_rate
                    logger.info(f'Initiating safety order buy #{count_of_buys} for {trade.pair} with stake amount of {stake_amount} which equals {amount}')
                    return stake_amount
                except Exception as exception:
                    logger.info(f'Error occured while trying to get stake amount for {trade.pair}: {str(exception)}')
                    return None
        return None

    def leverage(self, pair: str, current_time: datetime, current_rate: float, proposed_leverage: float, max_leverage: float, entry_tag, side: str, **kwargs) -> float:
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
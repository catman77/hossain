from pathlib import Path
import pandas as pd
from freqtrade.data.history import load_pair_history
from freqtrade.enums import CandleType
from freqtrade.configuration import Configuration
from freqtrade.data.btanalysis import load_backtest_stats
from freqtrade.resolvers import StrategyResolver
from freqtrade.data.dataprovider import DataProvider

conf_json = "c:\\hossein\\user_data\\config.json"
config_path = Path(conf_json)


config = Configuration.from_files([config_path])
backtest_dir = config["user_data_dir"] / "backtest_results"

data_location = config["datadir"]

pair = "XRP/USDT:USDT"

df1:pd.DataFrame = load_pair_history(datadir=data_location,timeframe=config["timeframe"],pair=pair,data_format = "json",candle_type=CandleType.FUTURES)
df = df1.tail(500)

df['close'].plot()

# strategy = StrategyResolver.load_strategy(config)
# strategy.dp = DataProvider(config, None, None)
# strategy.ft_bot_start()
# df = strategy.analyze_ticker(candles, {'pair': pair})


# stats:dict = load_backtest_stats(backtest_dir)
# sstats:dict = stats['strategy'][strategy]



# df = pd.DataFrame(columns=['dates','equity'], data=strategy_stats['daily_profit'])
# df['equity_daily'] = df['equity'].cumsum()

# fig = px.line(df, x="dates", y="equity_daily")
# fig.show()


# params ={"timeInForce":"GTC",
#         "reduceOnly":False}
# order = co.create_order(symbol= pair , type="limit" , side= 'sell' , amount= 10 , price= 0.522 , params= params)

# defaultId = 'x-167673045'
# brokerId = self.safe_string(self.options, 'brokerId', defaultId)
# request['client_id'] = brokerId + '-' + self.uuid16()
# params = {
#     "triggerPrice":0.529,
#     "reduceOnly":True,
#     "timeInForce":"GTC"
# }
# order = co.create_order(symbol= pair , type= 'limit' , side= 'buy' , price= 0.53  ,amount= 10 , params= params)
# print(order)



# params = {
#     "timeInForce":"GTC",
#     "reduceOnly":False,
#     "triggerPrice":0.5,
# }

# order = co.create_order(symbol= pair , type= "limit" , side= 'sell' , amount= 10 ,price= 0.49 , params= params)


# order = co.place_order(symbol= pair , type= 'market' , side= 'buy' , amount= 10)
# print(order)


''''
triger order

params = {
    'triggerPrice': 1700,
}
order = exchange.create_order('ETH/USDT', 'market', 'buy', 0.1, 1500, params)


#   stoploss order
params = {
    'stopLossPrice': 55.45,  # your stop loss price
}

order = exchange.create_order (symbol, type, side, amount, price, params)



create stop loss and take profit order

symbol = 'ETH/BTC'
type = 'limit'  # or 'market'
side = 'buy'
amount = 123.45  # your amount
price = 115.321  # your price
params = {
    'stopLoss': {
        'type': 'limit',  # or 'market', this field is not necessary if limit price is specified
        'price': 100.33,  # limit price for a limit stop loss order
        'triggerPrice': 101.25,
    },
    'takeProfit': {
        'type': 'market',  # or 'limit', this field is not necessary if limit price is specified
        # no limit price for a market take profit order
        # 'price': 160.33,  # this field is not necessary for a market take profit order
        'triggerPrice': 150.75,
    }
}
order = exchange.create_order (symbol, type, side, amount, price, params)


important we can use :
    'clientOrderId': 'World',
in params the uniq string
'''







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
   'limits': {'leverage': {'min': 1.0, 'max': 50.0}, 
   'amount': {'min': 10.0, 'max': None}, 
   'price': {'min': None, 'max': None}, 
   'cost': {'min': None, 'max': None}}, 
   'created': None, 
   'info': {'base_ccy': 'XRP', 
            'base_ccy_precision': '8', 
            'contract_type': 'linear', 
            'leverage': ['1', '2', '3', '5', '8', '10', '15', '20', '30', '50'], 
            'maker_fee_rate': '0', 
            'market': 'XRPUSDT', 
            'min_amount': '10',
            'open_interest_volume': '2034120', 
            'quote_ccy': 'USDT', 
            'quote_ccy_precision': '4', 
            'taker_fee_rate': '0'}, 
    'percentage': True}
'''

'''
/futures/order


'''
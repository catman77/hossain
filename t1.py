from freqtrade.configuration import Configuration
from pathlib  import Path
from freqtrade.resolvers import ExchangeResolver
import time
from datetime import datetime , timedelta


conf_json = "c:\\hossein\\user_data\\config.json"
config_path = Path(conf_json)

config:dict = Configuration.from_files([config_path])
exchange_config = config['exchange']


ex = ExchangeResolver.load_exchange(config= config , exchange_config= exchange_config , validate= True , load_leverage_tiers= True)

pair = 'KAVA/USDT:USDT'
# now = datetime.now()
# since = now - timedelta(days=30)

now = datetime.now()
since = now - timedelta(days= 10)

id = '143033902099'
price = None
order = ex.create_order(pair= pair , ordertype='market' , side= 'sell' , amount= 10 , rate= 0.545 , reduceOnly= True , leverage= 10)
print(order)

'''
create order  'limit  market
close position       market
fetch_l2_order_book


fo = self.exchange.fetch_order_or_stoploss_order(order.order_id, order.ft_pair, order.ft_order_side == "stoploss")


orders = self.exchange.fetch_orders(trade.pair, trade.open_date_utc - timedelta(seconds=10))

current_entry_rate, current_exit_rate = self.exchange.get_rates(trade.pair, True, trade.is_short)

exchange.get_min_pair_stake_amount(trade.pair, current_entry_rate, 0.0)

exchange.get_max_pair_stake_amount(trade.pair, current_entry_rate)

amount = self.exchange.amount_to_contract_precision(trade.pair, abs(float(stake_amount * trade.amount / trade.stake_amount)))

order_book = self.exchange.fetch_l2_order_book(pair, 1000)

order = self.exchange.create_order(pair=pair,ordertype=order_type,side=side,amount=amount,rate=enter_limit_requested,reduceOnly=False,time_in_force=time_in_force,leverage=leverage)

fee = self.exchange.get_fee(symbol=pair, taker_or_maker="maker")

base_currency = self.exchange.get_pair_base_currency(pair)

funding_fees = self.exchange.get_funding_fees(pair=pair,amount=amount + trade.amount if trade else amount,is_short=is_short,open_date=trade.date_last_filled_utc if trade else open_date)

enter_limit_requested = self.exchange.get_rate(pair, side="entry", is_short=(trade_side == "short"), refresh=True)

max_leverage = self.exchange.get_max_leverage(pair, stake_amount)




exit_rate = self.exchange.get_rate(trade.pair, side="exit", is_short=trade.is_short, refresh=True)

stoploss_norm = self.exchange.price_to_precision(trade.pair,trade.stoploss_or_liquidation,rounding_mode=ROUND_DOWN if trade.is_short else ROUND_UP)

exchange.stoploss_adjust(stoploss_norm, order, side=trade.exit_side)

proposed_rate = self.exchange.get_rate(trade.pair, side="entry", is_short=trade.is_short, refresh=True)

minstake = self.exchange.get_min_pair_stake_amount(trade.pair, trade.open_rate, self.strategy.stoploss)

corder = self.exchange.cancel_order_with_result(order_id, trade.pair, trade.amount)

order = self.exchange.cancel_order_with_result(order["id"], trade.pair, trade.amount)

self.exchange.get_funding_fees(pair=trade.pair,amount=trade.amount,is_short=trade.is_short,open_date=trade.date_last_filled_utc))

fee_cost, fee_currency, fee_rate = self.exchange.extract_cost_curr_rate(order["fee"], order["symbol"], order["cost"], order_obj.safe_filled)

trades = self.exchange.get_trades_for_order(self.exchange.get_order_id_conditional(order), trade.pair, order_obj.order_date)


'''
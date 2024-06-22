from pathlib import Path
from freqtrade.configuration import Configuration
from freqtrade.resolvers import ExchangeResolver
from datetime import datetime,timedelta
import time
from pprint import pp

conf_json = "c:\\hossein\\user_data\\config.json"
config_path = Path(conf_json)

config:dict = Configuration.from_files([config_path])
exchange_config = config['exchange']

ex = ExchangeResolver.load_exchange(config= config , exchange_config= exchange_config , validate= True , load_leverage_tiers= True)

now_ms = int(time.time() * 1000)

now = datetime.now()
since = now - timedelta(days= 10 )
since_ms = int(since.timestamp() * 1000)

pair = 'XRP/USDT:USDT'

fees = ex.fetch_orders(pair= pair , since= since)
print(fees)
print('my time stamp' , since_ms)

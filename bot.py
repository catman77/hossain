from pathlib import Path
import os
from freqtrade import main
from datetime import datetime, timedelta

folder_path = Path(__file__).parent
user_data_path = os.path.join(folder_path, 'user_data')
config_path = os.path.join(user_data_path, 'config.json')
pair_config_path = os.path.join(user_data_path, 'pair_config.json')


def timerange(day:int= 1 , houre:int = 0 , minute:int = 0):
    end_date = datetime.now()
    start_date = end_date - timedelta(days= day , hours= houre , minutes= minute)
    return f"{start_date.strftime('%Y%m%d')}-{end_date.strftime('%Y%m%d')}"




def install_ui():
    return ['install-ui']

def create_userdir():
    return ['create-userdir'  , '--userdir',user_data_path , '--reset']

def test_pairlist(exchange:str='coinex'):
    return ['test-pairlist' , '-c', pair_config_path , '--userdir',user_data_path , '--exchange' , exchange]

def download_data(exchange:str='bybit' , day_timerange:int = 30 , hour_timerange:int = 0 , minute_timerange:int = 0 , timeframe:str = '5m'):
    time_range = timerange(day=day_timerange, houre=hour_timerange, minute=minute_timerange)
    return ['download-data' , '-c',config_path,'--userdir',user_data_path , '--exchange' , exchange , '--timerange', time_range , '-t' , timeframe]

def list_strategies():
    return ['list-strategies' ,'--userdir',user_data_path ]

def new_strategy(strategy_name:str = None , template:str = 'advanced'):
    if strategy_name is None:
        raise ValueError('strategy_name is None')
    return ['new-strategy' ,'--userdir',user_data_path , '--template' , template , '-s' , strategy_name]

def strategy_update():
    return ['strategy-updater' , '-c',config_path,'--userdir',user_data_path]

def backtest(strategy_name:str = None , timeframe:str = '5m' , day_timerange:int = 28 , hour_timerange:int = 0 , minute_timerange:int = 0):
    time_range = timerange(day=day_timerange, houre=hour_timerange, minute=minute_timerange)
    return ['backtesting' , '-c',config_path,'--userdir',user_data_path , '--timerange', time_range ,'-s' , strategy_name , '--timeframe' , timeframe]

def backtesting_show():
    return ['backtesting-show' , '-c',config_path,'--userdir',user_data_path]

def plot_dataframe(strategy_name:str= None , pair_name:str = None ):
    return ['plot-dataframe' , '-c',config_path,'--userdir',user_data_path ,'-s' , strategy_name , '-p' , pair_name ]

def plot_profit():
    return ['plot-profit' , '-c',config_path,'--userdir',user_data_path ]

def hyperopt_list():
    return ['hyperopt-list' , '-c',config_path,'--userdir',user_data_path]

def webserver():
    return ['webserver' , '-c',config_path,'--userdir',user_data_path]

def trade(strategy_name:str = None):
    if strategy_name is None:
        raise ValueError('strategy_name is None')
    return ['trade' , '-c',config_path,'--userdir',user_data_path , '-s' , strategy_name ]

def hyperopt(strategy_name:str = None , hyperopt_loss:str = 'OnlyProfitHyperOptLoss' , epoch:int = 200):
    return ['hyperopt', '-c',config_path,'--userdir',user_data_path , '-s' , strategy_name , '--spaces' , 'roi' , 'stoploss' , 'trailing' , 'all' , '--hyperopt-loss' , hyperopt_loss , '-e' , str(epoch) , '--ignore-missing-spaces'  , '--analyze-per-epoch']

#  ShortTradeDurHyperOptLoss    OnlyProfitHyperOptLoss      SharpeHyperOptLoss      SharpeHyperOptLossDaily        SortinoHyperOptLoss       SortinoHyperOptLossDaily
#  CalmarHyperOptLoss       MaxDrawDownHyperOptLoss        MaxDrawDownRelativeHyperOptLoss     ProfitDrawDownHyperOptLoss

tempelates = ['full','minimal','advanced']


args = download_data()
main.main(args)



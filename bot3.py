from pathlib import Path
import os
from freqtrade import main
from datetime import datetime, timedelta
import json
import PySimpleGUI as sg
import bot_helper as bh
from layouts import (tab1_layout , tab2_layout , tab3_layout , tab4_layout,
                     frame1_layout , frame2_layout , layout)


sg.theme('DarkAmber')

config:dict = {}
time_range:str = ''
pair_list:list = []

      



window = sg.Window('Freqtrade Bot GUI', layout , element_padding=(5,5) , finalize= True)


while True:
    event, values = window.read()

    print(event)
    if event == 'Close':
        break
    
    if event == 'install ui':
        bh.install_ui()
    
    if event == 'create userdir':
        bh.create_userdir()
    
    if event == 'test pairlist':
        exchange_name = str(values['-exchange-'])
        asset_number = float(values['-asset_number-'])
        look_back = float(values['-look_back-'])
        min_price = float(values['-min_price-'])
        max_price = float(values['-max_price-'])
        refresh_period = float(values['-refresh_period-'])
        max_rank = float(values['-max_rank-'])
        bh.test_pairlist(exchange_name , asset_number , look_back , min_price , max_price , refresh_period , max_rank)



window.close()
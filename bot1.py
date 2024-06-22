from pathlib import Path
import os
from freqtrade import main
from datetime import datetime, timedelta
import PySimpleGUI as sg

sg.theme('DarkAmber')

size_a = 6
tab1_layout = [
    [sg.Text('Exchange:' , size= size_a)],
    [sg.Text('name:' , size= size_a) , sg.Input(default_text='bybit')],
    [sg.Text('key:', size= size_a)  , sg.Input(default_text='')],
    [sg.Text('secret:', size= size_a) , sg.Input(default_text='')],
    [sg.Te]
]


frame1 = [[sg.TabGroup([
        [sg.Tab('Config',layout= tab1_layout),
         sg.Tab('Tab 2', [[sg.Text('Content of Tab 2')]]),
         sg.Tab('Tab 3', [[sg.Text('Content of Tab 3')]]),
         sg.Tab('Tab 4', [[sg.Text('Content of Tab 4')]])]] , expand_x= True , expand_y= True)]]



frame2 = [[sg.Text('col 2')]]

frame3 = [[sg.Output(expand_x= True , expand_y= True , echo_stdout_stderr= True , horizontal_scroll= True)]]

layout = [[sg.Frame(title= '' , layout= frame1 , size=(400,500)) , sg.Frame(title= '' , layout= frame2 , size=(400,500))],
          [sg.Frame(title= '' , layout= frame3 , size=(810,120))],
          [sg.Button(button_text='Start' , size=15 ) ,sg.Button(button_text='Stop' , size= 15)]]

window = sg.Window('freqtrade' , layout= layout )

while True:
    event , value = window.read()

    if event == sg.WIN_CLOSED:
        break

window.close()
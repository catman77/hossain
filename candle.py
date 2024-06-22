import ccxt
import sys
from PyQt5.QtWidgets import QApplication, QMainWindow
import pyqtgraph as pg
from pyqtgraph import PlotWidget
import pandas as pd

class CandlestickChart(QMainWindow):
    def __init__(self, df):
        super().__init__()

        self.setWindowTitle('Candlestick Chart')
        self.setGeometry(100, 100, 800, 600)

        self.plot_widget = PlotWidget(self)
        self.setCentralWidget(self.plot_widget)
        self.plot_candlestick(df)


    def plot_candlestick(self, df:pd.DataFrame):

        candlesticks = []
        for i, row in df.iterrows():
            open_price = row['open']
            high_price = row['high']
            low_price = row['low']
            close_price = row['close']
            candlesticks.append((i, open_price, close_price, low_price, high_price))

        # Create the candlestick plot item
        candlestick_item = pg.graphicsItems.CandlestickItem.CandlestickItem(candlesticks)
        self.plot_widget.addItem(candlestick_item)

if __name__ == '__main__':
    data = {
        'time': ['2023-01-01', '2023-01-02'],
        'open': [100, 105],
        'high': [110, 115],
        'low': [90, 95],
        'close': [105, 100]
    }
    df = pd.DataFrame(data)

    app = QApplication(sys.argv)
    main_window = CandlestickChart(df)
    main_window.show()
    sys.exit(app.exec_())
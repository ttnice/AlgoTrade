'''
Plot Candle stick from internet
'''

import datetime as dt
import matplotlib.dates as mdates
import matplotlib.pyplot as plt
import pandas_datareader as web
from mpl_finance import candlestick_ohlc

start = dt.datetime(2010,1,1)
end = dt.datetime.now()

df = web.DataReader('AAPL', 'yahoo', start, end)

#print(df.head())

df = df[['Open', 'High', 'Low', 'Close']]

#print(df.head())

df.reset_index(inplace=True)

print(df.head())
print(type(df['Date'][0]))
df['Date'] = df['Date'].map(mdates.date2num)

print(df[-5:])
print(type(df['Open'][0]))

ax = plt.subplot()
candlestick_ohlc(ax, df.values, width=5, colorup='g', colordown='r')
ax.xaxis_date()
ax.grid(True)
plt.show()
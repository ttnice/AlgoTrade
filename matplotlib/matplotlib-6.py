'''
Plot with date via Datetime and formatter
'''

import numpy as np
import datetime
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from matplotlib.ticker import FuncFormatter
import matplotlib.ticker as ticker

days = [2, 3, 4, 5, 8, 9, 10, 11, 12, 15, 16]

time_list = [datetime.timedelta(0, 23820), datetime.timedelta(0, 27480),
             datetime.timedelta(0, 28500), datetime.timedelta(0, 24180),
             datetime.timedelta(0, 27540), datetime.timedelta(0, 28920),
             datetime.timedelta(0, 28800), datetime.timedelta(0, 29100),
             datetime.timedelta(0, 29100), datetime.timedelta(0, 24480),
             datetime.timedelta(0, 27000)]



def format_func(x, pos):
    hours = int(x//3600)
    minutes = int((x%3600)//60)
    seconds = int(x%60)

    return "{}:{}".format(hours, minutes)
    # return "{:d}:{:02d}:{:02d}".format(hours, minutes, seconds)

formatter = FuncFormatter(format_func)


def setup(ax):
    ax.spines['right'].set_color('none')
    ax.spines['left'].set_color('none')
    ax.yaxis.set_major_locator(ticker.NullLocator())
    ax.spines['top'].set_color('none')
    ax.xaxis.set_ticks_position('bottom')
    ax.tick_params(which='major', width=1.00)
    ax.tick_params(which='major', length=5)
    ax.tick_params(which='minor', width=0.75)
    ax.tick_params(which='minor', length=2.5)
    ax.set_xlim(0, 5)
    ax.set_ylim(0, 1)
    ax.patch.set_alpha(0.0)

labels = [2, 3, 4, 5, 8, 9, 10, 11, 12, 15, 16]
seconds = [i.seconds for i in time_list]
f = plt.figure()
ax = plt.subplot(1,1,1)
setup(ax)
ax.bar(labels, seconds)

ax.yaxis.set_major_formatter(formatter)

# this locates y-ticks at the hours
ax.yaxis.set_major_locator(ticker.MultipleLocator(base=3600))

# this ensures each bar has a 'date' label
ax.xaxis.set_major_locator(ticker.MultipleLocator(base=1))

plt.show()
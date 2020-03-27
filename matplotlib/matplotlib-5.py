'''
plot with date via datetime
'''

import numpy as np
import datetime
import matplotlib.pyplot as plt
import matplotlib.dates as mdates

days = [2, 3, 4, 5, 8, 9, 10, 11, 12, 15, 16]

time_list = [datetime.timedelta(0, 23820), datetime.timedelta(0, 27480),
             datetime.timedelta(0, 28500), datetime.timedelta(0, 24180),
             datetime.timedelta(0, 27540), datetime.timedelta(0, 28920),
             datetime.timedelta(0, 28800), datetime.timedelta(0, 29100),
             datetime.timedelta(0, 29100), datetime.timedelta(0, 24480),
             datetime.timedelta(0, 27000)]

# specify a date to use for the times
zero = datetime.datetime(2018,1,1)
time = [zero + t for t in time_list]
# convert datetimes to numbers
zero = mdates.date2num(zero)
time = [t-zero for t in mdates.date2num(time)]

f = plt.figure()
ax = f.add_subplot(1,1,1)

ax.bar(days, time, bottom=zero)
ax.yaxis_date()
ax.yaxis.set_major_formatter(mdates.DateFormatter("%H:%M"))

# add 10% margin on top (since ax.margins seems to not work here)
ylim = ax.get_ylim()
ax.set_ylim(None, ylim[1]+0.1*np.diff(ylim))

plt.show()
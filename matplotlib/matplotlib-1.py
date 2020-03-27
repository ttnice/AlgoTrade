'''
Plot an easy random graph
'''

import matplotlib.pyplot as plt
import time
import numpy as np


def show_plot():
    print('still working')
    time.sleep(4)
    print('wanna close')
    plt.close()
    print('done')


def close_plot():
    plt.close()


'''
vals = []
times = []
for i in range(500):
    times.append(np.random.randint(i+1))
    vals.append(i)
f = plt.figure()
ax1 = f.add_subplot()
ax1.plot(vals, times)
'''


plt.plot(np.random.random(120))
plt.show()
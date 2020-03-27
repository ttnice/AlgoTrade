'''
plot Numpy transpose to plot
'''

import matplotlib.pyplot as plt
import numpy as np

a = np.random.rand(3, 20)
a = a.transpose()
print(a)
plt.plot(a)
plt.show()
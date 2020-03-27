import datetime
from math import e
import time
import pandas as pd
import random
import numpy as np

class Primary:
    def __init__(self):
        self.df = pd.read_csv('data/data.csv', sep='\t', dtype={'Date': str, 'Time': str, 'Open': float, 'High': float, 'Low': float, 'Close': float, 'Index': int})

    def get_datas(self, high=False, low=False, close=False, index=False, ehigh=False, elow=False, eclose=False):
        self.current = self.current%self.last
        data = np.array([i[0] for i in self.df.loc[range(self.current,self.current+self.long), ['Eclose']].values])
        self.current += 1
        return data

    def get_datas_from(self, index):
        rang = range(index, index+self.long)
        a = self.df.loc[rang, ['Eclose']].values
        b = [i[0] for i in a]
        data = np.array(b)
        return data

    def spread(self):
        # valeur pour 1000 du prix
        spread = random.uniform(0.1, 0.9)
        return spread

    def get_info(self):
        info = self.df.loc[self.current, ['Close', 'Index']].values
        return info


if __name__ == '__main__':
    my_primary = Primary()
    print(my_primary.get_info())


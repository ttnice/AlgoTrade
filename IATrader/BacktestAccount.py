import pandas as pd
import numpy as np

class Account:
    def __init__(self):
        # [index, price, spread, tp, sl, action]
        self.df = pd.DataFrame(columns=['index', 'price', 'tp', 'sl', 'action'])
        self.win = 0
        self.lose = 0

    def open_trade(self, index, price, tp, sl, action, operator):
        self.df = self.df.append({'index': index, 'price': price, 'tp': tp, 'sl': sl, 'action': action, 'operator': operator}, ignore_index=True)

    def analyse(self, index, price):
        data_learn = self.df[self.df['action']*(price-self.df['tp']) >= 0]
        bad_decision = self.df[self.df['action']*(self.df['sl']-price) >= 0]
        too_long = self.df[index-self.df['index'] >= 30]
        #print(f'data-learn : {len(data_learn)} bad-decision {len(bad_decision)} too-long {len(too_long)}')

        dropper = np.concatenate((data_learn.index.values, bad_decision.index.values, too_long.index.values))
        self.df = self.df.drop(dropper)
        bad_decision.rename({'tp': 'sl', 'sl': 'tp'}, inplace=True)
        bad_decision['action'] = - bad_decision['action']

        self.win += len(data_learn)
        self.lose += len(bad_decision)

        # data_learn = pd.concat([data_learn, bad_decision])
        current_price = [price for i in range(len(data_learn))]
        data_learn['current_price'] = current_price
        data_learn.to_csv('Backtest/learn.csv')








from IATrader.BacktestPrimary import Primary
from IATrader.BacktestModel import easy_end
import pandas as pd
import random
import datetime




if __name__ == '__main__':
    my_primary = Primary()
    my_model = easy_end()

    #my_model.create_model()
    my_model.load()
    my_model.compiler(0.0000001)
    i = 1_000_000
    my_primary.current = i
    my_model.compiler(0.00_000_1)
    while True:
        datas = my_primary.get_datas()
        price, index = my_primary.get_info()



        if i%1_000 == 0:
            action, value = my_model.predict(datas, price)
            print(f'{i} - Action : {action} Value : {value} Price : {price} - {datetime.datetime.now()}')
        '''
        if action[0] >= action[1]:
            #BUY
            my_model.open_trade(index, price, value[0], value[1], 1, 'IA')
        else:
            #SELL
            my_model.open_trade(index, price, value[0], value[1], -1, 'IA')
        '''

        for _ in range(10):
            tp = random.uniform(0.001, 0.05)
            sl = random.uniform(0.001, 0.05)
            my_model.open_trade(index, price, price+tp, price-sl, 1, 'random')
            my_model.open_trade(index, price, price-tp, price+sl, -1, 'random')

        my_model.analyse(index, price)
        df = pd.read_csv('Backtest/learn.csv', dtype={'i': int, 'index': int, 'price': float, 'tp': float, 'sl': float, 'action': float, 'operator': str})

        datas = []
        labels = []
        ia = 0
        randome = 0
        for trade in df.values:
            datas.append(my_primary.get_datas_from(int(trade[0])))
            if trade[5] == 1:
                action = [1, 0]
            elif trade[5] == -1:
                action = [0, 1]
            else:
                print(trade[5])
            labels.append([action, [trade[3], trade[4], trade[2]]])
            if trade[6] == 'IA':
                ia += 1
            elif trade[6] == 'random':
                randome += 1
            else:
                print(trade[6])

        i += 1
        if len(datas) > 0:
            my_model.fit(datas, labels)
            my_model.save_folder()


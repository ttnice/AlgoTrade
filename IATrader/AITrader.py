from IATrader.AITraderSubModels import easy_end, easy_long
from IATrader.AITraderPrimary import Primary
import datetime
import random
import time

if __name__ == '__main__':
    my_primary = Primary()
    my_easy_end = easy_end(3)
    #my_easy_long = easy_long(3)

    object_list = [my_easy_end]
    my_primary.get_prices()


    for i in range(len(object_list)):
        object_list[i].load()
    '''
    for i in range(len(object_list)):
            object_list[i].create_model()
    '''

    while True:
        # print(datetime.datetime.now())
        completed = False
        while not completed:
            try:
                completed = my_primary.get_candle()
            except:
                print(f'Problem with get candle, maybe wifi')
        print(len(my_primary.times), end=' - ')
        print(my_primary.times)
        '''
        print(my_primary.closes)
        print(my_primary.highs)
        print(my_primary.lows)
        print(my_primary.volumes)
        '''
        for i in range(len(object_list)):
            completed = False
            while not completed:
                # try:
                data = my_primary.get_data()
                spread = my_primary.spread()
                # balance_available, balance = object_list[i].balance()
                balance_per_cent = object_list[i].balance_per_cent()
                completed = True
                # except:
                #    print(f'Problem with balance, maybe wifi')
            data_input = data + [spread] + [balance_per_cent]
            action, val = object_list[i].predict(data_input)
            if action[0][0] != 1:
                if action[0][1] == 1:
                    try:
                        object_list[i].open_trade(take_profit=val[0][0], stop_loss=-val[0][1], actual_price=my_primary.last_close, instrument='EUR_USD', action='BUY', data_input=data_input)
                        print(f'{object_list[i].name} BUY')
                    except:
                        pass
                if action[0][2] == 1:
                    try:
                        object_list[i].open_trade(take_profit=-val[0][0], stop_loss=val[0][1], actual_price=my_primary.last_close, instrument='EUR_USD', action='SELL', data_input=data_input)
                        print(f'{object_list[i].name} SELL')
                    except:
                        pass
            tp = random.uniform(0.00001, 0.0005)
            sl = random.uniform(0.00001, 0.0005)
            # object_list[i].open_trade(take_profit=tp, stop_loss=-sl, actual_price=my_primary.last_close, instrument='EUR_USD', action='BUY', data_input=data_input)
            object_list[i].open_trade(take_profit=-tp, stop_loss=sl, actual_price=my_primary.last_close, instrument='EUR_USD', action='SELL', data_input=data_input)
            object_list[i].checker(my_primary.last_close)

        with open('train/learning.txt') as file:
            lines = file.readlines()
            file.close()
        file = open('train/learning.txt', 'w')
        file.close()
        datas = []
        labels = []
        for i in range(0, len(lines), 2):
            datas.append([float(i) for i in lines[i][1:-2].split(',')])
            labels.append([float(i) for i in lines[i+1][1:-2].split(',')])

        for i in range(len(object_list)):
            if len(datas) > 0:
                print(datas)
                print(labels)
                object_list[i].fit(datas, labels, epochs=5)
                object_list[i].save_folder()
                print('                                                                                                FIT')

        time.sleep(30)



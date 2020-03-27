from IaObject import Ia
from PriceObject import Price
from datetime import datetime
import matplotlib.pyplot as plt
import numpy as np


def create():
    my_ia = Ia()
    my_ia.create_model()
    my_ia.compiler(0)
    my_price = Price(180)

    start = 1
    datas = [np.array(my_price.get_several_data(start, 120))]
    labels = [np.array(my_price.get_several_data(start+120, 30))]

    for i in range(1, 51):
        my_ia.fit(datas, labels, 100)

        print(f'{i} - {datetime.now()}')

        if i % 10 == 0:
            my_ia.save_folder(f'trainer{i}')


def use():
    my_ia = Ia()
    my_ia.load('10')
    my_price = Price(180)

    start = 1
    data = my_price.get_several_data(start, 120)
    label = my_price.get_several_data(start + 120, 30)
    predictions = my_ia.predict(data)

    label = data + label
    predictions = data + list(predictions[0])

    print(label)
    print(predictions)

    plt.plot(label)
    plt.plot(predictions)
    plt.show()


def bunch_data():
    my_ia = Ia()
    my_price = Price(180)

    start = 1
    datas = [np.array(my_price.get_several_data(start, 120))]
    labels = [np.array(my_price.get_several_data(start+120, 30))]

    data = my_price.get_several_data(start, 120)
    label = my_price.get_several_data(start + 120, 30)
    label = data + label

    for choice in [0, 1]:
        print(f'\nFOR CHOICE = {choice}')
        my_ia.create_model()
        my_ia.compiler(choice)
        for i in range(1, 51):
            my_ia.fit(datas, labels, 100)

            print(f'{i} - {datetime.now()}')

            if i % 10 == 0:
                predictions = my_ia.predict(data)
                predictions = data + list(predictions[0])

                plt.plot(label)
                plt.plot(predictions)
                plt.savefig(f'Backtest/{choice} - {i}')
                plt.clf()


if __name__ == '__main__':
    use()
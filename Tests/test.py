from IaObject import Ia
from PriceObject import Price
from random import randint
from time import time
from datetime import datetime
import matplotlib.pyplot as plt


def single_test():
    my_ia = Ia()
    my_ia.load('7')
    my_price = Price(180)

    start = randint(1, my_price.born)
    print(start)
    data = my_price.get_several_data(start, 120)
    label = my_price.get_several_data(start+120, 30)
    predictions = my_ia.predict(data)

    label = data+label
    predictions = data+list(predictions[0])

    print(label)
    print(predictions)

    plt.plot(label, label='Price')
    plt.plot(predictions, label='Predict')
    plt.legend()
    plt.show()


def bunch_test():
    my_price = Price(180)
    my_ia = Ia()
    liste = [6_421_500, 5_250_000, 4_000_000, 2_750_000, 1_500_000, 750_000]
    plt.figure(figsize=(15, 10))
    plt.subplots_adjust(hspace=0.4)
    for i in range(1, 15):
        my_ia.load(f'{i}')
        for position in range(len(liste)):
            start = liste[position]
            data = my_price.get_several_data(start, 120)
            label = my_price.get_several_data(start+120, 30)
            predictions = my_ia.predict(data)

            label = data+label
            predictions = data+list(predictions[0])
            plt.subplot(2, 3, position+1)
            plt.plot(label, label='Price')
            plt.plot(predictions, label='Predict')
            plt.legend()
            plt.title(my_price.price[start][0])
        plt.savefig(f'Backtest/{i}-{str(datetime.now())[:10]}')
        plt.clf()


if __name__ == '__main__':
    bunch_test()

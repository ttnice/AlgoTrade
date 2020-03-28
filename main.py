from IaObject import Ia
from PriceObject import Price

from random import randint
from time import time
from datetime import datetime
import matplotlib.pyplot as plt

if __name__ == '__main__':
    fois = 9
    my_ia = Ia()
    # my_ia.create_model()
    my_ia.load('9')
    lr = 0.01
    my_ia.compiler(loss='mean_squared_error', lr=lr, decay=0.000_001, momentum=0.9, nesterov=True)
    my_price = Price(180)

    start_test = 6_421_500
    datas_test = my_price.get_several_data(start_test, 120)
    labels_test = datas_test + my_price.get_several_data(start_test+120, 30)

    while True:
        datas = []
        labels = []
        for i in range(10_000):
            start = randint(1, my_price.born)

            datas.append(my_price.get_several_data(start, 120))
            labels.append(my_price.get_several_data(start+120, 30))

        my_ia.fit(datas, labels, 100)

        fois += 1
        lr = lr/2
        my_ia.compiler(loss='mean_squared_error', lr=lr, decay=0.000_001, momentum=0.9, nesterov=True)
        print(f'{fois} - {datetime.now()}')

        my_ia.save_folder(f'{fois}')

        predictions = datas_test + list(my_ia.predict(datas_test)[0])
        print(predictions)
        plt.plot(labels_test, label='Price')
        plt.plot(predictions, label='Predict')
        plt.title('Predict for the 2019.09.06 at 10:20')
        plt.legend()
        plt.savefig(f'Backtest/{fois} - {datetime.now()}.png')
        plt.clf()


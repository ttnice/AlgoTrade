from keras.models import Model,load_model, optimizers
from keras.layers import Input, Dense
from keras.optimizers import Adam, SGD
from datetime import datetime
import numpy as np


class Ia:
    def __init__(self):
        self.model = None

    def save_folder(self, name):
        self.model.save(f'Backtest/{name}.h5')

    def create_model(self):
        val_input = Input(shape=(120,), name='input')
        x = Dense(256, activation='linear')(val_input)
        x = Dense(512, activation='sigmoid')(x)
        x = Dense(512, activation='softplus')(x)
        x = Dense(1024, activation='linear')(x)
        x = Dense(1024, activation='softplus')(x)
        x = Dense(512, activation='sigmoid')(x)
        x = Dense(256, activation='linear')(x)
        val_output = Dense(30, activation='linear', name='action_output')(x)

        self.model = Model(inputs=[val_input], outputs=[val_output])

    def compiler(self, loss='mean_squared_error', lr=0.01, decay=0.000_001, momentum=0.9, nesterov=True):
        sgd = SGD(lr=lr, momentum=momentum, decay=decay, nesterov=nesterov)
        adam = Adam(lr)
        self.model.compile(optimizer=sgd, loss=loss)

    def fit(self, datas, labels, epochs=10):
        self.model.fit(np.array(datas), np.array(labels), epochs=epochs, verbose=0)

    def predict(self, data):
        values = self.model.predict(np.array([data]))
        return values

    def load(self, name):
        self.model = load_model(f'Backtest/{name}.h5')


if __name__ == '__main__':
    print('test')
    my_ia = Ia()
    my_ia.create_model()
    # my_ia.compiler()
    # my_ia.fit([np.random.random(120)], [np.random.random(30)], 100)
    a = my_ia.predict([np.random.random(120)])
    print(a)
    print(type(a[0]))

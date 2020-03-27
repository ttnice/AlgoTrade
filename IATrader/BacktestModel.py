from keras.models import Model, Sequential, load_model
from keras.layers import Input, Dense, Dropout, Activation, concatenate
from keras.optimizers import Adam
from keras.utils import plot_model
from math import e
import numpy as np
from IATrader.BacktestAccount import Account


class easy_end(Account):
    NAME = 'EASY_END'
    def __init__(self):
        Account.__init__(self)
        self.model = None

    def save_folder(self):
        self.model.save(f'Backtest/{self.NAME}.h5')

    def create_model(self):
        def input_activation(x):
            rang = 1e4
            return 1 / (1 + e ** (-rang * x + rang))

        def output_activation(x):
            return x/50

        input = Input(shape=(180,), name='input')
        x = Dense(256, activation='softmax')(input)
        x = Dropout(0.2)(x)
        x = Dense(1024, activation='relu')(x)
        x = Dropout(0.2)(x)
        x = Dense(1024, activation='relu')(x)
        x = Dropout(0.2)(x)
        x = Dense(1024, activation='relu')(x)
        x = Dropout(0.2)(x)
        x = Dense(256, activation='relu')(x)
        x = Dropout(0.2)(x)
        x = Dense(256, activation='relu')(x)

        # action (1, 0):BUY (0, 1):SELL
        action_output = Dense(2, activation='softmax', name='action_output')(x)
        # val (tp, sl)
        val_output = Dense(2, name='val_output', activation='relu')(x)

        self.model = Model(inputs=[input], outputs=[action_output, val_output])
        self.compiler(0.001)


    def compiler(self, lr):
        self.model.compile(optimizer=Adam(lr), loss=['categorical_crossentropy', 'mean_squared_error'])

    def compress_value(self, limit, price):
        return limit/price

    def uncompress_value(self, price, percent):
        return price*percent

    def fit(self, data, label, epochs=10):
        action_label = [i[0] for i in label]
        val_label = [[self.compress_value(i[1][0], i[1][2]), self.compress_value(i[1][1], i[1][2])] for i in label]
        self.model.fit([data], [action_label, val_label], epochs=epochs, verbose=0)

    def predict(self, data, price):
        action, value = self.model.predict([[data]])
        action, value = action[0], value[0]
        value = [self.uncompress_value(price, i) for i in value]
        return action, value

    def load(self):
        self.model = load_model(f'Backtest/{self.NAME}.h5')
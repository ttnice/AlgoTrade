from keras.models import Model, Sequential, load_model
from keras.layers import Input, Dense, Dropout, concatenate
from keras.optimizers import Adam
from keras.utils import plot_model
from IATrader.AITraderDrive import Drive
from IATrader.AITraderSubAccount import SubAccount

import numpy as np


class easy_end(SubAccount):
    NAME = 'EASY_END'
    def __init__(self, number):
        SubAccount.__init__(self, self.NAME, number)

        self.model = None

    def save_folder(self):
        self.model.save(f'models/{self.NAME}.h5')

    def create_model(self):
        input = Input(shape=(242,), name='input')
        x = Dense(256, activation='relu')(input)
        x = Dense(256, activation='relu')(x)
        x = Dropout(0.2)(x)
        x = Dense(256, activation='relu')(x)
        x = Dropout(0.2)(x)
        x = Dense(256, activation='relu')(x)
        x = Dropout(0.2)(x)
        x = Dense(256, activation='relu')(x)

        action_output = Dense(3, activation='softmax', name='action_output')(x)
        val_output = Dense(2, name='val_output')(x)

        self.model = Model(inputs=[input], outputs=[action_output, val_output])
        self.compiler(0.1)


    def compiler(self, lr):
        self.model.compile(optimizer=Adam(lr), loss=['categorical_crossentropy', 'mean_squared_error'])

    def fit(self, data, label, epochs=50):
        action_label = [i[:3] for i in label]
        val_label = [i[3:] for i in label]
        self.model.fit([data], [action_label, val_label], epochs=epochs)

    def predict(self, data):
        return self.model.predict([[data]])

    def load(self):
        self.model = load_model(f'models/{self.NAME}.h5')


class easy_long(SubAccount):
    NAME = 'EASY_LONG'

    def __init__(self, number):
        SubAccount.__init__(self, self.NAME, number)

        self.model = None

    def save_folder(self, model):
        model.save(f'models/{self.NAME}.h5')

    def create_model(self):
        input = Input(shape=(240,), name='input')
        x = Dense(256, activation='relu')(input)
        x = Dense(128, activation='relu')(x)
        x = Dropout(0.2)(x)
        x = Dense(128, activation='relu')(x)
        x = Dropout(0.2)(x)
        x = Dense(128, activation='relu')(x)
        x = Dropout(0.2)(x)
        x = Dense(128, activation='relu')(x)
        x = Dropout(0.2)(x)
        x = Dense(128, activation='relu')(x)
        x = Dropout(0.2)(x)
        x = Dense(128)(x)

        action_output = Dense(3, activation='softmax', name='action_output')(x)
        val_output = Dense(2, name='val_output')(x)

        self.model = Model(inputs=[input], outputs=[action_output, val_output])
        self.compiler(0.1)

    def compiler(self, lr):
        self.model.compile(optimizer=Adam(lr), loss=['categorical_crossentropy', 'mean_squared_error'])

    def fit(self, data, label, epochs=50):
        action_label = label[:3]
        val_label = label[3:]
        self.model.fit([data], [[action_label], [val_label]], epochs=epochs)

    def predict(self, data):
        return self.model.predict([[data]])

    def load(self):
        self.model = load_model(f'models/{self.NAME}.h5')


class easy_big_step(SubAccount):
    NAME = 'EASY'
    def __init__(self, number):
        SubAccount.__init__(self, self.NAME, number)

        self.model = None

    def save_folder(self, model):
        model.save(f'models/{self.NAME}.h5')

    def create_model(self):
        input_price = Input(shape=(240,), name='input_price')
        x = Dense(64, activation='relu')(input_price)
        x = Dense(256, activation='relu')(x)
        x = Dropout(0.2)(x)
        x = Dense(256, activation='relu')(x)
        x = Dropout(0.2)(x)
        x = Dense(256, activation='relu')(x)

        input_account = Input(shape=(3,), name='input_account')
        y = concatenate([x, input_account])
        y = Dense(128)(y)
        y = Dense(128)(y)

        action_output = Dense(3, activation='softmax', name='action_output')(y)
        val_output = Dense(2, name='val_output')(y)

        self.model = Model(inputs=[input], outputs=[action_output, val_output])
        self.compiler(0.01)


    def compiler(self, lr):
        self.model.compile(optimizer=Adam(lr, decay=0.001), loss=['categorical_crossentropy', 'mean_squared_error'])

    def fit(self, data, label, epochs=2):
        data_price = data[:180]
        data_account = data[180:]
        action_label = label[:3]
        val_label = label[3:]
        self.model.fit([[data_price], [data_account]], [[action_label], [val_label]])

    def predict(self, data):
        return self.model.predict([[data]])

    def load(self):
        self.model = load_model(f'models/{self.NAME}.h5')

def create_suite_data(mul=np.random.random()):
    if mul>0.2:
        data = [1]
        for i in range(182):
            data.append(data[-1]*mul)
        data = np.array(data)
        return data, [1, 0, 0, mul, 1-mul]
    else:
        data = np.random.rand(183)
        return data, [0, 1, 0, -1, -1]


if __name__ == '__main__':
    my_easy = easy_end(5)
    my_easy.create_model()
    #my_easy.load()
    for i in range(20):
        data, label = create_suite_data()
        print(data.shape)
        my_easy.fit(data, label)
    my_easy.save_folder(my_easy.model)

    data, label = create_suite_data(0.4)
    print(f'target label : {label}')
    print(f'label : {my_easy.predict(data)}')
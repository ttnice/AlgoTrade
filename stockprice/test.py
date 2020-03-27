import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

# url = 'https://raw.githubusercontent.com/mwitiderrick/stockprice/master/NSE-TATAGLOBAL.csv'
url = 'NSE-TATAGLOBAL.csv'
dataset_train = pd.read_csv(url)
training_set = dataset_train.iloc[:, 1:2].values

print(training_set)
print(max(training_set))

from sklearn.preprocessing import MinMaxScaler
# sc = MinMaxScaler(feature_range=(0,1))
sc = MinMaxScaler()
training_set_scaled = sc.fit_transform(training_set)

print(sc.data_max_)
print(sc.data_min_)
print(training_set_scaled)
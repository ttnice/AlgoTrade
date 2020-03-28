import numpy, sys
from keras.models import Sequential
from keras.layers import Dense
from keras.layers import Dropout
from keras.layers import LSTM
from keras.callbacks import ModelCheckpoint
from keras.utils import np_utils



# load the network weights
filename = "weights-improvement-19-1.9435.hdf5"
X_shape1 = 100
X_shape2 = 1
y_shape1 = 58
# define the LSTM model
model = Sequential()
model.add(LSTM(256, input_shape=(X_shape1, X_shape2)))
model.add(Dropout(0.2))
model.add(Dense(y_shape1, activation='softmax'))
model.load_weights(filename)
model.compile(loss='categorical_crossentropy', optimizer='adam')

# load ascii text and covert to lowercase
filename = "wonderland.txt"
raw_text = open(filename, 'r', encoding='utf-8').read()
raw_text = raw_text.lower()
# create mapping of unique chars to integers
chars = sorted(list(set(raw_text)))
n_chars = len(raw_text)
n_vocab = len(chars)
int_to_char = dict((i, c) for i, c in enumerate(chars))
char_to_int = dict((c, i) for i, c in enumerate(chars))
# prepare the dataset of input to output pairs encoded as integers
seq_length = 100
dataX = []
dataY = []
for i in range(0, n_chars - seq_length, 1):
    seq_in = raw_text[i:i + seq_length]
    seq_out = raw_text[i + seq_length]
    dataX.append([char_to_int[char] for char in seq_in])
    dataY.append(char_to_int[seq_out])
n_patterns = len(dataX)

# pick a random seed
start = numpy.random.randint(0, len(dataX)-1)
pattern = dataX[start]
print("Seed:")
print("\"", ''.join([int_to_char[value] for value in pattern]), "\"")
# generate characters
for i in range(1000):
    x = numpy.reshape(pattern, (1, len(pattern), 1))
    x = x / float(n_vocab)
    prediction = model.predict(x, verbose=0)
    index = numpy.argmax(prediction)
    result = int_to_char[index]
    seq_in = [int_to_char[value] for value in pattern]
    sys.stdout.write(result)
    pattern.append(index)
    pattern = pattern[1:len(pattern)]
print("\nDone.")
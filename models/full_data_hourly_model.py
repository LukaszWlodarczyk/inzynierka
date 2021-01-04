import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import pathlib
from keras.models import Sequential
from keras.layers import Dense
from keras.layers import LSTM
from keras.layers import Dropout
from sklearn.preprocessing import MinMaxScaler
from my_requests import get_hourly_last_3_months_data
from joblib import dump
from functions import load_standard_data_frame

ONE_BATCH_SIZE = 30
BATCH_SIZE = 32
EPOCHS = 30


# load Dataframe
data = load_standard_data_frame(get_hourly_last_3_months_data())
# print(data.head())

# Scaling data
sc = MinMaxScaler(feature_range=(0, 1))
sc.fit(data)
data = sc.transform(data)


# Split into training and test set
training_set = data[:int(0.8*len(data))]
test_set = data[int(0.8*len(data)):]

# Prepare samples
X_train = []
Y_train = []
X_test = []
Y_test = []
for i in range(ONE_BATCH_SIZE, len(training_set)):
    X_train.append(training_set[i - ONE_BATCH_SIZE:i])
    Y_train.append(training_set[i][5]) # 5 bo cena close jest na koncu
X_train, y_train = np.array(X_train), np.array(Y_train)
X_train = np.reshape(X_train, (X_train.shape[0], X_train.shape[1], 6))
y_train = np.reshape(y_train, (-1,1))
for i in range(ONE_BATCH_SIZE, len(test_set)):
    X_test.append(test_set[i - ONE_BATCH_SIZE:i])
    Y_test.append(test_set[i][5])
X_test, y_test = np.array(X_test), np.array(Y_test)
X_test = np.reshape(X_test, (X_test.shape[0], X_test.shape[1], 6))


# Build LSTM model
model = Sequential()
model.add(LSTM(units=56, return_sequences=True, input_shape = (X_train.shape[1], 6)))
model.add(Dropout(0.2))
model.add(LSTM(units=28, return_sequences=True))
model.add(Dropout(0.2))
model.add(LSTM(units=14, return_sequences=False))
model.add(Dropout(0.2))
model.add(Dense(units=1))

# Compile and fit model
model.compile(optimizer='adam', loss='mean_squared_error')
history = model.fit(X_train, y_train, validation_data=(X_test,y_test), epochs=EPOCHS, batch_size=BATCH_SIZE, shuffle=False)

loss = history.history['loss']
val_loss = history.history['val_loss']
epochs = range(len(loss))

model.save(f'../saved_model/model_for_hours_from_full_data__val_lose_{val_loss[-1]}')
dump(sc, f'../saved_model/scaler_for_model_for_full_data_hours_val_lose_{val_loss[-1]}')


plt.figure()
plt.plot(epochs, loss, 'b', label='Training loss')
plt.plot(epochs, val_loss, 'r', label='Validation loss')
plt.title("Training and Validation Loss")
plt.legend()
plt.show()



import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import pathlib
from keras.models import Sequential
from keras.layers import Dense
from keras.layers import LSTM
from keras.layers import Dropout
from sklearn.preprocessing import MinMaxScaler
from requests_module import get_all_historical_data, cut_input_data_2, cut_results_data_2, get_hourly_last_3_months_data

seven_days = 50


def predict_n_days(days, start_values):
    queue = start_values.copy()
    results = list()

    for x in range(int(days)):
        input_array = np.reshape(queue, (-1, 1))
        input_array = sc.transform(input_array)
        input_array = np.array(input_array)
        input_array = np.reshape(input_array, (1, seven_days, 1))
        predicted_price = model.predict(input_array)
        predicted_price = np.reshape(predicted_price, (-1, 1))
        predicted_price = sc.inverse_transform(predicted_price)
        results.append(predicted_price.item(0))
        queue.append(predicted_price.item(0))
        queue.pop(0)
    return results


# load Dataframe
# data = pd.DataFrame(get_all_historical_data(), columns=['close'])
data = pd.DataFrame(get_hourly_last_3_months_data(), columns=['close'])

# Scaling data
sc = MinMaxScaler(feature_range=(0, 1))
sc.fit(data)
data = sc.transform(data)

# Split into training and test set
# training_set = data[:int(1 * len(data))]
training_set = data[:int(0.8 * len(data))]
test_set = data[int(0.8 * len(data)):]

# Prepare 7day samples
X_train = []
y_train = []
for i in range(seven_days, len(training_set)):
    X_train.append(training_set[i - seven_days:i])
    y_train.append(training_set[i])
X_train, y_train = np.array(X_train), np.array(y_train)
y_train = np.reshape(y_train, (-1,1))
X_train = np.reshape(X_train, (X_train.shape[0], X_train.shape[1], 1))

X_test = []
y_test = []
for i in range(seven_days, len(test_set)):
    X_test.append(test_set[i - seven_days:i])
    y_test.append(test_set[i])
X_test, y_test = np.array(X_test), np.array(y_test)
y_test = np.reshape(y_test, (-1,1))
X_test = np.reshape(X_test, (X_test.shape[0], X_test.shape[1], 1))

# Build LSTM model
model = Sequential()
model.add(LSTM(units=64, return_sequences=True, input_shape=(X_train.shape[1],1), dropout=0.2))
model.add(LSTM(units=32, return_sequences=True, dropout=0.2))
model.add(LSTM(units=16, return_sequences=True, dropout=0.2))
model.add(Dense(units=1))
# Compile and fit model
model.compile(optimizer='adam', loss='mean_squared_error')
history = model.fit(X_train, y_train, validation_data=(X_test, y_test), epochs=30, batch_size=32)
# history = model.fit(X_train, y_train, validation_split=(0.1), epochs=30, batch_size=36)
plt.plot(history.history['loss'], color='blue', label="training")
plt.plot(history.history['val_loss'], color='red', label="validation")
plt.title("Loss")
plt.legend()
plt.show()

# model.save('saved_model/model1')
# Make a prediction
# predicted_stock_price = model.predict(X_test)


# Prepare data to display on the plot
# y_train = np.reshape(y_train, (-1,1))
# y_train = y_train.tolist()
# predicted_stock_price_denormalized = []
# for price in predicted_stock_price:
#     predicted_stock_price_denormalized.append(price)
# predicted_stock_price_denormalized = sc.inverse_transform(predicted_stock_price_denormalized)
# y_test = np.reshape(y_test, (-1,1))
# y_test = y_test.tolist()
# y_test = sc.inverse_transform(y_test)


# print(predict_n_days(14,[23424,23612,23763,23987,23999,24700,24600]))

result = predict_n_days(len(cut_results_data_2), cut_input_data_2[-seven_days:])

# fig = plt.Figure(figsize=(8,7), dpi=100)
# plot = fig.add_subplot(111)

series = [x for x in range(len(cut_input_data_2) + len(cut_results_data_2))]
plt.plot(series[-len(cut_results_data_2):], result, color='blue', label='Predicted price')
plt.plot(series[-len(cut_results_data_2):], cut_results_data_2, color="red", label="Real price")
plt.plot(series[:-len(cut_results_data_2)], cut_input_data_2, color="green", label="Real price")
plt.title("Bitcoin price prediction")
plt.xlabel('Timestamp')
plt.ylabel('Price [PLN]')
plt.legend()
plt.show()
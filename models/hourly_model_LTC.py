import pandas as pd
from keras.models import Sequential
from keras.layers import Dense
from keras.layers import LSTM
from keras.layers import Dropout
from sklearn.preprocessing import MinMaxScaler
from joblib import dump
from my_requests import get_hourly_last_3_months_data
from functions import splitter, prepare_samples, draw_training_and_validation_lost_plot, save_info

# Initial values
ONE_BATCH_SIZE = 30
BATCH_SIZE = 32
EPOCHS = 30
TRAIN_TEST_SPLIT_POINT = 0.8
X_TRAIN = []
Y_TRAIN = []
X_TEST = []
Y_TEST = []

# Load Dataframe
data = pd.DataFrame(get_hourly_last_3_months_data('LTC'), columns=['close'])

# Scale data
sc = MinMaxScaler(feature_range=(0, 1))
sc.fit(data)
data = sc.transform(data)

# Split into training and test set
training_set, test_set = splitter(data, TRAIN_TEST_SPLIT_POINT)

# Prepare samples
X_TRAIN, X_TEST, Y_TRAIN, Y_TEST = prepare_samples(ONE_BATCH_SIZE, training_set, test_set, X_TRAIN,
                                                   Y_TRAIN, X_TEST, Y_TEST)


# Build LSTM model
model = Sequential()
model.add(LSTM(units=56, return_sequences=True, input_shape=(X_TRAIN.shape[1], 1)))
model.add(Dropout(0.2))
model.add(LSTM(units=28, return_sequences=True))
model.add(Dropout(0.2))
model.add(LSTM(units=14, return_sequences=False))
model.add(Dropout(0.2))
model.add(Dense(units=1))

# Compile and fit model
model.compile(optimizer='adam', loss='mean_squared_error')
history = model.fit(X_TRAIN, Y_TRAIN, validation_data=(X_TEST, Y_TEST), epochs=EPOCHS, batch_size=BATCH_SIZE,
                    shuffle=False)

loss = history.history['loss']
val_loss = history.history['val_loss']
epochs = range(len(loss))

model.save(f'../LTC_saved_model/model_for_hours_val_lose_{val_loss[-1]}')
dump(sc, f'../LTC_saved_model/scaler_for_model_for_hours_val_lose_{val_loss[-1]}')

save_info(ONE_BATCH_SIZE,BATCH_SIZE,EPOCHS,TRAIN_TEST_SPLIT_POINT,loss,val_loss,model)
draw_training_and_validation_lost_plot(epochs, loss, val_loss)



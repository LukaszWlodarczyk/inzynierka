import pandas as pd
import numpy as np

import my_requests

pd.set_option('max_columns', None)


def load_standard_data_frame(input_array):
    df = pd.DataFrame(input_array).set_index('time')
    df.pop('conversionType')
    df.pop('conversionSymbol')
    return df


def predict_n_days(model, scaler, days, start_values, one_batch_size):
    queue = start_values.copy()
    results = list()
    for x in range(int(days)):
        input_array = np.reshape(queue, (-1,1))
        input_array = scaler.transform(input_array)
        input_array = np.array(input_array)
        input_array = np.reshape(input_array, (1, one_batch_size, 1))
        predicted_price = model.predict(input_array)
        predicted_price = np.reshape(predicted_price, (-1, 1))
        predicted_price = scaler.inverse_transform(predicted_price)
        results.append(predicted_price.item(-1))
        queue.append(predicted_price.item(0))
        queue.pop(0)
    return results

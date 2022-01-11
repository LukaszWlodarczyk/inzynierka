import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from contextlib import redirect_stdout


pd.set_option('max_columns', None)


def save_info(one_batch_size, batch_size, epochs, split_point, loss, val_loss, model, crypto, type):
    info = f'single batch size: {one_batch_size} \n' \
           f'batch size: {batch_size} \n' \
           f'epochs: {epochs} \n' \
           f'split point: {split_point} \n' \
           f'training loss: {loss} \n' \
           f'lowest training loss: {min(loss)}  \n' \
           f'last training loss: {loss[-1]}  \n' \
           f'validation loss: {val_loss} \n' \
           f'lowest validation loss: {min(val_loss)}  \n' \
           f'last validation loss: {val_loss[-1]}  \n'

    with open(f'../saved_model/{crypto}_info_model_for_{type}_val_lose_{val_loss[-1]}.txt','w') as file:
        file.write(info)
        with redirect_stdout(file):
            model.summary()


def draw_training_and_validation_lost_plot(epochs, training, validation):
    plt.figure()
    plt.plot(epochs, training, 'b', label='Training loss')
    plt.plot(epochs, validation, 'r', label='Validation loss')
    plt.title("Training and Validation Loss")
    plt.legend()
    plt.show()


def prepare_samples(single_batch_size, training_set, test_set, x_train, y_train, x_test, y_test, full_input_data=False):
    if full_input_data:
        for i in range(single_batch_size, len(training_set)):
            x_train.append(training_set[i - single_batch_size:i])
            y_train.append(training_set[i][5])

        for i in range(single_batch_size, len(test_set)):
            x_test.append(test_set[i - single_batch_size:i])
            y_test.append(test_set[i][5])
            x_train.append(test_set[i - single_batch_size:i])
            y_train.append(test_set[i][5])

        x_train, y_train = np.array(x_train), np.array(y_train)
        x_train = np.reshape(x_train, (x_train.shape[0], x_train.shape[1], 6))
        y_train = np.reshape(y_train, (-1, 1))
        x_test, y_test = np.array(x_test), np.array(y_test)
        x_test = np.reshape(x_test, (x_test.shape[0], x_test.shape[1], 6))
    else:
        for i in range(single_batch_size, len(training_set)):
            x_train.append(training_set[i - single_batch_size:i])
            y_train.append(training_set[i])

        for i in range(single_batch_size, len(test_set)):
            x_test.append(test_set[i - single_batch_size:i])
            y_test.append(test_set[i])
            x_train.append(test_set[i - single_batch_size:i])
            y_train.append(test_set[i])

        x_train, y_train = np.array(x_train), np.array(y_train)
        x_train = np.reshape(x_train, (x_train.shape[0], x_train.shape[1], 1))
        y_train = np.reshape(y_train, (-1, 1))
        x_test, y_test = np.array(x_test), np.array(y_test)
        x_test = np.reshape(x_test, (x_test.shape[0], x_test.shape[1], 1))
    y_test = np.reshape(y_test, (-1, 1))
    return x_train, x_test, y_train, y_test


def splitter(dataset, cut_point):
    training_set = dataset[:int(cut_point*len(dataset))]
    test_set = dataset[int(cut_point*len(dataset)):]
    return training_set, test_set


def load_standard_data_frame(input_array):
    df = pd.DataFrame(input_array).set_index('time')
    df.pop('conversionType')
    df.pop('conversionSymbol')
    return df


def predict_n_days(model, scaler, days, start_values, one_batch_size):
    queue = start_values.copy()
    results = list()
    for x in range(int(days)):
        input_array = np.array(queue)
        input_array = np.reshape(input_array, (-1,1))
        input_array = scaler.transform(input_array)
        input_array = np.array([input_array])
        input_array = np.array([input_array])
        input_array = np.reshape(input_array, (1, one_batch_size, 1))
        predicted_price = model.predict(input_array)
        predicted_price = scaler.inverse_transform(predicted_price)
        results.append(predicted_price[-1][-1])
        queue.append(predicted_price[-1][-1])
        queue.pop(0)
    return results

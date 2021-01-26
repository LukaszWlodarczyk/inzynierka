from datetime import datetime

import tensorflow as tf

from GUI.gui_service import *

TEST_REAL_CURRENCY = REAL_CURRENCY['USD']
TRAIN_TEST_SPLIT_POINT = 0.8
# value from 0 (0%) - 1 (100%) as index in whole_test_set
TEST_BATCH_BEGIN = [0.05, 0.25, 0.50]
ONE_BATCH_SIZE = 60
DAYS_TO_PREDICT = 5


def test_model_prediction():
    model = None
    scaler = None
    predicted_days = []

    date = datetime.now().strftime("%m_%d-%H_%M")

    with open(f'Prediction_test-{date}.txt', 'w') as f:
        for test_batch_begin in TEST_BATCH_BEGIN:
            print(f'TESTING begin: {test_batch_begin}')
            f.write(f'TEST_BATCH_BEGIN = {test_batch_begin}\n')

            for data_type in DATA_TYPE:
                print(f'\tTESTING data type: {data_type}')
                f.write(f'DATA_TYPE = {data_type}\n')

                for currency in CRYPTO_CURRENCY:
                    if data_type == DATA_TYPE['DAYS']:
                        scaler, model = models_loader.get_daily_model(currency)
                    elif data_type == DATA_TYPE['HOURS']:
                        scaler, model = models_loader.get_hourly_model(currency)
                    elif data_type == DATA_TYPE['MINUTES']:
                        scaler, model = models_loader.get_minutes_model(currency)

                    print(f'\t\tTESTING currency: {currency}')
                    data = get_hist_data_type(data_type, currency, TEST_REAL_CURRENCY)
                    whole_test_set = data[int(len(data) * TRAIN_TEST_SPLIT_POINT):]

                    temp_index = int(len(whole_test_set) * test_batch_begin)
                    if temp_index + 60 > len(whole_test_set) - DAYS_TO_PREDICT:
                        raise NameError('TEST BATCH BEGIN TO HIGH!')

                    batch = whole_test_set[temp_index:temp_index + 60]
                    real_values = whole_test_set[temp_index + 60:temp_index + 60 + DAYS_TO_PREDICT]
                    predicted_days = predict_n_days(model, scaler, DAYS_TO_PREDICT, batch, ONE_BATCH_SIZE)

                    print(f'Predicted: {predicted_days}')
                    print(f'Real: {real_values}')
                    f.write(f'{currency}:\nP={predicted_days}\nR={real_values}\n')

                tf.keras.backend.clear_session()


test_model_prediction()

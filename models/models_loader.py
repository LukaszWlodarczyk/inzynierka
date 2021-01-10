from keras.models import load_model
from joblib import load


def get_daily_model(crypto='BTC'):
    if crypto == 'BCH':
        model = load_model('../saved_model/BCH_model_for_days_val_lose_6.835738895460963e-05')
        scaler = load('../saved_model/BCH_scaler_for_model_for_days_val_lose_6.835738895460963e-05')
    elif crypto == 'ETH':
        model = load_model('../saved_model/ETH_model_for_days_val_lose_0.0008011589525267482')
        scaler = load('../saved_model/ETH_scaler_for_model_for_days_val_lose_0.0008011589525267482')
    elif crypto == 'LTC':
        model = load_model('../saved_model/LTC_model_for_days_val_lose_0.000672103080432862')
        scaler = load('../saved_model/LTC_scaler_for_model_for_days_val_lose_0.000672103080432862')
    else:
        model = load_model('../saved_model/BTC_model_for_days_val_lose_0.0008853988256305456')
        scaler = load('../saved_model/BTC_scaler_for_model_for_days_val_lose_0.0008853988256305456')
    return scaler, model


def get_full_data_daily_model(crypto='BTC'):
    if crypto == 'BCH':
        model = load_model('../saved_model/BCH_scaler_for_model_for_full_data_days_val_lose_0.00014146998000796884')
        scaler = load('../saved_model/BCH_scaler_for_model_for_full_data_days_val_lose_0.00014146998000796884')
    elif crypto == 'ETH':
        model = load_model('../saved_model/ETH_model_for_days_from_full_data__val_lose_0.0012043137103319168')
        scaler = load('../saved_model/ETH_scaler_for_model_for_full_data_days_val_lose_0.0012043137103319168')
    elif crypto == 'LTC':
        model = load_model('../saved_model/LTC_model_for_days_from_full_data__val_lose_0.0006487903883680701')
        scaler = load('../saved_model/LTC_scaler_for_model_for_full_data_days_val_lose_0.0006487903883680701')
    else:
        model = load_model('../saved_model/BTC_model_for_days_from_full_data__val_lose_0.0012485124170780182')
        scaler = load('../saved_model/BTC_scaler_for_model_for_full_data_days_val_lose_0.0012485124170780182')
    return scaler, model


def get_hourly_model(crypto='BTC'):
    if crypto == 'BCH':
        model = load_model('../saved_model/BCH_model_for_hours_val_lose_0.0012152665294706821')
        scaler = load('../saved_model/BCH_scaler_for_model_for_hours_val_lose_0.0012152665294706821')
    elif crypto == 'ETH':
        model = load_model('../saved_model/ETH_model_for_hours_val_lose_0.003915078938007355')
        scaler = load('../saved_model/ETH_scaler_for_model_for_hours_val_lose_0.003915078938007355')
    elif crypto == 'LTC':
        model = load_model('../saved_model/LTC_model_for_hours_val_lose_0.001086461590602994')
        scaler = load('../saved_model/LTC_scaler_for_model_for_hours_val_lose_0.001086461590602994')
    else:
        model = load_model('../saved_model/BTC_model_for_hours_val_lose_0.004351846408098936')
        scaler = load('../saved_model/BTC_scaler_for_model_for_hours_val_lose_0.004351846408098936')
    return scaler, model


def get_full_data_hourly_model(crypto='BTC'):
    if crypto == 'BCH':
        model = load_model('../saved_model/BCH_model_for_hours_from_full_data__val_lose_0.0008140421123243868')
        scaler = load('../saved_model/BCH_scaler_for_model_for_full_data_hours_val_lose_0.0008140421123243868')
    elif crypto == 'ETH':
        model = load_model('../saved_model/ETH_model_for_hours_from_full_data__val_lose_0.008936298079788685')
        scaler = load('../saved_model/ETH_scaler_for_model_for_full_data_hours_val_lose_0.008936298079788685')
    elif crypto == 'LTC':
        model = load_model('../saved_model/LTC_model_for_hours_from_full_data__val_lose_0.004277145955711603')
        scaler = load('../saved_model/LTC_scaler_for_model_for_full_data_hours_val_lose_0.004277145955711603')
    else:
        model = load_model('../saved_model/BTC_model_for_hours_from_full_data__val_lose_0.006839446723461151')
        scaler = load('../saved_model/BTC_scaler_for_model_for_full_data_hours_val_lose_0.006839446723461151')
    return scaler, model


def get_minutes_model(crypto='BTC'):
    if crypto == 'BCH':
        model = load_model('../saved_model/BCH_model_for_minutes_val_lose_0.0006603752844966948')
        scaler = load('../saved_model/BCH_scaler_for_model_for_minutes_val_lose_0.0006603752844966948')
    elif crypto == 'ETH':
        model = load_model('../saved_model/ETH_model_for_minutes_val_lose_0.0016128011047840118')
        scaler = load('../saved_model/ETH_scaler_for_model_for_minutes_val_lose_0.0016128011047840118')
    elif crypto == 'LTC':
        model = load_model('../saved_model/LTC_model_for_minutes_val_lose_0.0013784549664705992')
        scaler = load('../saved_model/LTC_scaler_for_model_for_minutes_val_lose_0.0013784549664705992')
    else:
        model = load_model('../saved_model/BTC_model_for_minutes_val_lose_0.00028970083803869784')
        scaler = load('../saved_model/BTC_scaler_for_model_for_minutes_val_lose_0.00028970083803869784')
    return scaler, model


def get_full_data_minutes_model(crypto='BTC'):
    if crypto == 'BCH':
        model = load_model('../saved_model/BCH_model_for_minutes_from_full_data__val_lose_0.0007887802203185856')
        scaler = load('../saved_model/BCH_scaler_for_model_for_full_data_minutes_val_lose_0.0007887802203185856')
    elif crypto == 'ETH':
        model = load_model('../saved_model/ETH_model_for_minutes_from_full_data__val_lose_0.004669217858463526')
        scaler = load('../saved_model/ETH_scaler_for_model_for_full_data_minutes_val_lose_0.004669217858463526')
    elif crypto == 'LTC':
        model = load_model('../saved_model/LTC_model_for_minutes_from_full_data__val_lose_0.002677817828953266')
        scaler = load('../saved_model/LTC_scaler_for_model_for_full_data_minutes_val_lose_0.002677817828953266')
    else:
        model = load_model('../saved_model/BTC_model_for_minutes_from_full_data__val_lose_0.005418878979980946')
        scaler = load('../saved_model/BTC_scaler_for_model_for_full_data_minutes_val_lose_0.005418878979980946')
    return scaler, model

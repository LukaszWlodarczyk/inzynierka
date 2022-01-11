from keras.models import load_model
from joblib import load


def get_daily_model(crypto='BTC'):
    if crypto == 'BCH':
        model = load_model('../saved_model/BCH_model_for_days_val_lose_0.0003556078299880028')
        scaler = load('../saved_model/BCH_scaler_for_model_for_days_val_lose_0.0003556078299880028')
    elif crypto == 'ETH':
        model = load_model('../saved_model/ETH_model_for_days_val_lose_0.0045670755207538605')
        scaler = load('../saved_model/ETH_scaler_for_model_for_days_val_lose_0.0045670755207538605')
    elif crypto == 'LTC':
        model = load_model('../saved_model/LTC_model_for_days_val_lose_0.001030375249683857')
        scaler = load('../saved_model/LTC_scaler_for_model_for_days_val_lose_0.001030375249683857')
    else:
        model = load_model('../saved_model/BTC_model_for_days_val_lose_0.0011318516917526722')
        scaler = load('../saved_model/BTC_scaler_for_model_for_days_val_lose_0.0011318516917526722')
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
        model = load_model('../saved_model/BCH_model_for_hours_val_lose_0.0001958483480848372')
        scaler = load('../saved_model/BCH_scaler_for_model_for_hours_val_lose_0.0001958483480848372')
    elif crypto == 'ETH':
        model = load_model('../saved_model/ETH_model_for_hours_val_lose_0.0007593229529447854')
        scaler = load('../saved_model/ETH_scaler_for_model_for_hours_val_lose_0.0007593229529447854')
    elif crypto == 'LTC':
        model = load_model('../saved_model/LTC_model_for_hours_val_lose_0.00015368525055237114')
        scaler = load('../saved_model/LTC_scaler_for_model_for_hours_val_lose_0.00015368525055237114')
    else:
        model = load_model('../saved_model/BTC_model_for_hours_val_lose_0.00048355001490563154')
        scaler = load('../saved_model/BTC_scaler_for_model_for_hours_val_lose_0.00048355001490563154')
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
        model = load_model('../saved_model/BCH_model_for_minutes_val_lose_0.0014615935506299138')
        scaler = load('../saved_model/BCH_scaler_for_model_for_minutes_val_lose_0.0014615935506299138')
    elif crypto == 'ETH':
        model = load_model('../saved_model/ETH_model_for_minutes_val_lose_0.0014071454061195254')
        scaler = load('../saved_model/ETH_scaler_for_model_for_minutes_val_lose_0.0014071454061195254')
    elif crypto == 'LTC':
        model = load_model('../saved_model/LTC_model_for_minutes_val_lose_0.0008961712010204792')
        scaler = load('../saved_model/LTC_scaler_for_model_for_minutes_val_lose_0.0008961712010204792')
    else:
        # model = load_model('../saved_model/BTC_model_for_minutes_val_lose_0.00028970083803869784')
        # scaler = load('../saved_model/BTC_scaler_for_model_for_minutes_val_lose_0.00028970083803869784')
        model = load_model('../saved_model/BTC_model_for_minutes_val_lose_0.0023628431372344494')
        scaler = load('../saved_model/BTC_scaler_for_model_for_minutes_val_lose_0.0023628431372344494')
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

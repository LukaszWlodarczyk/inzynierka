import pandas as pd
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

from models import models_loader
from preparing_model.functions import predict_n_days, load_standard_data_frame
from requests_module.my_requests import get_minute_last_day_data_with_limit, get_hourly_last_3_months_data_with_limit, \
    get_all_historical_data_with_limit, get_full_current_info, get_current_price, CRYPTO_CURRENCY, REAL_CURRENCY, \
    get_yesterday_price, get_all_historical_data, get_hourly_last_3_months_data, get_minute_last_day_data

theme = 'DarkGrey9'

DATA_TYPE = {
    'DAYS': 'DAYS',
    'HOURS': 'HOURS',
    'MINUTES': 'MINUTES'
}

default_selected_crypto = CRYPTO_CURRENCY['BTC']
default_selected_real_currency = REAL_CURRENCY['USD']
default_data_type = DATA_TYPE['MINUTES']
default_limit = 1440


def get_current_data(crypto_currency='BTC', real_currency='USD'):
    response = get_full_current_info(crypto_currency, real_currency)[0]
    price = response['PRICE']
    highday = response['HIGHDAY']
    lowday = response['LOWDAY']
    openday = response['OPENDAY']
    volumeday = response['VOLUMEDAY']
    return price, highday, lowday, openday, volumeday


def get_last_data(data_type=DATA_TYPE['DAYS'],
                  limit=1,
                  crypto_currency='BTC',
                  real_currency='USD'):
    if data_type == DATA_TYPE['DAYS']:
        response_frame = pd.DataFrame(
            get_all_historical_data_with_limit(limit, crypto_currency, real_currency),
            columns=['high', 'low', 'open', 'volumefrom', 'volumeto', 'close'])
    elif data_type == DATA_TYPE['HOURS']:
        response_frame = pd.DataFrame(
            get_hourly_last_3_months_data_with_limit(limit, crypto_currency, real_currency),
            columns=['high', 'low', 'open', 'volumefrom', 'volumeto', 'close'])
    elif data_type == DATA_TYPE['MINUTES']:
        response_frame = pd.DataFrame(
            get_minute_last_day_data_with_limit(limit, crypto_currency, real_currency),
            columns=['high', 'low', 'open', 'volumefrom', 'volumeto', 'close'])
    else:
        raise NameError('Zly argument')

    response_frame = response_frame.values.tolist()
    return response_frame


def get_exchange_rate(from_currency, to_currency):
    price1 = get_current_price(CRYPTO_CURRENCY['BTC'], from_currency)
    price2 = get_current_price(CRYPTO_CURRENCY['BTC'], to_currency)

    return round(price2 / price1, 4)


def get_predicted_data_from_only_price_model(days_to_predict, data_type=DATA_TYPE['MINUTES'],
                                             crypto_currency=CRYPTO_CURRENCY['BTC'], full_data=False):
    past_period = 60
    if data_type == DATA_TYPE['DAYS']:
        if full_data:
            scaler, model = models_loader.get_full_data_daily_model(crypto_currency)
            response_frame = load_standard_data_frame(get_all_historical_data_with_limit(past_period - 1,
                                                                                         crypto_currency))
        else:
            scaler, model = models_loader.get_daily_model(crypto_currency)
            response_frame = pd.DataFrame(get_all_historical_data_with_limit(past_period - 1, crypto_currency),
                                          columns=['close'])
    elif data_type == DATA_TYPE['HOURS']:
        if full_data:
            scaler, model = models_loader.get_full_data_daily_model(crypto_currency)
            response_frame = load_standard_data_frame(get_hourly_last_3_months_data_with_limit(past_period - 1,
                                                                                               crypto_currency))
        else:
            scaler, model = models_loader.get_hourly_model(crypto_currency)
            response_frame = pd.DataFrame(get_hourly_last_3_months_data_with_limit(past_period - 1, crypto_currency),
                                          columns=['close'])
    elif data_type == DATA_TYPE['MINUTES']:
        if full_data:
            scaler, model = models_loader.get_full_data_daily_model(crypto_currency)
            response_frame = load_standard_data_frame(get_minute_last_day_data_with_limit(past_period - 1,
                                                                                          crypto_currency))
        else:
            scaler, model = models_loader.get_minutes_model(crypto_currency)
            response_frame = pd.DataFrame(get_minute_last_day_data_with_limit(past_period - 1, crypto_currency),
                                          columns=['close'])
    else:
        raise NameError('Zly argument')
    response_frame = response_frame.values.tolist()
    results = []
    for xd in response_frame:
        results.append(*xd)
    return predict_n_days(model, scaler, days_to_predict, results, past_period)


def get_hist_data_with_limit_and_type(data_type=DATA_TYPE['MINUTES'],
                                      limit=59,
                                      crypto_currency='BTC',
                                      real_currency='USD'):
    if data_type == DATA_TYPE['DAYS']:
        response_frame = pd.DataFrame(get_all_historical_data_with_limit(limit,
                                                                         crypto_currency,
                                                                         real_currency), columns=['close'])
    elif data_type == DATA_TYPE['HOURS']:
        response_frame = pd.DataFrame(get_hourly_last_3_months_data_with_limit(limit,
                                                                               crypto_currency,
                                                                               real_currency), columns=['close'])
    elif data_type == DATA_TYPE['MINUTES']:
        response_frame = pd.DataFrame(get_minute_last_day_data_with_limit(limit,
                                                                          crypto_currency,
                                                                          real_currency), columns=['close'])
    else:
        raise NameError('Zly argument')

    response_frame = response_frame.values.tolist()
    results = []
    for xd in response_frame:
        results.append(*xd)

    return results


def get_hist_data_type(data_type=DATA_TYPE['MINUTES'],
                       crypto_currency='BTC',
                       real_currency='USD'):
    if data_type == DATA_TYPE['DAYS']:
        response_frame = pd.DataFrame(get_all_historical_data(crypto_currency,
                                                              real_currency), columns=['close'])
    elif data_type == DATA_TYPE['HOURS']:
        response_frame = pd.DataFrame(get_hourly_last_3_months_data(crypto_currency,
                                                                    real_currency), columns=['close'])
    elif data_type == DATA_TYPE['MINUTES']:
        response_frame = pd.DataFrame(get_minute_last_day_data(crypto_currency,
                                                               real_currency), columns=['close'])
    else:
        raise NameError('Zly argument')

    response_frame = response_frame.values.tolist()
    results = []
    for xd in response_frame:
        results.append(*xd)

    return results


def change(selected_crypto, selected_real_currency):
    return 100 * get_current_price(selected_crypto, selected_real_currency) / \
           get_yesterday_price(selected_crypto, selected_real_currency) - 100


def set_tb_change_color(window, key, value):
    if value > 0:
        window[key].update(background_color="#00aa22")
    elif value < 0:
        window[key].update(background_color='#aa2200')
    else:
        window[key].update(background_color='#666666')


def refresh_current_data(data, base_key, crypto_curr, real_curr, window):
    for i in range(len(data)):
        if i != len(data) - 1:
            main_key = f'{base_key}{i}-'
            window[main_key].update(f'{round(data[i], 2)} {real_curr}')
            if i != 0:
                temp_change_proc = round(100 * data[i] / data[0] - 100, 3)
                temp_change = round(data[i] - data[0], 2)
                window[f'{main_key}CHANGE-'].update(f'change {temp_change} {real_curr} {temp_change_proc}% ')
                set_tb_change_color(window, f'{main_key}CHANGE-', temp_change)
        else:
            temp_volume = round(data[i], 2)
            temp_volume2 = round(temp_volume * data[0], 2)
            window[f'{base_key}{i}-'].update(f'{temp_volume} {crypto_curr}')
            window[f'{base_key}{i}-VOLUME-'].update(f'{temp_volume2} {real_curr}')


def draw_figure(canvas, figure, loc=(0, 0)):
    figure_canvas_agg = FigureCanvasTkAgg(figure, master=canvas)
    figure_canvas_agg.draw()
    figure_canvas_agg.get_tk_widget().pack(side='top', fill='both', expand=1)
    return figure_canvas_agg

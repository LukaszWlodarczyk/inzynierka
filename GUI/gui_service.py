import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

from models import models_loader
from functions import predict_n_days
from my_requests import get_minute_last_day_data_with_limit,get_hourly_last_3_months_data_with_limit, \
    get_all_historical_data_with_limit, get_full_current_info
from my_requests import *

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


def get_exchange_rate(from_currency, to_currency):
    price1 = get_current_price(CRYPTO_CURRENCY['BTC'], from_currency)
    price2 = get_current_price(CRYPTO_CURRENCY['BTC'], to_currency)

    print(price1, price2, price2/price1)

    return round(price2/price1, 4)


def get_predicted_data_from_only_price_model(days_to_predict, data_type=DATA_TYPE['MINUTES']):
    if data_type == DATA_TYPE['DAYS']:
        scaler, model = models_loader.get_daily_model()
        response_frame = pd.DataFrame(get_all_historical_data_with_limit(29), columns=['close'])
    elif data_type == DATA_TYPE['HOURS']:
        scaler, model = models_loader.get_hourly_model()
        response_frame = pd.DataFrame(get_hourly_last_3_months_data_with_limit(29), columns=['close'])
    elif data_type == DATA_TYPE['MINUTES']:
        scaler, model = models_loader.get_minutes_model()
        response_frame = pd.DataFrame(get_minute_last_day_data_with_limit(13), columns=['close'])
    else:
        raise NameError('Zly argument')
    response_frame = response_frame.values.tolist()
    results = []
    for xd in response_frame:
        results.append(*xd)
    return predict_n_days(model, scaler, days_to_predict, results, 14)


def get_hist_data_with_limit_and_type(data_type=DATA_TYPE['MINUTES'],
                                      limit=29,
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


def change(selected_crypto, selected_real_currency):
    return 100 * get_current_price(selected_crypto, selected_real_currency) / \
           get_yesterday_price(selected_crypto, selected_real_currency) - 100


def update_limit_text(value, data_type):
    years = 0
    months = 0
    days = 0
    hours = 0
    minutes = 0
    if data_type == DATA_TYPE['DAYS']:
        years = divmod(value, 360)[0]
        months = divmod(value, 30)[0] % 12
        days = divmod(value, 30)[1]
    elif data_type == DATA_TYPE['HOURS']:
        months = divmod(value, 720)[0]
        days = divmod(value, 24)[0] % 30
        hours = divmod(value, 24)[1]
    elif data_type == DATA_TYPE['MINUTES']:
        days = divmod(value, 1440)[0]
        hours = divmod(value, 60)[0] % 24
        minutes = divmod(value, 60)[1]

    return f'Time limit: {years} years {months} months {days} days {hours} hours {minutes} minutes'


def update_chart(selected_crypto, selected_real_currency, data_type, limit, current_fig, window):
    data = None
    if data_type == DATA_TYPE['DAYS']:
        print('Days', selected_crypto, selected_real_currency)
        data = get_hist_data_with_limit_and_type(DATA_TYPE['DAYS'], limit, selected_crypto, selected_real_currency)
    elif data_type == DATA_TYPE['HOURS']:
        print('Hours', selected_crypto, selected_real_currency)
        data = get_hist_data_with_limit_and_type(DATA_TYPE['HOURS'], limit, selected_crypto, selected_real_currency)
    elif data_type == DATA_TYPE['MINUTES']:
        print('Minutes', selected_crypto, selected_real_currency)
        data = get_hist_data_with_limit_and_type(DATA_TYPE['MINUTES'], limit, selected_crypto, selected_real_currency)

    fig = plt.Figure(figsize=(7, 5), dpi=100)
    plot = fig.add_subplot(111)
    plot.plot(data, color='blue', label=f'{data_type} price')
    plot.set_title(f'{selected_crypto} price')
    plot.set_xlabel('Timestamp')
    plot.set_ylabel(f'Price [{selected_real_currency}]')
    plot.legend()

    canvas = window['-CANVAS-'].TKCanvas

    if current_fig is not None:
        current_fig.get_tk_widget().forget()
        plt.close('all')
    return draw_figure(canvas, fig, loc=(0, 0))


def draw_figure(canvas, figure, loc=(0, 0)):
    figure_canvas_agg = FigureCanvasTkAgg(figure, master=canvas)
    figure_canvas_agg.draw()
    figure_canvas_agg.get_tk_widget().pack(side='top', fill='both', expand=1)
    return figure_canvas_agg


# print(get_predicted_data_from_only_price_model(7,'days'))
# print(get_predicted_data_from_only_price_model(7,'HOURS'))
# print(get_predicted_data_from_only_price_model(14,'MINUTES'))
# print(get_predicted_data_from_only_price_model(7,'marocha')) throw exception NameError
# print(get_current_data())

from models import models_loader
import numpy as np
import pandas as pd
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

from functions import predict_n_days
from my_requests import get_minute_last_day_data_with_limit,get_hourly_last_3_months_data_with_limit, \
    get_all_historical_data_with_limit, get_full_current_info

DATA_TYPE = {
    'DAYS': 'DAYS',
    'HOURS': 'HOURS',
    'MINUTES': 'MINUTES'
}


def get_current_data(crypto_currency='BTC', real_currency='USD'):
    response = get_full_current_info(crypto_currency,real_currency)[0]
    price = response['PRICE']
    highday = response['HIGHDAY']
    lowday = response['LOWDAY']
    openday = response['OPENDAY']
    volumeday = response['VOLUMEDAY']
    return price, highday, lowday, openday, volumeday


def get_predicted_data_from_only_price_model(days_to_predict, data_type=DATA_TYPE['MINUTES']):
    if data_type == DATA_TYPE['DAYS']:
        scaler, model = models_loader.get_daily_model()
        response_frame = pd.DataFrame(get_all_historical_data_with_limit(29), columns=['close'])
    elif data_type == DATA_TYPE['HOURS']:
        scaler, model = models_loader.get_hourly_model()
        response_frame = pd.DataFrame(get_hourly_last_3_months_data_with_limit(29), columns=['close'])
    elif data_type == DATA_TYPE['MINUTES']:
        scaler, model = models_loader.get_minutes_model()
        response_frame = pd.DataFrame(get_minute_last_day_data_with_limit(29), columns=['close'])
    else:
        raise NameError('Zly argument')
    response_frame = response_frame.values.tolist()
    results = []
    for xd in response_frame:
        results.append(*xd)
    return predict_n_days(model, scaler, days_to_predict, results, 30)


def get_data_with_limit_and_type(data_type, limit=29, crypto_currency='BTC', real_currency='USD'):
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


def draw_figure(canvas, figure, loc=(0,0)):
    figure_canvas_agg = FigureCanvasTkAgg(figure, master=canvas)
    figure_canvas_agg.draw()
    figure_canvas_agg.get_tk_widget().pack(side='top', fill='both', expand=1)
    return figure_canvas_agg


# print(get_predicted_data_from_only_price_model(7,'days'))
# print(get_predicted_data_from_only_price_model(7,'hours'))
# print(get_predicted_data_from_only_price_model(7,'minutes'))
# print(get_predicted_data_from_only_price_model(7,'marocha')) throw exception NameError
# print(get_current_data())

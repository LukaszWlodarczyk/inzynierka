from models import models_loader
import numpy as np
import pandas as pd

from functions import predict_n_days
from my_requests import get_minute_last_day_data_with_limit,get_hourly_last_3_months_data_with_limit, \
    get_all_historical_data_with_limit


def get_predicted_data_from_only_price_model(days_to_predict,type='days'):
    if type == 'days':
        scaler, model = models_loader.get_daily_model()
        response_frame = pd.DataFrame(get_all_historical_data_with_limit(29), columns=['close'])
    elif type == "minutes":
        scaler, model = models_loader.get_minutes_model()
        response_frame = pd.DataFrame(get_minute_last_day_data_with_limit(29), columns=['close'])
    elif type == "hours":
        scaler, model = models_loader.get_hourly_model()
        response_frame = pd.DataFrame(get_hourly_last_3_months_data_with_limit(29), columns=['close'])
    else:
        raise NameError("Zly argument")
    response_frame = response_frame.values.tolist()
    results = []
    for xd in response_frame:
        results.append(*xd)
    return predict_n_days(model,scaler,days_to_predict,results,30)


print(get_predicted_data_from_only_price_model(7,'days'))
print(get_predicted_data_from_only_price_model(7,'hours'))
print(get_predicted_data_from_only_price_model(7,'minutes'))
# print(get_predicted_data_from_only_price_model(7,'marocha')) throw exception NameError

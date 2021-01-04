from keras.models import load_model
from joblib import load


def get_daily_model():
    model = load_model('../saved_model/model_for_days_val_lose_0.0005349027342163026')
    scaler = load('../saved_model/scaler_for_model_for_days_val_lose_0.0005349027342163026')
    return scaler, model


def get_full_data_daily_model():
    model = load_model('../saved_model/model_for_days_from_full_data__val_lose_0.0033478490076959133')
    scaler = load('../saved_model/scaler_for_model_for_full_data_days_val_lose_0.0033478490076959133')
    return scaler, model


def get_hourly_model():
    model = load_model('../saved_model/model_for_hours_val_lose_0.0011267336085438728')
    scaler = load('../saved_model/scaler_for_model_for_hours_val_lose_0.0011267336085438728')
    return scaler, model


def get_full_data_hourly_model():
    model = load_model('../saved_model/model_for_hours_from_full_data__val_lose_0.01617264375090599')
    scaler = load('../saved_model/scaler_for_model_for_full_data_hours_val_lose_0.01617264375090599')
    return scaler, model


def get_minutes_model():
    model = load_model('../saved_model/model_for_minutes_val_lose_0.00312849716283381')
    scaler = load('../saved_model/scaler_for_model_for_minutes_val_lose_0.00312849716283381')
    return scaler, model


def get_full_data_minutes_model():
    model = load_model('../saved_model/model_for_minutes_from_full_data__val_lose_0.0029307608492672443')
    scaler = load('../saved_model/scaler_for_model_for_full_data_minutes_val_lose_0.0029307608492672443')
    return scaler, model

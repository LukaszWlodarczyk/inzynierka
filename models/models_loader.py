from keras.models import load_model


def get_daily_model():
    model = load_model('../saved_model/model_for_days_val_lose_0.0008113147341646254')
    return model


def get_full_data_daily_model():
    model = load_model('../saved_model/model_for_days_from_full_data__val_lose_0.0017455299384891987')
    return model


def get_hourly_model():
    model = load_model('../saved_model/model_for_hours_val_lose_0.004689630586653948')
    return model


def get_full_data_hourly_model():
    model = load_model('../saved_model/model_for_hours_from_full_data__val_lose_0.0009352078777737916')
    return model


def get_minutes_model():
    model = load_model('../saved_model/model_for_minutes_val_lose_0.005587339401245117')
    return model


def get_full_data_minutes_model():
    model = load_model('../saved_model/model_for_minutes_from_full_data__val_lose_0.007111578248441219')
    return model

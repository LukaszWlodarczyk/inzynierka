import pandas as pd

import requests_module

pd.set_option('max_columns', None)


def load_standard_data_frame(input_array):
    df = pd.DataFrame(input_array).set_index('time')
    df.pop('conversionType')
    df.pop('conversionSymbol')
    return df


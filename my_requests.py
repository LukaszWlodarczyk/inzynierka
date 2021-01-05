import requests

endpoint = "https://min-api.cryptocompare.com/data/"

CRYPTO_CURRENCY = {
    'BTC': 'BTC',
    'ETH': 'ETH',
    'BCH': 'BCH',
    'LTC': 'LTC'
}
REAL_CURRENCY = {
    'PLN': 'PLN',
    'USD': 'USD',
    'EUR': 'EUR'
}


def get_all_historical_data(crypto_currency=CRYPTO_CURRENCY['BTC'], standard_currency=REAL_CURRENCY['USD']):
    res = requests.get(f'{endpoint}v2/histoday?fsym={crypto_currency}&tsym={standard_currency}&allData=true')
    return res.json()['Data']['Data']


def get_current_price(crypto_currency=CRYPTO_CURRENCY['BTC'], standard_currency=REAL_CURRENCY['USD']):
    res = requests.get(f'{endpoint}price?fsym={crypto_currency}&tsyms={standard_currency}')
    price = res.json()[standard_currency]
    return price


def get_yesterday_price(crypto_currency=CRYPTO_CURRENCY['BTC'], standard_currency=REAL_CURRENCY['USD']):
    res = requests.get(f'{endpoint}v2/histohour?fsym={crypto_currency}&tsym={standard_currency}&limit=24')
    return res.json()['Data']['Data'][0]['close']


def get_full_current_info(crypto_currency=CRYPTO_CURRENCY['BTC'], standard_currency=REAL_CURRENCY['USD']):
    res = requests.get(f'{endpoint}pricemultifull?fsyms={crypto_currency}&tsyms={standard_currency}')
    return res.json()['RAW'][crypto_currency][standard_currency], res.json()['DISPLAY'][crypto_currency][standard_currency]


def get_hourly_last_3_months_data(crypto_currency=CRYPTO_CURRENCY['BTC'], standard_currency=REAL_CURRENCY['USD']):
    res = requests.get(f'{endpoint}v2/histohour?fsym={crypto_currency}&tsym={standard_currency}&limit=2000')
    return res.json()['Data']['Data']


def get_minute_last_day_data(crypto_currency=CRYPTO_CURRENCY['BTC'], standard_currency=REAL_CURRENCY['USD']):
    res = requests.get(f'{endpoint}v2/histominute?fsym={crypto_currency}&tsym={standard_currency}')
    return res.json()['Data']['Data']


def get_minute_last_day_data_with_limit(limit, crypto_currency=CRYPTO_CURRENCY['BTC'], standard_currency=REAL_CURRENCY['USD']):
    res = requests.get(f'{endpoint}v2/histominute?fsym={crypto_currency}&tsym={standard_currency}&limit={limit}')
    return res.json()['Data']['Data']


def get_hourly_last_3_months_data_with_limit(limit, crypto_currency=CRYPTO_CURRENCY['BTC'], standard_currency=REAL_CURRENCY['USD']):
    res = requests.get(f'{endpoint}v2/histohour?fsym={crypto_currency}&tsym={standard_currency}&limit={limit}')
    return res.json()['Data']['Data']


def get_all_historical_data_with_limit(limit,crypto_currency=CRYPTO_CURRENCY['BTC'], standard_currency=REAL_CURRENCY['USD']):
    res = requests.get(f'{endpoint}v2/histoday?fsym={crypto_currency}&tsym={standard_currency}&limit={limit}')
    return res.json()['Data']['Data']

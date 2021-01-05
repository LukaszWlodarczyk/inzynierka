import PySimpleGUI as sg
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
import matplotlib

import GUI.gui_service as gs
from my_requests import get_current_price, get_yesterday_price, CRYPTO_CURRENCY, REAL_CURRENCY, \
    get_all_historical_data_with_limit
from GUI.menu import menubar, handle_menu_click

default_selected_crypto = CRYPTO_CURRENCY['BTC']
default_selected_real_currency = REAL_CURRENCY['USD']
default_data_type = gs.DATA_TYPE['MINUTES']
default_limit = 1600

cb_crypto_value = sg.Combo(
    list(CRYPTO_CURRENCY.values()),
    default_selected_crypto,
    enable_events=True,
    size=(5, 1),
    key='-CB-CRYPTO-CURRENCY-')

cb_currency = sg.Combo(
    list(REAL_CURRENCY.values()),
    default_selected_real_currency,
    enable_events=True,
    size=(5, 1),
    key='-CB-REAL-CURRENCY-')

cb_data_type = sg.Combo(
    list(gs.DATA_TYPE.values()),
    default_data_type,
    enable_events=True,
    size=(10, 1),
    key='-CB-DATA-TYPE-')

text_current_price = sg.Text(f'Current price: '
                             f'{get_current_price(default_selected_crypto, default_selected_real_currency)} '
                             f'{default_selected_real_currency}', enable_events=True, auto_size_text=True)
text_yesterday_price = sg.Text(f'Yesterday price: '
                               f'{get_yesterday_price(default_selected_crypto, default_selected_real_currency)} '
                               f'{default_selected_real_currency}', enable_events=True, auto_size_text=True)


def change(selected_crypto, selected_real_currency):
    return 100 * get_current_price(selected_crypto, selected_real_currency) / get_yesterday_price(selected_crypto,
                                                                                                  selected_real_currency) - 100


def update_limit_text(value, data_type):
    years = 0
    months = 0
    days = 0
    hours = 0
    minutes = 0
    if data_type == gs.DATA_TYPE['DAYS']:
        pass
    elif data_type == gs.DATA_TYPE['HOURS']:
        months = divmod(value, 720)[0]
        days = divmod(value, 24)[0] % 30
        hours = divmod(value, 24)[1]
    elif data_type == gs.DATA_TYPE['MINUTES']:
        days = divmod(value, 1440)[0]
        hours = divmod(value, 60)[0] % 24
        minutes = divmod(value, 60)[1]

    return f'Time limit: {years} years {months} months {days} days {hours} hours {minutes} minutes'


text_change = sg.Text(f'Change: {change(default_selected_crypto, default_selected_real_currency)} %')
input_limit_text = sg.Text(update_limit_text(default_limit, default_data_type))

col_left = sg.Column([
    [sg.Text('Cryptocurrency: '), cb_crypto_value],
    [sg.Text('Real currency: '), cb_currency],
    [text_current_price],
    [text_yesterday_price],
    [text_change]
], size=(400, 100))

col_right = sg.Column([
    [sg.Text('Data type: '), cb_data_type],
    [sg.Text('Enter time limit:')],
    [sg.Input(default_limit, enable_events=True, size=(10, 1), key='-INPUT-LIMIT-'),
     sg.Button('OK', size=(2, 1), key='-INPUT-OK-')],
    [input_limit_text]

])

layout_home = [[sg.Text('MAIN')],
               [col_left, col_right],
               [sg.Canvas(key='-CANVAS-', size=(50, 50))]]

layout_days = [[sg.Text('Days')]]

layout_hours = [[sg.Text('HOURS')]]

layout_minutes = [[sg.Text('MINUTES')]]

main_layout = [
    [sg.Frame('Button menu', [
        [sg.Text('PREDICTIONS', key='-TITLE-')],
        [sg.Button('Main', disabled=True, key='-MAIN-', size=(10, 2)),
         sg.Button('Days', key='-DAYS-', size=(10, 2)),
         sg.Button('Hours', key='-HOURS-', size=(10, 2)),
         sg.Button('Minutes', key='-MINUTES-', size=(10, 2))]
    ])],
    [sg.Column(layout_home, key='-COL-MAIN-'),
     sg.Column(layout_days, visible=False, key='-COL-DAYS-'),
     sg.Column(layout_hours, visible=False, key='-COL-HOURS-'),
     sg.Column(layout_minutes, visible=False, key='-COL-MINUTES-')]
]

window = sg.Window(title="Crypto$", layout=main_layout, margins=(10, 10), resizable=False, finalize=True)


def currency_change(event_values):
    new_selected_crypto = event_values['-CB-CRYPTO-CURRENCY-']
    new_selected_real_currency = event_values['-CB-REAL-CURRENCY-']

    current_price = get_current_price(new_selected_crypto, new_selected_real_currency)
    yesterday_price = get_yesterday_price(new_selected_crypto, new_selected_real_currency)

    text_current_price.update(f'Current price: '
                              f'{current_price} '
                              f'{new_selected_real_currency}')
    text_yesterday_price.update(f'Yesterday price: '
                                f'{yesterday_price} '
                                f'{new_selected_real_currency}')

    text_change.update(f'Change: {change(new_selected_crypto, new_selected_real_currency)} %')


def update_chart(selected_crypto, selected_real_currency, data_type, limit, current_fig):
    data = None
    if data_type == gs.DATA_TYPE['DAYS']:
        print('Days', selected_crypto, selected_real_currency)
        data = gs.get_data_with_limit_and_type(gs.DATA_TYPE['DAYS'], limit, selected_crypto, selected_real_currency)
    elif data_type == gs.DATA_TYPE['HOURS']:
        print('Hours', selected_crypto, selected_real_currency)
        data = gs.get_data_with_limit_and_type(gs.DATA_TYPE['HOURS'], limit, selected_crypto, selected_real_currency)
    elif data_type == gs.DATA_TYPE['MINUTES']:
        print('Minutes', selected_crypto, selected_real_currency)
        data = gs.get_data_with_limit_and_type(gs.DATA_TYPE['MINUTES'], limit, selected_crypto, selected_real_currency)

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
    return gs.draw_figure(canvas, fig, loc=(0, 0))


current_canvas_fig = update_chart(default_selected_crypto,
                                  default_selected_real_currency,
                                  default_data_type,
                                  default_limit,
                                  None)

current_limit = default_limit
current_layout = '-MAIN-'
while True:
    event, values = window.read()
    print(event, values)
    if event in (None, 'Exit'):
        break

    elif event in ['-MAIN-', '-DAYS-', '-HOURS-', '-MINUTES-']:
        window[current_layout].update(disabled=False)
        window[f'-COL{current_layout}'].update(visible=False)
        window[event].update(disabled=True)
        window[f'-COL{event}'].update(visible=True)
        current_layout = event

    elif event in ['-CB-REAL-CURRENCY-', '-CB-CRYPTO-CURRENCY-']:
        currency_change(values)
        current_canvas_fig = update_chart(values['-CB-CRYPTO-CURRENCY-'],
                                          values['-CB-REAL-CURRENCY-'],
                                          values['-CB-DATA-TYPE-'],
                                          current_limit,
                                          current_canvas_fig)
    elif event == '-INPUT-OK-':
        current_limit = int(values['-INPUT-LIMIT-'])
        input_limit_text.update(update_limit_text(current_limit, values['-CB-DATA-TYPE-']))
        current_canvas_fig = update_chart(values['-CB-CRYPTO-CURRENCY-'],
                                          values['-CB-REAL-CURRENCY-'],
                                          values['-CB-DATA-TYPE-'],
                                          current_limit,
                                          current_canvas_fig)

    elif event == '-INPUT-LIMIT-':
        if len(values['-INPUT-LIMIT-']) and values['-INPUT-LIMIT-'][-1] not in '0123456789':
            window['-INPUT-LIMIT-'].update(values['-INPUT-LIMIT-'][:-1])

    else:
        pass
window.close()

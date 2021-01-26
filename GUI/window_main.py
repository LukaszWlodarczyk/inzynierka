import PySimpleGUI as sg
from datetime import datetime, timedelta
from re import match
import tensorflow as tf

from GUI.gui_service import *
from my_requests import REAL_CURRENCY
from window_details import layout_details, handle_event

# from GUI.menu import menubar, handle_menu_click

# -----------------------------------------------------------------------------
sg.LOOK_AND_FEEL_TABLE['Marocha'] = {'BACKGROUND': '#709053',
                                     'TEXT': '#fff4c9',
                                     'INPUT': '#c7e78b',
                                     'TEXT_INPUT': '#000000',
                                     'SCROLL': '#c7e78b',
                                     'BUTTON': ('white', '#709053'),
                                     'PROGRESS': ('#01826B', '#D0D0D0'),
                                     'BORDER': 1, 'SLIDER_DEPTH': 0, 'PROGRESS_DEPTH': 0,
                                     }

sg.theme(theme)

cb_currency = sg.Combo(
    list(REAL_CURRENCY.values()),
    default_selected_real_currency,
    enable_events=True,
    size=(6, 1),
    key='-CB-REAL-CURRENCY-')

cb_theme = sg.Combo(
    ['SIWY', 'MAROCHA'],
    'MAROCHA',
    enable_events=True,
    size=(15, 1),
    key='-CB-THEME-')

start_time = datetime.now()
refresh_time = start_time
refresh_delay = 90
text_date_time = sg.Text(start_time.strftime("%B %d, %Y %H:%M:%S"))

# -----------------------------------------------------------------------------
left_bar = sg.Column([
    [sg.Frame('', [
        [sg.Column([
            [sg.Text('CRYPTO$', size=(15, 2), font='Any 14 bold', justification='center')],

            [sg.Frame('Select model to prediction', [
                [sg.Column([
                    [sg.Radio('from only price', 'RADIO_MODEL', key='-RB-ONLY-PRICE-', enable_events=True,
                              default=True)],
                    [sg.Radio('from full data', 'RADIO_MODEL', key='-RB-FULL-DATA-', enable_events=True)]
                ], size=(200, 50), pad=(5, 5))]
            ], title_color='black', font='Any 11 bold')],

            [sg.Frame('Language', [
                [sg.Column([
                    [sg.Radio('PL', 'RADIO_LANG', key='-RB-PL-', enable_events=True, ),
                     sg.Radio('EN', 'RADIO_LANG', key='-RB-EN-', enable_events=True, default=True)]
                ], size=(200, 20), pad=(5, 5))]
            ], title_color='black', font='Any 11 bold')],

            [sg.Frame('Currency', [
                [sg.Column([
                    [cb_currency]
                ], size=(200, 20), pad=(5, 5))]
            ], title_color='black', font='Any 11 bold')],

            [sg.Frame('Theme', [
                [sg.Column([
                    [cb_theme]
                ], size=(200, 20), pad=(5, 5))]
            ], title_color='black', font='Any 11 bold')],

            [sg.Frame('Date and time', [
                [sg.Column([
                    [text_date_time]
                ], size=(200, 20), pad=(5, 5))]
            ], title_color='black', font='Any 11 bold')],
        ])]
    ])]
])

# -----------------------------------------------------------------------------
top_bar = sg.Frame('Button menu', [
    [sg.Button('Main', disabled=True, key='-MAIN-', size=(10, 2), pad=(40, 5)),
     sg.Button('DAYS', key='-DAYS-', size=(10, 2), pad=(40, 5)),
     sg.Button('HOURS', key='-HOURS-', size=(10, 2), pad=(40, 5)),
     sg.Button('MINUTES', key='-MINUTES-', size=(10, 2), pad=(40, 5))]
], pad=(50, 10))

# -----------------------------------------------------------------------------
home_small_tile_size = (220, 50)
home_tile_center_line_size = (150, 2)

layout_home_tile_BTC = [
    sg.Frame('BTC', [
        [sg.Column([
            [sg.Column([[
                sg.Column([
                    [sg.Text('price:'), sg.Text('000000000000 ###', key='-TX-BTC-0-')],
                ], size=home_small_tile_size),
                sg.Column([
                    [sg.Text('today high:'), sg.Text('000000000000 ###', key='-TX-BTC-1-')],
                    [sg.Text('change: +000000 ### (+00,00%)', key='-TX-BTC-1-CHANGE-')]
                ], size=home_small_tile_size),
                sg.Column([
                    [sg.Text('today low:'), sg.Text('000000000000 ###', key='-TX-BTC-2-')],
                    [sg.Text('change: +000000 ### (+00,00%)', key='-TX-BTC-2-CHANGE-')]
                ], size=home_small_tile_size),
                sg.Column([
                    [sg.Text('today open:'), sg.Text('000000000000 ###', key='-TX-BTC-3-')],
                    [sg.Text('change: +000000 ### (+00,00%)', key='-TX-BTC-3-CHANGE-')]
                ], size=home_small_tile_size),
                sg.Column([
                    [sg.Text('volume:'), sg.Text('0000000000000000 ###', key='-TX-BTC-4-')],
                    [sg.Text('volume:'), sg.Text('+0000000000000000000 ###', key='-TX-BTC-4-VOLUME-')]
                ], size=home_small_tile_size),
                sg.Column([
                    [sg.Button('REFRESH', size=(12, 2), key='-B-BTC-REFRESH-')]
                ], size=home_small_tile_size)
            ]])],

            [sg.Text('_' * 140, size=home_tile_center_line_size, justification='center')],

            [sg.Column([[
                sg.Column([
                    [sg.Text('one DAY ago:'), sg.Text('000000000000 ###', key='-TX-BTC-HIST-D-')],
                    [sg.Text('change: +000000 ### (+00,00%)', key='-TX-BTC-HIST-D-CHANGE-')]
                ], size=home_small_tile_size),
                sg.Column([
                    [sg.Text('one HOUR ago:'), sg.Text('000000000000 ###', key='-TX-BTC-HIST-H-')],
                    [sg.Text('change: +000000 ### (+00,00%)', key='-TX-BTC-HIST-H-CHANGE-')]
                ], size=home_small_tile_size),
                sg.Column([
                    [sg.Text('one MINUTE ago:'), sg.Text('000000000000 ###', key='-TX-BTC-HIST-M-')],
                    [sg.Text('change: +000000 ### (+00,00%)', key='-TX-BTC-HIST-M-CHANGE-')]
                ], size=home_small_tile_size),
                sg.Column([
                    [sg.Text('price for DAY:'), sg.Text('000000000000 ###', key='-TX-BTC-PRED-D-')],
                    [sg.Text('change: +000000 ### (+00,00%)', key='-TX-BTC-PRED-D-CHANGE-')]
                ], size=home_small_tile_size),
                sg.Column([
                    [sg.Text('price for HOUR:'), sg.Text('000000000000 ###', key='-TX-BTC-PRED-H-')],
                    [sg.Text('change: +000000 ### (+00,00%)', key='-TX-BTC-PRED-H-CHANGE-')]
                ], size=home_small_tile_size),
                sg.Column([
                    [sg.Text('price for MINUTE:'), sg.Text('000000000000 ###', key='-TX-BTC-PRED-M-')],
                    [sg.Text('change: +000000 ### (+00,00%)', key='-TX-BTC-PRED-M-CHANGE-')]
                ], size=home_small_tile_size),
            ]])]
        ])]
    ])
]

layout_home_tile_ETH = [
    sg.Frame('ETH', [
        [sg.Column([
            [sg.Column([[
                sg.Column([
                    [sg.Text('price:'), sg.Text('000000000000 ###', key='-TX-ETH-0-')],
                ], size=home_small_tile_size),
                sg.Column([
                    [sg.Text('today high:'), sg.Text('000000000000 ###', key='-TX-ETH-1-')],
                    [sg.Text('change: +000000 ### (+00,00%)', key='-TX-ETH-1-CHANGE-')]
                ], size=home_small_tile_size),
                sg.Column([
                    [sg.Text('today low:'), sg.Text('000000000000 ###', key='-TX-ETH-2-')],
                    [sg.Text('change: +000000 ### (+00,00%)', key='-TX-ETH-2-CHANGE-')]
                ], size=home_small_tile_size),
                sg.Column([
                    [sg.Text('today open:'), sg.Text('000000000000 ###', key='-TX-ETH-3-')],
                    [sg.Text('change: +000000 ### (+00,00%)', key='-TX-ETH-3-CHANGE-')]
                ], size=home_small_tile_size),
                sg.Column([
                    [sg.Text('volume:'), sg.Text('0000000000000000 ###', key='-TX-ETH-4-')],
                    [sg.Text('volume:'), sg.Text('+0000000000000000000 ###', key='-TX-ETH-4-VOLUME-')]
                ], size=home_small_tile_size),
                sg.Column([
                    [sg.Button('REFRESH', size=(12, 2), key='-B-ETH-REFRESH-')]
                ], size=home_small_tile_size)
            ]])],

            [sg.Text('_' * 140, size=home_tile_center_line_size, justification='center')],

            [sg.Column([[
                sg.Column([
                    [sg.Text('one DAY ago:'), sg.Text('000000000000 ###', key='-TX-ETH-HIST-D-')],
                    [sg.Text('change: +000000 ### (+00,00%)', key='-TX-ETH-HIST-D-CHANGE-')]
                ], size=home_small_tile_size),
                sg.Column([
                    [sg.Text('one HOUR ago:'), sg.Text('000000000000 ###', key='-TX-ETH-HIST-H-')],
                    [sg.Text('change: +000000 ### (+00,00%)', key='-TX-ETH-HIST-H-CHANGE-')]
                ], size=home_small_tile_size),
                sg.Column([
                    [sg.Text('one MINUTE ago:'), sg.Text('000000000000 ###', key='-TX-ETH-HIST-M-')],
                    [sg.Text('change: +000000 ### (+00,00%)', key='-TX-ETH-HIST-M-CHANGE-')]
                ], size=home_small_tile_size),
                sg.Column([
                    [sg.Text('price for DAY:'), sg.Text('000000000000 ###', key='-TX-ETH-PRED-D-')],
                    [sg.Text('change: +000000 ### (+00,00%)', key='-TX-ETH-PRED-D-CHANGE-')]
                ], size=home_small_tile_size),
                sg.Column([
                    [sg.Text('price for HOUR:'), sg.Text('000000000000 ###', key='-TX-ETH-PRED-H-')],
                    [sg.Text('change: +000000 ### (+00,00%)', key='-TX-ETH-PRED-H-CHANGE-')]
                ], size=home_small_tile_size),
                sg.Column([
                    [sg.Text('price for MINUTE:'), sg.Text('000000000000 ###', key='-TX-ETH-PRED-M-')],
                    [sg.Text('change: +000000 ### (+00,00%)', key='-TX-ETH-PRED-M-CHANGE-')]
                ], size=home_small_tile_size),
            ]])]
        ])]
    ])
]

layout_home_tile_LTC = [
    sg.Frame('LTC', [
        [sg.Column([
            [sg.Column([[
                sg.Column([
                    [sg.Text('price:'), sg.Text('000000000000 ###', key='-TX-LTC-0-')],
                ], size=home_small_tile_size),
                sg.Column([
                    [sg.Text('today high:'), sg.Text('000000000000 ###', key='-TX-LTC-1-')],
                    [sg.Text('change: +000000 ### (+00,00%)', key='-TX-LTC-1-CHANGE-')]
                ], size=home_small_tile_size),
                sg.Column([
                    [sg.Text('today low:'), sg.Text('000000000000 ###', key='-TX-LTC-2-')],
                    [sg.Text('change: +000000 ### (+00,00%)', key='-TX-LTC-2-CHANGE-')]
                ], size=home_small_tile_size),
                sg.Column([
                    [sg.Text('today open:'), sg.Text('000000000000 ###', key='-TX-LTC-3-')],
                    [sg.Text('change: +000000 ### (+00,00%)', key='-TX-LTC-3-CHANGE-')]
                ], size=home_small_tile_size),
                sg.Column([
                    [sg.Text('volume:'), sg.Text('0000000000000000 ###', key='-TX-LTC-4-')],
                    [sg.Text('volume:'), sg.Text('+0000000000000000000 ###', key='-TX-LTC-4-VOLUME-')]
                ], size=home_small_tile_size),
                sg.Column([
                    [sg.Button('REFRESH', size=(12, 2), key='-B-LTC-REFRESH-')]
                ], size=home_small_tile_size)
            ]])],

            [sg.Text('_' * 140, size=home_tile_center_line_size, justification='center')],

            [sg.Column([[
                sg.Column([
                    [sg.Text('one DAY ago:'), sg.Text('000000000000 ###', key='-TX-LTC-HIST-D-')],
                    [sg.Text('change: +000000 ### (+00,00%)', key='-TX-LTC-HIST-D-CHANGE-')]
                ], size=home_small_tile_size),
                sg.Column([
                    [sg.Text('one HOUR ago:'), sg.Text('000000000000 ###', key='-TX-LTC-HIST-H-')],
                    [sg.Text('change: +000000 ### (+00,00%)', key='-TX-LTC-HIST-H-CHANGE-')]
                ], size=home_small_tile_size),
                sg.Column([
                    [sg.Text('one MINUTE ago:'), sg.Text('000000000000 ###', key='-TX-LTC-HIST-M-')],
                    [sg.Text('change: +000000 ### (+00,00%)', key='-TX-LTC-HIST-M-CHANGE-')]
                ], size=home_small_tile_size),
                sg.Column([
                    [sg.Text('price for DAY:'), sg.Text('000000000000 ###', key='-TX-LTC-PRED-D-')],
                    [sg.Text('change: +000000 ### (+00,00%)', key='-TX-LTC-PRED-D-CHANGE-')]
                ], size=home_small_tile_size),
                sg.Column([
                    [sg.Text('price for HOUR:'), sg.Text('000000000000 ###', key='-TX-LTC-PRED-H-')],
                    [sg.Text('change: +000000 ### (+00,00%)', key='-TX-LTC-PRED-H-CHANGE-')]
                ], size=home_small_tile_size),
                sg.Column([
                    [sg.Text('price for MINUTE:'), sg.Text('000000000000 ###', key='-TX-LTC-PRED-M-')],
                    [sg.Text('change: +000000 ### (+00,00%)', key='-TX-LTC-PRED-M-CHANGE-')]
                ], size=home_small_tile_size),
            ]])]
        ])]
    ])
]

layout_home_tile_BCH = [
    sg.Frame('BCH', [
        [sg.Column([
            [sg.Column([[
                sg.Column([
                    [sg.Text('price:'), sg.Text('000000000000 ###', key='-TX-BCH-0-')],
                ], size=home_small_tile_size),
                sg.Column([
                    [sg.Text('today high:'), sg.Text('000000000000 ###', key='-TX-BCH-1-')],
                    [sg.Text('change: +000000 ### (+00,00%)', key='-TX-BCH-1-CHANGE-')]
                ], size=home_small_tile_size),
                sg.Column([
                    [sg.Text('today low:'), sg.Text('000000000000 ###', key='-TX-BCH-2-')],
                    [sg.Text('change: +000000 ### (+00,00%)', key='-TX-BCH-2-CHANGE-')]
                ], size=home_small_tile_size),
                sg.Column([
                    [sg.Text('today open:'), sg.Text('000000000000 ###', key='-TX-BCH-3-')],
                    [sg.Text('change: +000000 ### (+00,00%)', key='-TX-BCH-3-CHANGE-')]
                ], size=home_small_tile_size),
                sg.Column([
                    [sg.Text('volume:'), sg.Text('0000000000000000 ###', key='-TX-BCH-4-')],
                    [sg.Text('volume:'), sg.Text('+0000000000000000000 ###', key='-TX-BCH-4-VOLUME-')]
                ], size=home_small_tile_size),
                sg.Column([
                    [sg.Button('REFRESH', size=(12, 2), key='-B-BCH-REFRESH-')]
                ], size=home_small_tile_size)
            ]])],

            [sg.Text('_' * 140, size=home_tile_center_line_size, justification='center')],

            [sg.Column([[
                sg.Column([
                    [sg.Text('one DAY ago:'), sg.Text('000000000000 ###', key='-TX-BCH-HIST-D-')],
                    [sg.Text('change: +000000 ### (+00,00%)', key='-TX-BCH-HIST-D-CHANGE-')]
                ], size=home_small_tile_size),
                sg.Column([
                    [sg.Text('one HOUR ago:'), sg.Text('000000000000 ###', key='-TX-BCH-HIST-H-')],
                    [sg.Text('change: +000000 ### (+00,00%)', key='-TX-BCH-HIST-H-CHANGE-')]
                ], size=home_small_tile_size),
                sg.Column([
                    [sg.Text('one MINUTE ago:'), sg.Text('000000000000 ###', key='-TX-BCH-HIST-M-')],
                    [sg.Text('change: +000000 ### (+00,00%)', key='-TX-BCH-HIST-M-CHANGE-')]
                ], size=home_small_tile_size),
                sg.Column([
                    [sg.Text('price for DAY:'), sg.Text('000000000000 ###', key='-TX-BCH-PRED-D-')],
                    [sg.Text('change: +000000 ### (+00,00%)', key='-TX-BCH-PRED-D-CHANGE-')]
                ], size=home_small_tile_size),
                sg.Column([
                    [sg.Text('price for HOUR:'), sg.Text('000000000000 ###', key='-TX-BCH-PRED-H-')],
                    [sg.Text('change: +000000 ### (+00,00%)', key='-TX-BCH-PRED-H-CHANGE-')]
                ], size=home_small_tile_size),
                sg.Column([
                    [sg.Text('price for MINUTE:'), sg.Text('000000000000 ###', key='-TX-BCH-PRED-M-')],
                    [sg.Text('change: +000000 ### (+00,00%)', key='-TX-BCH-PRED-M-CHANGE-')]
                ], size=home_small_tile_size),
            ]])]
        ])]
    ])
]

layout_home = [
    layout_home_tile_BTC,
    layout_home_tile_ETH,
    layout_home_tile_LTC,
    layout_home_tile_BCH
]

# -----------------------------------------------------------------------------
center = sg.Column([
    [sg.Column(layout_home, key='-COL-MAIN-'),
     sg.Column(layout_details, visible=False, key='-COL-DETAILS-')]
])

# -----------------------------------------------------------------------------
main_layout = [
    [left_bar, sg.Frame('', [
        [sg.Column([
            [top_bar], [center]
        ])]
    ])]
]

window = sg.Window(title="Crypto$", layout=main_layout, element_padding=(0, 0), margins=(10, 10), resizable=False,
                   finalize=True)


def refresh_data(crypto, real):
    global refresh_time, refresh_delay
    temp_time = datetime.now()
    print(f'Refresh ({temp_time.strftime("%H:%M:%S")}) {crypto} {real}')
    curr_data = get_current_data(crypto, real)
    hist_data = get_hist_data_with_limit_and_type(DATA_TYPE['MINUTES'], 1439, crypto, real)

    refresh_current_data(curr_data, f'-TX-{crypto}-', crypto, real, window)

    for data_type, index in {'D': 0, 'H': -60, 'M': -1}.items():
        main_key = f'-TX-{crypto}-HIST-{data_type}-'
        temp_change_proc = round(100 * hist_data[index] / curr_data[0] - 100, 3)
        temp_change = round(hist_data[index] - curr_data[0], 2)
        window[main_key].update(f'{hist_data[index]} {real}')
        window[f'{main_key}CHANGE-'].update(f'change: {temp_change} {real} {temp_change_proc}%')
        set_tb_change_color(window, f'{main_key}CHANGE-', temp_change)

    if temp_time > refresh_time:
        print(f'Refreshing main prediction')
        refresh_time += timedelta(seconds=refresh_delay)
        pred_day_price = get_predicted_data_from_only_price_model(1,
                                                                  DATA_TYPE['DAYS'],
                                                                  crypto)[0]
        tf.keras.backend.clear_session()
        pred_hour_price = get_predicted_data_from_only_price_model(1,
                                                                   DATA_TYPE['HOURS'],
                                                                   crypto)[0]
        tf.keras.backend.clear_session()
        pred_minute_price = get_predicted_data_from_only_price_model(1,
                                                                     DATA_TYPE['MINUTES'],
                                                                     crypto)[0]
        tf.keras.backend.clear_session()

        exchange_rate = get_exchange_rate('USD', real)
        pred_day_price = round(pred_day_price * exchange_rate, 2)
        pred_hour_price = round(pred_hour_price * exchange_rate, 2)
        pred_minute_price = round(pred_minute_price * exchange_rate, 2)

        for data_type, value in {'D': pred_day_price, 'H': pred_hour_price, 'M': pred_minute_price}.items():
            main_key = f'-TX-{crypto}-PRED-{data_type}-'
            temp_change_proc = round(100 * value / curr_data[0] - 100, 3)
            temp_change = round(value - curr_data[0], 2)
            window[main_key].update(f'{value} {real}')
            window[f'{main_key}CHANGE-'].update(f'change: {temp_change} {real} {temp_change_proc}%')
            set_tb_change_color(window, f'{main_key}CHANGE-', temp_change)
    else:
        print(f'Refresh main prediction at ({refresh_time.strftime("%H:%M:%S")})')

    print("--- ", (datetime.now()-temp_time))


# TODO: Nie dziala
def theme_change(theme):
    print(theme)
    current_them = sg.LOOK_AND_FEEL_TABLE[theme]

    try:
        window_bkg = current_them.get('BACKGROUND')
        window.TKroot.config(background=window_bkg)
    except Exception as e:
        print(e)

    # iterate over all widgets:
    for v, element in window.AllKeysDict.items():
        # for child in window.TKroot.frame.children.values():

        try:
            color = current_them.get(element.Type.upper())
            if color:
                if element.Type == 'button':
                    element.Widget.config(foreground=color[0], background=color[1])
                else:
                    element.Widget.config(background=color)

                element.update()
        except Exception as e:
            print(e)


# ====================== MAIN LOOP ============================================
# TODO: remove comments
# for crypto in CRYPTO_CURRENCY:
#     refresh_data(crypto, default_selected_real_currency)


current_layout = '-MAIN-'
while True:
    event, values = window.read()
    print(event, values)

    if event in (None, 'Exit'):
        break
    else:
        if event in ['-MAIN-', '-DAYS-', '-HOURS-', '-MINUTES-']:
            if event == '-MAIN-':
                window['-MAIN-'].update(disabled=True)
                window[current_layout].update(disabled=False)
                window['-COL-MAIN-'].update(visible=True)
                window['-COL-DETAILS-'].update(visible=False)
                for x in CRYPTO_CURRENCY:
                    refresh_data(x, values['-CB-REAL-CURRENCY-'])
            else:
                window[event].update(disabled=True)
                window[current_layout].update(disabled=False)
                window['-COL-MAIN-'].update(visible=False)
                window['-COL-DETAILS-'].update(visible=True)
            current_layout = event
        # MAIN view
        if window['-COL-MAIN-'].visible:
            if match('-B-.*-REFRESH-', event) is not None:
                refresh_data(event[3:6], values['-CB-REAL-CURRENCY-'])

            elif event == '-CB-REAL-CURRENCY-':
                for crypto in CRYPTO_CURRENCY:
                    refresh_data(crypto, values['-CB-REAL-CURRENCY-'])

            elif event == '-CB-THEME-':
                if values['-CB-THEME-'] == 'MAROCHA':
                    theme_change('DarkBlue8')
                elif values['-CB-THEME-'] == 'SIWY':
                    theme_change('DarkTeal4')
        # DETAILS view
        else:
            handle_event(event, values, window)

window.close()

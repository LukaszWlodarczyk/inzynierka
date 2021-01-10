from re import match

import PySimpleGUI as sg

from GUI.gui_service import *
# from GUI.window_main import window
from my_requests import CRYPTO_CURRENCY

# -----------------------------------------------------------------------------
sg.theme(theme)

current_data = []
hist_data = []
# pred_data = [30000, 31000, 32000, 29000, 30000, 31000]
pred_data = [40000, 41000, 42000, 49000, 40000, 41000]

current_last_data_limit = 20
current_next_data_limit = 5
current_tolerance = 0.5

current_data_type = ''

current_canvas_fig = None

cb_crypto_value = sg.Combo(
    list(CRYPTO_CURRENCY.values()),
    default_selected_crypto,
    enable_events=True,
    size=(6, 1),
    key='-CB-CRYPTO-CURRENCY-')

# -----------------------------------------------------------------------------
layout_details_size = (700, 300)
layout_details_top = sg.Column([
    [sg.Frame('Options', [
        [sg.Column([
            [sg.Text('Last ========:', key='-TX-LAST-')],
            [sg.Input(f'{current_last_data_limit}', enable_events=True, key='-INPUT-LAST-')],
            [sg.Text('Next ========:', key='-TX-NEXT-')],
            [sg.Input(f'{current_next_data_limit}', enable_events=True, key='-INPUT-NEXT-')],
            [sg.Text('Cryptocurrency:')],
            [cb_crypto_value],
            [sg.Text('Tolerance (%):')],
            [sg.Input(f'{current_tolerance}', enable_events=True, key='-INPUT-TOLERANCE-')],
            [sg.Button('SHOW DETAILS', size=(15, 1), key='-B-SHOW-DETAILS-')]
        ], pad=(5, 5), size=(150, 200))]
        # ], pad=(5, 5), size=(int(layout_details_size[0]/5), layout_details_size[1]))]
    ]),
     sg.Frame('Chart', [
         [sg.Column([
             [sg.Canvas(key='-CANVAS-', size=(50, 50))]
         ])],
         [sg.Checkbox('CLOSE price', enable_events=True, key='-CHB-CLOSE-', default=True),
          sg.Checkbox('OPEN price', enable_events=True, key='-CHB-OPEN-'),
          sg.Checkbox('LOWEST price', enable_events=True, key='-CHB-LOWEST-'),
          sg.Checkbox('HIGHEST price', enable_events=True, key='-CHB-HIGHEST-')]
         # ], size=(int(layout_details_size[0]/5*4), layout_details_size[1]))]
     ])]
])

# -----------------------------------------------------------------------------
bottom_small_tile_size = (220, 50)
bottom_small_tile_size2 = (220, 75)

layout_details_bottom_current = [
    sg.Frame('CURRENT', [
        [sg.Column([[
            sg.Column([
                [sg.Text('price:'), sg.Text('000000000000 ###', key='-TX-CURRENT-0-')],
            ], size=bottom_small_tile_size),
            sg.Column([
                [sg.Text('high:'), sg.Text('000000000000 ###', key='-TX-CURRENT-1-')],
                [sg.Text('change: +000000 ### (+00,00%)', key='-TX-CURRENT-1-CHANGE-')]
            ], size=bottom_small_tile_size),
            sg.Column([
                [sg.Text('low:'), sg.Text('000000000000 ###', key='-TX-CURRENT-2-')],
                [sg.Text('change: +000000 ### (+00,00%)', key='-TX-CURRENT-2-CHANGE-')]
            ], size=bottom_small_tile_size),
            sg.Column([
                [sg.Text('open:'), sg.Text('000000000000 ###', key='-TX-CURRENT-3-')],
                [sg.Text('change: +000000 ### (+00,00%)', key='-TX-CURRENT-3-CHANGE-')]
            ], size=bottom_small_tile_size),
            sg.Column([
                [sg.Text('volume:'), sg.Text('0000000000000000 ###', key='-TX-CURRENT-4-')],
                [sg.Text('volume:'), sg.Text('+0000000000000000000 ###', key='-TX-CURRENT-4-VOLUME-')]
            ], size=bottom_small_tile_size),
            sg.Column([
                [sg.Button('REFRESH', size=(12, 2), key='-B-DETAILS-REFRESH-')]
            ], size=bottom_small_tile_size)
        ]], pad=(5, 5))]
    ])
]

layout_details_bottom_last = [
    sg.Frame('LAST', [
        [sg.Column([[
            sg.Column([
                [sg.Text('high:'), sg.Text('000000000000 ###', key='-TX-LAST-0-')],
                [sg.Text('change: +000000 ### (+00,00%)', key='-TX-LAST-0-CHANGE-')]
            ], size=bottom_small_tile_size),
            sg.Column([
                [sg.Text('low:'), sg.Text('000000000000 ###', key='-TX-LAST-1-')],
                [sg.Text('change: +000000 ### (+00,00%)', key='-TX-LAST-1-CHANGE-')]
            ], size=bottom_small_tile_size),
            sg.Column([
                [sg.Text('open:'), sg.Text('000000000000 ###', key='-TX-LAST-2-')],
                [sg.Text('change: +000000 ### (+00,00%)', key='-TX-LAST-2-CHANGE-')]
            ], size=bottom_small_tile_size),
            sg.Column([
                [sg.Text('close:'), sg.Text('000000000000 ###', key='-TX-LAST-5-')],
                [sg.Text('change: +000000 ### (+00,00%)', key='-TX-LAST-5-CHANGE-')]
            ], size=bottom_small_tile_size),
            sg.Column([
                [sg.Text('volumefrom:'), sg.Text('0000000000000000 ###', key='-TX-LAST-3-')],
            ], size=bottom_small_tile_size),
            sg.Column([
                [sg.Text('volumeto:'), sg.Text('+0000000000000000000 ###', key='-TX-LAST-4-')]
            ], size=bottom_small_tile_size),
        ]], pad=(5, 5))]
    ], key='-F-LAST-')
]

layout_details_bottom_next = [
    sg.Frame('NEXT', [
        [sg.Column([[
            sg.Column([
                [sg.Text('date or time:'), sg.Text('DD:MM:YYYY HH:MM', key='-TX-NEXT-0-TIME-')],
                [sg.Text('price:'), sg.Text('000000000000 ###', key='-TX-NEXT-0-')],
                [sg.Text('change: +000000 ### (+00,00%)', key='-TX-NEXT-0-CHANGE-')]
            ], size=bottom_small_tile_size2),
            sg.Column([
                [sg.Text('date or time:'), sg.Text('DD:MM:YYYY HH:MM', key='-TX-NEXT-1-TIME-')],
                [sg.Text('price:'), sg.Text('000000000000 ###', key='-TX-NEXT-1-')],
                [sg.Text('change: +000000 ### (+00,00%)', key='-TX-NEXT-1-CHANGE-')]
            ], size=bottom_small_tile_size2),
            sg.Column([
                [sg.Text('date or time:'), sg.Text('DD:MM:YYYY HH:MM', key='-TX-NEXT-2-TIME-')],
                [sg.Text('price:'), sg.Text('000000000000 ###', key='-TX-NEXT-2-')],
                [sg.Text('change: +000000 ### (+00,00%)', key='-TX-NEXT-2-CHANGE-')]
            ], size=bottom_small_tile_size2),
            sg.Column([
                [sg.Text('date or time:'), sg.Text('DD:MM:YYYY HH:MM', key='-TX-NEXT-3-TIME-')],
                [sg.Text('price:'), sg.Text('000000000000 ###', key='-TX-NEXT-3-')],
                [sg.Text('change: +000000 ### (+00,00%)', key='-TX-NEXT-3-CHANGE-')]
            ], size=bottom_small_tile_size2),
            sg.Column([
                [sg.Text('date or time:'), sg.Text('DD:MM:YYYY HH:MM', key='-TX-NEXT-4-TIME-')],
                [sg.Text('price:'), sg.Text('000000000000 ###', key='-TX-NEXT-4-')],
                [sg.Text('change: +000000 ### (+00,00%)', key='-TX-NEXT-4-CHANGE-')]
            ], size=bottom_small_tile_size2),
            sg.Column([
                [sg.Text('date or time:'), sg.Text('DD:MM:YYYY HH:MM', key='-TX-NEXT-5-TIME-')],
                [sg.Text('price:'), sg.Text('000000000000 ###', key='-TX-NEXT-5-')],
                [sg.Text('change: +000000 ### (+00,00%)', key='-TX-NEXT-5-CHANGE-')]
            ], size=bottom_small_tile_size2),
        ]], pad=(5, 5))]
    ], key='-F-NEXT-')
]

layout_details_bottom = sg.Column(
    [layout_details_bottom_current,
     layout_details_bottom_last,
     layout_details_bottom_next]
)

# -----------------------------------------------------------------------------
layout_details = [
    [layout_details_top],
    [layout_details_bottom]
]


# -----------------------------------------------------------------------------
def update_chart(window, crypto, real):
    print('Refresh chart')
    global hist_data, pred_data, current_data_type
    data_high = []
    data_low = []
    data_open = []
    data_close = []

    hist_data = get_last_data(DATA_TYPE[current_data_type], current_last_data_limit, crypto, real)

    for i in range(len(hist_data) - 1):
        data_high.append(hist_data[i][0])
        data_low.append(hist_data[i][1])
        data_open.append(hist_data[i][2])
        data_close.append(hist_data[i][5])

    series = [x for x in range(len(data_close) + len(pred_data))]

    fig = plt.Figure(figsize=(12, 4), dpi=100)
    plot = fig.add_subplot(111)

    if window['-CHB-CLOSE-'].get():
        plot.plot(series[:len(data_close)], data_close, color='green', label=f'Close')
    if window['-CHB-OPEN-'].get():
        plot.plot(series[:len(data_close)], data_open, color='yellow', label=f'Open')
    if window['-CHB-LOWEST-'].get():
        plot.plot(series[:len(data_close)], data_low, color='blue', label=f'Lowest')
    if window['-CHB-HIGHEST-'].get():
        plot.plot(series[:len(data_close)], data_high, color='red', label=f'Highest')

    connection_plot = [data_close[-1], pred_data[0]]
    plot.plot(series[-len(pred_data) - 1:-len(pred_data)+1], connection_plot, color='lightgreen')
    plot.plot(series[-len(pred_data):], pred_data, color='lightgreen', label=f'Close (predicted)')

    plot.set_title(f'{crypto} price')
    plot.set_xlabel('Timestamp')
    plot.set_ylabel(f'Price [{real}]')
    plot.legend()

    canvas = window['-CANVAS-'].TKCanvas

    global current_canvas_fig
    if current_canvas_fig is not None:
        current_canvas_fig.get_tk_widget().forget()
        plt.close('all')
    return draw_figure(canvas, fig, loc=(0, 0))


# -----------------------------------------------------------------------------
def refresh_details_data(crypto, real, window):
    print(f'Refresh details {crypto} {real}')
    global current_data, hist_data
    current_data = get_current_data(crypto, real)
    hist_data = get_last_data(DATA_TYPE[current_data_type], current_last_data_limit, crypto, real)

    window['-TX-LAST-'].update(f'Last {current_data_type} limit')
    window['-TX-NEXT-'].update(f'Next {current_data_type} limit')
    window['-F-LAST-'].update(f'LAST {current_data_type[:-1]}')
    window['-F-NEXT-'].update(f'NEXT {current_data_type}')

    refresh_current_data(current_data, f'-TX-CURRENT-', crypto, real, window)

    for i in range(6):
        if i in [0, 1, 2, 5]:
            temp_change_proc = round(100 * hist_data[-2][i] / current_data[0] - 100, 3)
            temp_change = round(hist_data[-2][i] - current_data[0], 2)
            window[f'-TX-LAST-{i}-CHANGE-'].update(f'change: {temp_change} {real} {temp_change_proc}%')
            set_tb_change_color(window, f'-TX-LAST-{i}-CHANGE-', temp_change)

        if i != 3:
            window[f'-TX-LAST-{i}-'].update(f'{hist_data[-2][i]} {real}')
        else:
            window[f'-TX-LAST-{i}-'].update(f'{hist_data[-2][i]} {crypto}')

    global current_canvas_fig
    current_canvas_fig = update_chart(window, crypto, real)


# -----------------------------------------------------------------------------
def handle_event(event, values, window):
    print('Details event handle')
    global current_data_type, current_canvas_fig
    if event in ['-DAYS-', '-HOURS-', '-MINUTES-']:

        current_data_type = event[1:-1]
        refresh_details_data(values['-CB-CRYPTO-CURRENCY-'], values['-CB-REAL-CURRENCY-'], window)

        pass
    elif event in ['-CB-CRYPTO-CURRENCY-', '-CB-REAL-CURRENCY-']:
        refresh_details_data(values['-CB-CRYPTO-CURRENCY-'], values['-CB-REAL-CURRENCY-'], window)

    elif event == '-B-DETAILS-REFRESH-':
        refresh_details_data(values['-CB-CRYPTO-CURRENCY-'], values['-CB-REAL-CURRENCY-'], window)

    elif event == '-B-SHOW-DETAILS-':
        global current_last_data_limit, current_next_data_limit, current_tolerance
        current_last_data_limit = values['-INPUT-LAST-']
        current_next_data_limit = values['-INPUT-NEXT-']
        current_tolerance = values['-INPUT-TOLERANCE-']

        current_canvas_fig = update_chart(window, values['-CB-CRYPTO-CURRENCY-'], values['-CB-REAL-CURRENCY-'])

    elif match('-CHB-.*-', event) is not None:
        current_canvas_fig = update_chart(window, values['-CB-CRYPTO-CURRENCY-'], values['-CB-REAL-CURRENCY-'])

    elif event == '--INPUT-LAST-':
        if len(values['-INPUT-LAST-']) and values['-INPUT-LAST-'][-1] not in '0123456789':
            window['-INPUT-LAST-'].update(values['-INPUT-LAST-'][:-1])

    elif event == '-INPUT-NEXT-':
        if len(values['-INPUT-NEXT-']) and values['-INPUT-NEXT-'][-1] not in '0123456789':
            window['-INPUT-NEXT-'].update(values['-INPUT-NEXT-'][:-1])

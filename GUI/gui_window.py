import PySimpleGUI as sg
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
import matplotlib

from my_requests import get_current_price, get_yesterday_price, CRYPTO_CURRENCY, REAL_CURRENCY
# from GUI.gui_service import dupa
from GUI.menu import menubar, handle_menu_click, buttons_menu_layout

matplotlib.use('TkAgg')

default_selected_crypto = CRYPTO_CURRENCY['BTC']
default_selected_real_currency = REAL_CURRENCY['PLN']


cb_crypto_value = sg.Combo(
    list(CRYPTO_CURRENCY.values()),
    default_selected_crypto,
    enable_events=True,
    key='_CB_CRYPTO-CURRENCY_')

cb_currency = sg.Combo(
    list(REAL_CURRENCY.values()),
    default_selected_real_currency,
    enable_events=True,
    key='_CB_REAL-CURRENCY_')

text_current_price = sg.Text(f'Current price: '
                             f'{get_current_price(default_selected_crypto, default_selected_real_currency)} '
                             f'{default_selected_real_currency}', enable_events=True)
text_yesterday_price = sg.Text(f'Yesterday price: '
                               f'{get_yesterday_price(default_selected_crypto, default_selected_real_currency)} '
                               f'{default_selected_real_currency}', enable_events=True)


def change(selected_crypto, selected_real_currency):
    return 100*get_current_price(selected_crypto, selected_real_currency)/get_yesterday_price(selected_crypto, selected_real_currency)-100


text_change = sg.Text(f'Change: {change(default_selected_crypto, default_selected_real_currency)} %')

main_layout = [
    [menubar],
    [buttons_menu_layout],
    [sg.Text('Cryptocurrency: '), cb_crypto_value],
    [sg.Text('Real currency: '), cb_currency],
    [text_current_price],
    [text_yesterday_price],
    [text_change],
    # [sg.Canvas(key='_CANVAS_')]
]


def draw_figure(canvas, figure, loc=(0,0)):
    figure_canvas_agg = FigureCanvasTkAgg(figure, master=canvas)
    figure_canvas_agg.draw()
    figure_canvas_agg.get_tk_widget().pack(side='top', fill='both', expand=1)
    return figure_canvas_agg


# fig = plt.Figure(figsize=(8, 7), dpi=100)
# plot = fig.add_subplot(111)
# plot.plot(y_test, color='blue', label='Predicted price')
# plot.plot(y_test, color="red", label="Real price")
# plot.set_title("Bitcoin price prediction")
# plot.set_xlabel('Timestamp')
# plot.set_ylabel('Price [PLN]')
# plot.legend()

sg.ChangeLookAndFeel('Reddit')
sg.theme_background_color('white')
sg.SetOptions(element_padding=(0, 8))

window = sg.Window(title="Crypto$", layout=main_layout, margins=(50,50), resizable=True, finalize=True)
# fig_canvas_agg = draw_figure(window['_CANVAS_'].TKCanvas, fig, loc=(0, 0))


def real_currency_change(values):
    new_selected_crypto = values['_CB_CRYPTO-CURRENCY_']
    new_selected_real_currency = values['_CB_REAL-CURRENCY_']

    text_current_price.update(f'Current price: '
                              f'{get_current_price(new_selected_crypto, new_selected_real_currency)} '
                              f'{new_selected_real_currency}')
    text_yesterday_price.update(f'Yesterday price: '
                                f'{get_yesterday_price(new_selected_crypto, new_selected_real_currency)} '
                                f'{new_selected_real_currency}')
    text_change.update(f'Change: {change(new_selected_crypto, new_selected_real_currency)} %')


def crypto_currency_change(values):
    pass


def main_loop():
    while True:
        event, values = window.Read()
        # print(f'event: {event}')

        if event == sg.WIN_CLOSED:
            break
        elif event == '_CB_REAL-CURRENCY_':
            real_currency_change(values)
        elif event == '_CB_CRYPTO-CURRENCY_':
            crypto_currency_change(values)
        else:
            pass

    window.close()


if __name__ == "__main__":
    # print(list(CRYPTO_CURRENCY.values()))
    main_loop()

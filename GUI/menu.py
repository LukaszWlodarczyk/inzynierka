import PySimpleGUI as sg


# ------ Menu Definition ------ #
menu_def = [['&Predykcje', ['&Długoterminowa', '&Miesięczna', '&Tygodniowa', 'Mi&nutowa']],
            ['&Help', '&About...']]

menubar = sg.Menu(menu_def, tearoff=False)


def handle_menu_click(event):
    if event == 'About...':
        sg.popup('About this program', 'Version 1.0',
                 'PySimpleGUI Version', sg.version, grab_anywhere=True)
    elif event == 'Długoterminowa':
        print('Długoterminowa')
    elif event == 'Miesięczna':
        print('Miesięczna')
    elif event == 'Tygodniowa':
        print('Tygodniowa')
    elif event == 'Minutowa':
        print('Minutowa')

import PySimpleGUI as sg
import db_req
import pandas as pd
from datetime import datetime

list = db_req.getItems('')
date = db_req.getDate()

layout1 = [ [sg.Text('Item Name', background_color='Black', font = ('Yu Gothic UI Semilight', 15) ), sg.Input('',k='-FILTER-', focus=True, font=('Yu Gothic UI Semilight', 15))], 
            [sg.Button('  Search  ', font = ('Yu Gothic UI Semilight', 12)), sg.Text(date, k = '-DATE-', background_color='Black', font = ('Yu Gothic UI Semilight', 15) )],
            [sg.Table(headings = ['           ITEM NAME           ', '   AMOUNT   '], values = list, k='-TABLE-',num_rows=18, font = ('Yu Gothic UI Semilight', 12), hide_vertical_scroll=True, auto_size_columns=True, justification='left', enable_events=True, row_height=30, background_color='Black')],
            [sg.Text('Number', background_color='Black', font = ('Yu Gothic UI Semilight', 15) ), sg.Input('',k='-NUM-', focus=True, font=('Yu Gothic UI Semilight', 15),)],
            [sg.Button('  Inc/Dec  ', font = ('Yu Gothic UI Semilight', 12)), sg.Button('  Set To  ', font = ('Yu Gothic UI Semilight', 12))]
         ]

tabgrp = [[sg.TabGroup([[sg.Tab('                         BANK                          ', layout1, title_color='Red', k = 'tab1', border_width =10, background_color='Black')]],
                       title_color='Black', tab_background_color='Gray',selected_title_color='Red',
                       selected_background_color='Gray', border_width=0, size=(770, 760), background_color='Black', font = ('Yu Gothic UI Semilight', 12))]]

window = sg.Window("DHIO BANK", tabgrp, size = (900, 900), background_color='Black')

while True:
    event,values = window.read()
    if event == sg.WIN_CLOSED:
        break
    if event == '  Search  ':
        tmp = db_req.getItems(values['-FILTER-'])
        list = tmp
        window.Element('-TABLE-').update(tmp)
    elif event == '  Inc/Dec  ' and values['-NUM-'] != '' and len(values['-TABLE-']) > 0:
        index = values['-TABLE-'][0]
        db_req.addToBank(list[index][0], values['-NUM-'])
        window.Element('-TABLE-').update(db_req.getItems(values['-FILTER-']))
        db_req.changeDate()
        window.Element('-DATE-').update(db_req.getDate())
    elif event == '  Set To  ' and values['-NUM-'] != ''and len(values['-TABLE-']) > 0:
        index = values['-TABLE-'][0]
        db_req.updateAmount(list[index][0], values['-NUM-'])
        window.Element('-TABLE-').update(db_req.getItems(values['-FILTER-']))
        db_req.changeDate()
        window.Element('-DATE-').update(db_req.getDate())
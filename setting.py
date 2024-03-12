from tkinter import *
from tkinter.ttk import Combobox
from tkinter import messagebox
import json
import os

def translating_values_format():
    if (combo.get() == "Основной PDF" or combo.get() == "Показатели PDF" or combo.get() == "Тревоги PDF"): form = "pdf"
    elif (combo.get() == "Основной HTML" or combo.get() == "Показатели HTML" or combo.get() == "Тревоги HTML"): form = "html"
    elif (combo.get() == "Показатели CSV" or combo.get() == "Тревоги CSV"): form = "csv"
    elif (combo.get() == "Журнал ТиВ PDF"): form = "th1"
    return form

def translating_values_kind():
    if (combo.get() == "Основной PDF" or combo.get() == "Основной HTML"): kind = "main"
    elif (combo.get() == "Показатели CSV" or combo.get() == "Показатели HTML" or combo.get() == "Показатели PDF" or combo.get() == "Журнал ТиВ PDF"): kind = "alert"
    elif (combo.get() == "Тревоги CSV" or combo.get() == "Тревоги HTML" or combo.get() == "Тревоги PDF"): kind = "values"
    return kind

def translating_values_group():
    if (combo_dop.get() == "Без усреднения"): grou = "no"
    elif (combo_dop.get() == "5 минут"): grou = "5m"
    elif (combo_dop.get() == "1 час"): grou = "1h"
    elif (combo_dop.get() == "3 часа"): grou = "3h"
    elif (combo_dop.get() == "1 день"): grou = "1d"
    elif (combo_dop.get().find(':00') != -1): grou = combo_dop.get()[0]
    return grou

def translating_values_types():
    if (combo_filter.get() == "Только температура"): typ = "temp"
    elif (combo_filter.get() == "Температура и влажность"): typ = "tempСhum"
    elif (combo_filter.get() == "Только влажность"): typ = "hum"
    elif (combo_filter.get() == "Критические тревоги"): typ = "10"
    elif (combo_filter.get() == "Все тревоги"): typ = "20"
    elif (combo_filter.get() == "Тревоги и служебные"): typ = "30"
    return typ

def translating_values_time():
    if (combo_time.get() == "Прошлый месяц"): tim = "month"
    elif (combo_time.get() == "Прошлая неделя"): tim = "week"
    elif (combo_time.get() == "Прошлый день"): tim = "day"
    return tim

# Сохранение введенных данных
def clicked():
    if ((txt_email.get().find('@') != -1) and len(txt_email.get()) > 0 and (txt_email.get().find('.') != -1)):
        if (len(txt_pass.get()) > 0):
            if (len(txt_devset.get()) > 0):
                form = translating_values_format()
                kind = translating_values_kind()
                grou = translating_values_group()
                typ = translating_values_types()
                tim = translating_values_time()
                way = 0
                wsl = 0
                if (txt_way.get() != ""):
                    way = txt_way.get()
                if (txt_WSlocal.get() != ""):
                    wsl = txt_WSlocal.get()
                logpass = {
                    "Email": txt_email.get(),
                    "Pass": txt_pass.get(),
                    "Way": way,
                    "Wsl": wsl
                }
                if (combo_devset.get() == "DevID"):
                    if (combo.get() == "Тревоги CSV"):
                        res = {
                            "Kind": kind,
                            "Format": form,
                            "TimeZone": "device",
                            "Severity": typ,
                            "DevID": txt_devset.get(),
                            "T1": tim,
                            "T2": ""
                        }
                    elif (combo.get() == "Тревоги HTML" or combo.get() == "Тревоги PDF"):
                        res = {
                            "Kind": kind,
                            "Format": form,
                            "TimeZone": "device",
                            "Comments": "no",
                            "Severity": typ,
                            "DevID": txt_devset.get(),
                            "T1": tim,
                            "T2": ""
                        }
                    elif (combo.get() == "Журнал ТиВ PDF"):
                        res = {
                            "Kind": kind,
                            "Format": form,
                            "TimeZone": "device",
                            "Group": "no",
                            "Ease": "no",
                            "Hours": grou,
                            "Filter": "custom_types",
                            "DevID": txt_devset.get(),
                            "Types": typ,
                            "T1": tim,
                            "T2": ""
                        }
                    else:
                        res = {
                            "Kind": kind,
                            "Format": form,
                            "TimeZone": "device",
                            "Group": grou,
                            "Ease": "no",
                            "Filter": "custom_types",
                            "DevID": txt_devset.get(),
                            "Types": typ,
                            "T1": tim,
                            "T2": ""
                        }
                elif (combo_devset.get() == "SetID"):
                    if (combo.get() == "Журнал ТиВ PDF"):
                        res = {
                            "Kind": kind,
                            "Format": form,
                            "TimeZone": "device",
                            "Group": "no",
                            "Ease": "no",
                            "Hours": grou,
                            "SetID": txt_email.get(),
                            "T1": tim,
                            "T2": ""
                        }
                    else:
                        res = {
                            "Kind": kind,
                            "Format": form,
                            "TimeZone": "device",
                            "Group": grou,
                            "Ease": "no",
                            "SetID": txt_email.get(),
                            "T1": tim,
                            "T2": ""
                        }
                with open('settings.pkl', 'w') as f:
                    json.dump(res, f)
                with open('authorization.pkl', 'w') as f:
                    json.dump(logpass, f)
                messagebox.showinfo('', 'Настройки успешно сохранены!')
            else: messagebox.showwarning('', 'Не введен DevID/SetID!')
        else: messagebox.showwarning('', 'Не введен пароль!')
    else: messagebox.showwarning('', 'Данные Email заполнены не верно!')

# Смена выпадающих списком в зависимости от выбора
def on_combobox_change(event):
    selected_item_devset = combo_devset.get()
    selected_item = combo.get()

    if (combo_WSlocal.get() == "Локальный"):
        lbl_WSlocal.grid(column=0, row=4, sticky = "w")
        txt_WSlocal.grid(column=1, row=4)
    elif (combo_WSlocal.get() == "Облачный"):
        lbl_WSlocal.grid_remove()
        txt_WSlocal.grid_remove()

    if (selected_item_devset == "DevID"):
        combo['values'] = (
        "Основной PDF", "Основной HTML", "Показатели CSV", "Показатели HTML", "Показатели PDF", "Журнал ТиВ PDF",
        "Тревоги CSV", "Тревоги HTML", "Тревоги PDF")
        lbl_combo_filter.grid(column=0, row=7, sticky='w')
        combo_filter.grid(column=1, row=7)

    elif (selected_item_devset == "SetID"):
        combo['values'] = (
        "Основной PDF", "Основной HTML", "Показатели CSV", "Показатели HTML", "Показатели PDF", "Журнал ТиВ PDF")
        lbl_combo_filter.grid_remove()
        combo_filter.grid_remove()

    if ((selected_item == 'Основной PDF') or (selected_item == 'Основной HTML')):
        combo_filter['values'] = ("Только температура", "Температура и влажность", "Только влажность")
        lbl_combo_dop = Label(window, text="Выберите усреднение:")
        lbl_combo_dop.grid(column=0, row=8, sticky='w')
        combo_dop.grid(column=1, row=8)
        combo_dop['values'] = ("Без усреднения", "5 минут", "1 час", "3 часа", "1 день")
    elif ((selected_item == 'Показатели CSV') or (selected_item == 'Показатели PDF') or (
        selected_item == 'Показатели HTML')):
        combo_filter['values'] = ("Температура и влажность", "Только температура", "Только влажность")
        lbl_combo_dop = Label(window, text="Выберите усреднение:")
        lbl_combo_dop.grid(column=0, row=8, sticky='w')
        combo_dop.grid(column=1, row=8)
        combo_dop['values'] = ("Без усреднения", "5 минут", "1 час", "3 часа", "1 день")
    elif ((selected_item == 'Журнал ТиВ PDF')):
        combo_filter['values'] = ("Только температура", "Температура и влажность")
        lbl_combo_dop = Label(window, text="Выбор времени:             ")
        lbl_combo_dop.grid(column=0, row=8, sticky='w')
        combo_dop.grid(column=1, row=8)
        combo_dop['values'] = ("0:00", "1:00", "2:00", "3:00", "4:00", "5:00", "6:00", "7:00", "8:00", "9:00",
                               "10:00", "11:00", "12:00", "13:00", "14:00", "15:00", "16:00", "17:00", "18:00",
                               "19:00", "20:00", "21:00", "22:00", "23:00")
    elif ((selected_item == 'Тревоги CSV') or (selected_item == 'Тревоги HTML') or (
            selected_item == 'Тревоги PDF')):
        combo_filter['values'] = ("Критические тревоги", "Все тревоги", "Тревоги и служебные")


window = Tk() # Открываем окно
window.geometry('500x300') # Размер окна
window.resizable(width=FALSE, height=FALSE) # Блокировка размера окна
log = 1
try:
    with open('authorization.pkl', 'r') as f:
        logpass = json.load(f)
    with open('settings.pkl', 'r') as f:
        res = json.load(f)
except: log = 0
window.title("Настройка отчета Unimon!")
lbl_email = Label(window, text="Введите E-mail:")
lbl_email.grid(column=0, row=0, sticky='w')
txt_email = Entry(window,width=40)
txt_email.grid(column=1, row=0)
if (log != 0): txt_email.insert(0, logpass["Email"])
lbl_pass = Label(window, text="Введите Пароль:")
lbl_pass.grid(column=0, row=2, sticky='w')
txt_pass = Entry(window,width=40)
txt_pass.grid(column=1, row=2)
if (log != 0): txt_pass.insert(0, logpass["Pass"])
lbl_combo_WSlocal = Label(window, text="Выберите сервер:")
lbl_combo_WSlocal.grid(column=0, row=3, sticky='w')
combo_WSlocal = Combobox(window, width=37)
combo_WSlocal.grid(column=1, row=3)
combo_WSlocal['values'] = ("Облачный", "Локальный")
lbl_WSlocal = Label(window, text="Введите URL:")
txt_WSlocal = Entry(window, width=40)
combo_WSlocal['state'] = 'readonly'
combo_WSlocal.bind("<<ComboboxSelected>>", on_combobox_change)
lbl_combo_devset = Label(window, text="Выберите DevID|SetID:")
lbl_combo_devset.grid(column=0, row=5, sticky='w')
combo_devset = Combobox(window, width=37)
combo_devset.grid(column=1, row=5)
combo_devset['values'] = ("DevID", "SetID")
combo_devset['state'] = 'readonly'
combo_devset.bind("<<ComboboxSelected>>", on_combobox_change)
lbl_devset = Label(window, text=" = ")
lbl_devset.grid(column=2, row=5)
txt_devset = Entry(window,width=6)
txt_devset.grid(column=3, row=5)
if (log != 0): txt_devset.insert(0, (res["DevID"] or res["SetID"]))
lbl_combo = Label(window, text="Выберите формат:")
lbl_combo.grid(column=0, row=6, sticky='w')
combo = Combobox(window, width=37)
combo.grid(column=1, row=6)
combo['state'] = 'readonly'
combo.bind("<<ComboboxSelected>>", on_combobox_change)
lbl_combo_filter = Label(window, text="Выберите тип отчета:")
combo_filter = Combobox(window, width=37)
combo_filter['state'] = 'readonly'
lbl_combo_dop = Label(window, text="Выберите усреднение:")
combo_dop = Combobox(window, width=37)
combo_dop['state'] = 'readonly'
lbl_combo_time = Label(window, text="Выберите период:")
lbl_combo_time.grid(column=0, row=9, sticky='w')
combo_time = Combobox(window, width=37)
combo_time['values'] = ("Прошлый месяц", "Прошлая неделя", "Прошлый день")
combo_time.grid(column=1, row=9)
combo_time['state'] = 'readonly'
lbl_way = Label(window, text='*Путь для скаченного файла:  ')
lbl_way.grid(column=0, row=11, sticky="w")
txt_way = Entry(window,width=40)
txt_way.grid(column=1, row=11)
if (log != 0):
    way = os.path.normpath(logpass["Way"])
    txt_way.insert(0, logpass["Way"])
lbl_btn1 = Label(window, text="")
lbl_btn1.grid(column=0, row=13)
btn = Button(window, text="Сохранить!", command=clicked)
btn.grid(column=1, row=15)
lbl_way_p = Label(window, text='*Пример - C:\\Users\\****\\Папка для отчета')
lbl_way_p.place(x = 0, y = 270)
window.mainloop()

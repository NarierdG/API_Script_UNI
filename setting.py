import tkinter
from time import strftime
from tkinter import *
from tkinter.ttk import Combobox
from tkinter import messagebox, filedialog
from datetime import datetime
from tkcalendar import Calendar
import json
import os

def select_directory(entry_widget):
    directory = filedialog.askdirectory()
    if directory:
        entry_widget.delete(0, END)
        entry_widget.insert(0, directory)
def translating_values_format():
    if (combo.get() == "Основной PDF" or combo.get() == "Показатели PDF" or combo.get() == "Тревоги PDF"): form = "pdf"
    elif (combo.get() == "Основной HTML" or combo.get() == "Показатели HTML" or combo.get() == "Тревоги HTML"): form = "html"
    elif (combo.get() == "Показатели CSV" or combo.get() == "Тревоги CSV"): form = "csv"
    elif (combo.get() == "Журнал ТиВ PDF"): form = "th1"
    return form

def translating_values_kind():
    if (combo.get() == "Основной PDF" or combo.get() == "Основной HTML"): kind = "main"
    elif (combo.get() == "Показатели CSV" or combo.get() == "Показатели HTML" or combo.get() == "Показатели PDF" or combo.get() == "Журнал ТиВ PDF"): kind = "values"
    elif (combo.get() == "Тревоги CSV" or combo.get() == "Тревоги HTML" or combo.get() == "Тревоги PDF"): kind = "alerts"
    return kind

def translating_values_url():
    if (combo.get() == "Основной PDF" or combo.get() == "Основной HTML"): url = "main"
    elif (combo.get() == "Показатели CSV" or combo.get() == "Показатели HTML" or combo.get() == "Показатели PDF" or combo.get() == "Журнал ТиВ PDF"): url = "data"
    elif (combo.get() == "Тревоги CSV" or combo.get() == "Тревоги HTML" or combo.get() == "Тревоги PDF"): url = "alerts"
    return url

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
    elif (combo_filter.get() == "Температура и влажность"): typ = "temp,hum"
    elif (combo_filter.get() == "Только влажность"): typ = "hum"
    elif (combo_filter.get() == "Критические тревоги"): typ = "10"
    elif (combo_filter.get() == "Все тревоги"): typ = "20"
    elif (combo_filter.get() == "Тревоги и служебные"): typ = "30"
    return typ

def translating_values_time():
    if (combo_time.get() == "Прошлый месяц"): tim = "month"
    elif (combo_time.get() == "Прошлая неделя"): tim = "week"
    elif (combo_time.get() == "Прошлый день"): tim = "day"
    elif (combo_time.get() == "Выбор даты начала периода"):
        tim = time_p
    return tim


# Сохранение введенных данных
def clicked():
    if ((txt_email.get().find('@') != -1) and len(txt_email.get()) > 0 and (txt_email.get().find('.') != -1)):
        if (len(txt_pass.get()) > 0):
            if (len(txt_devset.get()) > 0):
                tim = translating_values_time()
                if (tim != ""):
                    form = translating_values_format()
                    kind = translating_values_kind()
                    grou = translating_values_group()
                    url = translating_values_url()
                    if (combo_devset.get() == "DevID"): typ = translating_values_types()
                    way = 0
                    wsl = 0
                    if (txt_way.get() != ""):
                        way = txt_way.get()
                    if (txt_WSlocal.get() != "" and combo_WSlocal.get() == "Локальный"):
                        wsl = txt_WSlocal.get()
                    logpass = {
                        "Email": txt_email.get(),
                        "Pass": txt_pass.get(),
                        "Way": way,
                        "Wsl": wsl,
                        "Url": url
                    }
                    res_load = {
                        "Combo": combo.get(),
                        "Filter": combo_filter.get(),
                        "Dop": combo_dop.get(),
                        "Time": combo_time.get()
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
                                "SetID": txt_devset.get(),
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
                                "SetID": txt_devset.get(),
                                "T1": tim,
                                "T2": ""
                            }
                    with open('settings.pkl', 'w') as f:
                        json.dump(res, f)
                    with open('authorization.pkl', 'w') as f:
                        json.dump(logpass, f)
                    with open('additional_load.pkl', 'w') as f:
                        json.dump(res_load, f)
                    messagebox.showinfo('', 'Настройки успешно сохранены!')
                    window.destroy()
                else: messagebox.showwarning('', 'Время заданно не верно')
            else: messagebox.showwarning('', 'Не введен DevID/SetID!')
        else: messagebox.showwarning('', 'Не введен пароль!')
    else: messagebox.showwarning('', 'Данные Email заполнены не верно!')

# Смена выпадающих списком в зависимости от выбора
def on_combobox_change(event):
    selected_item_devset = combo_devset.get()
    selected_item = combo.get()

    if (combo_time.get() == "Выбор даты начала периода"):

        def grad_date():
            global  time_p
            if (combo_S.get() == "" or combo_M.get() == "" or combo_H.get() == ""):
                messagebox.showwarning('', 'Не заполнены данные о времени')
            else:
                a, b, c = cal.get_date().split("/")
                if int(a) < 10:
                    a_t = "0" + a
                else:
                    a_t = a
                if int(b) < 10:
                    b_t = "0" + b
                else:
                    b_t = b
                c_t = "20" + c
                date.config(text="Выбранные параметры: " + c_t + "-" + a_t + "-" + b_t + " " + combo_H.get() + ":" + combo_M.get() + ":" + combo_S.get())
                time_p = c_t + "-" + a_t + "-" + b_t + " " + combo_H.get() + ":" + combo_M.get() + ":" + combo_S.get()
                messagebox.showinfo('', 'Дата начала периода успешно назначена')

        time = tkinter.Toplevel(window)
        time.title("Выбор даты начала периода")
        time.geometry('250x335')  # Размер окна
        time.resizable(width=FALSE, height=FALSE)  # Блокировка размера окна
        time.grab_set()
        current_year = datetime.now().year
        current_day = datetime.now().day
        current_month = datetime.now().month
        cal = Calendar(time, maxdate=datetime(current_year, current_month, current_day), mindate = datetime(current_year - 2, current_month, current_day))
        cal.grid(column=0, row=0)
        if (log != 0):
            date = Label(time, text="Выбранные параметры: " + str(res["T1"]))
        else:
            date = Label(time, text="")
        date.place(x = 0, y = 195)
        text_time = Label(time, text="Время:       H                 M                 S")
        text_time.place(x = 0, y = 220)
        combo_H = Combobox(time, width=6)
        combo_H.place(x = 35, y = 240)
        combo_H['state'] = 'readonly'
        combo_H['values'] = ('00', '01', '02', '03', '04', '05', '06', '07', '08', '09', '10', '11', '12', '13', '14', '15', '16', '17', '18', '19', '20', '21', '22', '23')
        combo_M = Combobox(time, width=6)
        combo_M.place(x = 95, y = 240)
        combo_M['state'] = 'readonly'
        combo_M['values'] = ('00', '01', '02', '03', '04', '05', '06', '07', '08', '09', '10', '11', '12', '13', '14', '15', '16', '17', '18', '19', '20', '21', '22', '23', '24', '25', '26', '27', '28', '29', '30', '31', '32', '33', '34', '35', '36', '37', '38', '39', '40', '41', '42', '43', '44', '45', '46', '47', '48', '49', '50', '51', '52', '53', '54', '55', '56', '57', '58', '59')
        combo_S = Combobox(time, width=6)
        combo_S.place(x = 155, y = 240)
        combo_S['state'] = 'readonly'
        combo_S['values'] = ('00', '01', '02', '03', '04', '05', '06', '07', '08', '09', '10', '11', '12', '13', '14', '15', '16', '17', '18', '19', '20', '21', '22', '23', '24', '25', '26', '27', '28', '29', '30', '31', '32', '33', '34', '35', '36', '37', '38', '39', '40', '41', '42', '43', '44', '45', '46', '47', '48', '49', '50', '51', '52', '53', '54', '55', '56', '57', '58', '59')
        Button(time, text="Подтвердить", command=grad_date).place(x = 80, y = 280)

    if (combo_WSlocal.get() == "Локальный"):
        lbl_WSlocal.grid(column=0, row=4, sticky = "w")
        txt_WSlocal.grid(column=1, row=4)
        devsetr = 85
        lbl_devset.place(x=365, y=devsetr)
        txt_devset.place(x=390, y=devsetr)
    elif (combo_WSlocal.get() == "Облачный"):
        lbl_WSlocal.grid_remove()
        txt_WSlocal.grid_remove()
        devsetr = 64
        lbl_devset.place(x=365, y=devsetr)
        txt_devset.place(x=390, y=devsetr)

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
        lbl_combo_dop = Label(window, text=" Выберите усреднение:")
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


window = tkinter.Tk() # Открываем окно
window.geometry('438x255') # Размер окна
window.resizable(width=FALSE, height=FALSE) # Блокировка размера окна

log = 1
try:
    with open('authorization.pkl', 'r') as f:
        logpass = json.load(f)
    with open('settings.pkl', 'r') as f:
        res = json.load(f)
    with open('additional_load.pkl', 'r') as f:
        res_load = json.load(f)
except: log = 0
window.title("Настройка экспорта")
try:
    icon_path = "logo.ico"
    window.iconbitmap(icon_path)
except:
    pass
lbl_email = Label(window, text=" Введите логин (E-mail):")
lbl_email.grid(column=0, row=0, sticky='w')
txt_email = Entry(window,width=40)
txt_email.grid(column=1, row=0)
if (log != 0): txt_email.insert(0, logpass["Email"])
lbl_pass = Label(window, text=" Введите пароль:")
lbl_pass.grid(column=0, row=2, sticky='w')
txt_pass = Entry(window,width=40)
txt_pass.grid(column=1, row=2)
if (log != 0): txt_pass.insert(0, logpass["Pass"])
lbl_combo_WSlocal = Label(window, text=" Тип сервера:")
lbl_combo_WSlocal.grid(column=0, row=3, sticky='w')
combo_WSlocal = Combobox(window, width=37)
combo_WSlocal.grid(column=1, row=3)
combo_WSlocal['values'] = ("Облачный", "Локальный")
lbl_WSlocal = Label(window, text=" Введите URL:")
txt_WSlocal = Entry(window, width=40)
combo_WSlocal['state'] = 'readonly'
combo_WSlocal.bind("<<ComboboxSelected>>", on_combobox_change)
lbl_combo_devset = Label(window, text=r" Выберите DevID\SetID:")
lbl_combo_devset.grid(column=0, row=5, sticky='w')
combo_devset = Combobox(window, width=25)
combo_devset.grid(column=1, row=5, sticky='w')
combo_devset['values'] = ("DevID", "SetID")
combo_devset['state'] = 'readonly'
combo_devset.bind("<<ComboboxSelected>>", on_combobox_change)
lbl_devset = Label(window, text=" = ")
txt_devset = Entry(window,width=6)
if (log == 0):
    devsetr = 64
    lbl_devset.place(x=365, y=devsetr)
    txt_devset.place(x=390, y=devsetr)
lbl_combo = Label(window, text=" Выберите формат:")
lbl_combo.grid(column=0, row=6, sticky='w')
combo = Combobox(window, width=37)
combo.grid(column=1, row=6)
combo['state'] = 'readonly'
combo.bind("<<ComboboxSelected>>", on_combobox_change)
lbl_combo_filter = Label(window, text=" Выберите тип отчета:")
combo_filter = Combobox(window, width=37)
combo_filter['state'] = 'readonly'
lbl_combo_dop = Label(window, text=" Выберите усреднение:")
combo_dop = Combobox(window, width=37)
combo_dop['state'] = 'readonly'
lbl_combo_time = Label(window, text=" Выберите период:")
lbl_combo_time.grid(column=0, row=9, sticky='w')
combo_time = Combobox(window, width=37)
combo_time.grid(column=1, row=9)
combo_time['values'] = ("Прошлый месяц", "Прошлая неделя", "Прошлый день", "Выбор даты начала периода")
combo_time['state'] = 'readonly'
combo_time.bind("<<ComboboxSelected>>", on_combobox_change)
txt_way = Entry(window,width=40)
lbl_way = Button(window, text=' Директория сохранения:', command=lambda:select_directory(txt_way))
lbl_way.grid(column=0, row=11, sticky="w")
txt_way = Entry(window,width=40)
txt_way.grid(column=1, row=11)
if (log != 0):
    try:
        if (logpass["Wsl"] == 0):
            combo_WSlocal.set("Облачный")
        else:
            combo_WSlocal.set("Локальный")
            txt_WSlocal.insert(0, logpass["Wsl"])
            way = os.path.normpath(logpass["Way"])
        if logpass["Way"] == 0:
            pass
        else:
            txt_way.insert(0, logpass["Way"])

        if ("DevID") in res:
            txt_devset.insert(0, (res["DevID"]))
            combo_devset.current(0)
            combo.set(res_load["Combo"])
            combo_filter.set(res_load["Filter"])
            if (res_load["Filter"] != "Тревоги CSV" and res_load["Filter"] != "Тревоги HTML" and res_load["Filter"] != "Тревоги PDF"): combo_dop.set(res_load["Dop"])
            combo_time.set(res_load["Time"])
        elif ("SetID") in res:
            txt_devset.insert(0, (res["SetID"]))
            combo_devset.current(1)
            combo.set(res_load["Combo"])
            combo_dop.set(res_load["Dop"])
            combo_time.set(res_load["Time"])
    except:
        log = 0


on_combobox_change("<<ComboboxSelected>>")
btn = Button(window, text="Сохранить", command=clicked)
btn.grid(column=1, row=15, sticky="e")

lbl_way_d = Label(window, text='Пример URL - https://my-test.ru/')
lbl_way_d.grid(column=0, row=15, sticky="w")
window.mainloop()
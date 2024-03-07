from tkinter import *
from tkinter.ttk import Combobox
from tkinter import messagebox
import json

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
    elif (combo_filter.get() == "Температура и влажность"): typ = "temp-hum"
    elif (combo_filter.get() == "Только влажность"): typ = "hum"
    elif (combo_filter.get() == "Критические тревоги"): typ = "10"
    elif (combo_filter.get() == "Все тревоги"): typ = "20"
    elif (combo_filter.get() == "Тревоги и служебные"): typ = "30"
    return typ

def translating_values_time():
    if (combo_time.get() == "1 день"): tim = "1d"
    elif (combo_time.get() == "7 дней"): tim = "7d"
    elif (combo_time.get() == "31 день"): tim = "31d"
    elif (combo_time.get() == "Текущий месяц"): tim = "month"
    elif (combo_time.get() == "Текущая неделя"): tim = "week"
    elif (combo_time.get() == "Текущий день"): tim = "day"
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
                logpass = {
                    "Email": txt_email.get(),
                    "Pass": txt_pass.get()
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

    if (selected_item_devset == "DevID"):
        combo['values'] = (
        "Основной PDF", "Основной HTML", "Показатели CSV", "Показатели HTML", "Показатели PDF", "Журнал ТиВ PDF",
        "Тревоги CSV", "Тревоги HTML", "Тревоги PDF")
        combo_devset['state'] = 'disabled'
        lbl_combo_filter.grid(column=0, row=5)
        combo_filter.grid(column=1, row=5)

    elif (selected_item_devset == "SetID"):
        combo['values'] = (
        "Основной PDF", "Основной HTML", "Показатели CSV", "Показатели HTML", "Показатели PDF", "Журнал ТиВ PDF")
        combo_devset['state'] = 'disabled'

    if ((selected_item == 'Основной PDF') or (selected_item == 'Основной HTML')):
        combo['state'] = 'disabled'
        combo_filter['values'] = ("Только температура", "Температура и влажность", "Только влажность")
        lbl_combo_dop = Label(window, text="Выберите усреднение:")
        lbl_combo_dop.grid(column=0, row=6)
        combo_dop.grid(column=1, row=6)
        combo_dop['values'] = ("Без усреднения", "5 минут", "1 час", "3 часа", "1 день")
    elif ((selected_item == 'Показатели CSV') or (selected_item == 'Показатели PDF') or (
        selected_item == 'Показатели HTML')):
        combo['state'] = 'disabled'
        combo_filter['values'] = ("Температура и влажность", "Только температура", "Только влажность")
        lbl_combo_dop = Label(window, text="Выберите усреднение:")
        lbl_combo_dop.grid(column=0, row=6)
        combo_dop.grid(column=1, row=6)
        combo_dop['values'] = ("Без усреднения", "5 минут", "1 час", "3 часа", "1 день")
    elif ((selected_item == 'Журнал ТиВ PDF')):
        combo['state'] = 'disabled'
        combo_filter['values'] = ("Только температура", "Температура и влажность")
        lbl_combo_dop = Label(window, text="Выбор времени:           ")
        lbl_combo_dop.grid(column=0, row=6)
        combo_dop.grid(column=1, row=6)
        combo_dop['values'] = ("0:00", "1:00", "2:00", "3:00", "4:00", "5:00", "6:00", "7:00", "8:00", "9:00",
                               "10:00", "11:00", "12:00", "13:00", "14:00", "15:00", "16:00", "17:00", "18:00",
                               "19:00", "20:00", "21:00", "22:00", "23:00")
    elif ((selected_item == 'Тревоги CSV') or (selected_item == 'Тревоги HTML') or (
            selected_item == 'Тревоги PDF')):
        combo['state'] = 'disabled'
        combo_filter['values'] = ("Критические тревоги", "Все тревоги", "Тревоги и служебные")


window = Tk() # Открываем окно
window.geometry('500x200') # Размер окна
window.resizable(width=FALSE, height=FALSE) # Блокировка размера окна
window.title("Настройка отчета Unimon!")
lbl_email = Label(window, text="Введите E-mail:              ")
lbl_email.grid(column=0, row=0)
txt_email = Entry(window,width=40)
txt_email.grid(column=1, row=0)
lbl_email = Label(window, text="Введите Пароль:           ")
lbl_email.grid(column=0, row=2)
txt_pass = Entry(window,width=40)
txt_pass.grid(column=1, row=2)
lbl_combo_devset = Label(window, text="Выберите DevID|SetID: ")
lbl_combo_devset.grid(column=0, row=3)
combo_devset = Combobox(window, width=37)
combo_devset.grid(column=1, row=3)
combo_devset['values'] = ("DevID", "SetID")
combo_devset['state'] = 'readonly'
combo_devset.bind("<<ComboboxSelected>>", on_combobox_change)
lbl_devset = Label(window, text=" = ")
lbl_devset.grid(column=2, row=3)
txt_devset = Entry(window,width=6)
txt_devset.grid(column=3, row=3)
lbl_combo = Label(window, text="Выберите формат:       ")
lbl_combo.grid(column=0, row=4)
combo = Combobox(window, width=37)
combo.grid(column=1, row=4)
combo['state'] = 'readonly'
combo.bind("<<ComboboxSelected>>", on_combobox_change)
lbl_combo_filter = Label(window, text="Выберите тип отчета:  ")
combo_filter = Combobox(window, width=37)
combo_filter['state'] = 'readonly'
combo_dop = Combobox(window, width=37)
combo_dop['state'] = 'readonly'
lbl_combo_time = Label(window, text="Выберите период:        ")
lbl_combo_time.grid(column=0, row=7)
combo_time = Combobox(window, width=37)
combo_time['values'] = ("1 день", "7 дней", "31 день", "Текущий месяц", "Текущая неделя", "Текущий день")
combo_time.grid(column=1, row=7)
combo_time['state'] = 'readonly'
lbl_btn1 = Label(window, text="       ")
lbl_btn1.grid(column=0, row=8)
lbl_btn2 = Label(window, text="       ")
lbl_btn2.grid(column=0, row=9)
btn = Button(window, text="Сохранить!", command=clicked)
btn.grid(column=1, row=9)
window.mainloop()
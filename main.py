from datetime import datetime, timedelta
import requests
import base64
import time
import json
import os
import sys

def main():

    # Визуальный вывод для CMD
    print("1. Данные для входа направлены")
    time.sleep(1)

    sta_code1 = 0

    if (id_token == 0):
        # Отправляем запрос на авторизацию
        login_url = "https://api.unimon.ru/v1/user/login"

        if (f_o["Wsl"] != 0):
            login_url = f_o["Wsl"] + "v1/user/login"

        login_data = {
            "Email": f_o["Email"],
            "Pass": f_o["Pass"],
            "ClientType": "External",
            "ClientCode": "TestAPI"
        }
        login_headers = {"Content-Type": "application/json"}
        login_response = requests.post(login_url, json=login_data, headers=login_headers)
        sta_code1 = login_response.status_code
    elif (id_token == 1): sta_code1 = 200

    if (sta_code1 == 200):

        if (id_token == 0):
            token = {
                "Email": f_o["Email"],
                "Pass": f_o["Pass"],
                "Token": login_response.text.strip()
            }
            with open('token.pkl', 'w') as f:
                json.dump(token, f)

        print("2. Авторизация прошла успешно")
        time.sleep(1)

        # Запись log авторизации в файл
        if (id_token == 0): f_l.write(str(login_response.status_code))
        elif (id_token == 1): f_l.write(str(sta_code1))
        f_l.write(" - код авторизации\n")

        if (id_token == 0): login_token = login_response.text.strip()  # Получаем токен из ответа
        elif (id_token == 1):
            login_token = f_t["Token"]

        # Формируем запрос на получение файла с использованием токена авторизации
        export_url = "https://api.unimon.ru/v1/export/main/tofile"

        if (f_o["Wsl"] != 0):
            export_url = f_o["Wsl"] + "v1/export/main/tofile"

        export_headers = {
            "Authorization": base64.b64encode(login_token.encode()).decode(),
            "Content-Type": "application/json",
            "Origin": "https://my.unimon.ru"
        }

        export_response = requests.get(export_url, params=f_s, headers=export_headers)

        if (export_response.status_code == 200):  # Проверяем статус ответа

            print("3. Запрос на получение отчета обработан")
            time.sleep(1)

            # Запись получения ссылки отчета и обработки Get запроса
            f_l.write(str(export_response.status_code))
            f_l.write(" - код получения ссылки\n")

            # Выводим полученную ссылку на отчет в log
            f_l.write(export_response.json()['url'])
            f_l.write(" - прямая ссылка на отчет\n")

            if (f_s["Format"] == "th1"):
                f_s["Format"] = "pdf"

            if (f_o["Way"] != 0 and os.path.exists(f_o["Way"])):
                r = requests.get(export_response.json()['url'])
                way = os.path.normpath(f_o["Way"])
                file_path = way + '/Report ' + id + timeDS + '.' + f_s["Format"]
                with open(file_path, 'wb') as f:
                    f.write(r.content)
                lbl_write = "4. Отчет загружен"
            else:
                r = requests.get(export_response.json()['url'])
                file_path = 'Report ' + id + timeDS + '.' + f_s["Format"]
                with open(file_path, 'wb') as f:
                    f.write(r.content)
                print("Не введен путь сохранения файла!")
                time.sleep(1)
                lbl_write = "4. Отчет загружен в корневую папку скрипта"

            print(lbl_write)
            time.sleep(2)

        elif (export_response.status_code == 400):
            f_l.write(str(export_response.status_code))
            f_l.write(" - проверьте правильность внесенных данных!\n")
            print("Ошибка: данные внесены не верно!")
            time.sleep(3)

        else:
            f_l.write(str(export_response.status_code))
            f_l.write(
                " - код ошибки входа, подробнее - https://ru.wikipedia.org/wiki/Список_кодов_состояния_HTTP#401\n")
            print("Ошибка: инспектирование в log.txt!")
            time.sleep(3)

    elif (sta_code1 == 400):
        f_l.write(str(sta_code1))
        f_l.write(" - проверьте правильность внесенных данных!\n")
        print("Ошибка: данные внесены не верно!")
        time.sleep(3)

    elif (sta_code1 == 403):
        f_l.write(str(sta_code1))
        f_l.write(" - неправильные данные для аутентификации или превышено количество попыток входа!\n")
        print("Ошибка: данные внесены не верно или превышено количество попыток входа!")
        time.sleep(3)

    else:
        f_l.write(str(sta_code1))
        f_l.write(" - код ошибки входа, подробнее - https://ru.wikipedia.org/wiki/Список_кодов_состояния_HTTP#401\n")
        print("Ошибка: инспектирование в log.txt!")
        time.sleep(3)

if __name__ == "__main__":
    f_l = open("log.txt", "w")

    # Занесение параметров из paramerts.txt
    try:
        with open('authorization.pkl') as f:
            f = f.read()
        f_o = json.loads(f)

        with open('settings.pkl') as f:
            f = f.read()
        f_s = json.loads(f)
    except:
        print("Ошибка: данные аунтифекации не заполнены!")
        f_l.write("Перед началом работы необходимо зайти в \"Параметры отчета\"!\n")
        time.sleep(3)
        sys.exit()

    id_token = 0
    try:
        with open('token.pkl') as f:
            f = f.read()
        f_t = json.loads(f)
        if (f_t["Email"] == f_o["Email"] and f_t["Pass"] == f_o["Pass"] and f_t["Token"] != ""): id_token = 1
    except: pass

    # Преобразование времени в Unix
    current_date = datetime.now()

    if f_s["T1"] == "month":
        f_s["T1"] = (current_date.replace(day=1, hour=0, minute=0, second=0, microsecond=0) - timedelta(days=1)).replace(day=1, hour=0, minute=0, second=0, microsecond=0)
        f_s["T2"] = current_date.replace(day=1, hour=0, minute=0, second=0, microsecond=0) - timedelta(seconds=1)
        timeDS = r" c " + str(f_s["T1"])[:10] + r" по " + str(f_s["T2"])[:10]
    elif f_s["T1"] == "week":
        f_s["T1"] = (current_date - timedelta(days=current_date.weekday() + 7)).replace(hour=0, minute=0, second=0,microsecond=0)
        f_s["T2"] = (f_s["T1"] + timedelta(days=7)).replace(hour=23, minute=59, second=59, microsecond=0) - timedelta(days=1)
        timeDS = r" c " + str(f_s["T1"])[:10] + r" по " + str(f_s["T2"])[:10]
    elif f_s["T1"] == "day":
        f_s["T1"] = current_date.replace(hour=0, minute=0, second=0, microsecond=0) - timedelta(days=1)
        f_s["T2"] = current_date.replace(hour=23, minute=59, second=59, microsecond=0) - timedelta(days=1)
        timeDS = r" c " + str(f_s["T1"])[:10] + r" по " + str(f_s["T2"])[:10]

    f_s["T1"] = int((f_s["T1"] - datetime(1970, 1, 1)).total_seconds()) * 1000
    f_s["T2"] = int((f_s["T2"] - datetime(1970, 1, 1)).total_seconds()) * 1000

    if ("DevID") in f_s:
        id = "D-" + f_s["DevID"]
    else: id = "S-" + f_s["SetID"]

    main()
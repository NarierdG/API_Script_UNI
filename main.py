from datetime import datetime, timedelta
import requests
import base64
import time
import json
import os

def main():

    # Визуальный вывод для CMD
    print("1. Данные для входа направлены")
    time.sleep(1)

    # Отправляем запрос на авторизацию
    login_url = "https://api.unimon.ru/v1/user/login"

    if (f_o["Wsl"] != 0):
        wsl = os.path.normpath(f_o["Wsl"])
        login_url = wsl + "user/login"

    login_data = {
        "Email": f_o["Email"],
        "Pass": f_o["Pass"],
        "ClientType": "External",
        "ClientCode": "TestAPI"
    }
    login_headers = {"Content-Type": "application/json"}
    login_response = requests.post(login_url, json=login_data, headers=login_headers)

    if (login_response.status_code == 200):

        print("2. Авторизация прошла успешно")
        time.sleep(1)

        # Запись log авторизации в файл
        f_l.write(str(login_response.status_code))
        f_l.write(" - код авторизации\n")

        login_token = login_response.text.strip()  # Получаем токен из ответа

        # Формируем запрос на получение файла с использованием токена авторизации
        export_url = "https://api.unimon.ru/v1/export/main/tofile"

        if (f_o["Wsl"] != 0):
            export_url = wsl + "export/main/tofile"

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

            r = requests.get(export_response.json()['url'])
            way = os.path.normpath(f_o["Way"])
            file_path = way + '/Отчет ' + str(datetime.now().date()) + '.' + f_s["Format"]
            with open(file_path, 'wb') as f:
                f.write(r.content)

            print("4. Отчет загружен")
            time.sleep(2)

        elif (export_response.status_code == 400):
            f_l.write(str(export_response.status_code))
            f_l.write(" - проверьте правильность внесенных данных!\n")
            print("Error: данные внесены не верно!")
            time.sleep(5)

        else:
            f_l.write(str(export_response.status_code))
            f_l.write(
                " - код ошибки входа, подробнее - https://ru.wikipedia.org/wiki/Список_кодов_состояния_HTTP#401\n")
            print("Error: инспектирование в log.txt!")
            time.sleep(5)

    elif (login_response.status_code == 400):
        f_l.write(str(login_response.status_code))
        f_l.write(" - проверьте правильность внесенных данных!\n")
        print("Error: данные внесены не верно!")
        time.sleep(5)

    elif (login_response.status_code == 403):
        f_l.write(str(login_response.status_code))
        f_l.write(" - неправильные данные для аунтификации или превышено количество попыток входа!\n")
        print("Error: данные внесены не верно или превышено количество попыток входа!")
        time.sleep(5)

    else:
        f_l.write(str(login_response.status_code))
        f_l.write(" - код ошибки входа, подробнее - https://ru.wikipedia.org/wiki/Список_кодов_состояния_HTTP#401\n")
        print("Error: инспектирование в log.txt!")
        time.sleep(5)

if __name__ == "__main__":
    f_l = open("log.txt", "w")

    # Занесение параметров из paramerts.txt
    with open('authorization.pkl') as f:
        f = f.read()
    f_o = json.loads(f)

    with open('settings.pkl') as f:
        f = f.read()
    f_s = json.loads(f)

    # Преобразование времени в Unix
    current_date = datetime.now()

    if f_s["T1"] == "month":
        f_s["T1"] = (current_date.replace(day=1, hour=0, minute=0, second=0, microsecond=0) - timedelta(days=1)).replace(day=1, hour=0, minute=0, second=0, microsecond=0)
        f_s["T2"] = current_date.replace(day=1, hour=0, minute=0, second=0, microsecond=0) - timedelta(seconds=1)
    elif f_s["T1"] == "week":
        f_s["T1"] = (current_date - timedelta(days=current_date.weekday() + 7)).replace(hour=0, minute=0, second=0,microsecond=0)
        f_s["T2"] = (f_s["T1"] + timedelta(days=7)).replace(hour=23, minute=59, second=59, microsecond=0) - timedelta(days=1)
    elif f_s["T1"] == "day":
        f_s["T1"] = current_date.replace(hour=0, minute=0, second=0, microsecond=0) - timedelta(days=1)
        f_s["T2"] = current_date.replace(hour=23, minute=59, second=59, microsecond=0) - timedelta(days=1)

    f_s["T1"] = int((f_s["T1"] - datetime(1970, 1, 1)).total_seconds()) * 1000
    f_s["T2"] = int((f_s["T2"] - datetime(1970, 1, 1)).total_seconds()) * 1000

    main()
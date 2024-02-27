import requests
import base64
import time
import json

def main():
    # Отправляем запрос на авторизацию
    login_url = "https://api.unimon.ru/v1/user/login"
    login_data = {
        "Email": f_o["Email"],
        "Pass": f_o["Pass"],
        "ClientType": "External",
        "ClientCode": "TestAPI"
    }
    login_headers = {"Content-Type": "application/json"}
    login_response = requests.post(login_url, json=login_data, headers=login_headers)

    if (login_response.status_code == 200):

        # Запись log авторизации в файл
        f_l.write(str(login_response.status_code))
        f_l.write(" - код авторизации\n")

        login_token = login_response.text.strip()  # Получаем токен из ответа

        # Запись полученного токена в log
        f_l.write(str(login_token))
        f_l.write(" - токен авторизации\n")

        # Формируем запрос на получение файла с использованием токена авторизации
        export_url = "https://api.unimon.ru/v1/export/main/tofile"
        export_params = {
            "Kind": "main",
            "Format": "pdf",
            "TimeZone": "user",
            "Group": f_o["Group"],
            "Ease": "no",
            "Filter": f_o["Filter"],
            "DevID": f_o["DevID"],
            "Types": f_o["Types"],
            'T1': t1_unix,
            'T2': t2_unix
        }

        export_headers = {
            "Authorization": base64.b64encode(login_token.encode()).decode(),
            "Content-Type": "application/json",
            "Origin": "https://my.unimon.ru"
        }

        export_response = requests.get(export_url, params=export_params, headers=export_headers)

        if (export_response.status_code == 200):  # Проверяем статус ответа

            # Запись получения ссылки отчета и обработки Get запроса
            f_l.write(str(export_response.status_code))
            f_l.write(" - код получения ссылки\n")

            # Выводим полученную ссылку на отчет в log
            f_l.write(export_response.json()['url'])
            f_l.write(" - прямая ссылка на отчет\n")

            r = requests.get(export_response.json()['url'])
            with open('Report.pdf', 'wb') as f:
                f.write(r.content)

        elif (login_response.status_code == 400):
            f_l.write(str(login_response.status_code))
            f_l.write(" - проверьте правльноть внесенных данных\n")

        else:
            f_l.write(str(login_response.status_code))
            f_l.write(
                " - код ошибки входа, подробнее - https://ru.wikipedia.org/wiki/Список_кодов_состояния_HTTP#401\n")

    elif (login_response.status_code == 400):
        f_l.write(str(login_response.status_code))
        f_l.write(" - проверьте правльноть внесенных данных\n")

    elif (login_response.status_code == 403):
        f_l.write(str(login_response.status_code))
        f_l.write(" - неправильные данные для аунтификации\n")

    else:
        f_l.write(str(login_response.status_code))
        f_l.write(" - код ошибки входа, подробнее - https://ru.wikipedia.org/wiki/Список_кодов_состояния_HTTP#401\n")

if __name__ == "__main__":
    f_l = open("log.txt", "w")

    # Занесение параметров из paramerts.txt
    with open('parameters.txt') as f:
        f = f.read()
    f_o = json.loads(f)

        # Преобразование времени в Unix
    t1_unix = int(time.mktime(time.strptime(f_o['T1'], '%Y-%m-%d %H:%M:%S')))
    t2_unix = int(time.mktime(time.strptime(f_o['T2'], '%Y-%m-%d %H:%M:%S')))
    t1_unix = str(t1_unix) + "000"
    t2_unix = str(t2_unix) + "000"
    main()
import schedule
import requests
import time

def perform_request(url):
    try:
        response = requests.get(url)
        response.raise_for_status()
        with open('log.txt', 'a+', encoding='utf-8') as file:
            file.write(f"Запрос выполнен успешно. Код состояния: {response.status_code}\n") 
    except requests.exceptions.HTTPError as errh:
        with open('log.txt', 'a+', encoding='utf-8') as file:
            file.write(f"Ошибка HTTP: {errh}\n")
    except requests.exceptions.ConnectionError as errc:
        with open('log.txt', 'a+', encoding='utf-8') as file:
            file.write(f"Ошибка подключения: {errc}\n")
    except requests.exceptions.RequestException as err:
        with open('log.txt', 'a+', encoding='utf-8') as file:
            file.write(f"Ошибка: {err}\n")


def main(url, start_interval, interval):
    time.sleep(start_interval)
    with open('log.txt', 'a+', encoding='utf-8') as file:
            file.write(f"Запуск планировщика запросов для URL: {url}\n")

    perform_request(url)
    
    schedule.every(interval).seconds.do(perform_request, url)
    
    
    while True:
        schedule.run_pending()


main('https://www.nbkr.kg/index.jsp?lang=RUS', 5, 0.5)
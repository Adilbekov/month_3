import schedule
import time
import requests

def job():
    print("Working...", time.ctime())

def notification_lesson_12_2b():
    print("Здравствуйте, сегодня у вас урок в 16:00")

def current_btc_price():
    url = "https://www.binance.com/api/v3/ticker/price?symbol=BTCUSDT"
    response = requests.get(url=url).json()
    print(response) 
    "Нужно из json вытащить стоимость крипты и также записать из каждые 10 минут в файл btc_logs.txt с датой и также временем"

current_btc_price()


# schedule.every(3).seconds.do(current_btc_price)
# schedule.every(2  ).seconds.do(job)
# schedule.every(1).minutes.do(job)
# schedule.every().saturday.at("16:24").do(job)
# schedule.every().saturday.at("16:27").do(notification_lesson_12_2b)
# schedule.every().saturday.at("16:29", 'Asia/Bishkek').do(notification_lesson_12_2b)
# schedule.every(2).seconds.do(job)
# schedule.every(4).seconds.do(notification_lesson_12_2b)

while True:
    schedule.run_pending()
    time.sleep(1)

import requests
import time
from bs4 import BeautifulSoup
from telegram import Bot
import os

# Получаем токен и chat_id из переменных окружения
TOKEN = os.getenv('7865772666:AAEQfToyarQrscGaYWa99-IlfVaDtjkprJY')
CHAT_ID = os.getenv('10010994646')
URL = 'https://www.list.am/en/c/1442'  # Ссылка на страницу с автомобилями

# Функция для получения данных с сайта list.am
def get_cars():
    response = requests.get(URL)
    soup = BeautifulSoup(response.text, 'html.parser')
    cars = soup.find_all('a', {'class': 'link_title'})
    
    car_list = []
    for car in cars:
        title = car.get_text()
        link = car['href']
        
        # Ищем цену в названии или описании (простой способ)
        price = None
        price_tag = car.find_next('div', {'class': 'price'})  # Предположим, что цена указана в этом классе
        if price_tag:
            price_text = price_tag.get_text().strip()
            # Преобразуем цену в число, если она есть
            try:
                price = int(''.join(filter(str.isdigit, price_text)))
            except ValueError:
                price = None
        
        # Если цена меньше или равна 3000, добавляем в список
        if price and price <= 3000:
            car_list.append(f"{title}: {link} - Цена: {price_text}")
    
    return car_list

# Функция для отправки сообщений в Telegram
def send_message(message):
    bot = Bot(token=TOKEN)
    bot.send_message(chat_id=CHAT_ID, text=message)

# Основной цикл для проверки автомобилей
while True:
    cars = get_cars()
    if cars:
        message = "\n".join(cars)
        send_message(message)
    time.sleep(3600)  # Пауза 1 час между запросами

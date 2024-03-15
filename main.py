import telebot
import requests
from bs4 import BeautifulSoup

OWM_API_KEY = "000be634412f078ad203b00957e74c50"
bot = telebot.TeleBot('7101899787:AAE0u5KhTl2Irool9X5LW4ZXkrNF1zLrrQE')

@bot.message_handler(commands=['start'])
def start_message(message):
    bot.send_message(message.chat.id, "Привет, я бот показываюший информация о погоде в городах,просто напиши свой после команды /search  ")

@bot.message_handler(commands=['search'])
def get_weather(message):
    try:
        city_name = message.text.split("/search ", 1)[1].capitalize()
        server = f"http://api.openweathermap.org/data/2.5/weather?q={city_name}&lang=ru&appid={OWM_API_KEY}&units=metric"
        response = requests.get(server)
        if response.status_code == 200:
            data = response.json()
            temperature = data["main"]["temp"]
            pressure = data["main"]["pressure"]
            humidity = data["main"]["humidity"]
            description = data["weather"][0]["description"]
            wind_speed = data["wind"]["speed"]
            
            answer = f"Погода в городе {city_name}:\n"
            answer += f"Температура: {temperature}°C\n"
            answer += f"Давление: {pressure} гПа\n"
            answer += f"Влажность: {humidity}%\n"
            answer += f"Осадки: {description}\n"
            answer += f"Скорость ветра: {wind_speed} м/c"
        else:
            answer = "Данный город не найден"
    except IndexError:
        answer = "Пожалуйста, укажите название города после команды /weather."
    except requests.exceptions.ReadTimeout:
        print("Извините, не удалось получить данные о погоде. Пожалуйста, попробуйте еще раз позже.")
    except Exception as e:
        answer = f"Произошла ошибка: {str(e)}"
    
    bot.send_message(message.chat.id, answer)

def get_crypto_price(crypto):
    try:
        if crypto.lower() == 'eth':
            url = "https://www.binance.com/ru-KZ/price/ethereum"
        elif crypto.lower() == 'btc':
            url = "https://www.binance.com/ru-KZ/price/bitcoin"
        elif crypto.lower() == 'doge':
            url = "https://www.binance.com/ru-KZ/price/dogecoin"
        elif crypto.lower() == 'bnb':
            url = "https://www.binance.com/ru-KZ/price/bnb"
        else:
            return None

        response = requests.get(url)
        soup = BeautifulSoup(response.content, 'html.parser')
        price = soup.find("div", {"data-bn-type": "text","class": "css-1bwgsh3"}).text
        return price
    except Exception as e:
        print("Ошибка при получении цены:", e)
        return None

@bot.message_handler(func=lambda message: message.text.lower() in ['eth', 'btc', 'bnb', 'doge'])
def handle_crypto_request(message):
    crypto = message.text.strip().lower()
    price = get_crypto_price(crypto)
    if price:
        bot.send_message(message.chat.id, f"{message.from_user.first_name}, 1 {crypto.upper()} = {price} USD")
    else:
        bot.send_message(message.chat.id, f"К сожалению, на данный момент невозможно получить цену на {crypto.upper()}.")


bot.polling()

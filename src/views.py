import json
import os
from datetime import datetime, time

import requests
from dotenv import load_dotenv

from src.utils import filtered_cards, filtered_top, generate_json

load_dotenv()


try:

    with open("user_settings.json", "r", encoding="utf-8") as file:
        data = json.load(file)

        currency_list = []
        currency_stock = []
        user_currencies = data.get("user_currencies", [])
        user_stocks = data.get("user_stocks", [])


except FileNotFoundError:
    print("Ошибка: файл 'user_settings.json' не найден.")
except json.JSONDecodeError as e:
    print(f"Ошибка чтения JSON: {e}")
except Exception as e:
    print(f"Произошла ошибка: {e}")


def get_currency_price(user_currencies):
    """Функция получающая курсы валют по отношению к Рублю"""
    api_key = os.getenv("PRICE_API_KEY")
    if not api_key:
        return {"error": "API-ключ не найден в .env файле"}

    url = f"https://api.apilayer.com/exchangerates_data/convert?to=RUB&from={user_currencies}&amount=1"

    try:
        headers = {"apiKey": api_key}
        response = requests.get(url, headers=headers)
        if response.status_code != 200:
            return {"error": "Ошибка при получении данных", "status_code": response.status_code}

        json_data = response.json()
        if not ("query" in json_data and "info" in json_data):
            return {"error": "Некорректная структура данных от API"}

        user_currency = json_data["query"]["from"]
        price = round(json_data["info"].get("rate", 0), 2)

        return {"currency": user_currency, "rate": price}

    except requests.exceptions.RequestException as e:
        return {"error": f"Ошибка сети: {str(e)}"}


def add_to_list():
    """Функция добавляет валюты в список currency_list, если они корректны"""
    currency_rates = {}
    for currency in user_currencies:
        result = get_currency_price(currency)
        if "error" not in result:
            currency_rates[result["currency"]] = result["rate"]
        else:
            print(f"Ошибка получения данных для валюты {currency}: {result['error']}")
    return currency_rates


def get_currency_stock(user_stocks, currency_stock=None):
    """
    Функция получающая цены акций.
    """
    if currency_stock is None:  # Проверка на значение по умолчанию
        currency_stock = []
    api_key_stock = os.getenv("STOCK_API_KEY")
    if not api_key_stock:
        return {"error": "API-ключ не найден в .env файле"}

    url = f"https://financialmodelingprep.com/api/v3/stock/list?apikey={api_key_stock}"

    try:
        response = requests.get(url)
        if response.status_code != 200:
            return {"error": "Ошибка при запросе данных о акциях", "status_code": response.status_code}

        stocks_data = response.json()

        for stock in stocks_data:
            for my_stock in user_stocks:
                if stock["symbol"] == my_stock:
                    currency_stock.append({"stock": stock["symbol"], "price": stock["price"]})
        return currency_stock
    except requests.exceptions.RequestException as e:
        return {"error": f"Ошибка сети: {str(e)}"}


def hi():
    """Функция приветствия, возвращающая соответствующее сообщение в зависимости от времени суток."""
    current_time = datetime.now().time()

    night_start = time(0, 0)
    night_end = time(5, 0)
    morning_start = time(5, 0)
    morning_end = time(12, 0)
    day_start = time(12, 0)
    day_end = time(17, 0)

    if night_start <= current_time <= night_end:
        return "Доброй ночи!"
    elif morning_start <= current_time <= morning_end:
        return "Доброе утро!"
    elif day_start <= current_time <= day_end:
        return "Добрый день!"
    else:
        return "Добрый вечер!"



def final_list(current_date, stocks=user_stocks):
    """Функция, формирующая конечный список из готовых данных"""

    # Вызов функции для генерации JSON
    generate_json(current_date)

    # Подготовка данных для транзакции
    transaction_for_print = [{}]
    transaction_for_print[0]["greeting"] = hi()  # Приветствие, возвращаемое функцией hi()
    transaction_for_print[0]["cards"] = filtered_cards()  # Список карт
    transaction_for_print[0]["top_transactions"] = filtered_top()  # Топ транзакций
    transaction_for_print[0]["currency_rates"] = add_to_list()  # Курсы валют
    transaction_for_print[0]["stock_prices"] = get_currency_stock(stocks)  # Цена акций

    return transaction_for_print

import logging
import os

import numpy as np
import pandas as pd

logger = logging.getLogger(__name__)
file_handler = logging.FileHandler("../logs/utils.log", "a")
file_handler.setLevel(logging.INFO)
file_formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
file_handler.setFormatter(file_formatter)
logger.addHandler(file_handler)
logger.setLevel(logging.DEBUG)

current_transactions = []
cards = []
top_list = []


def find_and_process_excel(
    formating,
    directory="data",
):
    """Ищет файл с указанным расширением в директории, читает Excel и возвращает данные в нужном формате."""
    try:
        logger.debug(f"Ищем файл с расширением .xlsx в директории {directory}")
        for root, _, files in os.walk(directory):
            for file in files:
                if file.endswith(".xlsx"):
                    file_path = os.path.join(root, file)
                    logger.info(f"Найден файл: {file_path}")
                    break
            else:
                continue
            break
        else:
            raise FileNotFoundError("Файл с расширением .xlsx не найден в директории {directory}")

        logger.debug("Пытаемся прочитать Excel файл")
        excel_data = pd.read_excel(file_path, engine="openpyxl")
        logger.info("Excel файл успешно открыт")

        if formating == "dataframe":
            logger.debug("Возвращаем данные в формате DataFrame")
            return excel_data

        elif formating == "dict":
            logger.debug("Преобразуем данные в словарь")
            current_transactions = []
            for transaction in excel_data.to_dict(orient="records"):
                transaction = {
                    key: (None if isinstance(value, float) and np.isnan(value) else value)
                    for key, value in transaction.items()
                }
                current_transactions.append(transaction)
            logger.info("Данные успешно преобразованы в словарь")
            return current_transactions

        else:
            logger.error("Указан неверный формат данных")
            raise ValueError("Некорректный формат. Используйте 'dataframe' или 'dict'.")

    except Exception as e:
        logger.error(f"Ошибка: {e}")
        raise


def generate_json(current_date):
    """Функция, возвращающая отфильтрованные по дате транзакции"""
    for transaction in find_and_process_excel("dict"):
        if (
            str(transaction["Дата платежа"])[2:10] == current_date[2:10]
            and str(transaction["Дата платежа"])[:2] <= current_date[:2]
        ):
            current_transactions.append(transaction)
    logger.debug("Correct data payment")
    logger.debug("Correct data payment")
    return current_transactions


def filtered_cards():
    """Функция, возвращающая правильный список карт"""
    cards.clear()

    try:
        for transaction in current_transactions:
            last_digit = str(transaction["Номер карты"])[-4:]
            if len(last_digit) != 4:
                logger.warning(f"Некорректный номер карты: {transaction['Номер карты']}")
                continue

            spent = abs(transaction["Сумма операции"])

            existing_card = next((card for card in cards if card["last_digit"] == last_digit), None)

            if existing_card:

                existing_card["total_spent"] += spent
            else:

                cards.append(
                    {
                        "last_digit": last_digit,
                        "total_spent": spent,
                    }
                )

        for card in cards:
            card["cashback"] = card["total_spent"] // 100
        logger.debug("Карты успешно отфильтрованы")
        return cards
    except KeyError as e:
        logger.error(f"Ошибка в данных транзакций для карт: {e}")
        raise
    except Exception as e:
        logger.error(f"Ошибка при обработке данных карт: {e}")
        raise


def filtered_top():
    """Функция, возвращающая топ-5 транзакций по платежам"""
    top_list.clear()
    try:
        # Сортировка транзакций по убыванию абсолютных значений суммы платежа
        sort_current_transactions = sorted(current_transactions, reverse=True, key=lambda x: abs(x["Сумма платежа"]))

        for transaction in sort_current_transactions:
            top = {
                "date": transaction["Дата платежа"],
                "amount": abs(transaction["Сумма платежа"]),
                "category": transaction.get("Категория", "Не указано"),
                "description": transaction["Описание"],
            }
            top_list.append(top)
            if len(top_list) >= 5:
                break
        logger.debug("Топ-5 транзакций успешно сформирован")
        return top_list
    except KeyError as e:
        logger.error(f"Ошибка в данных транзакций для топа: {e}")
        raise
    except Exception as e:
        logger.error(f"Ошибка при формировании топ-5 транзакций: {e}")
        raise

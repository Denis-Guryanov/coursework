import json
import logging
import os
from datetime import datetime
import pandas as pd
from dateutil.relativedelta import relativedelta

log_dir = "../logs"
if not os.path.exists(log_dir):
    os.makedirs(log_dir)

logger = logging.getLogger(__name__)
file_handler = logging.FileHandler(f"{log_dir}/utils.log", "w")
file_formatter = logging.Formatter("%(asctime)s %(levelname)s: %(filename)s %(funcName)s: %(message)s")
file_handler.setFormatter(file_formatter)
logger.addHandler(file_handler)
logger.setLevel(logging.DEBUG)


def report_decorator(filename=None):
    def decorator(func):
        def wrapper(*args, **kwargs):
            result = func(*args, **kwargs)
            result = [
                {key: (None if pd.isna(value) else value) for key, value in transaction.items()}
                for transaction in result
            ]
            with open(filename, mode="a", encoding="utf-8") as f:
                json.dump(result, f, ensure_ascii=False)
                f.write("\n")

            return result

        return wrapper

    return decorator


def date_now():
    """Функция, возвращающая текущую дату"""
    now = datetime.now()
    formatted_date = now.strftime("%d.%m.2021")
    return formatted_date


@report_decorator("report.txt")
def spending_by_category(transactions: pd.DataFrame, category, date=None):
    """Функция, возвращающая список транзакций по заданной категории за 3 месяца"""
    if date is None:
        date = date_now()
    try:
        date_format = "%d.%m.%Y"
        end_date = datetime.strptime(date, date_format)
        start_date = end_date - relativedelta(months=3)
    except ValueError:
        logger.error("Неверный формат даты")
        return "Неверный формат данных"

    current_transactions = []
    for index, transaction in transactions.iterrows():
        if not isinstance(transaction["Дата платежа"], str):
            continue
        try:
            transaction_date = datetime.strptime(transaction["Дата платежа"], date_format)
            if transaction["Категория"] == category and start_date <= transaction_date <= end_date:
                transaction_data = transaction.to_dict()
                current_transactions.append(
                    {key: (None if pd.isna(value) else value) for key, value in transaction_data.items()}
                )
        except Exception as e:
            logger.error(f"Ошибка при обработке строки: {transaction}, {e}")
            continue

    logger.debug(f"Скорректированные возвращенные расходы по категориям {category}")
    return current_transactions

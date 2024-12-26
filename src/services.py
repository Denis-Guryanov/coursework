import logging
import os

log_dir = "../logs"

if not os.path.exists(log_dir):
    os.makedirs(log_dir)
logger = logging.getLogger(__name__)
file_handler = logging.FileHandler(f"{log_dir}/utils.log", "w")
file_formatter = logging.Formatter("%(asctime)s %(levelname)s: %(filename)s %(funcName)s: %(message)s")
file_handler.setFormatter(file_formatter)
logger.addHandler(file_handler)
logger.setLevel(logging.DEBUG)


def find_numbers(list_transactions):
    current_transactions = []
    for transaction in list_transactions:
        if isinstance(transaction, dict) and "+" in transaction.get("Описание", ""):
            current_transactions.append(transaction)
    logger.debug("Правильные возвращенные номера телефонов в описании")
    return current_transactions

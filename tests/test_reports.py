import json
from unittest.mock import mock_open, patch

import pandas as pd
import pytest

from src.reports import spending_by_category



@pytest.fixture
def category():
    return [
        {
            "MCC": 5814.0,
            "Дата операции": "16.01.2018 12:16:11",
            "Дата платежа": "17.01.2018",
            "Номер карты": "*7197",
            "Статус": "OK",
            "Сумма операции": -289.0,
            "Валюта операции": "RUB",
            "Сумма платежа": -289.0,
            "Валюта платежа": "RUB",
            "Кэшбэк": None,
            "Категория": "Фастфуд",
            "Описание": "OOO Frittella",
            "Бонусы (включая кэшбэк)": 5,
            "Округление на инвесткопилку": 0,
            "Сумма операции с округлением": 289.0,
        },
        {
            "MCC": 5814.0,
            "Дата операции": "15.01.2018 12:36:29",
            "Дата платежа": "16.01.2018",
            "Номер карты": "*7197",
            "Статус": "OK",
            "Сумма операции": -209.0,
            "Валюта операции": "RUB",
            "Сумма платежа": -209.0,
            "Валюта платежа": "RUB",
            "Кэшбэк": None,
            "Категория": "Фастфуд",
            "Описание": "OOO Frittella",
            "Бонусы (включая кэшбэк)": 4,
            "Округление на инвесткопилку": 0,
            "Сумма операции с округлением": 209.0,
        },
    ]


@patch("builtins.open", new_callable=mock_open, read_data="{}")
@patch("src.utils.find_and_process_excel")
def test_spending_by_category(mock_find_and_process_excel, mock_open):
    transactions_list = [
        {
            "Дата операции": "16.01.2018 12:16:11",
            "Дата платежа": "17.01.2018",
            "Номер карты": "*7197",
            "Статус": "OK",
            "Сумма операции": -289.0,
            "Валюта операции": "RUB",
            "Сумма платежа": -289.0,
            "Валюта платежа": "RUB",
            "Кэшбэк": None,
            "Категория": "Фастфуд",
            "MCC": 5814.0,
            "Описание": "OOO Frittella",
            "Бонусы (включая кэшбэк)": 5,
            "Округление на инвесткопилку": 0,
            "Сумма операции с округлением": 289.0,
        },
        {
            "Дата операции": "15.01.2018 12:36:29",
            "Дата платежа": "16.01.2018",
            "Номер карты": "*7197",
            "Статус": "OK",
            "Сумма операции": -209.0,
            "Валюта операции": "RUB",
            "Сумма платежа": -209.0,
            "Валюта платежа": "RUB",
            "Кэшбэк": None,
            "Категория": "Фастфуд",
            "MCC": 5814.0,
            "Описание": "OOO Frittella",
            "Бонусы (включая кэшбэк)": 4,
            "Округление на инвесткопилку": 0,
            "Сумма операции с округлением": 209.0,
        },
    ]

    transactions_df = pd.DataFrame(transactions_list)

    mock_find_and_process_excel.return_value = transactions_df

    result = spending_by_category(transactions_df, "Фастфуд", "17.01.2018")
    assert result


def test_record_file(category):
    with open("report.txt", mode="r", encoding="utf-8") as file:
        content = file.read()

    file_data = json.loads(content)

    assert file_data == category

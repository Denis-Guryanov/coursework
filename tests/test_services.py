import json

from src.services import find_numbers


def test_find_numbers():
    test_transactions = [
        {
            "MCC": 123,
            "Бонусы (включая кэшбэк)": 0,
            "Валюта операции": "RUB",
            "Валюта платежа": "RUB",
            "Описание": "+79991234567",
        },
        {
            "MCC": 456,
            "Бонусы (включая кэшбэк)": 10,
            "Валюта операции": "RUB",
            "Валюта платежа": "RUB",
            "Описание": "Some description",
        },
        {
            "MCC": 789,
            "Бонусы (включая кэшбэк)": 5,
            "Валюта операции": "RUB",
            "Валюта платежа": "RUB",
            "Описание": "+70001112233",
        },
    ]
    expected_result_json = (
        '[{"MCC": 123, "Бонусы (включая кэшбэк)": 0, "Валюта операции": "RUB", '
        '"Валюта платежа": "RUB", "Описание": "+79991234567"}, {"MCC": 789, "Бонусы '
        '(включая кэшбэк)": 5, "Валюта операции": "RUB", "Валюта платежа": "RUB", '
        '"Описание": "+70001112233"}]'
    )


    expected_result = json.loads(expected_result_json)

    result = find_numbers(test_transactions)

    assert result == expected_result

from unittest.mock import MagicMock, mock_open, patch

import pandas as pd
import pytest

from src.utils import find_and_process_excel, generate_json


@patch("builtins.open", mock_open(read_data='{"key": "value"}'))
@patch("src.utils.os.walk")
@patch("src.utils.pd.read_excel")
def test_find_and_process_excel_dataframe(mock_read_excel, mock_os_walk):
    """Тестируем успешное чтение Excel в DataFrame"""

    mock_os_walk.return_value = [("../data", [], ["test.xlsx"])]

    mock_read_excel.return_value = MagicMock()

    result = find_and_process_excel("dataframe")
    assert mock_read_excel.called
    assert result is not None


@patch("src.utils.os.walk")
def test_find_and_process_excel_file_not_found(mock_os_walk):
    """Тестируем ошибку, когда файл не найден"""
    mock_os_walk.return_value = [("../data", [], [])]  # Нет файлов .xlsx
    with pytest.raises(FileNotFoundError):
        find_and_process_excel("dataframe")


@patch("src.utils.os.walk")
@patch("src.utils.pd.read_excel")
def test_find_and_process_excel_to_dict(mock_read_excel, mock_os_walk):
    """Тестируем успешное преобразование в словарь"""

    mock_os_walk.return_value = [("../data", [], ["test.xlsx"])]

    mock_read_excel.return_value = pd.DataFrame({"Дата платежа": ["2023-01-01"], "Сумма операции": [100.5]})

    result = find_and_process_excel("dict")
    assert isinstance(result, list)
    assert "Дата платежа" in result[0]
    assert result[0]["Сумма операции"] == 100.5


@patch("src.utils.find_and_process_excel")
def test_generate_json_success(mock_find_and_process_excel):
    """Тестируем успешную генерацию транзакций по дате"""
    mock_find_and_process_excel.return_value = [
        {"Дата платежа": "01.01.2023", "Сумма операции": -500, "Номер карты": "1234567890123456"},
        {"Дата платежа": "02.01.2023", "Сумма операции": -300, "Номер карты": "2345678901234567"},
    ]

    current_date = "01.01.2023"
    result = generate_json(current_date)
    assert isinstance(result, list)
    assert len(result) == 1
    assert result[0]["Сумма операции"] == -500
    assert result[0]["Дата платежа"] == "01.01.2023"


@patch("src.utils.find_and_process_excel")
def test_generate_json_key_error(mock_find_and_process_excel):
    """Тестируем отсутствие ключа в данных"""
    mock_find_and_process_excel.return_value = [{"Сумма операции": -500, "Номер карты": "1234567890123456"}]

    with pytest.raises(KeyError):
        generate_json("01.01.2023")

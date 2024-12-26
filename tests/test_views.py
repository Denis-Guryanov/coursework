import json

import unittest
from datetime import datetime
from unittest.mock import MagicMock, mock_open, patch

from freezegun import freeze_time


from src.views import add_to_list, final_list, get_currency_stock, hi


class TestFunctions(unittest.TestCase):

    @patch(
        "builtins.open",
        new_callable=mock_open,
        read_data='{"user_currencies": ["USD", "EUR"], "user_stocks": ["AAPL", "TSLA"]}',
    )
    def test_file_read_success(self, mock_file):
        """Тестируем успешное чтение JSON-файла."""

        with open("user_settings.json", "r", encoding="utf-8") as file:
            data = json.load(file)
            user_currencies = data.get("user_currencies", [])
            user_stocks = data.get("user_stocks", [])


        self.assertEqual(user_currencies, ["USD", "EUR"])
        self.assertEqual(user_stocks, ["AAPL", "TSLA"])
        mock_file.assert_called_with("user_settings.json", "r", encoding="utf-8")

    @patch("builtins.open", new_callable=mock_open)
    def test_file_not_found(self, mock_file):
        """Тестируем обработку ошибки при отсутствии файла."""
        mock_file.side_effect = FileNotFoundError
        with self.assertRaises(FileNotFoundError):
            with open("user_settings.json", "r", encoding="utf-8") as file:
                json.load(file)


    @patch("requests.get")
    def test_get_currency_stock_success(self, mock_get):
        """Тестируем успешный запрос для получения данных об акциях."""
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = [{"symbol": "AAPL", "price": 145.0}, {"symbol": "TSLA", "price": 650.0}]
        mock_get.return_value = mock_response

        result = get_currency_stock(["AAPL", "TSLA"])
        self.assertEqual(result, [{"stock": "AAPL", "price": 145.0}, {"stock": "TSLA", "price": 650.0}])

    @patch("requests.get")
    def test_get_currency_stock_failure(self, mock_get):
        """Тестируем неудачный запрос для получения данных об акциях."""
        mock_response = MagicMock()
        mock_response.status_code = 500
        mock_get.return_value = mock_response

        result = get_currency_stock(["AAPL", "TSLA"])
        self.assertEqual(result, {"error": "Ошибка при запросе данных о акциях", "status_code": 500})

    def test_hi(self):
        """Тестируем функцию приветствия."""
        with freeze_time("2023-10-15 08:00:00"):
            # Ваши логика и проверки здесь
            result = hi()
            self.assertEqual(result, "Доброе утро!")

        with freeze_time("2023-10-15 14:00:00"):
            # Вторая часть теста для другого времени
            result = hi()
            self.assertEqual(result, "Добрый день!")

        with freeze_time("2023-10-15 20:00:00"):
            # Третья часть теста для другого времени
            result = hi()
            self.assertEqual(result, "Добрый вечер!")

        @patch("src.utils.generate_json")
        @patch("src.utils.filtered_cards")
        @patch("src.utils.filtered_top")
        def test_final_list(self, mock_filtered_top, mock_filtered_cards, mock_generate_json):
            """Тестируем функцию final_list."""
            current_date = datetime.now().date()

            final_list(current_date)

            # Проверяем, что вызовы происходят
            mock_generate_json.assert_called_with(current_date)
            mock_filtered_cards.assert_called()
            mock_filtered_top.assert_called()

        @patch("src.utils.generate_json")
        @patch("src.utils.filtered_cards")
        @patch("src.utils.filtered_top")
        def test_add_to_list(self, mock_filtered_top, mock_filtered_cards, mock_generate_json):
            """Тестируем добавление валют в список."""
            global user_currencies
            user_currencies = ["USD", "EUR"]

            # Моки для функции get_currency_price
            with patch("your_module.get_currency_price") as mock_get_currency_price:
                mock_get_currency_price.side_effect = [
                    {"currency": "USD", "rate": 75.5},
                    {"currency": "EUR", "rate": 90.0},
                ]

                result = add_to_list()

            self.assertEqual(result, ["USD", "EUR"])

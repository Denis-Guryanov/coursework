from datetime import datetime

from src.reports import spending_by_category
from src.services import find_numbers
from src.utils import find_and_process_excel
from src.views import final_list, hi


def bank_app():
    print(hi())
    user_answer = input(
        "Выберите категорию из доступных:\n"
        "1. Главная\n"
        "2. Поиск по телефонным номерам\n"
        "3. Траты по категориям\n"
        "Пользователь: "
    )
    if user_answer == "1" or user_answer.lower() == "главная":
        while True:
            try:
                user_input = input('Введите корректную дату и время в формате "ДД.ММ.ГГГГ ЧЧ:ММ:СС"\nПользователь: ')
                datetime_format = datetime.strptime(user_input, "%d.%m.%Y %H:%M:%S")
                formatted_date = datetime_format.strftime("%d.%m.%Y %H:%M:%S")
                print(f"Дата и время успешно обработаны: {formatted_date}")

                user_result = final_list(formatted_date)

                return user_result

            except ValueError:
                print("Неверный формат. Попробуйте ещё раз (пример: 15.10.2023 00:00:00).")
                continue

    elif user_answer == "2" or user_answer.lower() == "поиск по телефонным номерам":
        try:
            phone_data = find_numbers(find_and_process_excel("dict"))
            user_result = find_numbers(phone_data)
            return user_result
        except Exception as e:
            return f"Ошибка в обработке: {e}"
    elif user_answer == "3" or user_answer.lower() == "траты по категориям":
        try:
            user_category = input("Введите категорию для поиска\nПользователь: ")
            user_data = input('Введите дату для поиска транзакций за 3 месяца в формате: "ДД.ММ.ГГГГ"\nПользователь: ')
            transaction_data = find_and_process_excel("dataframe")
            user_result = spending_by_category(transaction_data, user_category, user_data)
            return user_result
        except ValueError:
            return "Ошибка формата даты! Попробуйте ввести дату в формате: ДД.ММ.ГГГГ"
        except Exception as e:
            return f"Произошла ошибка: {e}"
    else:
        return "Неизвестная категория. Попробуйте выбрать один из пунктов меню."

    return user_answer


if __name__ == "__main__":
    print(bank_app())

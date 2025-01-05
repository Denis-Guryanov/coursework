# Курсовая работа №1
## Приложение для анализа транзакций находящихся в Excel файле

## Описание
В данном проекте реализованны:
1. Функции для Главной страницы в которой происходит логика обращенияи к внешним Api
2. Функции для поиска транзакций по телефонным номерам
3. Функции для поиска транзакций по категориям

## Установка

### Для установки в вашем редакторе кода пропишите:
```
git clone https://github.com/Denis-Guryanov/coursework.git

```
+ Установите зависимости:
```
poetry install
```

## Проверка проекта 

1. Для проверки проекта в Flake8 введите в терминале команду:
```
flake8 src
```
2. Для проверки проекта в mypy введите в терминале команду:
```
mypy src
```

## Тестирование

+ Для тестирования всех функций данного проекта введите команду:
```
pytest
```
+ Для тестирования всех функций данного проекта с анализом покрытия введите команду:

```
poetry run pytest -- cov
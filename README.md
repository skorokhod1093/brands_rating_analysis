# Brand Rating Analyzer

## Установка just через Scoop (PowerShell Windows)
### Установите Scoop (если ещё не установлен)

    Set-ExecutionPolicy RemoteSigned -Scope CurrentUser
    irm get.scoop.sh | iex

### Установите just

    scoop install just

## Установите зависимости в виртуальное окружение

    just setup

## Запуск программы
### Запуск программы с одним CSV-файлом

    just run ".products/products1.csv" "average-rating"

### Запуск программы с двумя CSV-файлами

    just run ".products/products1.csv .products/products2.csv" "average-rating"

## Запуск тестов

    just test

## Отдельные команды
### Проверка стиля кода

    just lint

### Форматирование кода (black)

    just format

### Проверка типов (mypy)

    just type-check

### Все проверки сразу

    just check

### Проверка типов (mypy)

    just check-check

## Удалить временные файлы

    just clean

## Полная очистка

    just clean-all

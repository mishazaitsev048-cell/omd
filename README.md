# omd

Домашнее задание по Python: реализация классов для векторизации текста и извлечения ключевых слов.

Реализованы классы CountVectorizer, BinaryVectorizer, TfidfVectorizer и KeywordExtractor.

## Требования

- Python 3.12 или новее

## Установка зависимостей

Внешние библиотеки для работы программы не требуются, дополнительно ничего устанавливать не нужно.

## Запуск

    python hw_classes_base.py

В Windows, если команда `python` не найдена, используй `py hw_classes_base.py`.

Программа запускает демонстрационные примеры работы классов и выводит результаты в консоль.

## Проверка качества кода

Для проверки используются flake8, pycodestyle (PEP 8) и mypy.

Установка:

    python -m pip install flake8 pycodestyle mypy

Проверка:

    python -m flake8 hw_classes_base.py
    python -m pycodestyle hw_classes_base.py
    python -m mypy hw_classes_base.py
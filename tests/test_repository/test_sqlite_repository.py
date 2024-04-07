import pytest
import sqlite3
from unittest.mock import MagicMock
from tempfile import NamedTemporaryFile
from pathlib import Path
from datetime import datetime
from typing import List, Dict

from ...bookkeeper.repository.memory_repository \
        import SQLiteRepository
from ...bookkeeper.models.expense import Expense
from ...bookkeeper.models.category import Category


@pytest.fixture
def db_file():
    # Создаем временный файл базы данных SQLite
    temp_file = NamedTemporaryFile(delete=False)
    temp_file.close()
    yield temp_file.name  # Предоставляем имя файла
    Path(temp_file.name).unlink()  # Удаляем файл после использования


def test_init(db_file):
    repository = SQLiteRepository(db_file, Expense)
    assert repository.db_file == db_file
    assert repository.table_name == 'expense'
    assert repository.fields != {'amount': int, 'category': int, 'comment': str}


def test_create_table(db_file):
    repository = SQLiteRepository(db_file, Expense)
    repository.create_table()

    # Проверяем, что таблица 'expense' создана с нужными столбцами
    connection = sqlite3.connect(db_file)
    cursor = connection.cursor()
    cursor.execute("PRAGMA table_info(expense)")
    columns = cursor.fetchall()
    expected_columns = [
        (0, 'amount', 'INTEGER', 0, None, 0),
        (1, 'category', 'INTEGER', 0, None, 0),
        (2, 'expense_date', 'TEXT', 0, None, 0),
        (3, 'added_date', 'TEXT', 0, None, 0),
        (4, 'comment', 'TEXT', 0, None, 0),
        (5, 'pk', 'INTEGER', 0, None, 1)
    ]
    assert columns == expected_columns


def test_add(db_file):
    repository = SQLiteRepository(db_file, Expense)

    # Создаем фиктивные данные для объекта Expense
    expense = Expense(amount=100, category=1, expense_date='2024-04-04', added_date='2024-04-05', comment='Test')

    # Добавляем объект в базу данных и получаем его pk
    pk = repository.add(expense)

    # Проверяем, что объект добавлен и у него присвоен pk
    assert pk is not None
    assert expense.pk == pk

    # Проверяем, что объект действительно добавлен в базу данных
    connection = sqlite3.connect(db_file)
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM expense WHERE pk=?", (pk,))
    result = cursor.fetchone()
    expected_result = (100, 1, '2024-04-04', '2024-04-05', 'Test', pk)
    assert result == expected_result


def test_get_all(db_file):
    repository = SQLiteRepository(db_file, Expense)

    # Создаем фиктивные данные для объектов Expense
    expenses_data = [
        {'amount': 100, 'category': 1, 'expense_date': '2024-04-04', 'added_date': '2024-04-05', 'comment': 'Test1'},
        {'amount': 150, 'category': 2, 'expense_date': '2024-04-05', 'added_date': '2024-04-06', 'comment': 'Test2'}
    ]

    # Добавляем объекты в базу данных
    for data in expenses_data:
        repository.add(Expense(**data))

    # Получаем все объекты из базы данных
    expenses = repository.get_all()

    # Проверяем, что количество полученных объектов совпадает с ожидаемым
    assert len(expenses) == len(expenses_data)

    # Проверяем, что каждый полученный объект имеет ожидаемые значения атрибутов
    for expense, data in zip(expenses, expenses_data):
        for key, value in data.items():
            assert getattr(expense, key) == value


def test_create_object(db_file):
    repository = SQLiteRepository(db_file, Expense)

    # Создаем фиктивные данные для словаря значений атрибутов
    obj_dict = {'amount': 100, 'category': 1, 'expense_date': '2024-04-04', 'added_date': '2024-04-05', 'comment': 'Test'}

    # Создаем объект Expense на основе словаря значений атрибутов
    expense = repository.create_object(obj_dict)

    # Проверяем, что созданный объект имеет ожидаемые значения атрибутов
    for key, value in obj_dict.items():
        assert getattr(expense, key) == value

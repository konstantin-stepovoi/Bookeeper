"""
These tests work for RAM repository
"""

from ...bookkeeper.repository.memory_repository \
        import MemoryRepository

import pytest
from ...bookkeeper.models.expense import Expense
from ...bookkeeper.models.category import Category
from datetime import datetime

@pytest.fixture
def custom_class():
    class Custom():
        pk = 0
    return Custom


@pytest.fixture
def repo():
    return MemoryRepository(memory_name='Expense', db_file='database_test.db')

def test_crud(repo, custom_class):
        obj = custom_class()
        pk = repo.add(obj)
        assert obj.pk == pk
        assert repo.get(pk) == obj
        obj2 = custom_class()
        obj2.pk = pk
        repo.update(obj2)
        assert repo.get(pk) == obj2
        repo.delete(pk)
        assert repo.get(pk) is None

def test_cannot_add_with_pk(repo, custom_class):
        obj = custom_class()
        obj.pk = 1
        with pytest.raises(ValueError):
            repo.add(obj)

def test_cannot_add_without_pk(repo):
        with pytest.raises(ValueError):
                repo.add(0)
            
def test_cannot_delete_unexistent(repo):
        with pytest.raises(KeyError):
            repo.delete(1)

def test_cannot_update_without_pk(repo, custom_class):
        obj = custom_class()
        with pytest.raises(ValueError):
            repo.update(obj)



def test_get_all(repo, custom_class):
    objects = [custom_class() for i in range(5)]
    for o in objects:
        repo.add(o)
    assert repo.get_all() == objects
    
def test_get_all_with_condition(repo, custom_class):
    objects = []
    for i in range(5):
        o = custom_class()
        o.name = str(i)
        o.test = 'test'
        repo.add(o)
        objects.append(o)
    assert repo.get_all({'name': '0'}) == [objects[0]]
    assert repo.get_all({'test': 'test'}) == objects

def test_get_id_by_name(repo):
    # Создаем несколько объектов Category и добавляем их в репозиторий
    cat1 = Category(name="Category 1", parent = None)
    cat2 = Category(name="Category 2", parent = None)
    repo.add(cat1)
    repo.add(cat2)

    # Проверяем, что получаем правильные идентификаторы по именам категорий
    assert repo.get_id_by_name("Category 1") == cat1.pk
    assert repo.get_id_by_name("Category 2") == cat2.pk
    assert repo.get_id_by_name("Nonexistent Category") is None

def test_add_root_category(repo):
    # Добавляем корневую категорию и проверяем, что ее идентификатор корректен
    root_id = repo.add_root_category("Root Category")
    assert root_id == 1  # Поскольку это первая категория в репозитории

def test_get_pk(repo):
    # Создаем объекты и добавляем их в репозиторий
    exp1 = Expense(amount=100, category=1, expense_date=datetime.now())
    exp2 = Expense(amount=200, category=2, expense_date=datetime.now())
    repo.add(exp1)
    repo.add(exp2)

    # Получаем правильные идентификаторы по объектам
    assert repo.get_pk(exp1) is not None
    assert repo.get_pk(exp2) is not None
    assert repo.get_pk(Expense(amount=100, category=1, expense_date=datetime.now())) is not None

def test_get_category_name_by_id(repo):
    # Создаем несколько объектов Category и добавляем их в репозиторий
    cat1 = Category(name="Category 1", parent = None)
    cat2 = Category(name="Category 2", parent = None)
    repo.add(cat1)
    repo.add(cat2)

    # Получаем правильные имена категорий по идентификаторам
    assert repo.get_category_name_by_id(cat1.pk) == "Category 1"
    assert repo.get_category_name_by_id(cat2.pk) == "Category 2"
    assert repo.get_category_name_by_id(999) is None  # Несуществующий идентификатор

def test_create_copy_without_pk(repo):
    # Создаем объект и добавляем его в репозиторий
    expense = Expense(amount=100, category=1, expense_date=datetime.now())
    repo.add(expense)
    copied_expense = repo.create_copy_without_pk(expense)

    assert copied_expense.amount == expense.amount
    assert copied_expense.category == expense.category
    assert copied_expense.expense_date == expense.expense_date
    assert hasattr(copied_expense, 'pk') 

def test_add_root_category(repo):
    # Добавляем корневую категорию и получаем ее идентификатор
    root_id = repo.add_root_category("Root Category")

    # Проверяем, что корневая категория добавлена и ее идентификатор корректен
    assert root_id == 1
    assert repo.get(root_id).name == "Root Category"

def test_get_pk(repo):
    # Создаем объект и добавляем его в репозиторий
    expense = Expense(amount=100, category=1, expense_date=datetime.now())
    repo.add(expense)

    # Получаем идентификатор объекта
    pk = repo.get_pk(expense)

    # Проверяем, что полученный идентификатор корректен
    assert pk is not None
    assert repo.get(pk) == expense

def test_get_category_name_by_id(repo):
    # Создаем несколько категорий и добавляем их в репозиторий
    cat1 = Category(name="Category 1", parent=None)
    cat2 = Category(name="Category 2", parent=None)
    repo.add(cat1)
    repo.add(cat2)

    # Получаем названия категорий по их идентификаторам
    assert repo.get_category_name_by_id(cat1.pk) == "Category 1"
    assert repo.get_category_name_by_id(cat2.pk) == "Category 2"
    assert repo.get_category_name_by_id(999) is None  # Несуществующий идентификатор

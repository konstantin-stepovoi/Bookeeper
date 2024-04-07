from itertools import count
from typing import Any, Optional
from dataclasses import asdict
from repository.abstract_repository import AbstractRepository, T
from models.category import Category
from models.expense import Expense
import sqlite3
from repository.sqlite_repository import SQLiteRepository


class MemoryRepository(AbstractRepository[T]):

    """
    This repo works in the RAM and contains all the data in the dict
    """
    def __init__(self, memory_name: str, db_file: str) -> None:
        """
        Инициализирует объект MemoryRepository.

        Args:
            memory_name (str): Имя репозитория в памяти.
            db_file (str): Имя файла базы данных.
        """
        self.memory_name = memory_name
        self._container: dict[int, T] = {}
        self._counter = count(1)
        self.db_file = db_file
        self.expense_table = SQLiteRepository(db_file, Expense)
        self.category_table = SQLiteRepository(db_file, Category)
        self.get_everything_from_db()

    def get_everything_from_db(self) -> None:
        """
        Получает данные из SQLiteRepository и загружает их в память.
        """
        if self.memory_name == 'ExpMemo':
            expenses = self.expense_table.get_all()
            for expense in expenses:
                self.add_without_pk(expense)
        elif self.memory_name == 'CatMemo':
            categories = self.category_table.get_all()
            for category in categories:
                self.add_without_pk(category)

    def copy_to_sqlite(self) -> None:
        """
        Копирует данные из MemoryRepository в SQLiteRepository.
        """
        with sqlite3.connect(self.db_file) as conn:
            cursor = conn.cursor()
            if self.memory_name == 'ExpMemo':
                cursor.execute("DELETE FROM expense")
            elif self.memory_name == 'CatMemo':
                cursor.execute("DELETE FROM category")
            conn.commit()
        for obj in self._container.values():
            obj2 = self.create_copy_without_pk(obj)
            if isinstance(obj, Expense):
                self.expense_table.add(obj2)
            elif isinstance(obj, Category):
                self.category_table.add(obj2)

    def create_copy_without_pk(self, obj: T) -> T:
        """
        Создает копию объекта без атрибута pk.

        Args:
            obj (T): Объект для копирования.

        Returns:
            T: Копия объекта без атрибута pk.
        """
        obj_dict = asdict(obj)
        obj_dict.pop('pk', None)
        obj_copy = obj.__class__(**obj_dict)
        return obj_copy

    def add_without_pk(self, obj: T) -> int:
        """
        Добавляет объект без атрибута pk.

        Args:
            obj (T): Объект для добавления.

        Returns:
            int: Идентификатор добавленного объекта.
        """
        obj_copy = self.create_copy_without_pk(obj)
        return self.add(obj_copy)

    def copy_from_sqlite(self):
        """ Copy data from SQLiteRepository to MemoryRepository """
        self._container.clear()
        expenses = self.expense_table.get_all()
        categories = self.category_table.get_all()

        for expense in expenses:
            self.add(expense)
        for category in categories:
            self.add(category)

    def add(self, obj: T) -> int:
        """" Добавиить объект в репозиторий,
        Args:  obj (T), returns: id добавленного"""
        if getattr(obj, 'pk', None) != 0:
            raise ValueError(
                f'trying to add object {obj} with filled `pk` attribute')
        pk = next(self._counter)
        self._container[pk] = obj
        obj.pk = pk
        return pk

    def get(self, pk: int) -> T | None:
        """" Получить объект из репозитория,
        Args: id (int), returns: obj (T)"""
        return self._container.get(pk)

    def get_all(self, where: dict[str, Any] | None = None) -> list[T]:
        """ Получить вообще все объекты из репозитория в виде list """
        if where is None:
            return list(self._container.values())
        return [obj for obj in self._container.values()
                if all(
                    getattr(obj, attr) == value
                    for attr, value in where.items())]

    def update(self, obj: T) -> None:
        """Обновить какую - то строку
        после редактирования, Args: obj(T)"""

        if obj.pk == 0:
            raise ValueError(
                'attempt to update object with unknown primary key')
        self._container[obj.pk] = obj

    def delete(self, pk: int) -> None:
        """ Удалить объект из репозитория Arg pk:int """
        self._container.pop(pk)

    def get_id_by_name(self, category_name):
        """ получить id: int объекта по имени: str """
        for category in self._container.values():
            if category.name == category_name:
                return category.pk
        return None

    def add_root_category(self, category_name):
        """ Если что-то является
        объектом класса Category, то эта ф.
        может добавить
        его в качестве корневого объекта"""
        new_category_id = max(
            self._container.keys(), default=0) + 1
        new_category = Category(
            name=category_name,
            parent=None,
            pk=new_category_id
        )
        self._container[new_category_id] = new_category
        return new_category_id

    def get_pk(
        repository: 'MemoryRepository[Expense]',
        obj: Expense) -> Optional[int]:
        """
        Get the primary key (pk)
        of an object in the repositor
        based on the object's attributes.
        """
        for pk, stored_obj in repository._container.items():
            if all(
                getattr(stored_obj, attr) == getattr(obj, attr)
                for attr in stored_obj.__annotations__ if attr != 'pk'
            ):
                return pk
        return None

    def get_category_name_by_id(
        self, category_id: int) -> Optional[str]:
        """
        Получает название
        категории по идентификатору.

        Args:
            category_id (int):
            Идентификатор категории.

        Returns:
            Optional[str]:
            Название категории или None,
            если категория не найдена.
        """
        for category in self._container.values():
            if category.pk == category_id:
                return category.name
        return None

import sqlite3
from typing import TypeVar, Type, Generic, List, Dict, Any
from inspect import get_annotations

T = TypeVar('T')


class SQLiteRepository(Generic[T]):
    """
    Репозиторий SQLite
    для работы с объектами базы данных.
    """
    def __init__(self, db_file: str, cls: Type[T]) -> None:
        """
        Инициализирует объект SQLiteRepository.

        Args:
            db_file (str): Имя файла базы данных.
            cls (Type[T]): Тип класса объекта.
        """
        self.db_file = db_file
        self.table_name = cls.__name__.lower()
        self.fields = get_annotations(cls, eval_str=True)
        self.fields.pop('pk')
        self.cls = cls
        self.connection = sqlite3.connect(self.db_file)
        self.cursor = self.connection.cursor()
        self.create_table()

    def create_table(self):
        columns = []
        """ Создает таблицу в базе
        данных, если она не существует. """
        if self.table_name == 'expense':
            columns = [
                "amount INTEGER",
                "category INTEGER",
                "expense_date TEXT",
                "added_date TEXT",
                "comment TEXT",
                "pk INTEGER PRIMARY KEY AUTOINCREMENT"
            ]
        elif self.table_name == 'category':
            columns = [
                "name TEXT",
                "parent INTEGER",
                "pk INTEGER PRIMARY KEY AUTOINCREMENT"
            ]
        else:
            ...

        columns_string = ", ".join(columns)
        if columns_string:  # Проверка наличия хотя бы одного столбца
            sql_string = (
                f"CREATE TABLE IF NOT EXISTS {self.table_name} "
                f"({columns_string})"
            )
            self.cursor.execute(sql_string)

    def add(self, obj: T) -> int:
        """
        Добавляет объект в базу данных.

        Args:
            obj (T): Объект для добавления.

        Returns:
            int: Идентификатор добавленного объекта.
        """
        if not hasattr(obj, "pk"):
            raise ValueError("Object must have 'pk' attribute")
        if obj.pk != 0:
            return obj.pk
        columns_str = ", ".join(self.fields.keys())
        placeholders = ", ".join(['?'] * len(self.fields))
        sql_string = (
            f"INSERT INTO {self.table_name} "
            f"({columns_str}) " f"VALUES ({placeholders})"
        )
        values = [getattr(obj, field) for field in self.fields]
        self.cursor.execute(sql_string, values)
        self.connection.commit()
        obj.pk = self.cursor.lastrowid
        return obj.pk

    def get_all(self) -> List[T]:
        """
        Получает все объекты из базы данных.

        Returns:
            List[T]: Список объектов.
        """
        sql_string = (
            f"SELECT {', '.join(self.fields.keys())} "
            f"FROM {self.table_name}"
        )
        self.cursor.execute(sql_string)
        rows = self.cursor.fetchall()
        objects = []

        for row in rows:
            obj_dict = {}
            for idx, field in enumerate(self.fields.keys()):
                obj_dict[field] = row[idx]
            objects.append(self.create_object(obj_dict))

        return objects

    def create_object(self, obj_dict: Dict[str, Any]) -> T:
        """
        Создает объект на основе словаря значений атрибутов.

        Args:
            obj_dict (Dict[str, Any]): Словарь значений атрибутов объекта.

        Returns:
            T: Созданный объект.
        """
        obj = self.cls(**obj_dict)
        obj.pk = obj_dict.get('pk', None)
        return obj

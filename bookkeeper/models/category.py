from dataclasses import dataclass
from typing import Union
from repository.abstract_repository import AbstractRepository


@dataclass
class Category:
    """
    Категория расходов, хранит название в
    атрибуте name и ссылку (id) на родителя в
    атрибуте parent (у категорий верхнего
    уровня None).
    """
    name: str
    parent: Union[int, None]
    pk: int = 0

    def get_parent(self,
            repo: AbstractRepository['Category']) -> 'Category | None':
        """
        Gets the parent category as a Category object
        If the method is called on a
        top-level category, returns None
        Only parameter is 'repo'
        """
        if self.parent is None:
            return None
        return repo.get(self.parent)

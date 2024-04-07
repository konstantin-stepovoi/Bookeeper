from abc import ABC, abstractmethod
from typing import Generic, TypeVar, Any, List, Protocol


class Model(Protocol):
    """
    Model should contain pk attribute
    """
    pk: int


T = TypeVar('T', bound=Model)


class AbstractRepository(ABC, Generic[T]):
    @abstractmethod
    def add(self, obj: T) -> int:
        """
        Add an object to the repository, return its id,
        also assign the id to the pk attribute.
        """

    @abstractmethod
    def get(self, pk: int) -> T | None:
        """ Get an object by id """

    @abstractmethod
    def update(self, obj: T) -> None:
        """ Update object data """

    @abstractmethod
    def delete(self, pk: int) -> None:
        """ Delete a record """

    @abstractmethod
    def get_all(self, where: dict[str, Any] | None = None) -> List[T]:
        """
        Get all records based on some condition where -
        condition in the form of a dictionary {'field_name': value}
        if no condition is provided (by default), return all records
        """

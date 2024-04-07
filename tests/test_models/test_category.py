import pytest
from unittest.mock import Mock
from ...bookkeeper.models.category import Category
from ...bookkeeper.repository.abstract_repository import AbstractRepository


@pytest.fixture
def cat_repo():
    """
    Fixture for creating a mock category repository.
    """
    mock_repo = Mock(spec=AbstractRepository)
    # Mocking the behavior of get_all method
    mock_cats = [
        Category(name='name1', pk=0, parent=None),
        Category(name='name1', pk=1, parent=0),
        Category(name='name1', pk=2, parent=None)]
    mock_repo.get_all.return_value = mock_cats
    mock_repo.add.return_value = lambda item: max(cat.pk for cat in mock_cats) + 1
    return mock_repo

def test_create_object():
    c = Category('name', None)
    assert c.name == 'name'
    assert c.pk == 0
    assert c.parent is None

    c = Category(name='name', parent=1, pk=2)
    assert c.name == 'name'
    assert c.parent == 1
    assert c.pk == 2

def test_reassign():
    """
    class should not be frozen
    """
    c = Category('name', None)
    c.name = 'test'
    c.pk = 1
    assert c.name == 'test'
    assert c.pk == 1

def test_eq():
    """
    class should implement __eq__ method
    """
    c1 = Category(name='name', parent=1, pk=2)
    c2 = Category(name='name', parent=1, pk=2)
    assert c1 == c2

def test_get_parent(cat_repo):
    c = Category('name', 1)
    parent_category = Category('parent', None)
    cat_repo.get.return_value = parent_category
    assert c.get_parent(cat_repo) == parent_category



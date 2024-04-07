from ...bookkeeper.repository.abstract_repository import AbstractRepository
import pytest

def test_cannot_create_abstract_repository():
    """
    Test that it's not possible to instantiate the AbstractRepository directly.
    """
    with pytest.raises(TypeError):
        AbstractRepository()

def test_can_create_sublclass():
    """
    Test that a subclass of AbstractRepository can be created.
    """
    class TestRepository(AbstractRepository):
        def add(self, obj):
            pass

        def get(self, pk):
            pass

        def get_all(self, where=None):
            pass

        def update(self, obj):
            pass

        def delete(self, pk):
            pass

    t = TestRepository()
    assert isinstance(t, AbstractRepository)

def test_add_method_is_abstract():
    """
    Test that add method is abstract in AbstractRepository.
    """
    with pytest.raises(TypeError):
        AbstractRepository().add(None)

def test_get_method_is_abstract():
    """
    Test that get method is abstract in AbstractRepository.
    """
    with pytest.raises(TypeError):
        AbstractRepository().get(1)

def test_get_all_method_is_abstract():
    """
    Test that get_all method is abstract in AbstractRepository.
    """
    with pytest.raises(TypeError):
        AbstractRepository().get_all()

def test_update_method_is_abstract():
    """
    Test that update method is abstract in AbstractRepository.
    """
    with pytest.raises(TypeError):
        AbstractRepository().update(None)

def test_delete_method_is_abstract():
    """
    Test that delete method is abstract in AbstractRepository.
    """
    with pytest.raises(TypeError):
        AbstractRepository().delete(1)

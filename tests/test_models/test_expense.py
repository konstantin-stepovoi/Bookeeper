from ...bookkeeper.models.expense import Expense
from ...bookkeeper.repository.memory_repository import MemoryRepository
from datetime import datetime
import pytest
from unittest.mock import Mock
from ...bookkeeper.repository.abstract_repository import AbstractRepository

@pytest.fixture
def expenses_repo():
    """
    Fixture for creating a mock expenses repository.
    """
    mock_repo = Mock(spec=AbstractRepository)
    # Mocking the behavior of add method
    mock_expenses = [
        Expense(expense_date=datetime(2024, 4, 1), amount=100, category=1, pk = 1),
        Expense(expense_date=datetime(2024, 4, 2), amount=200, category=1, pk = 2),
        Expense(expense_date=datetime(2024, 4, 4), amount=300, category=1, pk = 3)]
    mock_repo.add.side_effect = lambda item: max((ex.pk for ex in mock_expenses), default=-1) + 1
    return mock_repo


def test_create_with_full_args_list():
    e = Expense(amount=100,
    category=1,
    expense_date=datetime.now(), added_date=datetime.now(),
    comment='test', pk=1)
    assert e.amount == 100
    assert e.category == 1
    
def test_can_add_to_repo(expenses_repo):
    e = Expense(100, 1)
    pk = expenses_repo.add(e)
    assert pk == 4
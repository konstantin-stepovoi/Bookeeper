import pytest
from unittest.mock import Mock
from ...bookkeeper.models.budget import Budget
from ...bookkeeper.repository.abstract_repository import AbstractRepository
from ...bookkeeper.models.expense import Expense
import datetime

@pytest.fixture
def expenses_repo():
    """
    Fixture for creating a mock expenses repository.
    """
    mock_repo = Mock(spec=AbstractRepository)
    # Mocking the behavior of get_all method
    mock_expenses = [
        Expense(expense_date=datetime.datetime(2024, 4, 1), amount=100, category=1),
        Expense(expense_date=datetime.datetime(2024, 4, 2), amount=200, category=1),
        Expense(expense_date=datetime.datetime(2024, 4, 4), amount=300, category=1)]
    mock_repo.get_all.return_value = mock_expenses
    return mock_repo

def test_update_spent_sum_day(expenses_repo):
    """
    Test update_spent_sum method for 'Day' period.
    """
    budget = Budget()
    budget.time = 'Day'
    budget.budget = 1000
    spent_difference = budget.update_spent_sum(expenses_repo)
    assert spent_difference == 1000
    
def test_update_spent_sum_week(expenses_repo):
    """
    Test update_spent_sum method for 'Week' period.
    """
    budget = Budget()
    budget.time = 'Week'
    budget.budget = 1000
    spent_difference = budget.update_spent_sum(expenses_repo)
    assert spent_difference == 400  # Same as above, since all expenses are within the same week

def test_update_spent_sum_month(expenses_repo):
    """
    Test update_spent_sum method for 'Month' period.
    """
    budget = Budget()
    budget.time = 'Month'
    budget.budget = 1000
    spent_difference = budget.update_spent_sum(expenses_repo)
    assert spent_difference == 400

def test_update_spent_sum_empty(expenses_repo):
    """
    Test update_spent_sum method for 'Empty' period.
    """
    budget = Budget(time='Empty', budget=1000)
    spent_difference = budget.update_spent_sum(expenses_repo)
    assert spent_difference == 0  


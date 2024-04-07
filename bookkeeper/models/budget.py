from dataclasses import dataclass
from repository.abstract_repository import AbstractRepository
from models.expense import Expense
import utils


@dataclass
class Budget:

    """
    This is a model of user's budget
    it contains time, which can be
    [day, week, month, None]
    (period when U did buings)
    sum - spent money
    budget - free money U have
    pk - key
    """
    time: str = "Empty"
    spent_sum: float = 0
    budget: float = 0
    pk: int = 0

    def __init__(self,
                 pk: int = 0,
                 time: str = 'Empty',
                 spent_sum: float = 0,
                 budget: float = 0):
        if time not in ['Day', 'Week', 'Month', 'Empty']:
            raise ValueError('Unknown period type!!!1!')

    def update_spent_sum(
        self, expenses_repo: AbstractRepository[Expense]
    ) -> float:

        """
        Обновляет сумму расходов в бюджете.

        Args:
            expenses_repo (AbstractRepository[Expense]): Репозиторий расходов.

        Returns:
            float: Разница между бюджетом и суммой расходов.
        """

        expenses_list = expenses_repo.get_all()
        for exp in expenses_list:
            pure_date = str(exp.expense_date).split()[0]
            year, month, day = pure_date.split("-")

            if utils.date_is_in_range(self.time, year, month, day):
                self.spent_sum += float(exp.amount)
        return self.budget - self.spent_sum

from PySide6 import QtWidgets
from view.expense_tracker import ExpenseTracker
from view.categories_tracker import CategoryApp
from view.budget_app import BudgetApp
from repository.memory_repository import MemoryRepository
from models.category import Category
from models.expense import Expense


class MainApp(QtWidgets.QWidget):
    """
    Основной виджет приложения,
    управляющий редакторами расходов,
    категорий и бюджета.
    """
    def __init__(self):
        super().__init__()
        self.expense_repo = MemoryRepository[Expense](
            'ExpMemo',
            "bookkeeper.db")
        self.category_repo = MemoryRepository[Category](
            'CatMemo', "bookkeeper.db")
        self.setWindowTitle('Main Application')
        self.resize(500, 100)
        self.category_app = CategoryApp(self)
        self.expense_tracker = ExpenseTracker(self)
        self.budget_app = BudgetApp(self)
        self.init_ui()

    def init_ui(self) -> None:
        """
        Инициализация пользовательского
        интерфейса с кнопками
        для открытия различных редакторов.
        """
        layout = QtWidgets.QVBoxLayout(self)
        self.expense_button = QtWidgets.QPushButton("Редактор расходов")
        self.category_button = QtWidgets.QPushButton("Редактор категорий")
        self.budget_button = QtWidgets.QPushButton("Проверялка бюджета")
        self.saveandclose_button = QtWidgets.QPushButton("Сохранить данные")
        self.expense_button.clicked.connect(self.open_expense_tracker)
        self.category_button.clicked.connect(self.open_category_app)
        self.budget_button.clicked.connect(self.open_budget_app)
        self.saveandclose_button.clicked.connect(self.save_and_close)
        layout.addWidget(self.expense_button)
        layout.addWidget(self.category_button)
        layout.addWidget(self.budget_button)
        layout.addWidget(self.saveandclose_button)

    def open_category_app(self) -> None:
        """ Открыть окно редактора категорий. """
        self.category_app.show()
        self.hide()

    def open_expense_tracker(self) -> None:
        """ Открыть окно отслеживания расходов. """
        self.expense_tracker.show()
        self.hide()

    def open_budget_app(self) -> None:
        """ Открыть окно редактора бюджета. """
        self.budget_app.show()
        self.hide()

    def save_and_close(self) -> None:
        """ Сохранить изменения в репозиторий """
        self.expense_repo.copy_to_sqlite()
        self.category_repo.copy_to_sqlite()
        QtWidgets.QMessageBox.warning(
            self,
            "Готово",
            f"Данные сохранены в ПЗУ",
            QtWidgets.QMessageBox.Ok)

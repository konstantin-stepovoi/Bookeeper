from PySide6 import QtWidgets
from models.budget import Budget


class BudgetApp(QtWidgets.QMainWindow):
    """
    Окно субприложения для управления бюджетом.
    """
    def __init__(self, main_app) -> None:
        """
        Инициализация окна управления бюджетом.

        Args:
            main_app (QtWidgets.QWidget): Основное приложение.
        """
        super().__init__()
        self.setWindowTitle('Личный Счетовод')
        self.main_app = main_app
        self.setFixedSize(200, 150)
        layout = QtWidgets.QVBoxLayout()

        # определяем 2 кнопки для старта:
        self.add_button = QtWidgets.QPushButton("Новая проверка")
        self.back_button = QtWidgets.QPushButton("Назад")

        # подключаем кнопки к слотам
        self.add_button.clicked.connect(self.add_budget)
        self.back_button.clicked.connect(self.go_back)

        layout.addWidget(self.add_button)
        layout.addWidget(self.back_button)

        # устанавливаем макет для главного окна
        central_widget = QtWidgets.QWidget()
        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)

    def go_back(self) -> None:
        """
        Вернуться к главному окну.
        """
        self.hide()
        self.main_app.show()

    def add_budget(self) -> None:
        """
        Создаёт новый объект
        класса Budget согласно тому
        что пользователь ввёл
        """
        self.budget_input_widget = BudgetInputWidget(
            self.main_app, self
        )
        self.setCentralWidget(
            self.budget_input_widget
        )

    def handle_budget_creation(self, budget) -> None:
        """
        Обработать создание бюджета.

        Args:
            budget(Budget):
            Бюджет, созданный пользователем выше
        """
        expenses_repo = self.main_app.expense_repo
        result = budget.update_spent_sum(expenses_repo)
        if result > 0:
            QtWidgets.QMessageBox.warning(
                self,
                "Всё круто",
                f"У вас осталось {result} денег",
                QtWidgets.QMessageBox.Ok)
        elif result < 0:
            QtWidgets.QMessageBox.warning(
                self,
                "Превышение плана",
                f"ваш дефицит {-result} денег",
                QtWidgets.QMessageBox.Ok)
        else:
            QtWidgets.QMessageBox.warning(
                self,
                "Тютелька в тютельку",
                f"Вы уложились точно в бюджет",
                QtWidgets.QMessageBox.Ok)
        self.go_back()


class BudgetInputWidget(QtWidgets.QWidget):
    """
    Виджет для ввода информации о бюджете.
    """
    def __init__(self, main_app, parent=None):
        """
        Инициализация виджета
        для ввода информации о бюджете.

        Args:
            main_app(QtWidgets.QWidget):
            Основное приложение.
            parent: Родительский виджет.
        """
        super().__init__(parent)
        self.main_app = main_app
        layout = QtWidgets.QVBoxLayout()

        self.period_label = QtWidgets.QLabel(
            "Период планирования:"
        )
        self.period_combobox = QtWidgets.QComboBox()
        self.period_combobox.addItems(
            ['Empty', 'Day', 'Week', 'Month']
        )
        self.amount_label = QtWidgets.QLabel("Сумма трат:")
        self.amount_input = QtWidgets.QLineEdit()
        self.amount_input.setText('0')
        self.submit_button = QtWidgets.QPushButton("Готово")
        self.submit_button.clicked.connect(
            self.create_budget
        )
        layout.addWidget(self.period_label)
        layout.addWidget(self.period_combobox)
        layout.addWidget(self.amount_label)
        layout.addWidget(self.amount_input)
        layout.addWidget(self.submit_button)
        self.setLayout(layout)

    def create_budget(self) -> None:
        """
        Создать бюджет на основе введенной информации.
        """
        period = self.period_combobox.currentText()
        amount = float(self.amount_input.text())
        budg = Budget(time=period, budget=float(amount))
        budg.time = period
        budg.budget = float(amount)
        self.parent().handle_budget_creation(budg)

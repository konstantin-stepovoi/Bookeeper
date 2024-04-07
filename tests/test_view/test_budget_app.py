import pytest
from PySide6 import QtWidgets
from ...bookkeeper.view.budget_app import BudgetApp, BudgetInputWidget
from ...bookkeeper.models.budget import Budget
from unittest.mock import MagicMock, Mock
from PySide6.QtWidgets import QApplication
import sys


@pytest.fixture
def app():
    app = QApplication.instance()
    if not app:
        app = QApplication(sys.argv)  # Создать QApplication только в случае его отсутствия
    yield app



def test_budget_app_show(app):
    if not QApplication.instance():
        app = QApplication(sys.argv)  # Создать QApplication только в случае его отсутствия

    main_app = QApplication.instance()
    budget_app = BudgetApp(main_app)
    budget_app.show()
    assert budget_app.isVisible()
    
def test_go_back(app):
    main_app = Mock()
    budget_app = BudgetApp(main_app)
    
    budget_app.go_back()
    assert not budget_app.isVisible()
    assert main_app.show.called

def test_handle_budget_creation(app):
    main_app = Mock()
    budget_app = BudgetApp(main_app)
    
    budget = Mock()
    budget.update_spent_sum.return_value = 10
    budget_app.handle_budget_creation(budget)
    
    assert not budget_app.isVisible()
    assert main_app.show.called

@pytest.fixture
def budget_input_widget(qtbot):
    widget = BudgetInputWidget(QtWidgets.QWidget())
    qtbot.addWidget(widget)
    return widget


def test_budget_input_widget_initial_state(budget_input_widget):
    assert budget_input_widget.period_combobox.currentText() == 'Empty'
    assert budget_input_widget.amount_input.text() == '0'


def test_budget_input_widget_create_budget(qtbot, budget_input_widget):
    main_app = Mock()
    budget_app = BudgetApp(main_app)
    period = 'Week'
    amount = '500.00'

    # Устанавливаем значения в полях
    budget_input_widget.period_combobox.setCurrentText(period)
    budget_input_widget.amount_input.setText(amount)

    # Вызываем метод click для кнопки "Готово"
    budget_input_widget.submit_button.click()

    assert not budget_input_widget.submit_button.connect == 1

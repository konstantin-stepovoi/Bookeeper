import pytest
from PySide6 import QtWidgets, QtCore
from ...bookkeeper.view.Main_window import MainApp
from ...bookkeeper.view.expense_tracker import ExpenseTracker
from ...bookkeeper.view.categories_tracker import CategoryApp
from ...bookkeeper.view.budget_app import BudgetApp
from ...bookkeeper.repository.memory_repository import MemoryRepository
from ...bookkeeper.models.category import Category
from ...bookkeeper.models.expense import Expense
from unittest.mock import MagicMock
from pytestqt import qtbot

@pytest.fixture
def main_app():
    return MainApp()

def test_main_app_init(main_app):
    assert isinstance(main_app.expense_repo, MemoryRepository)
    assert isinstance(main_app.category_repo, MemoryRepository)
    assert main_app.windowTitle() == 'Main Application'
    assert main_app.layout().count() == 4
    assert isinstance(main_app.category_app, CategoryApp)
    assert isinstance(main_app.expense_tracker, ExpenseTracker)
    assert isinstance(main_app.budget_app, BudgetApp)

def test_main_app_init_ui(main_app):
    assert main_app.layout().count() == 4
    assert isinstance(main_app.expense_button, QtWidgets.QPushButton)
    assert isinstance(main_app.category_button, QtWidgets.QPushButton)
    assert isinstance(main_app.budget_button, QtWidgets.QPushButton)
    assert isinstance(main_app.saveandclose_button, QtWidgets.QPushButton)
    assert main_app.expense_button.text() == 'Редактор расходов'
    assert main_app.category_button.text() == 'Редактор категорий'
    assert main_app.budget_button.text() == 'Проверялка бюджета'
    assert main_app.saveandclose_button.text() == 'Сохранить данные'

def test_main_app_open_category_app(main_app):
    main_app.category_app.show = MagicMock()
    main_app.hide = MagicMock()
    main_app.open_category_app()
    main_app.category_app.show.assert_called_once()
    main_app.hide.assert_called_once()

def test_main_app_open_expense_tracker(main_app):
    main_app.expense_tracker.show = MagicMock()
    main_app.hide = MagicMock()
    main_app.open_expense_tracker()
    main_app.expense_tracker.show.assert_called_once()
    main_app.hide.assert_called_once()

def test_main_app_open_budget_app(main_app):
    main_app.budget_app.show = MagicMock()
    main_app.hide = MagicMock()
    main_app.open_budget_app()
    main_app.budget_app.show.assert_called_once()
    main_app.hide.assert_called_once()

def test_main_app_save_and_close(main_app):
    main_app.expense_repo.copy_to_sqlite = MagicMock()
    main_app.category_repo.copy_to_sqlite = MagicMock()
    QtWidgets.QMessageBox.warning = MagicMock()
    main_app.save_and_close()
    main_app.expense_repo.copy_to_sqlite.assert_called_once()
    main_app.category_repo.copy_to_sqlite.assert_called_once()
    QtWidgets.QMessageBox.warning.assert_called_once()

def test_main_app_expense_button_clicked(main_app, qtbot):
    qtbot.mouseClick(main_app.expense_button, QtCore.Qt.LeftButton)
    assert main_app.expense_tracker.isVisible()

def test_main_app_category_button_clicked(main_app, qtbot):
    qtbot.mouseClick(main_app.category_button, QtCore.Qt.LeftButton)
    assert main_app.category_app.isVisible()

def test_main_app_budget_button_clicked(main_app, qtbot):
    qtbot.mouseClick(main_app.budget_button, QtCore.Qt.LeftButton)
    assert main_app.budget_app.isVisible()

def test_main_app_save_and_close_button_clicked(main_app, qtbot):
    main_app.expense_repo.copy_to_sqlite = MagicMock()
    main_app.category_repo.copy_to_sqlite = MagicMock()
    QtWidgets.QMessageBox.warning = MagicMock()

    qtbot.mouseClick(main_app.saveandclose_button, QtCore.Qt.LeftButton)

    main_app.expense_repo.copy_to_sqlite.assert_called_once()
    main_app.category_repo.copy_to_sqlite.assert_called_once()
    QtWidgets.QMessageBox.warning.assert_called_once()

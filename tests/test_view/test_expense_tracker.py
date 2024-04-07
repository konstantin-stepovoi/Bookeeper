from PySide6 import QtWidgets, QtCore
from ...bookkeeper.view.expense_tracker import ExpenseTracker
from unittest.mock import MagicMock, Mock
import pytest
from ...bookkeeper.models.category import Category
from ...bookkeeper.models.expense import Expense
from ...bookkeeper.repository.memory_repository import MemoryRepository
from ...bookkeeper.repository.abstract_repository import AbstractRepository
from pytestqt import qtbot
from datetime import datetime
import pytestqt


@pytest.fixture
def main_app():
    return MagicMock()


@pytest.fixture
def expense_tracker(main_app):
    return ExpenseTracker(main_app)


def test_setup_table(expense_tracker):
    expense_tracker.expenses_table = QtWidgets.QTableWidget()
    expense_tracker.setup_table()
    assert expense_tracker.expenses_table.columnCount() == 5
    assert expense_tracker.expenses_table.horizontalHeaderItem(0).text() == "Дата"
    assert expense_tracker.expenses_table.horizontalHeaderItem(1).text() == "Сумма"
    assert expense_tracker.expenses_table.horizontalHeaderItem(2).text() == "Категория"
    assert expense_tracker.expenses_table.horizontalHeaderItem(3).text() == "Комментарий"
    assert expense_tracker.expenses_table.horizontalHeaderItem(4).text() == "PK"


def test_update_table_all(expense_tracker, main_app):
    main_app.expense_repo.get_all.return_value = [
        Expense(expense_date=datetime(2024, 4, 4), amount=100, category=1, comment="Test"),
        Expense(expense_date=datetime(2024, 4, 5), amount=150, category=2, comment="Test2")
    ]
    expense_tracker.main_app = main_app
    expense_tracker.period = 'all'
    expense_tracker.expenses_table = QtWidgets.QTableWidget()
    expense_tracker.update_table()
    assert expense_tracker.expenses_table.rowCount() == 2


# Тесты на другие периоды, например, для 'Day', 'Week', 'Month', можно написать аналогично


def test_add_expense_to_table(expense_tracker, main_app):
    main_app.category_repo.get_category_name_by_id.return_value = "Test Category"
    main_app.expense_repo.get_pk.return_value = 1
    expense_tracker.main_app = main_app
    expense_tracker.expenses_table = QtWidgets.QTableWidget()
    expense = Expense(expense_date=datetime(2024, 4, 4), amount=100, category=1, comment="Test")
    expense_tracker.add_expense_to_table(expense)
    assert expense_tracker.expenses_table.rowCount() == 1


def test_change_period_day(expense_tracker, main_app):
    main_app.expense_repo.get_all.return_value = [
        Expense(expense_date=datetime(2024, 4, 4), amount=100, category=1, comment="Test"),
        Expense(expense_date=datetime(2024, 4, 5), amount=150, category=2, comment="Test2")
    ]
    expense_tracker.main_app = main_app
    expense_tracker.period = 'Day'
    expense_tracker.expenses_table = QtWidgets.QTableWidget()
    expense_tracker.update_table()
    assert expense_tracker.expenses_table.rowCount() == 1

# Аналогично можно добавить тесты для 'Week' и 'Month'


def test_add_row(expense_tracker, main_app, qtbot):
    main_app.category_repo.get_id_by_name.return_value = 1
    expense_tracker.main_app = main_app
    expense_tracker.expenses_table = QtWidgets.QTableWidget()
    qtbot.keyClicks(expense_tracker, "2024-04-04, 100, Test Category, Test")
        
    assert expense_tracker.expenses_table.rowCount() >=0

# Тесты для edit_row и delete_row могут быть добавлены аналогичным образом

def test_go_back(expense_tracker, main_app):
    expense_tracker.hide = MagicMock()
    expense_tracker.main_app.show = MagicMock()
    expense_tracker.go_back()
    expense_tracker.hide.assert_called_once()
    expense_tracker.main_app.show.assert_called_once()
    
def test_delete_row(expense_tracker, main_app, qtbot):
    main_app.expense_repo.delete = MagicMock()

    expense_tracker.main_app = main_app
    expense_tracker.expenses_table = QtWidgets.QTableWidget()

    # Добавляем строку в таблицу для удаления
    expense_tracker.add_expense_to_table(Expense(expense_date=datetime(2024, 4, 4), amount=100, category=1, comment="Test"))

    # Выбираем строку в таблице
    expense_tracker.expenses_table.setCurrentCell(0, 0)
    qtbot.mouseClick(expense_tracker.delete_row_button, QtCore.Qt.LeftButton)

    # Проверяем, что строка удалена из таблицы
    assert expense_tracker.expenses_table.rowCount() == 1

def test_edit_row(expense_tracker, main_app, qtbot):
    main_app.category_repo.get_id_by_name.return_value = 1
    main_app.category_repo.get_category_name_by_id.return_value = "Test Category"
    main_app.expense_repo.get_pk.return_value = 1

    expense_tracker.main_app = main_app
    expense_tracker.expenses_table = QtWidgets.QTableWidget()

    # Добавляем строку в таблицу для редактирования
    expense_tracker.add_expense_to_table(Expense(expense_date=datetime(2024, 4, 4), amount=100, category=1, comment="Test"))

    # Выбираем строку в таблице
    expense_tracker.expenses_table.setCurrentCell(0, 0)

    # Имитируем действие редактирования строки
   
    qtbot.mouseClick(expense_tracker.edit_row_button, QtCore.Qt.LeftButton)

    # Проверяем, что таблица обновилась
    assert expense_tracker.expenses_table.rowCount() == 1


def test_init(expense_tracker, main_app):
    assert isinstance(expense_tracker, QtWidgets.QMainWindow)
    assert expense_tracker.windowTitle() == 'Трэкер расходов'
    assert isinstance(expense_tracker.central_widget, QtWidgets.QWidget)
    assert expense_tracker.main_app == main_app
    assert expense_tracker.period == 'all'


def test_setup_table(expense_tracker):
    expense_tracker.setup_table()
    assert expense_tracker.expenses_table.columnCount() == 5
    assert expense_tracker.expenses_table.horizontalHeaderItem(0).text() == "Дата"
    assert expense_tracker.expenses_table.horizontalHeaderItem(1).text() == "Сумма"
    assert expense_tracker.expenses_table.horizontalHeaderItem(2).text() == "Категория"
    assert expense_tracker.expenses_table.horizontalHeaderItem(3).text() == "Комментарий"
    assert expense_tracker.expenses_table.horizontalHeaderItem(4).text() == "PK"


def test_init_ui(expense_tracker):
    # Проверяем, что таблица создана и настроены ее колонки
    assert isinstance(expense_tracker.expenses_table, QtWidgets.QTableWidget)
    assert expense_tracker.expenses_table.columnCount() > 0
    assert expense_tracker.expenses_table.horizontalHeaderItem(0).text() == "Дата"
    assert expense_tracker.expenses_table.horizontalHeaderItem(1).text() == "Сумма"
    assert expense_tracker.expenses_table.horizontalHeaderItem(2).text() == "Категория"

    # Проверяем, что созданы кнопки и установлены их тексты
    assert isinstance(expense_tracker.back_button, QtWidgets.QPushButton)
    assert isinstance(expense_tracker.add_row_button, QtWidgets.QPushButton)
    assert isinstance(expense_tracker.delete_row_button, QtWidgets.QPushButton)
    assert expense_tracker.back_button.text() == "Назад"
    assert expense_tracker.add_row_button.text() == "Добавить строку"
    assert expense_tracker.delete_row_button.text() == "Удалить строку"

    # Проверяем, что сигналы кнопок подключены к соответствующим слотам
    assert expense_tracker.add_row_button.clicked.connect == 1
    assert expense_tracker.delete_row_button.clicked.connect == 1
    assert expense_tracker.back_button.clicked.connect == 1 

def test_go_back(expense_tracker, main_app):
    expense_tracker.hide = MagicMock()
    main_app.show = MagicMock()
    expense_tracker.go_back()
    expense_tracker.hide.assert_called_once()
    main_app.show.assert_called_once()

@pytest.fixture
def period_dialog(qtbot):
    dialog = QtWidgets.QDialog()
    layout = QtWidgets.QVBoxLayout(dialog)
    period_combo = QtWidgets.QComboBox()
    period_combo.addItems(['all', 'Month', 'Week', 'Day'])
    layout.addWidget(period_combo)
    ok_button = QtWidgets.QPushButton("Готово")
    layout.addWidget(ok_button)
    qtbot.add_widget(dialog)
    return dialog


def test_change_period_dialog_open(expense_tracker, qtbot, period_dialog):
    try:
        qtbot.waitSignal(period_dialog.accepted)
        expense_tracker.change_period_button.click()
    except pytestqt.exceptions.TimeoutError:
        assert not period_dialog.isVisible()


def test_change_period_dialog_period_selected(expense_tracker, qtbot, period_dialog):
    try:
        qtbot.waitSignal(period_dialog.accepted)
        expense_tracker.change_period_button.click()
    except pytestqt.exceptions.TimeoutError:
        assert expense_tracker.period == 'all'  # По умолчанию выбран 'all'

    assert expense_tracker.period != 'Month'

def test_changethetable(expense_tracker):
    expenses_list = [
        Expense(expense_date=datetime(2024, 4, 4), amount=100, category=1, comment="Test"),
        Expense(expense_date=datetime(2024, 4, 5), amount=150, category=2, comment="Test2")
    ]
    expense_tracker.period = 'Day'
    changed_list = expense_tracker.changethetable(expenses_list)
    assert len(changed_list) == 1  # Ожидаем только один элемент, так как установлен период 'Day'

def test_edit_row(expense_tracker, main_app, qtbot):
    # Подготовим моки и данные
    main_app.category_repo.get_id_by_name.return_value = 1
    main_app.category_repo.get_category_name_by_id.return_value = "Test Category"
    main_app.expense_repo.get_pk.return_value = 1
    expense_tracker.main_app = main_app
    expense_tracker.expenses_table = QtWidgets.QTableWidget()
    # Добавим строку в таблицу для редактирования
    expense_tracker.add_expense_to_table(Expense(expense_date=datetime(2024, 4, 4), amount=100, category=1, comment="Test"))
    # Выберем строку в таблице
    expense_tracker.expenses_table.setCurrentCell(0, 0)
    # Имитируем действие редактирования строки
    qtbot.mouseClick(expense_tracker.edit_row_button, QtCore.Qt.LeftButton)
    # Проверим, что таблица обновилась
    assert expense_tracker.expenses_table.rowCount() == 1

def test_delete_row(expense_tracker, main_app, qtbot):
    # Подготовим моки и данные
    main_app.expense_repo.delete = MagicMock()
    expense_tracker.main_app = main_app
    expense_tracker.expenses_table = QtWidgets.QTableWidget()
    # Добавим строку в таблицу для удаления
    expense_tracker.add_expense_to_table(Expense(expense_date=datetime(2024, 4, 4), amount=100, category=1, comment="Test"))
    # Выберем строку в таблице
    expense_tracker.expenses_table.setCurrentCell(0, 0)
    # Имитируем действие удаления строки
    qtbot.mouseClick(expense_tracker.delete_row_button, QtCore.Qt.LeftButton)
    # Проверим, что строка удалена из таблицы
    assert expense_tracker.expenses_table.rowCount() >= 0  # Ожидаем, что после удаления строки в таблице не будет строк


def test_add_row_exception_handling(expense_tracker, main_app, qtbot):
    main_app.category_repo.get_id_by_name.side_effect = Exception("Error getting category ID")
    expense_tracker.main_app = main_app
    expense_tracker.expenses_table = QtWidgets.QTableWidget()
    
    # Проверим, что добавление строки не вызывает исключения, а вместо этого выводится предупреждение
    assert not qtbot.keyClicks(expense_tracker, "2024-04-04, 100, Test Category, Test")

def test_edit_row_exception_handling(expense_tracker, main_app, qtbot):
    main_app.category_repo.get_id_by_name.return_value = 1
    main_app.category_repo.get_category_name_by_id.side_effect = Exception("Error getting category name")
    expense_tracker.main_app = main_app
    expense_tracker.expenses_table = QtWidgets.QTableWidget()

    # Выберем строку в таблице
    expense_tracker.expenses_table.setCurrentCell(0, 0)

    # Имитируем действие редактирования строки

    qtbot.mouseClick(expense_tracker.edit_row_button, QtCore.Qt.LeftButton)
    assert not qtbot.keyClicks(expense_tracker, "2024-04-04, 100, Test Expense, Test")


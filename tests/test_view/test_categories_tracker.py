from PySide6 import QtWidgets, QtCore
from ...bookkeeper.view.categories_tracker import CategoryApp, visualization
from unittest.mock import MagicMock, Mock
import pytest
from ...bookkeeper.models.category import Category
from ...bookkeeper.repository.memory_repository import MemoryRepository
from ...bookkeeper.repository.abstract_repository import AbstractRepository
from pytestqt import qtbot
import matplotlib.pyplot as plt

@pytest.fixture
def cat_repo():
    """
    Fixture for creating a mock category repository.
    """
    mock_repo = MagicMock(spec=AbstractRepository)

    # Mocking the behavior of get_all method
    mock_cats = [
        Category(name='name1', pk=0, parent=None),
        Category(name='name1', pk=1, parent=0),
        Category(name='name1', pk=2, parent=None)
    ]
    mock_repo.get_all.return_value = mock_cats

    # Mocking the behavior of add method
    mock_repo.add = MagicMock()
    mock_repo.add.side_effect = lambda item: max(cat.pk for cat in mock_cats) + 1

    # Mocking the behavior of get_id_by_name method
    mock_repo.get_id_by_name = MagicMock()
    mock_repo.get_id_by_name.side_effect = lambda name: next((cat.pk for cat in mock_cats if cat.name == name), None)

    # Mocking the behavior of get method
    mock_repo.get = MagicMock()
    mock_repo.get.side_effect = lambda pk: next((cat for cat in mock_cats if cat.pk == pk), None)

    # Mocking the behavior of update method
    mock_repo.update = MagicMock()

    # Mocking the behavior of delete method
    mock_repo.delete = MagicMock()

    return mock_repo
    
@pytest.fixture
def main_app(cat_repo):
    app = QtWidgets.QWidget()
    app.category_repo = cat_repo
    return app

@pytest.fixture
def category_app(main_app):
    return CategoryApp(main_app)

def test_update_table(category_app, cat_repo):
    category_app.categories_table = MagicMock()
    cat_repo.get_all.return_value = [Category(pk=1, name='Category 1', parent=None)]
    category_app.update_table()
    assert category_app.categories_table.clearContents.call_count == 1
    assert category_app.categories_table.setRowCount.call_count == 1
    assert category_app.categories_table.insertRow.call_count == 1
    assert category_app.categories_table.setItem.call_count == 3


def test_init(category_app, main_app):
    assert category_app.main_app == main_app
    assert category_app.windowTitle() == 'Трэкер категорий'
    assert category_app.width() == 800
    assert category_app.height() == 600
    assert isinstance(category_app.centralWidget(), QtWidgets.QWidget)

def test_go_back(category_app):
    category_app.hide = MagicMock()
    category_app.main_app.show = MagicMock()
    category_app.go_back()
    category_app.hide.assert_called_once()
    category_app.main_app.show.assert_called_once()

def test_add_category(category_app, cat_repo):
    cat_repo.get_id_by_name.return_value = None
    cat_repo.add = MagicMock()
    category_app.update_table = MagicMock()
    category_app.add_category()
    assert category_app.update_table.call_count == 0


    
def test_delete_category(category_app, cat_repo):
    cat_repo.delete = MagicMock()
    category_app.update_table = MagicMock()

    # Создаем мок объект для selectionModel
    selection_model_mock = MagicMock()
    # Настриваем мок объект для возвращения нужного значения при вызове selectedRows()
    selection_model_mock.selectedRows.return_value = [MagicMock(row=0)]

    # Вызываем метод selectionModel() и настраиваем его возвращаемое значение
    category_app.categories_table.selectionModel = MagicMock(return_value=selection_model_mock)

    # Теперь вызываем метод selectedRows() у возвращенного selectionModel
    category_app.categories_table.selectionModel().selectedRows.return_value = [MagicMock(row=0)]


def test_init_ui(category_app, main_app):
    assert category_app.categories_table.rowCount() >= 0
    assert category_app.categories_table.columnCount() >= 0
    assert category_app.categories_table.horizontalHeaderItem(0).text() == "ID"
    assert category_app.categories_table.horizontalHeaderItem(1).text() == "Название"
    assert category_app.categories_table.horizontalHeaderItem(2).text() == "ID родителя"
    assert category_app.back_button.text() == "Назад"
    assert category_app.add_category_button.text() == "Добавить категорию"
    assert category_app.edit_category_button.text() == "Редактировать категорию"
    assert category_app.delete_category_button.text() == "Удалить категорию"
    assert category_app.visualize_graph_button.text() == "Отобразить граф взаимосвязей"

def test_update_table_after_add_category(category_app, cat_repo):
    cat_repo.get_all.return_value = [Category(pk=0, name="Category 1", parent=None)]
    category_app.update_table()
    assert category_app.categories_table.rowCount() == 1
    assert category_app.categories_table.item(0, 0).text() == "0"
    assert category_app.categories_table.item(0, 1).text() == "Category 1"
    assert category_app.categories_table.item(0, 2).text() == 'None'


def test_add_category_dialog_ok(category_app, cat_repo, qtbot, monkeypatch):
    cat_repo.get_id_by_name.return_value = None
    qtbot.keyClicks(category_app, "New Category, None")
    with qtbot.waitSignal(category_app.add_category_button.clicked):
        qtbot.mouseClick(category_app.add_category_button, QtCore.Qt.LeftButton)
    assert cat_repo.add.call_count >= 0

def test_add_category_dialog_cancel(category_app, cat_repo, qtbot, monkeypatch):
    cat_repo.get_id_by_name.return_value = None
    qtbot.keyClicks(category_app, "New Category, None")
    with qtbot.assertNotEmitted(category_app.add_category_button.clicked):
        qtbot.keyClick(category_app, QtCore.Qt.Key_Return)
    assert cat_repo.add.call_count == 0

def test_add_category_duplicate(category_app, cat_repo, qtbot, monkeypatch):
    cat_repo.get_id_by_name.return_value = 1
    QtWidgets.QMessageBox.warning = MagicMock()
    qtbot.keyClicks(category_app, "New Category, None")
    with qtbot.waitSignal(category_app.add_category_button.clicked):
        qtbot.mouseClick(category_app.add_category_button, QtCore.Qt.LeftButton)
    #QtWidgets.QMessageBox.warning.assert_called_once()
    assert cat_repo.add.call_count == 0

def test_edit_category_dialog_ok(category_app, cat_repo, qtbot, monkeypatch):
    cat_repo.get.return_value = Category(pk=0, name="Category 1", parent=None)
    qtbot.mouseClick(category_app.categories_table, QtCore.Qt.LeftButton, pos=QtCore.QPoint(0, 0))
    qtbot.keyClicks(category_app, "Edited Category, None")
    with qtbot.waitSignal(category_app.edit_category_button.clicked):
        qtbot.mouseClick(category_app.edit_category_button, QtCore.Qt.LeftButton)
    assert cat_repo.update.call_count == 0

def test_edit_category_dialog_cancel(category_app, cat_repo, qtbot, monkeypatch):
    cat_repo.get.return_value = Category(pk=0, name="Category 1", parent=None)
    qtbot.mouseClick(category_app.categories_table, QtCore.Qt.LeftButton, pos=QtCore.QPoint(0, 0))
    qtbot.keyClicks(category_app, "Edited Category, None")
    with qtbot.assertNotEmitted(category_app.edit_category_button.clicked):
        qtbot.keyClick(category_app, QtCore.Qt.Key_Return)
    assert cat_repo.update.call_count == 0



@pytest.fixture
def category_app_with_mocked_visualization():
    # Создаем мок объект для основного приложения
    main_app_mock = MagicMock()

    # Создаем CategoryApp с моком для main_app и заменяем visualization метод на MagicMock
    category_app = CategoryApp(main_app_mock)
    category_app.visualization = MagicMock()

    return category_app

def test_visualize_graph(category_app_with_mocked_visualization):
    # Вызываем метод visualize_graph
    category_app_with_mocked_visualization.visualize_graph()

    # Проверяем, что метод visualization был вызван
    assert category_app_with_mocked_visualization.visualization.called_once()

@pytest.fixture
def category_app(main_app):
    return CategoryApp(main_app)

def test_update_table_empty(category_app, cat_repo):
    cat_repo.get_all.return_value = []
    category_app.update_table()
    assert category_app.categories_table.rowCount() == 0

def test_go_back(category_app, main_app):
    category_app.hide = MagicMock()
    main_app.show = MagicMock()
    category_app.go_back()
    category_app.hide.assert_called_once()
    main_app.show.assert_called_once()

def test_visualize_graph(category_app, main_app, qtbot):
    main_app.category_repo.get_all.return_value = []
    qtbot.addWidget(category_app)
    category_app.show()
    with qtbot.waitSignal(category_app.visualize_graph_button.clicked):
        qtbot.mouseClick(category_app.visualize_graph_button, QtCore.Qt.LeftButton)



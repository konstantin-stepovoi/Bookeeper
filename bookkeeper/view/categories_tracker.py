from PySide6 import QtWidgets
from models.category import Category
import networkx as nx
import matplotlib.pyplot as plt


def visualization(categories) -> None:
    """
    Визуализация графа взаимосвязей категорий.

    Args:
        categories (list[Category]): Список категорий.
    """
    G = nx.DiGraph()
    for category in categories:
        G.add_node(category.pk, label=category.name)
        if category.parent is not None:
            G.add_edge(category.parent, category.pk)
    pos = nx.circular_layout(G)
    labels = nx.get_node_attributes(G, 'label')
    plt.figure()
    nx.draw(G, pos,
            with_labels=True,
            labels=labels,
            node_color='skyblue',
            node_size=2000,
            font_size=10,
            font_weight='bold',
            arrows=True)
    plt.title('Граф взаимосвязей категорий')
    plt.show()


class CategoryApp(QtWidgets.QMainWindow):
    """
    Окно приложения для управления категориями.
    """
    def __init__(self, main_app) -> None:
        """
        Инициализация окна управления категориями.

        Args:
            main_app (QtWidgets.QWidget): Основное приложение.
        """

        super().__init__()
        self.main_app = main_app
        self.setWindowTitle('Трэкер категорий')
        self.resize(800, 600)
        self.central_widget = QtWidgets.QWidget()
        self.setCentralWidget(self.central_widget)
        self.init_ui()

    def go_back(self) -> None:
        """
        Вернуться к главному окну.
        """
        self.hide()
        self.main_app.show()

    def init_ui(self) -> None:
        """
        Инициализация пользовательского интерфейса.
        """
        # Создаем таблицу
        self.categories_table = QtWidgets.QTableWidget()
        self.categories_table.setColumnCount(3)
        self.categories_table.setHorizontalHeaderLabels(
            ["ID", "Название", "ID родителя"]
        )
        header = self.categories_table.horizontalHeader()
        header.setSectionResizeMode(QtWidgets.QHeaderView.Stretch)
        self.categories_table.setEditTriggers(
            QtWidgets.QAbstractItemView.NoEditTriggers
        )
        self.categories_table.verticalHeader().hide()
        self.update_table()
        vertical_layout = QtWidgets.QVBoxLayout(
            self.central_widget
        )
        vertical_layout.addWidget(self.categories_table)
        # Создаем кнопки
        self.back_button = QtWidgets.QPushButton("Назад")
        self.add_category_button = QtWidgets.QPushButton("Добавить категорию")
        self.edit_category_button = QtWidgets.QPushButton(
            "Редактировать категорию"
        )
        self.delete_category_button = QtWidgets.QPushButton(
            "Удалить категорию"
        )
        self.visualize_graph_button = QtWidgets.QPushButton(
            "Отобразить граф взаимосвязей"
        )
        # Подключаем сигналы к слотам
        self.add_category_button.clicked.connect(self.add_category)
        self.edit_category_button.clicked.connect(self.edit_category)
        self.delete_category_button.clicked.connect(
            self.delete_category)
        self.visualize_graph_button.clicked.connect(
            self.visualize_graph)
        self.back_button.clicked.connect(self.go_back)
        # Добавляем кнопки в макет
        vertical_layout.addWidget(
            self.add_category_button)
        vertical_layout.addWidget(
            self.edit_category_button)
        vertical_layout.addWidget(
            self.delete_category_button)
        vertical_layout.addWidget(
            self.visualize_graph_button)
        vertical_layout.addWidget(
            self.back_button)

    def update_table(self) -> None:
        """
        Обновить
        таблицу категорий
        (это надо чтобы отображать изменения после кликов)
        """
        self.categories_table.clearContents()
        self.categories_table.setRowCount(0)
        categories = self.main_app.category_repo.get_all()
        for category in categories:
            row_position = self.categories_table.rowCount()
            self.categories_table.insertRow(row_position)
            self.categories_table.setItem(
                row_position,
                0,
                QtWidgets.QTableWidgetItem(str(category.pk)))
            self.categories_table.setItem(
                row_position,
                1,
                QtWidgets.QTableWidgetItem(category.name))
            self.categories_table.setItem(
                row_position,
                2,
                QtWidgets.QTableWidgetItem(str(category.parent)))

    def visualize_graph(self) -> None:
        """
        Отобразить граф взаимосвязей категорий в отдельном окошке
        """
        categories = self.main_app.category_repo.get_all()
        visualization(categories)

    def add_category(self) -> None:
        """
        Добавить новую категорию в формате "имя, No. родителя"
        """
        text, ok = QtWidgets.QInputDialog.getText(
            self,
            'Добавить категорию',
            'Введите имя и Имя Родителя:'
        )
        if ok:
            try:
                name, parent = text.split(',')
            except ValueError:
                QtWidgets.QMessageBox.warning(
                    self,
                    'Ошибка',
                    'Ожидается два значения, разделенных запятой.'
                )
                return
            if not parent.strip():
                parent_id = None
            else:
                parent_id = self.main_app.category_repo.get_id_by_name(
                    parent.strip()
                )
            new_category = Category(
                name=name.strip(),
                parent=parent_id
            )
            existing_categories = self.main_app.category_repo.get_all()
            if any(
                cat.name == new_category.name
                and cat.parent == new_category.parent
                for cat in existing_categories
            ):
                QtWidgets.QMessageBox.warning(
                    self,
                    'Ошибка',
                    'Такая категория уже существует.'
                )
                return
            self.main_app.category_repo.add(
                new_category)
            self.update_table()

    def edit_category(self) -> None:
        """
        Редактировать категорию.
        """
        selected_rows = self.categories_table.selectionModel().selectedRows()
        if selected_rows:
            row = selected_rows[0].row()
            pk = int(self.categories_table.item(
                row, 0
            ).text())
            current_name = self.categories_table.item(
                row, 1
            ).text()
            current_parent_id = self.categories_table.item(
                row, 2
            ).text()
            text, ok = QtWidgets.QInputDialog.getText(
                self,
                'Редактировать категорию (род по ID)',
                'Введите новые данные через запятую:',
                text=f"{current_name}, {current_parent_id}"
            )
            if ok:
                try:
                    edited_category_data = text.split(',')
                    if len(edited_category_data) == 2:
                        name = edited_category_data[0].strip()
                        parent_id = edited_category_data[1].strip()
                        if not parent_id or parent_id == "None":
                            parent_id = None
                        else:
                            parent_id = int(parent_id)
                        if parent_id is not None:
                            parent_category = self.main_app.category_repo.get(
                                parent_id)
                            if parent_category is None:
                                QtWidgets.QMessageBox.warning(
                                    self,
                                    'Ошибка',
                                    'Родительская категория не существует.')
                                return
                        updated_category = Category(
                            name=name,
                            parent=parent_id,
                            pk=pk)
                        self.main_app.category_repo.update(
                            updated_category)
                        self.update_table()
                    else:
                        QtWidgets.QMessageBox.warning(
                            self,
                            'Ошибка',
                            'Неверное кол-во значений. Ожидается 2 значения.')
                except ValueError:
                    QtWidgets.QMessageBox.warning(
                        self,
                        'Ошибка',
                        'Неверный формат данных.')

    def delete_category(self) -> None:
        """
        Удалить категорию.
        """
        selected_rows = self.categories_table.selectionModel().selectedRows()
        if selected_rows:
            row = selected_rows[0].row()
            pk = int(self.categories_table.item(row, 0).text())  # Получаем pk
            self.main_app.category_repo.delete(pk)
            self.update_table()

from PySide6 import QtWidgets
from models.expense import Expense
import datetime
from models.category import Category
import utils


class ExpenseTracker(QtWidgets.QMainWindow):
    """
    Окно отслеживания расходов
    """
    def __init__(self, main_app) -> None:
        """
        Инициализация окна отслеживания расходов.

        Args:
            main_app(QtWidgets.QWidget):
            Основное приложение.
        """
        super().__init__()
        self.setWindowTitle('Трэкер расходов')
        self.central_widget = QtWidgets.QWidget()
        self.setCentralWidget(self.central_widget)
        self.main_app = main_app
        self.period = 'all'
        self.init_ui()

    def setup_table(self) -> None:
        """
        Настройка таблицы расходов.
        """
        self.expenses_table.setColumnCount(5)
        self.expenses_table.setHorizontalHeaderLabels(
            ["Дата", "Сумма", "Категория", "Комментарий", "PK"]
        )

    def init_ui(self) -> None:
        """
        Инициализация пользовательского интерфейса.
        """
        self.expenses_table = QtWidgets.QTableWidget()
        self.setup_table()  # Настройка таблицы
        self.expenses_table.setSelectionBehavior(
            QtWidgets.QAbstractItemView.SelectRows
        )
        self.expenses_table.setSelectionMode(
            QtWidgets.QAbstractItemView.SingleSelection
        )
        self.update_table()
        # Создаем вертикальный макет и добавляем таблицу в него
        vertical_layout = QtWidgets.QVBoxLayout(
            self.central_widget
        )
        vertical_layout.addWidget(
            self.expenses_table
        )

        # Создаем кнопки
        self.add_row_button = QtWidgets.QPushButton("Добавить строку")
        self.edit_row_button = QtWidgets.QPushButton("Редактировать строку")
        self.delete_row_button = QtWidgets.QPushButton("Удалить строку")
        self.change_period_button = QtWidgets.QPushButton("Выбрать период")
        self.back_button = QtWidgets.QPushButton("Назад")

        # Подключаем сигналы к слотам
        self.add_row_button.clicked.connect(self.add_row)
        self.edit_row_button.clicked.connect(self.edit_row)
        self.delete_row_button.clicked.connect(self.delete_row)
        self.back_button.clicked.connect(self.go_back)
        self.change_period_button.clicked.connect(self.change_period)

        # Добавляем кнопки в макет
        vertical_layout.addWidget(self.add_row_button)
        vertical_layout.addWidget(self.edit_row_button)
        vertical_layout.addWidget(self.delete_row_button)
        vertical_layout.addWidget(self.change_period_button)
        vertical_layout.addWidget(self.back_button)

    def change_period(self) -> None:
        """
        Отображает диалоговое окно для выбора периода.
        """
        period_dialog = QtWidgets.QDialog(self)
        period_dialog.setWindowTitle("Выберите период отображения")
        layout = QtWidgets.QVBoxLayout(period_dialog)
        period_combo = QtWidgets.QComboBox()
        period_combo.addItems(['all', 'Month', 'Week', 'Day'])
        layout.addWidget(period_combo)
        ok_button = QtWidgets.QPushButton("Готово")
        layout.addWidget(ok_button)
        ok_button.clicked.connect(period_dialog.accept)

        if period_dialog.exec_():
            self.period = period_combo.currentText()
            self.update_table()

    def update_table(self) -> None:
        """
        Обновление таблицы расходов после внесения изменений.
        """
        outer_expenses = self.main_app.expense_repo.get_all()
        self.expenses_table.setRowCount(0)
        for expense in outer_expenses:
            if isinstance(expense.expense_date, str):
                expense_date = datetime.datetime.strptime(
                    expense.expense_date,
                    '%Y-%m-%d %H:%M:%S')
            else:
                expense_date = expense.expense_date

            if self.period == 'all':
                self.add_expense_to_table(expense)
            else:
                this_year, this_month, this_day = map(
                    int, str(datetime.date.today()).split("-"))
                expense_year, expense_month, expense_day = map(
                    int, str(expense_date.date()).split("-"))
                if (self.period == 'Day'
                    and this_year == expense_year
                    and this_month == expense_month
                    and this_day == expense_day):
                    self.add_expense_to_table(expense)

                elif self.period == 'Week':
                    today_date = datetime.date(
                        this_year, this_month, this_day)
                    if isinstance(expense_date, datetime.datetime):
                        expense_date = expense_date.date()
                    week_start = today_date - datetime.timedelta(
                        days=today_date.weekday()
                    )
                    week_end = week_start + datetime.timedelta(days=6)
                    if week_start <= expense_date <= week_end:
                        self.add_expense_to_table(expense)
                elif (self.period == 'Month'
                      and this_year == expense_year
                      and this_month == expense_month):
                    self.add_expense_to_table(expense)

    def add_expense_to_table(self, expense: Expense) -> None:
        """
        Добавление расхода в таблицу.
        """
        row_position = self.expenses_table.rowCount()
        self.expenses_table.insertRow(row_position)
        self.expenses_table.setItem(
            row_position, 0,
            QtWidgets.QTableWidgetItem(
                str(str(expense.expense_date).split()[0])))
        self.expenses_table.setItem(
            row_position, 1,
            QtWidgets.QTableWidgetItem(
                str(expense.amount)))
        self.expenses_table.setItem(
            row_position, 2,
            QtWidgets.QTableWidgetItem(
                str(
                    self.main_app.category_repo.get_category_name_by_id(
                        expense.category
                    ))))
        self.expenses_table.setItem(
            row_position, 3,
            QtWidgets.QTableWidgetItem(expense.comment))
        self.expenses_table.setItem(
            row_position, 4,
            QtWidgets.QTableWidgetItem(
                str(self.main_app.expense_repo.get_pk(expense))))

    def changethetable(self, expenses_list):
        changed_list = []
        for exp in expenses_list:
            pure_date = str(
                exp.expense_date).split()[0]
            year, month, day = pure_date.split("-")
            if utils.date_is_in_range(
                self.period,
                year,
                month,
                day
            ):
                changed_list.append(exp)
        return changed_list

    def add_row(self) -> None:
        """
        Добавление новой строки расхода
        """
        text, ok = QtWidgets.QInputDialog.getText(
            self, 'Добавить покупку',
            'Введите данные через запятую:')
        if ok:
            date, amount, category_name, comment = (
                part.strip() for part in text.split(','))
            ctd = self.main_app.category_repo.get_id_by_name(
                category_name
            )
            category_id = ctd
            if category_id is None:
                new_category = Category(name=category_name, parent=None)
                self.main_app.category_repo.add(new_category)
                self.main_app.category_app.update_table()
                cad = self.main_app.category_repo.get_id_by_name(
                    category_name
                )
                category_id = cad

            # Преобразование даты
            expense_date = utils.reorder_time(date)
            new_expense = Expense(
                amount=int(amount),
                comment=comment,
                expense_date=expense_date,
                category=category_id)
            self.main_app.expense_repo.add(new_expense)
            self.update_table()

    def edit_row(self) -> None:
        """
        Редактирование строки расхода.
        """
        selected_rows = self.expenses_table.selectionModel().selectedRows()
        if selected_rows:
            row = selected_rows[0].row()
            pk = int(self.expenses_table.item(
                row,
                self.expenses_table.columnCount() - 1
            ).text())

            text, ok = QtWidgets.QInputDialog.getText(
                self,
                'Редактировать покупку',
                'Введите данные через запятую:',
                text=self.expenses_table.item(row, 0).text() + ', ' +
                self.expenses_table.item(row, 1).text() + ', ' +
                self.expenses_table.item(row, 2).text() + ', ' +
                self.expenses_table.item(row, 3).text()
            )
            if ok:
                try:
                    date, amount, category_name, comment = text.split(',')
                    cd = self.main_app.category_repo.get_id_by_name(
                        category_name
                    )
                    category_id = cd
                    if category_id is None:
                        new_category = Category(
                            name=category_name,
                            parent=None)
                        self.main_app.category_repo.add(new_category)
                        self.main_app.category_app.update_table()
                        cid = self.main_app.category_repo.get_id_by_name(
                            category_name
                        )
                        category_id = cid

                    try:
                        expense_date = datetime.datetime.strptime(
                            date, '%Y-%m-%d')
                    except ValueError:
                        day, month, year = map(int, date.split('.'))
                        expense_date = datetime.datetime(year, month, day)

                    edited_expense = Expense(
                        amount=int(amount),
                        comment=comment,
                        expense_date=expense_date,
                        category=category_id,
                        pk=pk)
                    self.main_app.expense_repo.update(edited_expense)
                    self.update_table()
                except Exception as e:
                    QtWidgets.QMessageBox.warning(
                        self, 'Ошибка', f'Ошибка редактирования данных: {e}'
                    )

    def delete_row(self) -> None:
        """
        Удаление строки расхода.
        """
        selected_rows = self.expenses_table.selectionModel().selectedRows()
        if selected_rows:
            row = selected_rows[0].row()
            pk = int(
                self.expenses_table.item(
                    row, self.expenses_table.columnCount() - 1).text())
            if pk is not None:
                self.main_app.expense_repo.delete(pk)
                self.update_table()  # Обновление таблицы
            else:
                QtWidgets.QMessageBox.warning(
                    self, 'Ошибка', 'Объект не найден в репозитории.')

    def go_back(self) -> None:
        """
        Вернуться к главному окну.
        """
        self.hide()
        self.main_app.show()

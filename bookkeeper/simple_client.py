from PySide6 import QtWidgets
import sys
from view.Main_window import MainApp


def create_or_get_app():
    if QtWidgets.QApplication.instance() is not None:
        app = QtWidgets.QApplication.instance()
    else:
        app = QtWidgets.QApplication(sys.argv)
    return app


def load_styles_from_file(filename):
    with open(filename, 'r', encoding='utf-8') as file:
        return file.read()


app = create_or_get_app()
styles = load_styles_from_file('stile.txt')
app.setStyleSheet(styles)
main_app = MainApp()
main_app.show()
sys.exit(app.exec())

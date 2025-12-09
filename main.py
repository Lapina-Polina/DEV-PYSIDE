import sys
from PyQt6.QtWidgets import QApplication, QWidget, QPushButton, QVBoxLayout

# Импорты всех окон
from ui.login import LoginWindow
from ui.b_login import BLoginWindow
from main_window import MainWindow
from ui.engine_settings import EngineControlUI
from ui.profile_card import ProfileCardWindow
from ui.book_shop import BookShopWindow
from ui.calculator import CalculatorWindow
from ui.ship_parameters import ShipParametersUI

class Launcher(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Выберите окно для запуска")
        self.setGeometry(100, 100, 300, 400)

        layout = QVBoxLayout()

        # Кнопки для запуска каждого окна
        buttons = [
            ("Логин", LoginWindow),
            ("Логин (В)", BLoginWindow),
            ("Основное окно", MainWindow),
            ("Параметры корабля", ShipParametersUI),
            ("Управление основными двигателями", EngineControlUI),
            ("Профиль", ProfileCardWindow),
            ("Книжный магазин", BookShopWindow),
            ("Калькулятор", CalculatorWindow),
        ]

        for text, window_class in buttons:
            btn = QPushButton(text)
            btn.clicked.connect(lambda checked, wc=window_class: self.open_window(wc))
            layout.addWidget(btn)

        self.setLayout(layout)

    def open_window(self, window_class):
        # Открываем выбранное окно
        window = window_class()
        window.show()
        # Чтобы окно не закрылось сразу, сохраняем ссылку
        setattr(self, f"_open_{window_class.__name__}", window)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    launcher = Launcher()
    launcher.show()
    sys.exit(app.exec())

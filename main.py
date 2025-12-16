import sys
from PySide6.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton

# Импорт классов окон для лабораторных работ
from widgets.lab1.main_window_lab1 import MainWindowLab1  # Лабораторная работа 1
from widgets.lab2.main_window_lab2 import MainWindowLab2  # Лабораторная работа 2


class Launcher(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Выберите лабораторную работу")

        # Уменьшаем размеры окна для компактности
        self.setGeometry(100, 100, 250, 200)  # Размеры окна изменены для компактности

        # Создаем вертикальный макет (QVBoxLayout)
        layout = QVBoxLayout()

        # Кнопки для выбора лабораторной работы
        buttons = [
            ("Лабораторная работа 1", MainWindowLab1),
            ("Лабораторная работа 2", MainWindowLab2),
        ]

        # Создаем кнопки для каждой лабораторной работы
        for text, window_class in buttons:
            btn = QPushButton(text)
            # При нажатии открываем соответствующее окно лабораторной работы
            btn.clicked.connect(self.create_window_handler(window_class))
            layout.addWidget(btn)

        self.setLayout(layout)

    def create_window_handler(self, window_class):
        """Возвращает обработчик для открытия окна лабораторной работы"""
        def handler():
            """Открывает выбранное окно лабораторной работы"""
            window = window_class()
            window.show()
            setattr(self, f"_open_{window_class.__name__}", window)  # Сохраняем ссылку на окно
        return handler


if __name__ == "__main__":
    app = QApplication(sys.argv)
    launcher = Launcher()  # Создаем окно выбора лабораторной работы
    launcher.show()  # Показываем окно
    sys.exit(app.exec())  # Запуск приложения

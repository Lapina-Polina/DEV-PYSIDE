from PyQt6.QtWidgets import QApplication, QWidget
from PyQt6.QtCore import QTimer
from PyQt6 import uic
import sys
import time

class SignalWindow(QWidget):
    def __init__(self):
        super().__init__()

        # Загрузка UI из файла
        uic.loadUi('ui/c_signals_events_form.ui', self)

        # Инициализация переменных
        self.last_pos = self.pos()
        self.last_size = self.size()

        # Подключаем кнопки
        self.pushButtonLT.clicked.connect(self.move_to_top_left)
        self.pushButtonRT.clicked.connect(self.move_to_top_right)
        self.pushButtonCenter.clicked.connect(self.center_window)
        self.pushButtonLB.clicked.connect(self.move_to_bottom_left)
        self.pushButtonRB.clicked.connect(self.move_to_bottom_right)
        self.pushButtonMoveCoords.clicked.connect(self.move_to_coordinates)
        self.pushButtonGetData.clicked.connect(self.get_window_data)

        # Таймер для обновления состояния окна
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_status)
        self.timer.start(1000)

    def move_to_top_left(self):
        """ Переместить окно в верхний левый угол """
        screen_geometry = self.screen().availableGeometry()
        self.move(0, 0)
        self.update_status()

    def move_to_top_right(self):
        """ Переместить окно в верхний правый угол """
        screen_geometry = self.screen().availableGeometry()
        self.move(screen_geometry.width() - self.width(), 0)
        self.update_status()

    def move_to_bottom_left(self):
        """ Переместить окно в нижний левый угол """
        screen_geometry = self.screen().availableGeometry()
        self.move(0, screen_geometry.height() - self.height())
        self.update_status()

    def move_to_bottom_right(self):
        """ Переместить окно в нижний правый угол """
        screen_geometry = self.screen().availableGeometry()
        self.move(screen_geometry.width() - self.width(), screen_geometry.height() - self.height())
        self.update_status()

    def center_window(self):
        """ Центрировать окно на экране """
        screen_geometry = self.screen().availableGeometry()
        self.move((screen_geometry.width() - self.width()) // 2, (screen_geometry.height() - self.height()) // 2)
        self.update_status()

    def move_to_coordinates(self):
        """ Переместить окно по заданным координатам """
        x = self.spinBoxX.value()
        y = self.spinBoxY.value()
        self.move(x, y)
        self.update_status()

    def update_status(self):
        """ Обновляем состояние окна в поле логов """
        screen = self.screen()
        screen_geometry = screen.availableGeometry()
        window_position = self.pos()
        window_size = self.size()
        window_min_size = self.minimumSize()
        window_center = self.rect().center()

        # Получаем текущее состояние окна
        state = self.windowStateToStr()

        status_text = (
            f"Time: {time.strftime('%Y-%m-%d %H:%M:%S')}\n"
            f"Number of Screens: {QApplication.screens().__len__()}\n"
            f"Current Screen: {screen.name()}\n"
            f"Screen Resolution: {screen_geometry.width()}x{screen_geometry.height()}\n"
            f"Window Position: {window_position.x()}, {window_position.y()}\n"
            f"Window Size: {window_size.width()}x{window_size.height()}\n"
            f"Minimum Window Size: {window_min_size.width()}x{window_min_size.height()}\n"
            f"Window Center: {window_center.x()}, {window_center.y()}\n"
            f"Window State: {state}\n"
        )

        # Выводим в текстовое поле
        self.plainTextEdit.setPlainText(status_text)

    def windowStateToStr(self):
        """ Возвращает строковое представление состояния окна """
        if self.isMinimized():
            return "Minimized"
        elif self.isMaximized():
            return "Maximized"
        elif self.isVisible():
            return "Visible"
        else:
            return "Hidden"

    def get_window_data(self):
        """ Получаем данные окна и выводим в консоль """
        window_position = self.pos()
        window_size = self.size()
        print(f"Window Position: {window_position.x()}, {window_position.y()}")
        print(f"Window Size: {window_size.width()}x{window_size.height()}")

    def moveEvent(self, event):
        # Отслеживаем перемещение окна
        old_pos = self.last_pos
        new_pos = self.pos()
        print(f"Window moved from {old_pos.x()}, {old_pos.y()} to {new_pos.x()}, {new_pos.y()}")
        self.last_pos = new_pos
        super().moveEvent(event)

    def resizeEvent(self, event):
        # Отслеживаем изменение размера окна
        old_size = self.last_size
        new_size = self.size()
        print(f"Window resized from {old_size.width()}x{old_size.height()} to {new_size.width()}x{new_size.height()}")
        self.last_size = new_size
        super().resizeEvent(event)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = SignalWindow()
    window.show()
    sys.exit(app.exec())

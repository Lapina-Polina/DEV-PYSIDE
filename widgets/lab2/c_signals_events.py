import sys
import time

from PySide6.QtWidgets import QApplication, QWidget
from PySide6.QtCore import QTimer, QFile
from PySide6.QtUiTools import QUiLoader


class SignalWindow(QWidget):
    def __init__(self):
        super().__init__()

        # Загрузка UI
        loader = QUiLoader()
        ui_file = QFile("ui/c_signals_events_form.ui")
        ui_file.open(QFile.ReadOnly)
        self.ui = loader.load(ui_file, self)
        ui_file.close()

        # делаем ui главным layout
        self.setLayout(self.ui.layout())

        # Инициализация переменных
        self.last_pos = self.pos()
        self.last_size = self.size()

        # Подключаем кнопки
        self.ui.pushButtonLT.clicked.connect(self.move_to_top_left)
        self.ui.pushButtonRT.clicked.connect(self.move_to_top_right)
        self.ui.pushButtonCenter.clicked.connect(self.center_window)
        self.ui.pushButtonLB.clicked.connect(self.move_to_bottom_left)
        self.ui.pushButtonRB.clicked.connect(self.move_to_bottom_right)
        self.ui.pushButtonMoveCoords.clicked.connect(self.move_to_coordinates)
        self.ui.pushButtonGetData.clicked.connect(self.get_window_data)

        # Таймер
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_status)
        self.timer.start(1000)

    def move_to_top_left(self):
        self.move(0, 0)
        self.update_status()

    def move_to_top_right(self):
        screen = self.screen().availableGeometry()
        self.move(screen.width() - self.width(), 0)
        self.update_status()

    def move_to_bottom_left(self):
        screen = self.screen().availableGeometry()
        self.move(0, screen.height() - self.height())
        self.update_status()

    def move_to_bottom_right(self):
        screen = self.screen().availableGeometry()
        self.move(
            screen.width() - self.width(),
            screen.height() - self.height()
        )
        self.update_status()

    def center_window(self):
        screen = self.screen().availableGeometry()
        self.move(
            (screen.width() - self.width()) // 2,
            (screen.height() - self.height()) // 2
        )
        self.update_status()

    def move_to_coordinates(self):
        x = self.ui.spinBoxX.value()
        y = self.ui.spinBoxY.value()
        self.move(x, y)
        self.update_status()

    def update_status(self):
        screen = self.screen()
        screen_geometry = screen.availableGeometry()

        state = self.window_state_to_str()

        status_text = (
            f"Time: {time.strftime('%Y-%m-%d %H:%M:%S')}\n"
            f"Number of Screens: {len(QApplication.screens())}\n"
            f"Current Screen: {screen.name()}\n"
            f"Screen Resolution: {screen_geometry.width()}x{screen_geometry.height()}\n"
            f"Window Position: {self.x()}, {self.y()}\n"
            f"Window Size: {self.width()}x{self.height()}\n"
            f"Minimum Window Size: {self.minimumWidth()}x{self.minimumHeight()}\n"
            f"Window State: {state}\n"
        )

        self.ui.plainTextEdit.setPlainText(status_text)

    def window_state_to_str(self):
        if self.isMinimized():
            return "Minimized"
        if self.isMaximized():
            return "Maximized"
        return "Normal"

    def get_window_data(self):
        print(f"Window Position: {self.x()}, {self.y()}")
        print(f"Window Size: {self.width()}x{self.height()}")

    def moveEvent(self, event):
        print(
            f"Window moved from {self.last_pos.x()}, {self.last_pos.y()} "
            f"to {self.x()}, {self.y()}"
        )
        self.last_pos = self.pos()
        super().moveEvent(event)

    def resizeEvent(self, event):
        print(
            f"Window resized from {self.last_size.width()}x{self.last_size.height()} "
            f"to {self.width()}x{self.height()}"
        )
        self.last_size = self.size()
        super().resizeEvent(event)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = SignalWindow()
    window.show()
    sys.exit(app.exec())

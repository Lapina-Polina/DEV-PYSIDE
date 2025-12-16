import sys
import time

from PySide6.QtWidgets import QApplication, QWidget
from PySide6.QtCore import QTimer, QFile
from PySide6.QtUiTools import QUiLoader


class SignalWindow(QWidget):
    def __init__(self):
        super().__init__()

        # ---------- Load UI ----------
        loader = QUiLoader()
        ui_file = QFile("ui/c_signals_events_form.ui")

        if not ui_file.open(QFile.ReadOnly):
            raise RuntimeError("Не удалось открыть ui/c_signals_events_form.ui")

        self.ui = loader.load(ui_file, self)
        ui_file.close()

        if not self.ui:
            raise RuntimeError("Ошибка загрузки UI")

        # ---------- Init state ----------
        self.last_pos = self.pos()
        self.last_size = self.size()

        # ---------- Connect buttons ----------
        self.ui.pushButtonLT.clicked.connect(self.move_to_top_left)
        self.ui.pushButtonRT.clicked.connect(self.move_to_top_right)
        self.ui.pushButtonCenter.clicked.connect(self.center_window)
        self.ui.pushButtonLB.clicked.connect(self.move_to_bottom_left)
        self.ui.pushButtonRB.clicked.connect(self.move_to_bottom_right)
        self.ui.pushButtonMoveCoords.clicked.connect(self.move_to_coordinates)
        self.ui.pushButtonGetData.clicked.connect(self.get_window_data)

        # ---------- Timer ----------
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_status)
        self.timer.start(1000)

    # Window movement
    def move_to_top_left(self):
        self.move(0, 0)
        self.update_status()

    def move_to_top_right(self):
        geo = self.screen().availableGeometry()
        self.move(geo.width() - self.width(), 0)
        self.update_status()

    def move_to_bottom_left(self):
        geo = self.screen().availableGeometry()
        self.move(0, geo.height() - self.height())
        self.update_status()

    def move_to_bottom_right(self):
        geo = self.screen().availableGeometry()
        self.move(geo.width() - self.width(), geo.height() - self.height())
        self.update_status()

    def center_window(self):
        geo = self.screen().availableGeometry()
        self.move(
            (geo.width() - self.width()) // 2,
            (geo.height() - self.height()) // 2
        )
        self.update_status()

    def move_to_coordinates(self):
        x = self.ui.spinBoxX.value()
        y = self.ui.spinBoxY.value()
        self.move(x, y)
        self.update_status()

    # Status
    def update_status(self):
        screen = self.screen()
        geo = screen.availableGeometry()

        pos = self.pos()
        size = self.size()
        min_size = self.minimumSize()
        center = self.rect().center()
        state = self.window_state_to_str()

        text = (
            f"Time: {time.strftime('%Y-%m-%d %H:%M:%S')}\n"
            f"Number of Screens: {len(QApplication.screens())}\n"
            f"Current Screen: {screen.name()}\n"
            f"Screen Resolution: {geo.width()}x{geo.height()}\n"
            f"Window Position: {pos.x()}, {pos.y()}\n"
            f"Window Size: {size.width()}x{size.height()}\n"
            f"Minimum Window Size: {min_size.width()}x{min_size.height()}\n"
            f"Window Center: {center.x()}, {center.y()}\n"
            f"Window State: {state}\n"
        )

        self.ui.plainTextEdit.setPlainText(text)

    def window_state_to_str(self):
        if self.isMinimized():
            return "Minimized"
        if self.isMaximized():
            return "Maximized"
        if self.isVisible():
            return "Visible"
        return "Hidden"

    # Data
    def get_window_data(self):
        pos = self.pos()
        size = self.size()
        print(f"Window Position: {pos.x()}, {pos.y()}")
        print(f"Window Size: {size.width()}x{size.height()}")

    # Events
    def moveEvent(self, event):
        new_pos = self.pos()
        print(
            f"Window moved from {self.last_pos.x()}, {self.last_pos.y()} "
            f"to {new_pos.x()}, {new_pos.y()}"
        )
        self.last_pos = new_pos
        super().moveEvent(event)

    def resizeEvent(self, event):
        new_size = self.size()
        print(
            f"Window resized from {self.last_size.width()}x{self.last_size.height()} "
            f"to {new_size.width()}x{new_size.height()}"
        )
        self.last_size = new_size
        super().resizeEvent(event)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = SignalWindow()
    window.show()
    sys.exit(app.exec())

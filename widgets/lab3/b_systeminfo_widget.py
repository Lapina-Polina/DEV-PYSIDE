from PySide6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QSpinBox
from PySide6.QtCore import Qt

from widgets.lab3.a_threads import SystemInfo


class SystemInfoWindow(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Системная информация")
        self.setGeometry(200, 200, 300, 200)

        # UI
        main_layout = QVBoxLayout()

        # поле задержки
        delay_layout = QHBoxLayout()
        delay_label = QLabel("Задержка (сек):")

        self.delay_spin = QSpinBox()
        self.delay_spin.setRange(1, 10)
        self.delay_spin.setValue(1)

        delay_layout.addWidget(delay_label)
        delay_layout.addWidget(self.delay_spin)

        # CPU
        self.cpu_label = QLabel("CPU: -- %")
        self.cpu_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # RAM
        self.ram_label = QLabel("RAM: -- %")
        self.ram_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        main_layout.addLayout(delay_layout)
        main_layout.addWidget(self.cpu_label)
        main_layout.addWidget(self.ram_label)

        self.setLayout(main_layout)

        # THREAD
        self.thread = SystemInfo()

        # передаём начальную задержку
        self.thread.delay = self.delay_spin.value()

        # подключаем сигнал
        self.thread.systemInfoReceived.connect(self.update_info)

        # горячее изменение задержки
        self.delay_spin.valueChanged.connect(self.change_delay)

        # запуск потока сразу
        self.thread.start()

    def update_info(self, data: list):
        cpu, ram = data
        self.cpu_label.setText(f"CPU: {cpu} %")
        self.ram_label.setText(f"RAM: {ram} %")

    def change_delay(self, value: int):
        # поток сразу реагирует на изменение
        self.thread.delay = value

    def closeEvent(self, event):
        # корректное завершение потока
        if self.thread.isRunning():
            self.thread.terminate()
            self.thread.wait()
        event.accept()

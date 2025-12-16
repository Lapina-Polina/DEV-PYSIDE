from PySide6.QtWidgets import (
    QApplication, QWidget, QDial, QSlider,
    QLCDNumber, QComboBox, QVBoxLayout
)

from PySide6.QtCore import Qt, QEvent, QSettings


class EventFilterSettings(QWidget):
    def __init__(self):
        super().__init__()

        # Инициализация UI элементов
        self.dial = QDial()
        self.slider = QSlider(Qt.Orientation.Horizontal)
        self.lcd = QLCDNumber()
        self.comboBox = QComboBox()

        # Добавляем элементы в комбобокс
        self.comboBox.addItems(["dec", "hex", "oct", "bin"])

        # Инициализация настроек
        self.settings = QSettings("MyCompany", "MyApp")

        # Сохранение и загрузка настроек
        self.load_settings()

        # Устанавливаем начальные значения
        self.dial.setValue(0)
        self.slider.setValue(0)
        self.lcd.display(0)

        # Устанавливаем фильтрацию событий для dials и slider
        self.dial.installEventFilter(self)
        self.slider.installEventFilter(self)

        # Соединяем сигналы
        self.dial.valueChanged.connect(self.on_value_changed)
        self.slider.valueChanged.connect(self.on_value_changed)
        self.comboBox.currentTextChanged.connect(self.on_combo_changed)

        # Layout для размещения виджетов
        layout = QVBoxLayout(self)
        layout.addWidget(self.dial)
        layout.addWidget(self.slider)
        layout.addWidget(self.lcd)
        layout.addWidget(self.comboBox)

        self.setLayout(layout)
        self.resize(500, 300)  # Устанавливаем размер окна 500x300

    def load_settings(self):
        """ Загружаем настройки из QSettings """
        mode = self.settings.value("lcd/mode", "dec")  # По умолчанию "dec"
        self.comboBox.setCurrentText(mode)
        lcd_value = self.settings.value("lcd/value", 0)  # По умолчанию 0
        self.dial.setValue(lcd_value)
        self.slider.setValue(lcd_value)

    def save_settings(self):
        """ Сохраняем настройки в QSettings """
        self.settings.setValue("lcd/mode", self.comboBox.currentText())
        self.settings.setValue("lcd/value", self.dial.value())

    def on_value_changed(self, value):
        """ Обновляем значения в LCD и сохраняем состояние """
        self.lcd.display(value)
        self.save_settings()

    def on_combo_changed(self, mode):
        """ Изменяем режим отображения в LCD """
        if mode == "hex":
            self.lcd.setMode(QLCDNumber.Mode.Hex)
        elif mode == "dec":
            self.lcd.setMode(QLCDNumber.Mode.Dec)
        elif mode == "oct":
            self.lcd.setMode(QLCDNumber.Mode.Oct)
        elif mode == "bin":
            self.lcd.setMode(QLCDNumber.Mode.Bin)
        self.save_settings()

    def eventFilter(self, watched, event):
        """ Фильтруем события, чтобы добавить поддержку клавиш + и - для QDial и QSlider """
        if watched == self.dial and event.type() == QEvent.Type.KeyPress:
            if event.key() == Qt.Key.Key_Plus:
                self.dial.setValue(self.dial.value() + 1)
            elif event.key() == Qt.Key.Key_Minus:
                self.dial.setValue(self.dial.value() - 1)

        elif watched == self.slider and event.type() == QEvent.Type.KeyPress:
            if event.key() == Qt.Key.Key_Plus:
                self.slider.setValue(self.slider.value() + 1)
            elif event.key() == Qt.Key.Key_Minus:
                self.slider.setValue(self.slider.value() - 1)

        return super().eventFilter(watched, event)


if __name__ == "__main__":
    app = QApplication([])
    window = EventFilterSettings()
    window.show()
    app.exec()

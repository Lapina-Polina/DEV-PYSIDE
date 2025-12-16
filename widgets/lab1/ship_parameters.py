import sys
from PyQt6.QtWidgets import QApplication, QWidget, QLineEdit, QFormLayout

class ShipParametersUI(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Параметры корабля")
        self.setGeometry(100, 100, 300, 200)

        layout = QFormLayout()

        # Температура
        self.temp_edit = QLineEdit("22 C")
        self.temp_edit.setReadOnly(True)
        self.temp_edit.setStyleSheet("color: orange;")
        layout.addRow("Температура на борту", self.temp_edit)

        # Разгерметизация
        self.depressurization_edit = QLineEdit("Отсутствует")
        self.depressurization_edit.setReadOnly(True)
        self.depressurization_edit.setStyleSheet("color: green;")
        layout.addRow("Разгерметизация", self.depressurization_edit)

        # Баки
        self.tank1_edit = QLineEdit("Норма")
        self.tank1_edit.setReadOnly(True)
        self.tank1_edit.setStyleSheet("color: green;")
        layout.addRow("Бак №1", self.tank1_edit)

        self.tank2_edit = QLineEdit("Норма")
        self.tank2_edit.setReadOnly(True)
        self.tank2_edit.setStyleSheet("color: green;")
        layout.addRow("Бак №2", self.tank2_edit)

        self.tank3_edit = QLineEdit("Норма")
        self.tank3_edit.setReadOnly(True)
        self.tank3_edit.setStyleSheet("color: green;")
        layout.addRow("Бак №3", self.tank3_edit)

        # Сохраняем баки в список для удобного обновления
        self.tanks = [self.tank1_edit, self.tank2_edit, self.tank3_edit]

        self.setLayout(layout)

    def update_parameters(self, temp=None, depressurization=None, tanks=None):
        """Обновление значений и цветов"""
        if temp is not None:
            self.temp_edit.setText(f"{temp} C")
            color = "red" if temp > 50 else "orange"
            self.temp_edit.setStyleSheet(f"color: {color};")

        if depressurization is not None:
            text = "Есть" if depressurization else "Отсутствует"
            color = "red" if depressurization else "green"
            self.depressurization_edit.setText(text)
            self.depressurization_edit.setStyleSheet(f"color: {color};")

        if tanks is not None:
            for edit, value in zip(self.tanks, tanks):
                edit.setText(value)
                color = "green" if value == "Норма" else "red"
                edit.setStyleSheet(f"color: {color};")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = ShipParametersUI()
    window.show()

    # Пример обновления параметров
    window.update_parameters(temp=60, depressurization=True, tanks=["Норма", "Пусто", "Норма"])

    sys.exit(app.exec())

import sys
from PySide6.QtWidgets import (
    QApplication, QDialog, QLabel, QLineEdit, QSlider, QPushButton,
    QVBoxLayout, QHBoxLayout
)
from PySide6.QtCore import Qt
from PySide6.QtGui import QFont


class CalculatorWindow(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Калькулятор")
        self.setGeometry(100, 100, 400, 350)

        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(20, 20, 20, 20)
        main_layout.setSpacing(15)

        # Первое число
        first_layout = QHBoxLayout()
        label1 = QLabel("Первое число:")
        self.slider1 = QSlider(Qt.Orientation.Horizontal)
        self.slider1.setMinimum(0)
        self.slider1.setMaximum(100)
        self.slider1.setValue(0)
        self.input1 = QLineEdit("0")
        self.input1.setFixedWidth(60)

        first_layout.addWidget(label1)
        first_layout.addWidget(self.slider1)
        first_layout.addWidget(self.input1)
        main_layout.addLayout(first_layout)

        # Второе число
        second_layout = QHBoxLayout()
        label2 = QLabel("Второе число:")
        self.slider2 = QSlider(Qt.Orientation.Horizontal)
        self.slider2.setMinimum(0)
        self.slider2.setMaximum(100)
        self.slider2.setValue(0)
        self.input2 = QLineEdit("0")
        self.input2.setFixedWidth(60)

        second_layout.addWidget(label2)
        second_layout.addWidget(self.slider2)
        second_layout.addWidget(self.input2)
        main_layout.addLayout(second_layout)

        # Кнопки операций
        buttons_layout = QHBoxLayout()
        button_size = (60, 40)
        self.btn_add = QPushButton("+")
        self.btn_sub = QPushButton("-")
        self.btn_mul = QPushButton("*")
        self.btn_div = QPushButton("/")

        for btn in [self.btn_add, self.btn_sub, self.btn_mul, self.btn_div]:
            btn.setFixedSize(*button_size)
            buttons_layout.addWidget(btn)

        main_layout.addLayout(buttons_layout)

        # Результат
        self.result_label = QLabel("0")
        self.result_label.setFont(QFont("Arial", 32, QFont.Weight.Bold))  # больше шрифт
        self.result_label.setStyleSheet("color: blue;")  # синий цвет
        self.result_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        main_layout.addWidget(self.result_label)

        self.setLayout(main_layout)

        # Связь ползунков и полей ввода
        self.slider1.valueChanged.connect(lambda v: self.input1.setText(str(v)))
        self.slider2.valueChanged.connect(lambda v: self.input2.setText(str(v)))

        self.input1.textChanged.connect(self.update_slider1)
        self.input2.textChanged.connect(self.update_slider2)

        # Связь кнопок с вычислениями
        self.btn_add.clicked.connect(lambda: self.calculate("+"))
        self.btn_sub.clicked.connect(lambda: self.calculate("-"))
        self.btn_mul.clicked.connect(lambda: self.calculate("*"))
        self.btn_div.clicked.connect(lambda: self.calculate("/"))

    def update_slider1(self, text):
        if text.isdigit():
            self.slider1.setValue(int(text))

    def update_slider2(self, text):
        if text.isdigit():
            self.slider2.setValue(int(text))

    def calculate(self, op):
        try:
            a = int(self.input1.text())
            b = int(self.input2.text())
            if op == "+":
                res = a + b
            elif op == "-":
                res = a - b
            elif op == "*":
                res = a * b
            elif op == "/":
                res = a / b
            self.result_label.setText(str(res))
        except Exception as e:
            self.result_label.setText("Ошибка")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = CalculatorWindow()
    window.show()
    sys.exit(app.exec())

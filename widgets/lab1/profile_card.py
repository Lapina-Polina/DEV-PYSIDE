from PySide6.QtWidgets import (
    QApplication, QDialog, QLabel, QLineEdit, QPushButton,
    QVBoxLayout, QHBoxLayout, QMessageBox, QSizePolicy
)
import sys
import re

class ProfileCardWindow(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Профиль")
        self.setGeometry(100, 100, 400, 250)

        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(20, 20, 20, 20)
        main_layout.setSpacing(10)

        # Фиксированная ширина для всех полей ввода
        input_width = 250

        # Фамилия
        lastname_layout = QHBoxLayout()
        self.label_lastname = QLabel("Фамилия:")
        self.label_lastname.setFixedWidth(100)
        self.input_lastname = QLineEdit()
        self.input_lastname.setPlaceholderText("Введите Вашу фамилию")
        self.input_lastname.setFixedWidth(input_width)
        lastname_layout.addWidget(self.label_lastname)
        lastname_layout.addWidget(self.input_lastname)
        main_layout.addLayout(lastname_layout)

        # Имя
        firstname_layout = QHBoxLayout()
        self.label_firstname = QLabel("Имя:")
        self.label_firstname.setFixedWidth(100)
        self.input_firstname = QLineEdit()
        self.input_firstname.setPlaceholderText("Введите Ваше имя")
        self.input_firstname.setFixedWidth(input_width)
        firstname_layout.addWidget(self.label_firstname)
        firstname_layout.addWidget(self.input_firstname)
        main_layout.addLayout(firstname_layout)

        # Отчество (необязательно)
        middlename_layout = QHBoxLayout()
        self.label_middlename = QLabel("Отчество:")
        self.label_middlename.setFixedWidth(100)
        self.input_middlename = QLineEdit()
        self.input_middlename.setPlaceholderText("Введите Ваше отчество")
        self.input_middlename.setFixedWidth(input_width)
        middlename_layout.addWidget(self.label_middlename)
        middlename_layout.addWidget(self.input_middlename)
        main_layout.addLayout(middlename_layout)

        # Телефон
        phone_layout = QHBoxLayout()
        self.label_phone = QLabel("Телефон:")
        self.label_phone.setFixedWidth(100)
        self.input_phone = QLineEdit()
        self.input_phone.setPlaceholderText("Введите Ваш телефон (11 цифр)")
        self.input_phone.setFixedWidth(input_width)
        phone_layout.addWidget(self.label_phone)
        phone_layout.addWidget(self.input_phone)
        main_layout.addLayout(phone_layout)

        # Кнопка Сохранить
        self.save_button = QPushButton("Сохранить")
        self.save_button.setFixedWidth(100)
        self.save_button.clicked.connect(self.save_profile)
        main_layout.addWidget(self.save_button)

        self.setLayout(main_layout)

    def save_profile(self):
        lastname = self.input_lastname.text().strip()
        firstname = self.input_firstname.text().strip()
        middlename = self.input_middlename.text().strip()
        phone = self.input_phone.text().strip()

        # Проверка обязательных полей
        if not lastname:
            QMessageBox.warning(self, "Ошибка", "Введите фамилию")
            return
        if not firstname:
            QMessageBox.warning(self, "Ошибка", "Введите имя")
            return
        # Проверка телефона: ровно 11 цифр
        if not re.fullmatch(r"\d{11}", phone):
            QMessageBox.warning(self, "Ошибка", "Телефон должен состоять из 11 цифр")
            return

        # Всё верно
        QMessageBox.information(
            self, "Сохранено",
            f"Фамилия: {lastname}\nИмя: {firstname}\nОтчество: {middlename}\nТелефон: {phone}"
        )
        self.accept()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = ProfileCardWindow()
    window.show()
    sys.exit(app.exec())

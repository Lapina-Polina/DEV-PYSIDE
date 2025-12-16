import sys
from PySide6.QtWidgets import QApplication, QDialog, QPushButton, QFormLayout, QLineEdit, QMessageBox


class BLoginWindow(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Логин (В)")
        self.setGeometry(100, 100, 300, 150)

        layout = QFormLayout()
        self.username = QLineEdit()
        self.password = QLineEdit()
        self.password.setEchoMode(QLineEdit.EchoMode.Password)

        layout.addRow("Логин:", self.username)
        layout.addRow("Пароль:", self.password)

        self.login_btn = QPushButton("Войти")
        self.login_btn.clicked.connect(self.login)
        layout.addRow(self.login_btn)

        self.setLayout(layout)

        # Переменные для хранения введённых данных
        self.entered_username = ""
        self.entered_password = ""

    def login(self):
        self.entered_username = self.username.text()
        self.entered_password = self.password.text()

        if self.entered_username and self.entered_password:
            print(f"BLogin: {self.entered_username}, Password: {self.entered_password}")
            self.accept()  # Закрываем окно
        else:
            QMessageBox.warning(self, "Ошибка", "Введите логин и пароль")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = BLoginWindow()
    if window.exec():  # Окно модальное, закроется только после accept()
        print("Окно BLogin закрыто")
        print("Введённый логин:", window.entered_username)
        print("Введённый пароль:", window.entered_password)
    sys.exit(app.exec())

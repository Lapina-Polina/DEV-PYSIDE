from PyQt6.QtWidgets import QApplication, QDialog, QMessageBox
from ui_generated.login_ui import Ui_Dialog

class LoginWindow(QDialog):
    def __init__(self):
        super().__init__()
        self.ui = Ui_Dialog()
        self.ui.setupUi(self)

        # Подключаем кнопку "Войти" к обработчику
        self.ui.pushButton.clicked.connect(self.login)

        # Переменные для хранения введенных данных
        self.username = ""
        self.password = ""

    def login(self):
        self.username = self.ui.lineEdit.text()
        self.password = self.ui.lineEdit_2.text()

        if self.username and self.password:
            print(f"Login: {self.username}, Password: {self.password}")
            self.accept()  # закрываем окно после успешного ввода
        else:
            QMessageBox.warning(self, "Ошибка", "Введите логин и пароль")


if __name__ == "__main__":
    import sys
    app = QApplication(sys.argv)
    window = LoginWindow()
    window.show()
    sys.exit(app.exec())

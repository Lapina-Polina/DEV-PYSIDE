from PySide6.QtWidgets import (
    QApplication, QWidget, QLabel,
    QLineEdit, QVBoxLayout, QHBoxLayout, QPushButton
)


class Window(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.initUi()

    def initUi(self) -> None:
        """
        Инициализация интерфейса

        :return: None
        """
        # Создаем виджеты QLabel
        labelLogin = QLabel("Логин")
        labelRegistration = QLabel("Регистрация")

        # Создаем QLineEdit для ввода логина
        self.lineEditLogin = QLineEdit()
        self.lineEditLogin.setPlaceholderText("Введите логин")

        # Создаем QLineEdit для ввода пароля
        self.lineEditPassword = QLineEdit()
        self.lineEditPassword.setPlaceholderText("Введите пароль")
        self.lineEditPassword.setEchoMode(QLineEdit.EchoMode.Password)

        # Создаем кнопки
        self.pushButtonLogin = QPushButton("Войти")
        self.pushButtonRegistration = QPushButton("Регистрация")

        # Привязываем обработчики событий
        self.pushButtonLogin.clicked.connect(self.onLoginClicked)
        self.pushButtonRegistration.clicked.connect(self.onRegistrationClicked)

        # Создаем QHBoxLayout для логина
        layoutLogin = QHBoxLayout()
        layoutLogin.addWidget(labelLogin)
        layoutLogin.addWidget(self.lineEditLogin)

        # Создаем QHBoxLayout для пароля
        layoutPassword = QHBoxLayout()
        layoutPassword.addWidget(labelRegistration)
        layoutPassword.addWidget(self.lineEditPassword)

        # Создаем QHBoxLayout для кнопок
        layoutButtons = QHBoxLayout()
        layoutButtons.addWidget(self.pushButtonLogin)
        layoutButtons.addWidget(self.pushButtonRegistration)

        # Создаем QVBoxLayout для основного макета
        layoutMain = QVBoxLayout()
        layoutMain.addLayout(layoutLogin)
        layoutMain.addLayout(layoutPassword)
        layoutMain.addLayout(layoutButtons)

        self.setLayout(layoutMain)  # Устанавливаем layoutMain на основной виджет

    def onLoginClicked(self):
        """Обработчик для кнопки Войти"""
        login = self.lineEditLogin.text()
        password = self.lineEditPassword.text()
        print(f"Вход: Логин = {login}, Пароль = {password}")

        # Логика для проверки логина и пароля
        # Если вход успешен, закроем окно
        self.close()  # Закрытие окна после выполнения логики входа

    def onRegistrationClicked(self):
        """Обработчик для кнопки Регистрация"""
        login = self.lineEditLogin.text()
        password = self.lineEditPassword.text()
        print(f"Регистрация: Логин = {login}, Пароль = {password}")

        # Логика для регистрации
        # После регистрации закроем окно
        self.close()  # Закрытие окна после выполнения логики регистрации


if __name__ == "__main__":
    app = QApplication([])
    window = Window()
    window.show()
    app.exec()

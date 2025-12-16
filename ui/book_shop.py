import sys
from PySide6.QtWidgets import QApplication, QDialog, QVBoxLayout,\
    QPushButton, QLabel, QListWidget, QButtonGroup, QRadioButton
from PySide6.QtGui import QFont
from PySide6.QtCore import Qt

class BookShopWindow(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Книжный магазин")
        self.setGeometry(100, 100, 400, 500)

        # Основной вертикальный layout
        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(20, 20, 20, 20)
        main_layout.setSpacing(15)

        # Заголовок "Выберите книгу"
        self.label_books = QLabel("ВЫБЕРИТЕ КНИГУ")
        self.label_books.setFont(QFont("Arial", 14, QFont.Weight.Bold))
        self.label_books.setStyleSheet("color: purple;")
        main_layout.addWidget(self.label_books, alignment=Qt.AlignmentFlag.AlignLeft)

        # Список книг
        self.book_list = QListWidget()
        self.book_list.addItems([
            "Война и мир — Лев Толстой",
            "Преступление и наказание — Фёдор Достоевский",
            "Гарри Поттер — Джоан Роулинг",
            "Мастер и Маргарита — Михаил Булгаков",
            "1984 — Джордж Оруэлл",
            "Гарри Поттер и узник Азкабана — Джоан Роулинг",
            "Благословение небожителей. Том 3 — Мосян Тунсю",
            "Унесенные ветром — Маргарет Митчелл"
        ])
        main_layout.addWidget(self.book_list)

        # Заголовок "Выберите способ оплаты"
        self.label_payment = QLabel("ВЫБЕРИТЕ СПОСОБ ОПЛАТЫ")
        self.label_payment.setFont(QFont("Arial", 14, QFont.Weight.Bold))
        self.label_payment.setStyleSheet("color: purple;")
        main_layout.addWidget(self.label_payment, alignment=Qt.AlignmentFlag.AlignLeft)

        # Способы оплаты
        self.payment_group = QButtonGroup(self)
        self.radio_card = QRadioButton("По карте")
        self.radio_qr = QRadioButton("По QR")
        self.radio_cash = QRadioButton("Наличными")

        # Добавляем в группу, чтобы можно было выбрать только один
        self.payment_group.addButton(self.radio_card)
        self.payment_group.addButton(self.radio_qr)
        self.payment_group.addButton(self.radio_cash)

        # Вертикальный layout
        payment_layout = QVBoxLayout()
        payment_layout.addWidget(self.radio_card)
        payment_layout.addWidget(self.radio_qr)
        payment_layout.addWidget(self.radio_cash)
        main_layout.addLayout(payment_layout)

        # Кнопка Оплатить
        self.pay_button = QPushButton("Оплатить")
        self.pay_button.setFixedHeight(40)
        main_layout.addWidget(self.pay_button, alignment=Qt.AlignmentFlag.AlignCenter)

        self.setLayout(main_layout)

        # Подключаем кнопку (для примера)
        self.pay_button.clicked.connect(self.pay_action)

    def pay_action(self):
        selected_book = self.book_list.currentItem()
        selected_payment = None
        for btn in self.payment_group.buttons():
            if btn.isChecked():
                selected_payment = btn.text()
        if selected_book and selected_payment:
            print(f"Вы выбрали книгу: {selected_book.text()}, способ оплаты: {selected_payment}")
            self.accept()  # Закрывает окно после успешного выбора
        else:
            print("Выберите книгу и способ оплаты")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = BookShopWindow()
    window.show()
    sys.exit(app.exec())

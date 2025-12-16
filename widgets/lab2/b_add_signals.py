from PySide6.QtWidgets import (
    QApplication, QWidget, QLineEdit, QVBoxLayout, QHBoxLayout,
    QPushButton, QComboBox, QTextEdit, QPlainTextEdit,
    QSpinBox, QDoubleSpinBox, QTimeEdit, QDateTimeEdit
)

from PySide6.QtCore import QTime, QDateTime
import random


class AddWindow(QWidget):

    def __init__(self, parent=None):
        super().__init__(parent)
        self.initUi()

    def initUi(self):
        """
        Инициализация интерфейса
        """

        # comboBox -----------------------------------------------------------
        self.comboBox = QComboBox()
        self.comboBox.addItem("Элемент 1")
        self.comboBox.addItem("Элемент 2")
        self.comboBox.addItems(["Элемент 3", "Элемент 4", "Элемент 5"])
        self.comboBox.insertItem(0, "")

        self.pushButtonComboBox = QPushButton("Получить данные")
        layoutComboBox = QHBoxLayout()
        layoutComboBox.addWidget(self.comboBox)
        layoutComboBox.addWidget(self.pushButtonComboBox)

        # lineEdit -----------------------------------------------------------
        self.lineEdit = QLineEdit()
        self.lineEdit.setPlaceholderText("Введите текст")
        self.pushButtonLineEdit = QPushButton("Получить данные")
        layoutLineEdit = QHBoxLayout()
        layoutLineEdit.addWidget(self.lineEdit)
        layoutLineEdit.addWidget(self.pushButtonLineEdit)

        # textEdit -----------------------------------------------------------
        self.textEdit = QTextEdit()
        self.textEdit.setPlaceholderText("Введите текст")
        self.pushButtonTextEdit = QPushButton("Получить данные")
        layoutTextEdit = QHBoxLayout()
        layoutTextEdit.addWidget(self.textEdit)
        layoutTextEdit.addWidget(self.pushButtonTextEdit)

        # plainTextEdit ------------------------------------------------------
        self.plainTextEdit = QPlainTextEdit()
        self.plainTextEdit.setPlaceholderText("Введите текст")
        self.pushButtonPlainTextEdit = QPushButton("Получить данные")
        layoutPlainTextEdit = QHBoxLayout()
        layoutPlainTextEdit.addWidget(self.plainTextEdit)
        layoutPlainTextEdit.addWidget(self.pushButtonPlainTextEdit)

        # spinBox ------------------------------------------------------------
        self.spinBox = QSpinBox()
        self.spinBox.setValue(random.randint(-50, 50))
        self.pushButtonSpinBox = QPushButton("Получить данные")
        layoutSpinBox = QHBoxLayout()
        layoutSpinBox.addWidget(self.spinBox)
        layoutSpinBox.addWidget(self.pushButtonSpinBox)

        # doubleSpinBox ------------------------------------------------------
        self.doubleSpinBox = QDoubleSpinBox()
        self.doubleSpinBox.setValue(random.randint(-50, 50))
        self.pushButtonDoubleSpinBox = QPushButton("Получить данные")
        layoutDoubleSpinBox = QHBoxLayout()
        layoutDoubleSpinBox.addWidget(self.doubleSpinBox)
        layoutDoubleSpinBox.addWidget(self.pushButtonDoubleSpinBox)

        # timeEdit -----------------------------------------------------------
        self.timeEdit = QTimeEdit()
        self.timeEdit.setTime(QTime.currentTime().addSecs(random.randint(-10000, 10000)))
        self.pushButtonTimeEdit = QPushButton("Получить данные")
        layoutTimeEdit = QHBoxLayout()
        layoutTimeEdit.addWidget(self.timeEdit)
        layoutTimeEdit.addWidget(self.pushButtonTimeEdit)

        # dateTimeEdit -------------------------------------------------------
        self.dateTimeEdit = QDateTimeEdit()
        self.dateTimeEdit.setDateTime(QDateTime.currentDateTime().addDays(random.randint(-10, 10)))
        self.pushButtonDateTimeEdit = QPushButton("Получить данные")
        layoutDateTimeEdit = QHBoxLayout()
        layoutDateTimeEdit.addWidget(self.dateTimeEdit)
        layoutDateTimeEdit.addWidget(self.pushButtonDateTimeEdit)

        # plainTextEditLog ---------------------------------------------------
        self.plainTextEditLog = QPlainTextEdit()
        self.pushButtonClearLog = QPushButton("Очистить лог")
        layoutLog = QHBoxLayout()
        layoutLog.addWidget(self.plainTextEditLog)
        layoutLog.addWidget(self.pushButtonClearLog)

        # main layout
        layoutMain = QVBoxLayout()
        layoutMain.addLayout(layoutComboBox)
        layoutMain.addLayout(layoutLineEdit)
        layoutMain.addLayout(layoutTextEdit)
        layoutMain.addLayout(layoutPlainTextEdit)
        layoutMain.addLayout(layoutSpinBox)
        layoutMain.addLayout(layoutDoubleSpinBox)
        layoutMain.addLayout(layoutTimeEdit)
        layoutMain.addLayout(layoutDateTimeEdit)
        layoutMain.addLayout(layoutLog)

        self.setLayout(layoutMain)

        # Connect signals
        self.pushButtonComboBox.clicked.connect(self.onPushButtonComboBoxClicked)
        self.pushButtonLineEdit.clicked.connect(self.onPushButtonLineEditClicked)
        self.pushButtonTextEdit.clicked.connect(self.onPushButtonTextEditClicked)
        self.pushButtonPlainTextEdit.clicked.connect(self.onPushButtonPlainTextEditClicked)
        self.pushButtonSpinBox.clicked.connect(self.onPushButtonSpinBoxClicked)
        self.pushButtonDoubleSpinBox.clicked.connect(self.onPushButtonDoubleSpinBoxClicked)
        self.pushButtonTimeEdit.clicked.connect(self.onPushButtonTimeEditClicked)
        self.pushButtonDateTimeEdit.clicked.connect(self.onPushButtonDateTimeEditClicked)
        self.pushButtonClearLog.clicked.connect(self.plainTextEditLog.clear)

    # Slot for lineEdit button
    def onPushButtonLineEditClicked(self) -> None:
        self.plainTextEditLog.setPlainText(self.lineEdit.text())

    # Slot for comboBox button
    def onPushButtonComboBoxClicked(self) -> None:
        self.plainTextEditLog.setPlainText(self.comboBox.currentText())

    # Slot for textEdit button
    def onPushButtonTextEditClicked(self) -> None:
        self.plainTextEditLog.setPlainText(self.textEdit.toPlainText())

    # Slot for plainTextEdit button
    def onPushButtonPlainTextEditClicked(self) -> None:
        self.plainTextEditLog.setPlainText(self.plainTextEdit.toPlainText())

    # Slot for spinBox button
    def onPushButtonSpinBoxClicked(self) -> None:
        self.plainTextEditLog.setPlainText(str(self.spinBox.value()))

    # Slot for doubleSpinBox button
    def onPushButtonDoubleSpinBoxClicked(self) -> None:
        self.plainTextEditLog.setPlainText(str(self.doubleSpinBox.value()))

    # Slot for timeEdit button
    def onPushButtonTimeEditClicked(self) -> None:
        self.plainTextEditLog.setPlainText(self.timeEdit.time().toString())

    # Slot for dateTimeEdit button
    def onPushButtonDateTimeEditClicked(self) -> None:
        self.plainTextEditLog.setPlainText(self.dateTimeEdit.dateTime().toString())

if __name__ == "__main__":
    app = QApplication([])
    window = AddWindow()
    window.show()
    app.exec()

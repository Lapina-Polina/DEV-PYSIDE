from PyQt6 import QtCore, QtGui, QtWidgets

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(300, 160)
        Dialog.setWindowTitle("Логин")

        self.verticalLayout = QtWidgets.QVBoxLayout(Dialog)
        self.verticalLayout.setContentsMargins(20, 20, 20, 20)
        self.verticalLayout.setSpacing(10)

        # Поле Логин
        self.label = QtWidgets.QLabel(Dialog)
        self.label.setText("Логин")
        self.verticalLayout.addWidget(self.label)

        self.lineEdit = QtWidgets.QLineEdit(Dialog)
        self.verticalLayout.addWidget(self.lineEdit)

        # Поле Пароль
        self.label_2 = QtWidgets.QLabel(Dialog)
        self.label_2.setText("Пароль")
        self.verticalLayout.addWidget(self.label_2)

        self.lineEdit_2 = QtWidgets.QLineEdit(Dialog)
        self.lineEdit_2.setEchoMode(QtWidgets.QLineEdit.EchoMode.Password)
        self.verticalLayout.addWidget(self.lineEdit_2)

        # Кнопка
        self.pushButton = QtWidgets.QPushButton(Dialog)
        self.pushButton.setText("Войти")

        # Создаем горизонтальный layout для кнопки и выравниваем влево
        self.buttonLayout = QtWidgets.QHBoxLayout()
        self.buttonLayout.addWidget(self.pushButton)
        self.buttonLayout.addStretch()  # чтобы остальное пространство оставалось справа
        self.verticalLayout.addLayout(self.buttonLayout)

        QtCore.QMetaObject.connectSlotsByName(Dialog)

import sys
from PySide6.QtWidgets import (
    QApplication, QWidget, QLabel, QSlider, QVBoxLayout,
    QHBoxLayout, QFrame, QSizePolicy, QPushButton
)
from PySide6.QtCore import Qt


class EngineControlUI(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Управление основными двигателями")
        self.setGeometry(100, 100, 920, 380)

        # Флаг, чтобы избежать рекурсивных обновлений при изменении слайдеров
        self._internal_update = False

        # Главный горизонтальный layout (левая часть: двигатели, правая часть: нагрузка и тяга)
        main_layout = QHBoxLayout()
        main_layout.setContentsMargins(14, 14, 14, 14)
        main_layout.setSpacing(18)
        self.setLayout(main_layout)

        # Левая часть: слайдеры двигателей
        motors_container = QWidget()
        motors_layout = QHBoxLayout()
        motors_layout.setSpacing(24)
        motors_layout.setContentsMargins(0, 0, 0, 0)
        motors_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        motors_container.setLayout(motors_layout)

        self.motor_sliders = []       # список слайдеров двигателей
        self.motor_value_labels = []  # цифровые метки значений слайдеров
        self.motor_text_labels = []   # подписи под слайдерами

        per_block_width = 120  # ширина каждого блока двигателя

        for i in range(1, 5):
            # Создаем вертикальный блок для каждого двигателя
            block = QWidget()
            block.setFixedWidth(per_block_width)
            vbox = QVBoxLayout()
            vbox.setContentsMargins(0, 0, 0, 0)
            vbox.setSpacing(6)
            vbox.setAlignment(Qt.AlignmentFlag.AlignCenter)
            block.setLayout(vbox)

            # Метка с цифровым значением слайдера
            val_label = QLabel("50")
            val_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
            val_label.setFixedHeight(22)
            val_label.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
            self.motor_value_labels.append(val_label)

            # Вертикальный слайдер двигателя
            slider = QSlider(Qt.Orientation.Vertical)
            slider.setMinimum(0)
            slider.setMaximum(100)
            slider.setValue(50)
            slider.setFixedHeight(200)
            slider.setFixedWidth(28)
            slider.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Expanding)
            slider.setTickPosition(QSlider.TickPosition.TicksBothSides)
            slider.setTickInterval(10)
            self.motor_sliders.append(slider)

            # Подпись под слайдером
            text_label = QLabel(f"Двигатель {i}")
            text_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
            text_label.setFixedHeight(20)
            text_label.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
            self.motor_text_labels.append(text_label)

            # Добавляем метку, слайдер и подпись в вертикальный блок
            vbox.addWidget(val_label)
            vbox.addWidget(slider, alignment=Qt.AlignmentFlag.AlignHCenter)
            vbox.addWidget(text_label)

            # Добавляем блок двигателя в горизонтальный layout
            motors_layout.addWidget(block, alignment=Qt.AlignmentFlag.AlignCenter)

        # Подключаем обработчики изменения значений слайдеров
        for idx, s in enumerate(self.motor_sliders):
            s.valueChanged.connect(self._make_motor_changed_handler(idx))

        main_layout.addWidget(motors_container, stretch=3)

        # Разделительная линия
        line = QFrame()
        line.setFrameShape(QFrame.Shape.VLine)
        line.setFrameShadow(QFrame.Shadow.Sunken)
        main_layout.addWidget(line)

        # Правая часть: нагрузка и общая тяга
        right_container = QWidget()
        right_layout = QVBoxLayout()
        right_layout.setSpacing(12)
        right_layout.setContentsMargins(8, 0, 0, 0)
        right_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        right_container.setLayout(right_layout)

        # Заголовок правой части
        header = QLabel("Нагрузка и общая тяга")
        header.setAlignment(Qt.AlignmentFlag.AlignCenter)
        header.setFixedHeight(24)
        right_layout.addWidget(header)

        # Горизонтальный слайдер нагрузки (лимит общей тяги)
        load_label = QLabel("Нагрузка (лимит общей тяги)")
        load_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        load_label.setFixedHeight(18)

        self.load_slider = QSlider(Qt.Orientation.Horizontal)
        self.load_slider.setMinimum(0)
        self.load_slider.setMaximum(100)
        self.load_slider.setValue(50)
        self.load_slider.setFixedHeight(28)
        self.load_slider.setTickPosition(QSlider.TickPosition.TicksBelow)
        self.load_slider.setTickInterval(10)
        self.load_slider.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        self.load_slider.valueChanged.connect(self.on_load_changed)

        # Метка отображения текущего значения нагрузки
        self.load_value_label = QLabel(str(self.load_slider.value()))
        self.load_value_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.load_value_label.setFixedHeight(18)

        right_layout.addWidget(load_label)
        right_layout.addWidget(self.load_slider)
        right_layout.addWidget(self.load_value_label)

        # Вертикальный слайдер общей тяги
        total_block = QWidget()
        total_vbox = QVBoxLayout()
        total_vbox.setContentsMargins(0, 0, 0, 0)
        total_vbox.setAlignment(Qt.AlignmentFlag.AlignCenter)
        total_block.setLayout(total_vbox)

        self.total_value_label = QLabel("50")
        self.total_value_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.total_value_label.setFixedHeight(22)

        self.total_slider = QSlider(Qt.Orientation.Vertical)
        self.total_slider.setMinimum(0)
        self.total_slider.setMaximum(self.load_slider.value())
        self.total_slider.setValue(50)
        self.total_slider.setFixedHeight(220)
        self.total_slider.setFixedWidth(36)
        self.total_slider.setTickPosition(QSlider.TickPosition.TicksBothSides)
        self.total_slider.setTickInterval(10)
        self.total_slider.valueChanged.connect(self.on_total_changed)

        total_text = QLabel("Общая тяга")
        total_text.setAlignment(Qt.AlignmentFlag.AlignCenter)
        total_text.setFixedHeight(18)

        total_vbox.addWidget(self.total_value_label)
        total_vbox.addWidget(self.total_slider, alignment=Qt.AlignmentFlag.AlignHCenter)
        total_vbox.addWidget(total_text)
        right_layout.addWidget(total_block)

        # Кнопки управления
        buttons_block = QWidget()
        buttons_layout = QHBoxLayout()
        buttons_layout.setContentsMargins(0, 0, 0, 0)
        buttons_layout.setSpacing(8)
        buttons_block.setLayout(buttons_layout)

        btn_reset = QPushButton("Сброс")
        btn_reset.clicked.connect(self.reset_motors)
        btn_even = QPushButton("Распределить поровну")
        btn_even.clicked.connect(self.even_distribution)

        buttons_layout.addWidget(btn_reset)
        buttons_layout.addWidget(btn_even)
        right_layout.addWidget(buttons_block)

        main_layout.addWidget(right_container, stretch=2)

        # Инициализация меток и синхронизация общей тяги
        self._update_motor_labels()
        self._sync_total_from_motors(initial=True)

    # Обработчики изменений

    def _make_motor_changed_handler(self, idx):
        """Создает обработчик для конкретного мотора по индексу"""
        def handler(value):
            if self._internal_update:
                return
            self.on_motor_changed(idx, value)
        return handler

    def _update_motor_labels(self):
        """Обновляет цифровые метки всех двигателей"""
        for lbl, sld in zip(self.motor_value_labels, self.motor_sliders):
            lbl.setText(str(sld.value()))

    def on_motor_changed(self, idx, value):
        """Обработка изменения одного двигателя пользователем"""
        if self._internal_update:
            return

        self._internal_update = True
        try:
            # обновляем цифровую метку конкретного двигателя
            self.motor_value_labels[idx].setText(str(value))

            # пересчитываем среднюю тягу по двигателям
            motor_values = [s.value() for s in self.motor_sliders]
            avg = round(sum(motor_values) / len(motor_values))

            # если средняя тяга > лимита нагрузки, масштабируем вниз
            load_max = self.load_slider.value()
            if avg > load_max and load_max >= 0:
                factor = load_max / avg if avg != 0 else 0
                for s in self.motor_sliders:
                    s.setValue(round(s.value() * factor))
                motor_values = [s.value() for s in self.motor_sliders]
                avg = round(sum(motor_values) / len(motor_values))

            # обновляем общую тягу и метки
            self.total_slider.setValue(avg)
            self.total_value_label.setText(str(self.total_slider.value()))
            self._update_motor_labels()
        finally:
            self._internal_update = False

    def on_total_changed(self, value):
        """Обработка изменения общей тяги пользователем — пропорционально меняем моторы"""
        if self._internal_update:
            return

        self._internal_update = True
        try:
            self.total_value_label.setText(str(value))

            current_vals = [s.value() for s in self.motor_sliders]
            current_sum = sum(current_vals)
            desired_sum = value * len(self.motor_sliders)

            if current_sum == 0:
                # если все значения 0, распределяем поровну
                per = round(desired_sum / len(self.motor_sliders)) if self.motor_sliders else 0
                for s in self.motor_sliders:
                    s.setValue(per)
            else:
                factor = desired_sum / current_sum
                for s in self.motor_sliders:
                    new_v = round(s.value() * factor)
                    new_v = max(0, min(100, new_v))
                    s.setValue(new_v)

            self._update_motor_labels()

            # проверка лимита нагрузки
            motor_avg = round(sum([s.value() for s in self.motor_sliders]) / len(self.motor_sliders))
            load_max = self.load_slider.value()
            if motor_avg > load_max:
                factor2 = load_max / motor_avg if motor_avg != 0 else 0
                for s in self.motor_sliders:
                    s.setValue(round(s.value() * factor2))
                self._update_motor_labels()
                self.total_slider.setValue(load_max)
                self.total_value_label.setText(str(self.total_slider.value()))
        finally:
            self._internal_update = False

    def on_load_changed(self, value):
        """Обработка изменения лимита нагрузки"""
        if self._internal_update:
            return

        self._internal_update = True
        try:
            self.load_value_label.setText(str(value))
            self.total_slider.setMaximum(value)

            # если текущая общая тяга > нового лимита, масштабируем моторы
            current_total = self.total_slider.value()
            if current_total > value:
                self.total_slider.setValue(value)
                desired_sum = value * len(self.motor_sliders)
                current_sum = sum([s.value() for s in self.motor_sliders])
                if current_sum == 0:
                    per = round(desired_sum / len(self.motor_sliders)) if self.motor_sliders else 0
                    for s in self.motor_sliders:
                        s.setValue(per)
                else:
                    factor = desired_sum / current_sum
                    for s in self.motor_sliders:
                        s.setValue(max(0, min(100, round(s.value() * factor))))
                self._update_motor_labels()
                self.total_value_label.setText(str(self.total_slider.value()))
        finally:
            self._internal_update = False

    # Утилиты

    def reset_motors(self):
        """Сброс всех двигателей и общей тяги на 0"""
        self._internal_update = True
        try:
            for s in self.motor_sliders:
                s.setValue(0)
            self.total_slider.setValue(0)
            self.total_value_label.setText("0")
            self._update_motor_labels()
        finally:
            self._internal_update = False

    def even_distribution(self):
        """Равномерное распределение текущей общей тяги по всем моторам"""
        self._internal_update = True
        try:
            val = self.total_slider.value()
            per = round(val)
            for s in self.motor_sliders:
                s.setValue(per)
            self._update_motor_labels()
        finally:
            self._internal_update = False

    def _sync_total_from_motors(self, initial=False):
        """Инициализация общей тяги при запуске, по среднему значениям моторов"""
        motor_values = [s.value() for s in self.motor_sliders]
        avg = round(sum(motor_values) / len(motor_values))
        load_max = self.load_slider.value()
        if avg > load_max:
            avg = load_max
        self.total_slider.setMaximum(load_max)
        self.total_slider.setValue(avg)
        self.total_value_label.setText(str(self.total_slider.value()))
        self._update_motor_labels()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = EngineControlUI()
    window.show()
    sys.exit(app.exec())

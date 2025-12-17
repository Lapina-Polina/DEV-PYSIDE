import os
import time

from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QPushButton,
    QLineEdit,
    QLabel,
    QProgressBar,
    QPlainTextEdit,
    QFileDialog,
    QMessageBox
)
from PySide6.QtCore import QThread, Qt, QSettings

from widgets.lab4.folder_scanner_worker import FolderScannerWorker
from widgets.lab4.scan_statistics import ScanStatistics


class MainWindowLab4(QWidget):
    """
    Главное окно проекта Lab4 (Экзамен).
    Проект: «Сканер папки»
    """

    def __init__(self):
        super().__init__()

        self.thread = None
        self.worker = None

        self.settings = QSettings("Exam", "FolderScanner")
        self.scan_history = []

        self.init_ui()
        self.load_settings()

    # ---------- UI ----------

    def init_ui(self):
        self.setWindowTitle("Сканер папки")
        self.resize(750, 550)

        main_layout = QVBoxLayout()
        main_layout.setAlignment(Qt.AlignmentFlag.AlignTop)

        # ---------- Path selection ----------
        path_layout = QHBoxLayout()

        self.path_edit = QLineEdit()
        self.path_edit.setReadOnly(True)

        select_btn = QPushButton("Выбрать папку")
        select_btn.clicked.connect(self.select_folder)

        path_layout.addWidget(self.path_edit)
        path_layout.addWidget(select_btn)

        # ---------- Control buttons ----------
        control_layout = QHBoxLayout()

        self.start_btn = QPushButton("Начать сканирование")
        self.start_btn.clicked.connect(self.start_scan)

        self.stop_btn = QPushButton("Остановить")
        self.stop_btn.setEnabled(False)
        self.stop_btn.clicked.connect(self.stop_scan)

        control_layout.addWidget(self.start_btn)
        control_layout.addWidget(self.stop_btn)

        # ---------- Progress ----------
        self.progress_bar = QProgressBar()
        self.progress_bar.setValue(0)

        # ---------- Stats ----------
        self.stats_label = QLabel("Файлы: 0 | Размер: 0 Б")
        self.stats_label.setStyleSheet("font-weight: bold;")

        # ---------- Log ----------
        self.log_edit = QPlainTextEdit()
        self.log_edit.setReadOnly(True)

        # ---------- Layout ----------
        main_layout.addLayout(path_layout)
        main_layout.addLayout(control_layout)
        main_layout.addWidget(self.progress_bar)
        main_layout.addWidget(self.stats_label)
        main_layout.addWidget(self.log_edit)

        self.setLayout(main_layout)

    # ---------- Settings ----------

    def load_settings(self):
        last_path = self.settings.value("last_folder", "")
        if last_path:
            self.path_edit.setText(last_path)

    def save_settings(self, folder: str):
        self.settings.setValue("last_folder", folder)

    # ---------- Logic ----------

    def select_folder(self):
        folder = QFileDialog.getExistingDirectory(
            self,
            "Выберите папку для сканирования"
        )
        if folder:
            self.path_edit.setText(folder)
            self.save_settings(folder)
            self.log(f"Выбрана папка для анализа: {folder}")

    def start_scan(self):
        folder = self.path_edit.text()

        if not folder or not os.path.exists(folder):
            QMessageBox.warning(self, "Ошибка", "Папка не выбрана или не существует")
            return

        if self.thread:
            self.log("Сканирование уже выполняется")
            return

        self.progress_bar.setValue(0)
        self.stats_label.setText("Файлы: 0 | Размер: 0 Б")

        self.start_btn.setEnabled(False)
        self.stop_btn.setEnabled(True)

        # ---- LOG START ----
        self.log("Сканирование начато")
        self.log("Начат рекурсивный анализ файловой структуры в фоновом потоке")

        self.thread = QThread()
        self.worker = FolderScannerWorker(folder)
        self.worker.moveToThread(self.thread)

        # Signals
        self.thread.started.connect(self.worker.run)
        self.worker.progress_changed.connect(self.update_progress)
        self.worker.scan_finished.connect(self.scan_finished)
        self.worker.error_occurred.connect(self.scan_error)

        # Cleanup
        self.worker.scan_finished.connect(self.cleanup)
        self.worker.error_occurred.connect(self.cleanup)

        self.thread.start()

    def stop_scan(self):
        if self.worker:
            self.worker.stop()
            self.log("Сканирование остановлено пользователем")

    def update_progress(self, current: int, total: int):
        self.progress_bar.setMaximum(total)
        self.progress_bar.setValue(current)

    def scan_finished(
        self,
        file_count: int,
        total_size: int,
        start_time: float,
        end_time: float,
        folder_path: str
    ):
        # ---- LOG ANALYSIS RESULT ----
        self.log("Формирование итоговой статистики анализа")

        stats = ScanStatistics(
            file_count=file_count,
            total_size=total_size,
            start=start_time,
            end=end_time
        )

        self.scan_history.append(stats)

        self.stats_label.setText(stats.summary())

        self.log(
            f"Сканирование завершено\n"
            f"Путь анализа: {folder_path}\n"
            f"{stats.summary()}"
        )

        self.save_log_to_file(stats)

    def scan_error(self, message: str):
        self.log(f"Ошибка: {message}")
        QMessageBox.critical(self, "Ошибка", message)

    def cleanup(self):
        if self.thread:
            self.thread.quit()
            self.thread.wait()

        self.thread = None
        self.worker = None

        self.start_btn.setEnabled(True)
        self.stop_btn.setEnabled(False)

        self.log("Готово")

    # ---------- Helpers ----------

    def log(self, text: str):
        timestamp = time.strftime("%H:%M:%S")
        self.log_edit.appendPlainText(f"[{timestamp}] {text}")

    def save_log_to_file(self, stats: ScanStatistics):
        try:
            with open("scan_log.txt", "a", encoding="utf-8") as f:
                f.write(stats.detailed_report())
                f.write("\n" + "-" * 40 + "\n")
        except Exception as e:
            self.log(f"Ошибка сохранения лога: {e}")

    # ---------- Close ----------

    def closeEvent(self, event):
        if self.worker:
            self.worker.stop()
        event.accept()
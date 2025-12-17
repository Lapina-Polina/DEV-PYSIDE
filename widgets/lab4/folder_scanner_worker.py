import os
import time
from PySide6.QtCore import QObject, Signal


class FolderScannerWorker(QObject):
    """
    Worker для фонового сканирования папки.

    Функциональность:
    - рекурсивно обходит все файлы в папке
    - считает общее количество файлов
    - считает суммарный размер файлов
    - отправляет прогресс в UI
    - корректно останавливается по запросу
    """

    # ---------- Signals ----------
    progress_changed = Signal(int, int)        # current, total
    scan_finished = Signal(
        int,        # file_count
        int,        # total_size (bytes)
        float,      # start_time
        float,      # end_time
        str         # folder_path
    )
    error_occurred = Signal(str)

    # ---------- Init ----------
    def __init__(self, folder_path: str):
        super().__init__()
        self.folder_path = folder_path
        self._is_running = True

    # ---------- Public API ----------
    def stop(self):
        """Запрос на остановку сканирования"""
        self._is_running = False

    # ---------- Main logic ----------
    def run(self):
        """
        Основной метод сканирования.
        Выполняется в отдельном потоке.
        """
        try:
            start_time = time.time()

            # Собираем список всех файлов заранее
            files = self._collect_files()
            total_files = len(files)

            total_size = 0

            for index, file_path in enumerate(files, start=1):
                if not self._is_running:
                    # Остановка по запросу пользователя
                    return

                try:
                    total_size += os.path.getsize(file_path)
                except (OSError, FileNotFoundError):
                    # Файл мог быть удалён или недоступен
                    pass

                # Отправляем прогресс
                self.progress_changed.emit(index, total_files)

            end_time = time.time()

            # Сигнал завершения
            self.scan_finished.emit(
                total_files,
                total_size,
                start_time,
                end_time,
                self.folder_path
            )

        except Exception as exc:
            self.error_occurred.emit(str(exc))

    # ---------- Helpers ----------
    def _collect_files(self) -> list:
        """
        Рекурсивно собирает все файлы в папке.
        """
        collected_files = []

        for root, _, files in os.walk(self.folder_path):
            if not self._is_running:
                break

            for file_name in files:
                full_path = os.path.join(root, file_name)
                collected_files.append(full_path)

        return collected_files
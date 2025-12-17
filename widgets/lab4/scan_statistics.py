from dataclasses import dataclass
from datetime import datetime


@dataclass
class ScanStatistics:
    """
    Класс для хранения и форматирования результатов сканирования папки.
    Используется в Lab4 (Экзаменационное задание).
    """

    file_count: int
    total_size: int  # bytes
    start: float     # timestamp
    end: float       # timestamp

    # ---------- Time ----------

    @property
    def duration(self) -> float:
        """Длительность сканирования в секундах"""
        return round(self.end - self.start, 2)

    @property
    def start_time_str(self) -> str:
        """Время начала в читаемом формате"""
        return datetime.fromtimestamp(self.start).strftime("%Y-%m-%d %H:%M:%S")

    @property
    def end_time_str(self) -> str:
        """Время окончания в читаемом формате"""
        return datetime.fromtimestamp(self.end).strftime("%Y-%m-%d %H:%M:%S")

    # ---------- Size ----------

    @property
    def total_size_kb(self) -> float:
        return round(self.total_size / 1024, 2)

    @property
    def total_size_mb(self) -> float:
        return round(self.total_size / (1024 ** 2), 2)

    # ---------- Output ----------

    def summary(self) -> str:
        """
        Краткая строка статистики (для QLabel)
        """
        return (
            f"Файлов: {self.file_count} | "
            f"Размер: {self.total_size_mb} МБ | "
            f"Время: {self.duration} сек"
        )

    def detailed_report(self) -> str:
        """
        Подробный отчет (для лога / файла)
        """
        return (
            "РЕЗУЛЬТАТ СКАНИРОВАНИЯ\n"
            f"Начало: {self.start_time_str}\n"
            f"Окончание: {self.end_time_str}\n"
            f"Длительность: {self.duration} сек\n"
            f"Количество файлов: {self.file_count}\n"
            f"Общий размер: {self.total_size} байт "
            f"({self.total_size_mb} МБ)\n"
        )

    def __str__(self) -> str:
        return self.detailed_report()

"""
storage.py — Універсальний клас для збереження та завантаження даних у CSV-файлах.

ЗАВДАННЯ ДЛЯ РОЗРОБНИКА:
    Цей файл — твоя зона відповідальності. Клас FileStorage вже має базову структуру.
    Твоє завдання:
      1. Реалізувати метод save() — запис списку словників у CSV файл.
      2. Реалізувати метод load() — читання даних з CSV файлу у список словників.
      3. (Опційно) Додати обробку помилок: що робити якщо файл не існує, пошкоджений тощо.

    Клас повинен бути УНІВЕРСАЛЬНИМ — він не знає нічого про контакти чи нотатки,
    тільки зберігає та повертає список словників (list of dicts).

ПРИКЛАД ВИКОРИСТАННЯ:
    storage = FileStorage("data/contacts.csv")
    storage.save([{"name": "John", "phone": "123"}])
    data = storage.load()  # повертає [{"name": "John", "phone": "123"}]
"""

import csv
import os
from typing import Optional
from pathlib import Path

base_dir = Path(__file__).parent

class FileStorage:
    """
    Універсальний клас для роботи з CSV-файлами.

    Атрибути:
        filepath (str): Шлях до CSV файлу.
    """

    def __init__(self, filepath: str):
        """
        Ініціалізація сховища.

        Args:
            filepath: Шлях до CSV файлу (наприклад, "data/contacts.csv").
        """
        self.filepath = filepath
        # Автоматично створюємо папку, якщо вона не існує
        os.makedirs(os.path.dirname(filepath), exist_ok=True)

    def save(self, data: list[dict], fieldnames: Optional[list[str]] = None) -> None:
        """
        Зберігає список словників у CSV файл.

        Args:
            data: Список словників для збереження.
                  Приклад: [{"name": "John", "phone": "123"}, ...]
            fieldnames: Список назв колонок. Якщо None — береться з першого елементу data.
        Підказка: використай csv.DictWriter
        """
        if not data and not fieldnames:
            return

        file_path = base_dir / self.filepath

        with file_path.open("w", newline="", encoding="utf-8") as csvfile:
            fieldnames = fieldnames or list(data[0].keys())
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

            writer.writeheader()
            for item in data:
                writer.writerow(item)

    def load(self) -> list[dict]:
        """
        Завантажує дані з CSV файлу.

        Returns:
            Список словників з даними.
            Якщо файл не існує — повертає порожній список [].
        """
        file_path = base_dir / self.filepath

        if not file_path.exists():
            return []

        with file_path.open("r", newline="", encoding="utf-8") as csvfile:
            reader = csv.DictReader(csvfile)
            return [row for row in reader]

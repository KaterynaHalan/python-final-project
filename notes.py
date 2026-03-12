"""
notes.py — Модуль для управління нотатками.

ЗАВДАННЯ ДЛЯ РОЗРОБНИКА:
    Цей файл — твоя зона відповідальності.
    Реалізуй усі методи, позначені коментарем "TODO".

    Клас Note:
      - Поля: title, content, tags (рядок через кому, напр. "робота,важливо").

    Клас NoteManager:
      - Методи: add, find, edit, delete, get_all, find_by_tag

ВАЖЛИВО:
    - Використовуй FileStorage з storage.py для збереження.
    - Не змінюй назви методів — main.py їх викликає.

БОНУСНЕ ЗАВДАННЯ (+10 балів):
    - Реалізуй теги (поле tags у Note).
    - Метод find_by_tag() — пошук нотаток за тегом.
    - Метод get_all() може сортувати нотатки за тегом (опційно).
"""
import os
from storage import FileStorage


# ==================== МОДЕЛЬ ДАНИХ ====================

class Note:
    """
    Представляє одну нотатку.

    Атрибути:
        title   (str): Заголовок нотатки (обов'язковий).
        content (str): Текст нотатки.
        tags    (str): Теги через кому — "робота,важливо,python".
                       Порожній рядок якщо тегів немає.
    """

    # Список полів для збереження в CSV
    FIELDS = ["title", "content", "tags"]

    def __init__(self, title: str, content: str = "", tags: str = ""):
        """
        Ініціалізація нотатки.

        Args:
            title:   Заголовок (обов'язковий).
            content: Текст нотатки (необов'язково).
            tags:    Теги через кому (необов'язково). Бонусне завдання.
        """
        self.title = title
        self.content = content
        self.tags = tags  # Бонус: рядок тегів через кому

    def get_tags_list(self) -> list[str]:
        """
        Повертає теги у вигляді списку рядків.

        Returns:
            ["робота", "важливо"] або [] якщо тегів немає.
        """
        return [] if not self.tags else [t.strip().lower() for t in self.tags.split(",")]

    def to_dict(self) -> dict:
        """
        Конвертує нотатку у словник для збереження в CSV.

        Returns:
            {"title": ..., "content": ..., "tags": ...}
        """
        return {
            "title": self.title,
            "content": self.content,
            "tags": self.tags,
        }

    @classmethod
    def from_dict(cls, data: dict) -> "Note":
        """
        Створює об'єкт Note зі словника (при завантаженні з CSV).

        Args:
            data: Словник з даними нотатки.

        Returns:
            Новий об'єкт Note.
        """
        return Note(data["title"], data["content"], data["tags"])

    def has_query(self, query: str) -> bool:
        query_lower = query.lower()
        return (
            query_lower in self.tags.lower() or
            query_lower in self.content.lower() or
            query_lower in self.title.lower()
        )

    def has_tag(self, tag: str) -> bool:
        return tag.lower() in self.get_tags_list()

    def __str__(self) -> str:
        """Повертає зрозумілий рядок для виводу в консоль."""
        # "[робота, python] Заголовок: Перший рядок тексту..."
        return f"[{self.tags}] {self.title}: {self.content}"


# ==================== МЕНЕДЖЕР НОТАТОК ====================
class NoteManager:
    """
    Управляє колекцією нотаток.
    Завантажує дані при старті, зберігає при кожній зміні.

    Атрибути:
        storage (FileStorage): Об'єкт для роботи з CSV файлом.
        notes   (list[Note]):  Список нотаток у пам'яті.
    """

    def __init__(self, filepath: str = "data/notes.csv"):
        self.storage = FileStorage(filepath)
        self.notes: list[Note] = []
        self._load()

    def add(self, note: Note) -> None:
        """
        Додає нотатку до списку та зберігає у файл.
        """
        self.notes.append(note)
        self._save()

    def find(self, query: str) -> list["Note"]:
        """
        Шукає нотатки за заголовком, текстом або тегами (часткове співпадіння).

        Args:
            query: Рядок для пошуку.

        Returns:
            Список нотаток, що відповідають запиту.
        """
        return [n for n in self.notes if n.has_query(query)]

    def find_by_tag(self, tag: str) -> list["Note"]:
        """
        Шукає нотатки за точним тегом (бонусне завдання).

        Args:
            tag: Рядок тегу для пошуку (наприклад, "робота").

        Returns:
            Список нотаток з цим тегом.
        """
        return [n for n in self.notes if n.has_tag(tag)]

    def edit(self, title: str, updated_note: "Note") -> bool:
        """
        Замінює нотатку з вказаним заголовком на новий об'єкт.

        Args:
            title:        Заголовок нотатки, яку треба оновити.
            updated_note: Новий об'єкт Note з оновленими даними.

        Returns:
            True якщо знайдено і оновлено, False якщо не знайдено.
        """
        note = next(n for n in self.notes if n.title == title)
        if note:
            self.notes[self.notes.index(note)] = updated_note
            self._save()
            return True
        return False

    def delete(self, title: str) -> bool:
        """
        Видаляє нотатку за точним заголовком.

        Returns:
            True якщо видалено, False якщо не знайдено.
        """
        note = next(n for n in self.notes if n.title == title)
        if note:
            self.notes.remove(note)
            self._save()
            return True
        return False

    def get_all(self, sort_by_tag: bool = False) -> list["Note"]:
        """
        Повертає всі нотатки.

        Args:
            sort_by_tag: Якщо True — сортує нотатки за першим тегом (бонус).

        Returns:
            Список нотаток.
        """
        return sorted(self.notes, key=lambda n: n.get_tags_list()[0]) if sort_by_tag else self.notes

    # ---- Приватні допоміжні методи ----

    def _save(self) -> None:
        """Зберігає всі нотатки у CSV через FileStorage."""
        self.storage.save([n.to_dict() for n in self.notes], Note.FIELDS)

    def _load(self) -> None:
        """Завантажує нотатки з CSV через FileStorage."""
        data = self.storage.load()
        self.notes = [Note.from_dict(d) for d in data]

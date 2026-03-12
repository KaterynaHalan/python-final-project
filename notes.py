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

        TODO (бонус): Реалізувати!
        Підказка: self.tags.split(",") з очищенням пробілів
        """
        # --- ТВІЙ КОД ТУТ (бонус) ---
        raise NotImplementedError("Метод get_tags_list() ще не реалізований!")

    def to_dict(self) -> dict:
        """
        Конвертує нотатку у словник для збереження в CSV.

        Returns:
            {"title": ..., "content": ..., "tags": ...}

        TODO: Реалізувати!
        """
        # --- ТВІЙ КОД ТУТ ---
        raise NotImplementedError("Метод to_dict() ще не реалізований!")

    @classmethod
    def from_dict(cls, data: dict) -> "Note":
        """
        Створює об'єкт Note зі словника (при завантаженні з CSV).

        Args:
            data: Словник з даними нотатки.

        Returns:
            Новий об'єкт Note.

        TODO: Реалізувати!
        """
        # --- ТВІЙ КОД ТУТ ---
        raise NotImplementedError("Метод from_dict() ще не реалізований!")

    def __str__(self) -> str:
        """Повертає зрозумілий рядок для виводу в консоль."""
        # TODO: Реалізувати — наприклад:
        # "[робота, python] Заголовок: Перший рядок тексту..."
        raise NotImplementedError("Метод __str__() ще не реалізований!")


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
        # TODO: Завантажити нотатки при ініціалізації
        # self._load()

    def add(self, note: Note) -> None:
        """
        Додає нотатку до списку та зберігає у файл.

        TODO: Реалізувати!
        """
        # --- ТВІЙ КОД ТУТ ---
        raise NotImplementedError("Метод add() ще не реалізований!")

    def find(self, query: str) -> list["Note"]:
        """
        Шукає нотатки за заголовком, текстом або тегами (часткове співпадіння).

        Args:
            query: Рядок для пошуку.

        Returns:
            Список нотаток, що відповідають запиту.

        TODO: Реалізувати!
        """
        # --- ТВІЙ КОД ТУТ ---
        raise NotImplementedError("Метод find() ще не реалізований!")

    def find_by_tag(self, tag: str) -> list["Note"]:
        """
        Шукає нотатки за точним тегом (бонусне завдання).

        Args:
            tag: Рядок тегу для пошуку (наприклад, "робота").

        Returns:
            Список нотаток з цим тегом.

        TODO (бонус): Реалізувати!
        Підказка: виклич note.get_tags_list() для кожної нотатки
        """
        # --- ТВІЙ КОД ТУТ (бонус) ---
        raise NotImplementedError("Метод find_by_tag() ще не реалізований!")

    def edit(self, title: str, updated_note: "Note") -> bool:
        """
        Замінює нотатку з вказаним заголовком на новий об'єкт.

        Args:
            title:        Заголовок нотатки, яку треба оновити.
            updated_note: Новий об'єкт Note з оновленими даними.

        Returns:
            True якщо знайдено і оновлено, False якщо не знайдено.

        TODO: Реалізувати!
        """
        # --- ТВІЙ КОД ТУТ ---
        raise NotImplementedError("Метод edit() ще не реалізований!")

    def delete(self, title: str) -> bool:
        """
        Видаляє нотатку за точним заголовком.

        Returns:
            True якщо видалено, False якщо не знайдено.

        TODO: Реалізувати!
        """
        # --- ТВІЙ КОД ТУТ ---
        raise NotImplementedError("Метод delete() ще не реалізований!")

    def get_all(self, sort_by_tag: bool = False) -> list["Note"]:
        """
        Повертає всі нотатки.

        Args:
            sort_by_tag: Якщо True — сортує нотатки за першим тегом (бонус).

        Returns:
            Список нотаток.

        TODO: Реалізувати!
        """
        # --- ТВІЙ КОД ТУТ ---
        raise NotImplementedError("Метод get_all() ще не реалізований!")

    # ---- Приватні допоміжні методи ----

    def _save(self) -> None:
        """Зберігає всі нотатки у CSV через FileStorage."""
        # TODO: self.storage.save([n.to_dict() for n in self.notes], Note.FIELDS)
        raise NotImplementedError("Метод _save() ще не реалізований!")

    def _load(self) -> None:
        """Завантажує нотатки з CSV через FileStorage."""
        # TODO: data = self.storage.load(); self.notes = [Note.from_dict(d) for d in data]
        raise NotImplementedError("Метод _load() ще не реалізований!")

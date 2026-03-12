"""
contacts.py — Модуль для управління контактами.

ЗАВДАННЯ ДЛЯ РОЗРОБНИКА:
    Цей файл — твоя зона відповідальності.
    Реалізуй усі методи, позначені коментарем "TODO".

    Клас Contact:
      - Представляє один контакт.
      - Поля: name, address, phone, email, birthday (рядок у форматі "DD.MM.YYYY")

    Клас ContactManager:
      - Керує списком контактів.
      - Зберігає/завантажує через FileStorage.
      - Методи: add, find, edit, delete, get_all, birthdays_soon

    Валідація (дивись клас Validator нижче):
      - Перевірка формату телефону при додаванні/редагуванні.
      - Перевірка формату email при додаванні/редагуванні.

ВАЖЛИВО:
    - Використовуй FileStorage з storage.py для збереження.
    - Не змінюй назви методів — main.py їх викликає.
"""

import re
from datetime import datetime, date
from storage import FileStorage


# ==================== ВАЛІДАЦІЯ ====================

class Validator:
    """
    Клас з методами валідації вхідних даних.
    Усі методи статичні — виклик без створення об'єкта: Validator.is_valid_phone(...)
    """

    @staticmethod
    def is_valid_phone(phone: str) -> bool:
        """
        Перевіряє чи номер телефону має коректний формат.

        Очікуваний формат: рядок цифр, можливо з +, пробілами, дефісами, дужками.
        Приклади: "+38 (050) 123-45-67", "0501234567", "+380501234567"

        Args:
            phone: Рядок з номером телефону.

        Returns:
            True якщо формат коректний, False — якщо ні.

        TODO: Реалізувати цей метод!
        Підказка: використай re.fullmatch() з відповідним патерном
        """
        # --- ТВІЙ КОД ТУТ ---
        raise NotImplementedError("Метод is_valid_phone() ще не реалізований!")

    @staticmethod
    def is_valid_email(email: str) -> bool:
        """
        Перевіряє чи email має коректний формат (наприклад, user@example.com).

        Args:
            email: Рядок з email адресою.

        Returns:
            True якщо формат коректний, False — якщо ні.

        TODO: Реалізувати цей метод!
        Підказка: використай re.fullmatch() або re.match()
        """
        # --- ТВІЙ КОД ТУТ ---
        raise NotImplementedError("Метод is_valid_email() ще не реалізований!")


# ==================== МОДЕЛЬ ДАНИХ ====================

class Contact:
    """
    Представляє один контакт адресної книги.

    Атрибути:
        name     (str): Ім'я контакту (обов'язкове).
        address  (str): Адреса.
        phone    (str): Номер телефону.
        email    (str): Адреса електронної пошти.
        birthday (str): День народження у форматі "DD.MM.YYYY".
    """

    # Список полів для збереження в CSV (має збігатись з атрибутами об'єкта)
    FIELDS = ["name", "address", "phone", "email", "birthday"]

    def __init__(
        self,
        name: str,
        address: str = "",
        phone: str = "",
        email: str = "",
        birthday: str = "",
    ):
        """
        Ініціалізація контакту.

        Args:
            name:     Ім'я (обов'язкове).
            address:  Адреса (необов'язково).
            phone:    Телефон у форматі, що проходить валідацію (необов'язково).
            email:    Email (необов'язково).
            birthday: День народження у форматі DD.MM.YYYY (необов'язково).
        """
        self.name = name
        self.address = address
        self.phone = phone
        self.email = email
        self.birthday = birthday

    def days_to_birthday(self) -> int | None:
        """
        Повертає кількість днів до наступного дня народження.

        Returns:
            Ціле число днів (0 = сьогодні, 1 = завтра тощо).
            None — якщо birthday не заданий або має невірний формат.

        TODO: Реалізувати цей метод!
        Підказка: використай datetime.strptime, date.today()
        """
        # --- ТВІЙ КОД ТУТ ---
        raise NotImplementedError("Метод days_to_birthday() ще не реалізований!")

    def to_dict(self) -> dict:
        """
        Конвертує контакт у словник для збереження в CSV.

        Returns:
            {"name": ..., "address": ..., "phone": ..., "email": ..., "birthday": ...}

        TODO: Реалізувати цей метод!
        """
        # --- ТВІЙ КОД ТУТ ---
        raise NotImplementedError("Метод to_dict() ще не реалізований!")

    @classmethod
    def from_dict(cls, data: dict) -> "Contact":
        """
        Створює об'єкт Contact зі словника (при завантаженні з CSV).

        Args:
            data: Словник з даними контакту.

        Returns:
            Новий об'єкт Contact.

        TODO: Реалізувати цей метод!
        """
        # --- ТВІЙ КОД ТУТ ---
        raise NotImplementedError("Метод from_dict() ще не реалізований!")

    def __str__(self) -> str:
        """Повертає зрозумілий рядок для виводу в консоль."""
        # TODO: Реалізувати — включи всі поля, наприклад:
        # "John Doe | вул. Хрещатик 1 | +380501234567 | john@ex.com | 01.01.1990"
        raise NotImplementedError("Метод __str__() ще не реалізований!")


# ==================== МЕНЕДЖЕР КОНТАКТІВ ====================

class ContactManager:
    """
    Управляє колекцією контактів.
    Завантажує дані при старті, зберігає при кожній зміні.

    Атрибути:
        storage  (FileStorage):   Об'єкт для роботи з CSV файлом.
        contacts (list[Contact]): Список контактів у пам'яті.
    """

    def __init__(self, filepath: str = "data/contacts.csv"):
        self.storage = FileStorage(filepath)
        self.contacts: list[Contact] = []
        # TODO: Завантажити контакти з файлу при ініціалізації
        # self._load()

    def add(self, contact: Contact) -> None:
        """
        Додає контакт до списку та зберігає у файл.

        Args:
            contact: Об'єкт Contact.

        TODO: Реалізувати!
        """
        # --- ТВІЙ КОД ТУТ ---
        raise NotImplementedError("Метод add() ще не реалізований!")

    def find(self, query: str) -> list[Contact]:
        """
        Шукає контакти за іменем, телефоном або email (часткове співпадіння).

        Args:
            query: Рядок для пошуку.

        Returns:
            Список відповідних контактів.

        TODO: Реалізувати!
        """
        # --- ТВІЙ КОД ТУТ ---
        raise NotImplementedError("Метод find() ще не реалізований!")

    def edit(self, name: str, updated_contact: Contact) -> bool:
        """
        Замінює контакт з вказаним ім'ям на новий об'єкт.

        Args:
            name:            Ім'я контакту, який треба замінити.
            updated_contact: Новий об'єкт Contact з оновленими даними.

        Returns:
            True якщо знайдено і оновлено, False якщо не знайдено.

        TODO: Реалізувати!
        """
        # --- ТВІЙ КОД ТУТ ---
        raise NotImplementedError("Метод edit() ще не реалізований!")

    def delete(self, name: str) -> bool:
        """
        Видаляє контакт за точним ім'ям.

        Args:
            name: Ім'я контакту.

        Returns:
            True якщо видалено, False якщо не знайдено.

        TODO: Реалізувати!
        """
        # --- ТВІЙ КОД ТУТ ---
        raise NotImplementedError("Метод delete() ще не реалізований!")

    def get_all(self) -> list[Contact]:
        """
        Повертає всі контакти.

        TODO: Реалізувати!
        """
        # --- ТВІЙ КОД ТУТ ---
        raise NotImplementedError("Метод get_all() ще не реалізований!")

    def birthdays_soon(self, days: int) -> list[Contact]:
        """
        Повертає контакти, у яких день народження протягом наступних `days` днів.

        Args:
            days: Кількість днів вперед для перевірки (включно з сьогодні).

        Returns:
            Список контактів із найближчими днями народження.

        TODO: Реалізувати!
        Підказка: виклич contact.days_to_birthday() для кожного контакту
        і відфільтруй ті, де значення <= days
        """
        # --- ТВІЙ КОД ТУТ ---
        raise NotImplementedError("Метод birthdays_soon() ще не реалізований!")

    # ---- Приватні допоміжні методи ----

    def _save(self) -> None:
        """Зберігає всі контакти у CSV через FileStorage."""
        # TODO: self.storage.save([c.to_dict() for c in self.contacts], Contact.FIELDS)
        raise NotImplementedError("Метод _save() ще не реалізований!")

    def _load(self) -> None:
        """Завантажує контакти з CSV через FileStorage."""
        # TODO: data = self.storage.load(); self.contacts = [Contact.from_dict(d) for d in data]
        raise NotImplementedError("Метод _load() ще не реалізований!")

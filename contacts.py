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
        """
        clean_phone = ''.join(char for char in phone if char.isdigit())
        
        if len(clean_phone) == 10 and clean_phone[0] == '0':
            return True
        elif len(clean_phone) == 12 and clean_phone.startswith("380"):
            return True
        else:
            return False

    @staticmethod
    def is_valid_email(email: str) -> bool:
        """
        Перевіряє чи email має коректний формат (наприклад, user@example.com).

        Args:
            email: Рядок з email адресою.

        Returns:
            True якщо формат коректний, False — якщо ні.
        """
        pattern = r"[\w.+-]+@[\w-]+\.[\w.]+"
        match = re.search(pattern, email)
        return match is not None


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
        self.phone = self._format_phone(phone) if phone else ""
        self.email = email
        self.birthday = birthday

    def _format_phone(self, phone: str) -> str:
        """Форматує телефон до міжнародного формату +380..."""
        clean_phone = ''.join(char for char in phone if char.isdigit())
        
        if len(clean_phone) == 10 and clean_phone[0] == '0':
            return "+38" + clean_phone
        elif len(clean_phone) == 12 and clean_phone.startswith("380"):
            return "+" + clean_phone
        else:
            return phone

    def days_to_birthday(self) -> int | None:
        """
        Повертає кількість днів до наступного дня народження.

        Returns:
            Ціле число днів (0 = сьогодні, 1 = завтра тощо).
            None — якщо birthday не заданий або має невірний формат.
        """
        if not self.birthday:
            return None
        
        try:
            birthday_date = datetime.strptime(self.birthday, "%d.%m.%Y").date()
            today = date.today()
            birthday_this_year = birthday_date.replace(year=today.year)
            
            if birthday_this_year < today:
                birthday_this_year = birthday_this_year.replace(year=today.year + 1)
            
            delta_days = (birthday_this_year - today).days
            return delta_days
        except ValueError:
            return None

    def to_dict(self) -> dict:
        """
        Конвертує контакт у словник для збереження в CSV.

        Returns:
            {"name": ..., "address": ..., "phone": ..., "email": ..., "birthday": ...}
        """
        return {
            "name": self.name,
            "address": self.address,
            "phone": self.phone,
            "email": self.email,
            "birthday": self.birthday
        }

    @classmethod
    def from_dict(cls, data: dict) -> "Contact":
        """
        Створює об'єкт Contact зі словника (при завантаженні з CSV).

        Args:
            data: Словник з даними контакту.

        Returns:
            Новий об'єкт Contact.
        """
        return cls(
            name=data.get("name", ""),
            address=data.get("address", ""),
            phone=data.get("phone", ""),
            email=data.get("email", ""),
            birthday=data.get("birthday", "")
        )

    def __str__(self) -> str:
        """Повертає зрозумілий рядок для виводу в консоль."""
        parts = [self.name]
        
        if self.address:
            parts.append(self.address)
        if self.phone:
            parts.append(self.phone)
        if self.email:
            parts.append(self.email)
        if self.birthday:
            parts.append(self.birthday)
        
        return " | ".join(parts)


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
        self._load()

    def add(self, contact: Contact) -> None:
        """
        Додає контакт до списку та зберігає у файл.

        Args:
            contact: Об'єкт Contact.
        """
        self.contacts.append(contact)
        self._save()

    def find(self, query: str) -> list[Contact]:
        """
        Шукає контакти за іменем, телефоном або email (часткове співпадіння).

        Args:
            query: Рядок для пошуку.

        Returns:
            Список відповідних контактів.
        """
        query_lower = query.lower()
        results = []
        
        for contact in self.contacts:
            if (query_lower in contact.name.lower() or
                query_lower in contact.phone.lower() or
                query_lower in contact.email.lower()):
                results.append(contact)
        
        return results

    def edit(self, name: str, updated_contact: Contact) -> bool:
        """
        Замінює контакт з вказаним ім'ям на новий об'єкт.

        Args:
            name:            Ім'я контакту, який треба замінити.
            updated_contact: Новий об'єкт Contact з оновленими даними.

        Returns:
            True якщо знайдено і оновлено, False якщо не знайдено.
        """
        for i, contact in enumerate(self.contacts):
            if contact.name == name:
                self.contacts[i] = updated_contact
                self._save()
                return True
        return False

    def delete(self, name: str) -> bool:
        """
        Видаляє контакт за точним ім'ям.

        Args:
            name: Ім'я контакту.

        Returns:
            True якщо видалено, False якщо не знайдено.
        """
        for i, contact in enumerate(self.contacts):
            if contact.name == name:
                del self.contacts[i]
                self._save()
                return True
        return False

    def get_all(self) -> list[Contact]:
        """
        Повертає всі контакти.
        """
        return self.contacts

    def birthdays_soon(self, days: int) -> list[Contact]:
        """
        Повертає контакти, у яких день народження протягом наступних `days` днів.

        Args:
            days: Кількість днів вперед для перевірки (включно з сьогодні).

        Returns:
            Список контактів із найближчими днями народження.
        """
        upcoming = []
        
        for contact in self.contacts:
            days_to_bd = contact.days_to_birthday()
            if days_to_bd is not None and days_to_bd <= days:
                upcoming.append(contact)
        
        return upcoming

    # ---- Приватні допоміжні методи ----

    def _save(self) -> None:
        """Зберігає всі контакти у CSV через FileStorage."""
        data = [contact.to_dict() for contact in self.contacts]
        self.storage.save(data, Contact.FIELDS)

    def _load(self) -> None:
        """Завантажує контакти з CSV через FileStorage."""
        data = self.storage.load()
        self.contacts = [Contact.from_dict(d) for d in data]
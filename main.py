"""
main.py — Точка входу програми "Персональний помічник".

Запуск:
    python main.py

Структура меню:
    1. Контакти
       1. Додати контакт
       2. Знайти контакт
       3. Редагувати контакт
       4. Видалити контакт
       5. Показати всі контакти
       6. Іменинники (день народження протягом N днів)
       0. Назад
    2. Нотатки
       1. Додати нотатку
       2. Знайти нотатку
       3. Редагувати нотатку
       4. Видалити нотатку
       5. Показати всі нотатки
       6. Знайти за тегом (бонус)
       0. Назад
    0. Вийти
"""

import sys
import io

# На Windows консоль за замовчуванням використовує cp1252,
# що викликає UnicodeEncodeError при виводі кирилиці.
# isinstance-перевірка потрібна щоб уникнути помилки Pylance —
# у деяких середовищах stdout може бути не TextIOWrapper (напр. у тестах).
if isinstance(sys.stdout, io.TextIOWrapper):
    sys.stdout.reconfigure(encoding="utf-8")
if isinstance(sys.stderr, io.TextIOWrapper):
    sys.stderr.reconfigure(encoding="utf-8")

from typing import TypeVar
from contacts import ContactManager, Contact, Validator
from notes import NoteManager, Note

# Генеричний тип для select_from_results — дозволяє функції працювати
# з будь-яким типом (Contact, Note тощо) і повертати правильний тип без дублювання коду.
T = TypeVar("T")


# ==================== ДОПОМІЖНІ ФУНКЦІЇ ====================

def print_separator():
    """Виводить розділювальну лінію."""
    print("-" * 45)


def print_header(title: str):
    """Виводить заголовок розділу."""
    print_separator()
    print(f"  {title}")
    print_separator()


def select_from_results(results: list[T], label: str = "Оберіть номер") -> T | None:
    """
    Якщо знайдено кілька результатів — показує список і просить вибрати за номером.
    Якщо знайдено один — повертає одразу.
    """
    if not results:
        return None
    if len(results) == 1:
        return results[0]
    for i, item in enumerate(results, 1):
        print(f"  {i}. {item}")
    while True:
        try:
            choice = int(input(f"{label} (1-{len(results)}, 0 — скасувати): "))
            if choice == 0:
                return None
            if 1 <= choice <= len(results):
                return results[choice - 1]
        except ValueError:
            pass
        print(f"  Введіть число від 0 до {len(results)}")


def input_contact() -> Contact | None:
    """
    Запитує у користувача всі поля для нового/оновленого контакту.
    Валідує телефон і email — показує помилку і просить ввести ще раз.

    Returns:
        Об'єкт Contact або None якщо ім'я не введено.
    """
    name = input("Ім'я: ").strip()
    if not name:
        print("Ім'я не може бути порожнім!")
        return None

    address = input("Адреса: ").strip()

    # Валідація телефону
    while True:
        phone = input("Телефон (або Enter щоб пропустити): ").strip()
        if not phone:
            break
        if Validator.is_valid_phone(phone):
            break
        print("  Невірний формат телефону! Приклад: +38 (050) 123-45-67 або 0501234567")

    # Валідація email
    while True:
        email = input("Email (або Enter щоб пропустити): ").strip()
        if not email:
            break
        if Validator.is_valid_email(email):
            break
        print("  Невірний формат email! Приклад: user@example.com")

    birthday = input("День народження (DD.MM.YYYY, або Enter щоб пропустити): ").strip()

    return Contact(name=name, address=address, phone=phone, email=email, birthday=birthday)


def input_note_edit(existing: Note) -> Note:
    """
    Запитує нові значення полів для редагування нотатки.
    Порожній ввід (Enter) залишає поточне значення.
    """
    title = input(f"Заголовок [{existing.title}]: ").strip() or existing.title
    content = input(f"Текст [{existing.content}]: ").strip() or existing.content
    tags = input(f"Теги [{existing.tags}]: ").strip() or existing.tags
    return Note(title=title, content=content, tags=tags)


# ==================== МЕНЮ КОНТАКТІВ ====================

def contacts_menu(manager: ContactManager):
    """Підменю для роботи з контактами."""
    while True:
        print_header("КОНТАКТИ")
        print("1. Додати контакт")
        print("2. Знайти контакт")
        print("3. Редагувати контакт")
        print("4. Видалити контакт")
        print("5. Показати всі контакти")
        print("6. Іменинники (найближчі дні народження)")
        print("0. Назад")
        print_separator()

        choice = input("Оберіть дію: ").strip()

        if choice == "1":
            print("\n--- Додати контакт ---")
            contact = input_contact()
            if contact:
                manager.add(contact)
                print(f"✓ Контакт '{contact.name}' додано!")

        elif choice == "2":
            print("\n--- Пошук контакту ---")
            query = input("Введіть ім'я, телефон або email: ").strip()
            results = manager.find(query)
            if results:
                for i, c in enumerate(results, 1):
                    print(f"{i}. {c}")
            else:
                print("Контактів не знайдено.")

        elif choice == "3":
            print("\n--- Редагувати контакт ---")
            name = input("Введіть точне ім'я контакту для редагування: ").strip()
            print("Введіть нові дані (Enter — залишити поточне значення):")
            updated = input_contact()
            if updated:
                if manager.edit(name, updated):
                    print(f"✓ Контакт '{name}' оновлено.")
                else:
                    print(f"Контакт '{name}' не знайдено.")

        elif choice == "4":
            print("\n--- Видалити контакт ---")
            name = input("Введіть ім'я контакту: ").strip()
            if manager.delete(name):
                print(f"✓ Контакт '{name}' видалено.")
            else:
                print(f"Контакт '{name}' не знайдено.")

        elif choice == "5":
            print("\n--- Всі контакти ---")
            contacts = manager.get_all()
            if contacts:
                for i, c in enumerate(contacts, 1):
                    print(f"{i}. {c}")
                print(f"\nВсього: {len(contacts)} контактів.")
            else:
                print("Список контактів порожній.")

        elif choice == "6":
            print("\n--- Іменинники ---")
            try:
                days = int(input("За скільки днів від сьогодні шукати? "))
            except ValueError:
                print("Введіть ціле число!")
                input("\nНатисніть Enter для продовження...")
                continue
            results = manager.birthdays_soon(days)
            if results:
                print(f"Іменинники протягом {days} днів:")
                for c in results:
                    print(f"  {c}")
            else:
                print(f"Іменинників протягом {days} днів немає.")

        elif choice == "0":
            break

        else:
            print("Невірний вибір. Спробуйте ще раз.")

        input("\nНатисніть Enter для продовження...")


# ==================== МЕНЮ НОТАТОК ====================

def notes_menu(manager: NoteManager):
    """Підменю для роботи з нотатками."""
    while True:
        print_header("НОТАТКИ")
        print("1. Додати нотатку")
        print("2. Знайти нотатку")
        print("3. Редагувати нотатку")
        print("4. Видалити нотатку")
        print("5. Показати всі нотатки")
        print("6. Знайти за тегом (бонус)")
        print("0. Назад")
        print_separator()

        choice = input("Оберіть дію: ").strip()

        if choice == "1":
            print("\n--- Додати нотатку ---")
            title = input("Заголовок: ").strip()
            if not title:
                print("Заголовок не може бути порожнім!")
                input("\nНатисніть Enter для продовження...")
                continue

            content = input("Текст нотатки: ").strip()
            tags = input("Теги через кому (або Enter щоб пропустити): ").strip()
            note = Note(title=title, content=content, tags=tags)
            manager.add(note)
            print(f"✓ Нотатку '{title}' додано!")

        elif choice == "2":
            print("\n--- Пошук нотатки ---")
            query = input("Введіть заголовок, текст або тег: ").strip()
            results = manager.find(query)
            if results:
                for i, n in enumerate(results, 1):
                    print(f"{i}. {n}")
            else:
                print("Нотаток не знайдено.")

        elif choice == "3":
            print("\n--- Редагувати нотатку ---")
            query = input("Пошук нотатки (заголовок, текст або тег): ").strip()
            results = manager.find(query)
            if not results:
                print("Нотаток не знайдено.")
            else:
                existing = select_from_results(results, "Оберіть нотатку для редагування")
                if existing:
                    print("Введіть нові дані (Enter — залишити поточне значення):")
                    updated = input_note_edit(existing)
                    manager.edit(existing, updated)
                    print(f"✓ Нотатку '{existing.title}' оновлено.")

        elif choice == "4":
            print("\n--- Видалити нотатку ---")
            query = input("Пошук нотатки (заголовок, текст або тег): ").strip()
            results = manager.find(query)
            if not results:
                print("Нотаток не знайдено.")
            else:
                note = select_from_results(results, "Оберіть нотатку для видалення")
                if note:
                    manager.delete(note)
                    print(f"✓ Нотатку '{note.title}' видалено.")

        elif choice == "5":
            print("\n--- Всі нотатки ---")
            notes = manager.get_all()
            if notes:
                for i, n in enumerate(notes, 1):
                    print(f"{i}. {n}")
                print(f"\nВсього: {len(notes)} нотаток.")
            else:
                print("Список нотаток порожній.")

        elif choice == "6":
            print("\n--- Пошук за тегом (бонус) ---")
            tag = input("Введіть тег: ").strip()
            results = manager.find_by_tag(tag)
            if results:
                for i, n in enumerate(results, 1):
                    print(f"{i}. {n}")
            else:
                print(f"Нотаток з тегом '{tag}' не знайдено.")

        elif choice == "0":
            break

        else:
            print("Невірний вибір. Спробуйте ще раз.")

        input("\nНатисніть Enter для продовження...")


# ==================== ГОЛОВНЕ МЕНЮ ====================

def main():
    """Точка входу. Ініціалізує менеджери та запускає головне меню."""
    print("=" * 45)
    print("      ПЕРСОНАЛЬНИЙ ПОМІЧНИК")
    print("=" * 45)

    # Ініціалізація менеджерів (автоматично завантажують дані з файлів)
    contact_manager = ContactManager()
    note_manager = NoteManager()

    while True:
        print_header("ГОЛОВНЕ МЕНЮ")
        print("1. Контакти")
        print("2. Нотатки")
        print("0. Вийти")
        print_separator()

        choice = input("Оберіть розділ: ").strip()

        if choice == "1":
            contacts_menu(contact_manager)
        elif choice == "2":
            notes_menu(note_manager)
        elif choice == "0":
            print("\nДо побачення!")
            break
        else:
            print("Невірний вибір. Спробуйте ще раз.")


if __name__ == "__main__":
    main()

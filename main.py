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

import difflib
import questionary
from typing import TypeVar
from rich.console import Console
from rich.table import Table
from contacts import ContactManager, Contact, Validator
from notes import NoteManager, Note

console = Console()

# Генеричний тип для select_from_results — дозволяє функції працювати
# з будь-яким типом (Contact, Note тощо) і повертати правильний тип без дублювання коду.
T = TypeVar("T")


# ==================== ДОПОМІЖНІ ФУНКЦІЇ ====================

def print_separator():
    """Виводить розділювальну лінію."""
    print("-" * 45)


def print_contacts_table(contacts: list[Contact]) -> None:
    table = Table(show_header=True, header_style="bold cyan")
    table.add_column("#", style="dim", width=3)
    table.add_column("Ім'я")
    table.add_column("Телефон")
    table.add_column("Email")
    table.add_column("День народження")
    table.add_column("Адреса")
    for i, c in enumerate(contacts, 1):
        table.add_row(str(i), c.name, c.phone, c.email, c.birthday, c.address)
    console.print(table)


_TAG_PALETTE = [
    "cyan", "magenta", "yellow", "green", "blue",
    "red", "bright_cyan", "bright_magenta", "bright_yellow", "bright_green",
]

def _tag_colors(notes: list[Note]) -> dict[str, str]:
    """Призначає кожному унікальному тегу колір зі палітри (стабільно для одного виклику)."""
    all_tags = sorted({t for n in notes for t in n.get_tags_list()})
    return {tag: _TAG_PALETTE[i % len(_TAG_PALETTE)] for i, tag in enumerate(all_tags)}

def _format_tags(tags_str: str, colors: dict[str, str]) -> str:
    if not tags_str:
        return ""
    parts = [t.strip() for t in tags_str.split(",")]
    return ", ".join(f"[{colors.get(t.lower(), 'white')}]{t}[/]" for t in parts)


def print_notes_table(notes: list[Note]) -> None:
    colors = _tag_colors(notes)
    table = Table(show_header=True, header_style="bold cyan")
    table.add_column("#", style="dim", width=3)
    table.add_column("Заголовок")
    table.add_column("Текст")
    table.add_column("Теги")
    for i, n in enumerate(notes, 1):
        table.add_row(str(i), n.title, n.content, _format_tags(n.tags, colors))
    console.print(table)


def suggest_similar(query: str, candidates: list[str]) -> None:
    """Виводить схожі варіанти через difflib якщо пошук нічого не знайшов.
    Порівнює по першому слові в lowercase — 'homre' → 'homer' → 'Homer Simpson'.
    """
    q = query.lower()
    # Беремо перше слово кожного кандидата (ім'я), зберігаємо mapping → повна назва
    first_word_map: dict[str, str] = {}
    for c in candidates:
        words = c.split()
        if words:
            first_word_map[words[0].lower()] = c

    matched = difflib.get_close_matches(q, first_word_map.keys(), n=3, cutoff=0.5)
    matches = [first_word_map[w] for w in matched]
    if matches:
        print(f"  Можливо, ви мали на увазі: {', '.join(matches)}?")


def select_from_results(results: list[T], label: str = "Оберіть") -> T | None:
    """
    Якщо знайдено кілька результатів — показує список зі стрілковою навігацією.
    Якщо знайдено один — повертає одразу без питань.
    value=індекс щоб коректно розрізняти дублі (questionary повертає value, не об'єкт).
    """
    if not results:
        return None
    if len(results) == 1:
        return results[0]

    choices = [questionary.Choice(title=str(r), value=i) for i, r in enumerate(results)]
    choices.append(questionary.Choice(title="↩ Скасувати", value=-1))

    idx = questionary.select(label, choices=choices).ask()
    if idx is None or idx == -1:
        return None
    return results[idx]


def input_contact_edit(existing: Contact) -> Contact:
    """
    Запитує нові значення полів контакту для редагування.
    Порожній ввід (Enter) залишає поточне значення.
    """
    name = input(f"Ім'я [{existing.name}]: ").strip() or existing.name
    address = input(f"Адреса [{existing.address}]: ").strip() or existing.address

    while True:
        phone = input(f"Телефон [{existing.phone}] (або Enter щоб залишити): ").strip()
        if not phone:
            phone = existing.phone
            break
        if Validator.is_valid_phone(phone):
            break
        print("  Невірний формат телефону! Приклад: +38 (050) 123-45-67 або 0501234567")

    while True:
        email = input(f"Email [{existing.email}] (або Enter щоб залишити): ").strip()
        if not email:
            email = existing.email
            break
        if Validator.is_valid_email(email):
            break
        print("  Невірний формат email! Приклад: user@example.com")

    while True:
        birthday = input(f"День народження [{existing.birthday}] (або Enter щоб залишити): ").strip()
        if not birthday:
            birthday = existing.birthday
            break
        if Validator.is_valid_birthday(birthday):
            break
        print("  Невірний формат дати! Приклад: 07.11.1995")

    return Contact(name=name, address=address, phone=phone, email=email, birthday=birthday)


def input_contact() -> Contact | None:
    """
    Запитує у користувача всі поля для нового контакту.
    Валідує телефон, email і дату — показує помилку і просить ввести ще раз.

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

    # Валідація дня народження
    while True:
        birthday = input("День народження (DD.MM.YYYY, або Enter щоб пропустити): ").strip()
        if not birthday:
            break
        if Validator.is_valid_birthday(birthday):
            break
        print("  Невірний формат дати! Приклад: 07.11.1995")

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
        choice = questionary.select(
            "КОНТАКТИ — оберіть дію:",
            choices=[
                "Додати контакт",
                "Знайти контакт",
                "Редагувати контакт",
                "Видалити контакт",
                "Показати всі контакти",
                "Іменинники (найближчі дні народження)",
                "↩ Назад",
            ]
        ).ask()

        if choice is None or choice == "↩ Назад":
            break

        elif choice == "Додати контакт":
            print("\n--- Додати контакт ---")
            contact = input_contact()
            if contact:
                manager.add(contact)
                print(f"✓ Контакт '{contact.name}' додано!")

        elif choice == "Знайти контакт":
            print("\n--- Пошук контакту ---")
            query = input("Введіть ім'я, телефон або email: ").strip()
            results = manager.find(query)
            if results:
                print_contacts_table(results)
            else:
                print("Контактів не знайдено.")
                suggest_similar(query, [c.name for c in manager.get_all()])

        elif choice == "Редагувати контакт":
            print("\n--- Редагувати контакт ---")
            query = input("Пошук контакту (ім'я, телефон або email; Enter — показати всі): ").strip()
            results = manager.find(query)
            if not results:
                print("Контактів не знайдено.")
            else:
                existing = select_from_results(results, "Оберіть контакт для редагування")
                if existing:
                    print("Введіть нові дані (Enter — залишити поточне значення):")
                    updated = input_contact_edit(existing)
                    manager.edit(existing, updated)
                    print(f"✓ Контакт '{updated.name}' оновлено.")

        elif choice == "Видалити контакт":
            print("\n--- Видалити контакт ---")
            query = input("Пошук контакту (ім'я, телефон або email; Enter — показати всі): ").strip()
            results = manager.find(query)
            if not results:
                print("Контактів не знайдено.")
            else:
                contact = select_from_results(results, "Оберіть контакт для видалення")
                if contact:
                    manager.delete(contact)
                    print(f"✓ Контакт '{contact.name}' видалено.")

        elif choice == "Показати всі контакти":
            print("\n--- Всі контакти ---")
            contacts = manager.get_all()
            if contacts:
                print_contacts_table(contacts)
                print(f"Всього: {len(contacts)} контактів.")
            else:
                print("Список контактів порожній.")

        elif choice == "Іменинники (найближчі дні народження)":
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
                print_contacts_table(results)
            else:
                print(f"Іменинників протягом {days} днів немає.")

        input("\nНатисніть Enter для продовження...")


# ==================== МЕНЮ НОТАТОК ====================

def notes_menu(manager: NoteManager):
    """Підменю для роботи з нотатками."""
    while True:
        choice = questionary.select(
            "НОТАТКИ — оберіть дію:",
            choices=[
                "Додати нотатку",
                "Знайти нотатку",
                "Редагувати нотатку",
                "Видалити нотатку",
                "Показати всі нотатки",
                "Знайти за тегом",
                "↩ Назад",
            ]
        ).ask()

        if choice is None or choice == "↩ Назад":
            break

        elif choice == "Додати нотатку":
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

        elif choice == "Знайти нотатку":
            print("\n--- Пошук нотатки ---")
            query = input("Введіть заголовок, текст або тег: ").strip()
            results = manager.find(query)
            if results:
                print_notes_table(results)
            else:
                print("Нотаток не знайдено.")
                suggest_similar(query, [n.title for n in manager.get_all()])

        elif choice == "Редагувати нотатку":
            print("\n--- Редагувати нотатку ---")
            query = input("Пошук нотатки (заголовок, текст або тег; Enter — показати всі): ").strip()
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

        elif choice == "Видалити нотатку":
            print("\n--- Видалити нотатку ---")
            query = input("Пошук нотатки (заголовок, текст або тег; Enter — показати всі): ").strip()
            results = manager.find(query)
            if not results:
                print("Нотаток не знайдено.")
            else:
                note = select_from_results(results, "Оберіть нотатку для видалення")
                if note:
                    manager.delete(note)
                    print(f"✓ Нотатку '{note.title}' видалено.")

        elif choice == "Показати всі нотатки":
            print("\n--- Всі нотатки ---")
            sort = questionary.confirm("Сортувати за тегами?", default=False).ask()
            notes = manager.get_all(sort_by_tag=bool(sort))
            if notes:
                print_notes_table(notes)
                print(f"Всього: {len(notes)} нотаток.")
            else:
                print("Список нотаток порожній.")

        elif choice == "Знайти за тегом":
            print("\n--- Пошук за тегом ---")
            tag = input("Введіть тег: ").strip()
            results = manager.find_by_tag(tag)
            if results:
                print_notes_table(results)
            else:
                print(f"Нотаток з тегом '{tag}' не знайдено.")

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
        choice = questionary.select(
            "ГОЛОВНЕ МЕНЮ — оберіть розділ:",
            choices=["Контакти", "Нотатки", "Вийти"]
        ).ask()

        if choice is None or choice == "Вийти":
            print("\nДо побачення!")
            break
        elif choice == "Контакти":
            contacts_menu(contact_manager)
        elif choice == "Нотатки":
            notes_menu(note_manager)


if __name__ == "__main__":
    main()

import pickle
from datetime import datetime, timedelta
from assistant.classes import Field, Name, Phone, Birthday, Record, AddressBook

# ---------- ДЕКОРАТОР ДЛЯ ОБРОБКИ ПОМИЛОК ----------

def input_error(func):
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except (IndexError, ValueError, KeyError) as e:
            return f"Error: {e}"
    return wrapper

# ---------- КОМАНДНІ ФУНКЦІЇ ----------

@input_error
def add_contact(args, book):
    name, phone = args
    record = book.find(name)
    if not record:
        record = Record(name)
        book.add_record(record)
    record.add_phone(phone)
    return f"Contact updated: {record}"

@input_error
def change_contact(args, book):
    name, old_phone, new_phone = args
    record = book.find(name)
    if not record:
        return f"No contact with name '{name}' found."
    record.edit_phone(old_phone, new_phone)
    return f"Phone updated for {name}."

@input_error
def show_phone(args, book):
    name = args[0]
    record = book.find(name)
    if not record:
        return f"No contact with name '{name}' found."
    phones = "; ".join(p.value for p in record.phones)
    return f"{name}'s phones: {phones}"

@input_error
def show_all(args, book):
    return str(book) if book.data else "Address book is empty."

@input_error
def add_birthday(args, book):
    name, bday = args
    record = book.find(name)
    if not record:
        return f"No contact with name '{name}' found."
    record.add_birthday(bday)
    return f"Birthday added for {name}."

@input_error
def show_birthday(args, book):
    name = args[0]
    record = book.find(name)
    if not record:
        return f"No contact with name '{name}' found."
    return f"{name}'s birthday is {record.show_birthday()}."

@input_error
def birthdays(args, book):
    upcoming = book.get_upcoming_birthdays()
    if not upcoming:
        return "No upcoming birthdays this week."
    return "\n".join(f"{name}: {date}" for name, date in upcoming)

# ---------- ПАРСИНГ КОМАНД ----------

def parse_input(user_input):
    parts = user_input.strip().split()
    if not parts:
        return "", []
    command = parts[0].lower()
    args = parts[1:]
    return command, args


def load_data():
    try:
        with open("contacts.pkl", "rb") as file:
            return pickle.load(file)
    except FileNotFoundError:
        return AddressBook()

def save_data(book):
    with open("contacts.pkl", "wb") as file:
        pickle.dump(book, file)


# ---------- ОСНОВНА ФУНКЦІЯ ----------

def main():
    book = load_data()
    print("Welcome! This is your assistant bot. Enter a command.")

    while True:
        user_input = input(">>> ").strip()
        if not user_input:
            continue

        command, args = parse_input(user_input)

        if command == "add":
            print(add_contact(args, book))
        elif command == "change":
            print(change_contact(args, book))
        elif command == "phone":
            print(show_phone(args, book))
        elif command == "add-birthday":
            print(add_birthday(args, book))
        elif command == "show-birthday":
            print(show_birthday(args, book))
        elif command == "birthdays":
            print(birthdays(args, book))
        elif command == "all":
            print(show_all(args, book))
        elif command in ("exit", "close", "goodbye", "good", "bye"):
            save_data(book)
            print("Goodbye!")
            break
        else:
            print("Unknown command. Try again.")

# ---------- ЗАПУСК ----------

if __name__ == "__main__":
    main()


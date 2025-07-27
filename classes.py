from collections import UserDict
from datetime import datetime, timedelta

# ---------- КЛАСИ ----------

class Field:
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return str(self.value)


class Name(Field):
    pass


class Phone(Field):
    def __init__(self, value):
        if not value.isdigit() or len(value) != 10:
            raise ValueError("Phone number must contain exactly 10 digits.")
        super().__init__(value)


class Birthday(Field):
    def __init__(self, value):
        try:
            datetime.strptime(value, "%d.%m.%Y")
        except ValueError:
            raise ValueError("Invalid date format. Use DD.MM.YYYY")
        self.value = value


class Record:
    def __init__(self, name):
        self.name = Name(name)
        self.phones = []
        self.birthday = None

    def add_phone(self, phone):
        self.phones.append(Phone(phone))

    def remove_phone(self, phone):
        phone_obj = self.find_phone(phone)
        if phone_obj:
            self.phones.remove(phone_obj)
        else:
            raise ValueError("Phone number not found.")

    def edit_phone(self, old_phone, new_phone):
        for phone in self.phones:
            if phone.value == old_phone:
                # Перевірити новий номер, якщо невалідний — не видаляти старий
                try:
                    new_phone_obj = Phone(new_phone)
                except ValueError as e:
                    raise ValueError("Invalid new phone number format.")
                phone.value = new_phone_obj.value
                return
        raise ValueError("Old phone number not found.")

    def find_phone(self, phone):
        for p in self.phones:
            if p.value == phone:
                return p
        return None

    def add_birthday(self, bday):
        self.birthday = Birthday(bday)

    def show_birthday(self):
        return self.birthday.value if self.birthday else "No birthday set"

    def __str__(self):
        phones_str = "; ".join(str(p) for p in self.phones)
        bday = f", birthday: {self.show_birthday()}" if self.birthday else ""
        return f"Contact name: {self.name.value}, phones: {phones_str}{bday}"


class AddressBook(UserDict):
    def add_record(self, record):
        self.data[record.name.value] = record

    def find(self, name):
        return self.data.get(name)

    def delete(self, name):
        if name in self.data:
            del self.data[name]

    def get_upcoming_birthdays(self):
        today = datetime.today().date()
        upcoming = []

        for record in self.data.values():
            if record.birthday:
                try:
                    bday = datetime.strptime(record.birthday.value, "%d.%m.%Y").date()
                except ValueError:
                    continue

                bday_this_year = bday.replace(year=today.year)
                if bday_this_year < today:
                    bday_this_year = bday_this_year.replace(year=today.year + 1)

                days_diff = (bday_this_year - today).days
                if 0 <= days_diff <= 7:
                    if bday_this_year.weekday() >= 5:
                        bday_this_year += timedelta(days=(7 - bday_this_year.weekday()))
                    upcoming.append((record.name.value, bday_this_year.strftime("%d.%m.%Y")))

        return upcoming

    def __str__(self):
        return "\n".join(str(record) for record in self.data.values())

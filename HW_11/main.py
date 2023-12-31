from collections import UserDict
from datetime import datetime


class Field:
    def __init__(self, value):
        if not self.is_valid(value):
            raise ValueError
        self.__value = value

    @property
    def value(self):
        return self.__value

    @value.setter
    def value(self, value):
        if not self.is_valid(value):
            raise ValueError
        self.__value = value

    def is_valid(self, value):
        return True

    def __str__(self):
        return str(self.value)


class Name(Field):
    pass


class Phone(Field):
    def is_valid(self, new_value):
        if isinstance(new_value, str) and new_value.isdigit() and len(new_value) == 10:
            return True
        else:
            return False


class Birthday(Field):
    def is_valid(self, date):
        try:
            datetime.strptime(date, "%Y-%m-%d")
            return True
        except ValueError:
            return False


class Record:
    def __init__(self, name, birthday=None):
        self.name = Name(name)
        self.phones = []
        if birthday:
            self.birthday = Birthday(birthday)

    def add_phone(self, numb):
        self.phones.append(Phone(numb))

    def remove_phone(self, numb):
        for phone in self.phones:
            if phone.value == numb:
                self.phones.remove(phone)

    def edit_phone(self, old_numb, new_numb):
        for phone in self.phones:
            if phone.value == old_numb:
                phone.value = new_numb
                break
        else:
            raise ValueError

    def find_phone(self, numb):
        for phone in self.phones:
            if phone.value == numb:
                return phone
        return None

    def __str__(self):
        return f"Contact name: {self.name.value}, \
                phones: {'; '.join(p.value for p in self.phones)}"

    def days_to_birthday(self):
        if self.birthday:
            today = datetime.now().date()
            next_birthday = datetime(today.year, *map(int, self.birthday.value.split("-"))).date()
            if today > next_birthday:
                next_birthday = datetime(today.year + 1, *map(int, self.birthday.value.split("-"))).date()
            return (next_birthday - today).days
        else:
            return None


class AddressBook(UserDict):
    def add_record(self, name):
        self.data[name.name.value] = name

    def find(self, name):
        return self.data.get(name)

    def delete(self, name):
        if name in self.data:
            self.data.pop(name)

    def iterator(self, N=5):
        records = list(self.data.values())
        for i in range(0, len(records), N):
            yield records[i:i + N]

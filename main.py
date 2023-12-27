from collections import UserDict


class Field:
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return str(self.value)


class Name(Field):
    pass


class Phone(Field):
    def __init__(self, value):
        if len(value) == 10 and value.isdigit():
            self.value = value
        else:
            raise ValueError("Invalid value. It must be a 10-digit string of digits.")


class Record:
    def __init__(self, name):
        self.name = Name(name)
        self.phones = []

    def add_phone(self, phone):
        phone_add = Phone(phone)
        self.phones.append(phone_add)

    def remove_phone(self, phone):
        new_phones = []
        for el in self.phones:
            if phone != el.value:
                new_phones.append(el)
        self.phones = new_phones

    def edit_phone(self, old_phone, new_phone):
       for el in self.phones:
            if el.value == old_phone:
                self.remove_phone(old_phone)
                self.add_phone(new_phone)
                break
            else:
                raise ValueError('Phone does not exist')

    def find_phone(self, phone):
        for el in self.phones:
            if el.value == phone:
                return el

    def __str__(self):
        return f"Contact name: {self.name.value}, phones: {'; '.join(p.value for p in self.phones)}"


class AddressBook(UserDict):
    def add_record(self, record):
        self.data[record.name.value] = record

    def find(self, name):
        try:
            return self.data[name]
        except KeyError:
            print('Name does not exist')
    
    def delete(self, name):
        try:
            del self.data[name]
        except KeyError:
            print('Name does not exist')

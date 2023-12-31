import json
from collections import UserDict
from datetime import datetime
from json import JSONDecodeError


class Field:
    def __init__(self, value):
        if self.check_value(value):
            self.__value = value
        else:
            self.__value = None

    def check_value(self, value):
        return True

    def __str__(self):
        return str(self.__value)

    @property
    def value(self):
        return self.__value

    @value.setter
    def value(self, value):
        if self.check_value(value):
            self.__value = value
        else:
            self.__value = None



class Name(Field):
    pass


class Phone(Field):
    def check_value(self, value):
        if value is not None:
            if len(value) == 10 and value.isdigit():
                return True
            else:
                raise ValueError("Invalid value. It must be a 10-digit string of digits.")
        return False


class Birthday(Field):
    def check_value(self, value):
        if value is not None:
            try:
                datetime.strptime(value, '%d.%m.%Y')
                return True
            except ValueError:
                raise ValueError("Invalid date format. It must be in 00.00.0000 format.")
        return False


class Record:
    def __init__(self, name, birthday_value=None):
        self.name = Name(name)
        self.phones = []
        self.birthday_day = Birthday(birthday_value)

    def days_to_birthday(self):
        birth_date = datetime.strptime(self.birthday_day.value, "%d.%m.%Y")
        today = datetime.now()
        next_birthday = birth_date.replace(year=today.year)
        if next_birthday < today:
            next_birthday = next_birthday.replace(year=today.year + 1)
        days_until = (next_birthday - today).days
        return days_until + 1

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
    def __init__(self):
        super().__init__()
        self.current_index = 0

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

    def iterator(self, n=1):
        records = list(self.data.values())
        while self.current_index < len(records):
            yield records[self.current_index:self.current_index + n]
            self.current_index += n

    def save_to_json(self, file_name):
        with open(file_name, 'w') as fh:
            json.dump(list(self.data.values()), fh, default=self.serialize_record)

    def serialize_record(self, record):
        serialized_phones = [phone.value for phone in record.phones]
        return {
            'name': record.name.value,
            'phones': serialized_phones,
            'birthday_day': record.birthday_day.value
        }

    def load_from_json(self, filename):
        try:
            with open(filename, 'r') as file:
                try:
                    records = json.load(file)
                    for record in records:
                        self.add_record(self.deserialize_record(record))
                except JSONDecodeError:
                    print(f"File '{filename}' is empty or doesn't contain valid JSON data.")
        except FileNotFoundError:
            print(f"File '{filename}' not found.")

    def deserialize_record(self, data):
        record = Record(data['name'], data['birthday_day'])
        for phone in data['phones']:
            record.add_phone(phone)
        return record

    def search(self, part):
        matching_records = []
        part = str(part)
        for record in self.data.values():
            if part in record.name.value:
                matching_records.append(record)
            else:
                for phone in record.phones:
                    if part in phone.value:
                        matching_records.append(record)
                        break
        return matching_records


if __name__ == '__main__':
    try:
        phone = Phone('99999000990')
        print(phone)
    except ValueError as e:
        print(e)

    try:
        birth = Birthday('20.02.200')
        print(birth)
    except ValueError as e:
        print(e)

    try:
        record = Record('stopa', '06.01.2085')
        record1 = Record('sdsva', '06.01.2025')
        record2 = Record('ffsdfpa', '06.01.2025')
        record3 = Record('ssdfsd', '06.01.2025')
        record4 = Record('fsdf', '06.01.2025')
        record5 = Record('dff', '06.01.2025')
        record6 = Record('sdff', '06.01.2025')
        print(record.birthday_day)
        days = record.days_to_birthday()
        print(days)
    except ValueError as e:
        print(e)

    try:
        adress = AddressBook()
        adress.add_record(record)
        adress.add_record(record1)
        adress.add_record(record2)
        adress.add_record(record3)
        adress.add_record(record4)
        adress.add_record(record5)
        adress.add_record(record6)

        for el in adress.iterator(2):
            print(el[0])
    except ValueError as e:
        print(e)
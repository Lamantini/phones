from main import Name, Phone, Birthday, Record, AddressBook
phone_dict = {}
adress_book = AddressBook()
adress_book.load_from_json('test.json')


def input_error(func):
    def inner(request):
        try:
            result = func(request)
        except KeyError:
            return 'Enter user name'
        except ValueError:
            return 'Give me name and phone please'
        except IndexError:
            return 'Give me name and phone please'
        return result
    return inner


@input_error
def handler_add(request):
    n_p = request.split(' ')
    record_name = n_p[1]
    record = adress_book.find(record_name)
    if record:
        record.add_phone(n_p[2])
        answer = 'Phone added to existing contact'
    else:
        new_record = Record(record_name)
        adress_book.add_record(new_record)
        answer = 'Added new contact'
    return answer


@input_error
def handler_change(request):
    n_p = request.split(' ')
    record_name = n_p[1]
    record = adress_book.find(record_name)
    if record:
        record.edit_phone(n_p[1], n_p[2])
        answer = 'Changed'
    else:
        answer = 'This name is not exist'
    return answer


@input_error
def handler_phone(request):
    n_p = request.split(' ')
    record_name = n_p[1]
    record = adress_book.find(record_name)
    if record:
        return record.phones.value


OPERATIONS = {
            'add': handler_add,
            'change': handler_change,
            'phone': handler_phone
        }


def main():
    while True:
        request = input('')
        request = request.lower()
        if request == 'hello':
            print('How can I help you?')
        elif request.startswith('show all'):
            for record in adress_book.data.values():
                print(record)
        elif request.startswith(('good bye', 'close', 'exit')):
            print('Good bye!')
            adress_book.save_to_json('test.json')
            return False
        else:
            handler = get_handler(request)
            print(handler(request))


def get_handler(request):
    if request.split(' ')[0] in OPERATIONS:
        return OPERATIONS[request.split(' ')[0]]
    else:
        return (lambda x: 'Give me correct command')


if __name__ == '__main__':
    main()

from token import Token


def print_tokens(tokens):
    for t in tokens:
        print('''({}: '{}')'''.format(t.get_type(), t.get_value()), end=' ')
    print()


class Thread:
    def __init__(self, name, data, count = 0):
        self.name = name
        self.data = data
        self.status = 'init'
        self.count = count

    def get_count(self):
        return self.count

    def set_count(self, new_count):
        self.count = new_count

    def get_status(self):
        return self.status

    def set_count(self, new_status):
        self.count = new_status

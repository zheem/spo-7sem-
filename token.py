class Token:
    def __init__(self, type, value):
        self.type = type
        self.value = value

    def get_type(self):
        return self.type

    def set_type(self, t):
        self.type = t

    def get_value(self):
        return self.value

    def set_value(self, v):
        self.value = v


def print_tokens(tokens):
    for t in tokens:
        print('''({}: '{}')'''.format(t.get_type(), t.get_value()), end=' ')
    print()
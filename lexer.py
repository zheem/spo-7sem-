import re
from token import Token
class Lexer:
    def __init__(self):
        self.tokens = []
        self.rules = [
        ('0|([1-9][0-9]*)',        'DIGIT'),
        ('if',                      'IF'),
        ('while',                   'WHILE'),
        ('function\s[a-zA-Z]+\d*',      'FN'),
        ('else',                     'ELSE'),
        ('return',                   'RETURN'),
        ('[a-zA-Z]+\d*',            'VAR'),
        ('\+|-|\*|/',                'ARI_OP'),
        ('==|!=|<|>',             'LOG_OP'),
        ('\(',                       'OP'),
        ('\)',                       'CP'),
        ('{',                       'OB'),
        ('}',                       'CB'),
        (';',                'SEMICOLON'),
        ('=',               'ASSIGN_OP')]

    def get_tokens(self):
        return self.tokens

    def print_tokens(self):
        for t in self.tokens:
            print('''({}: '{}')'''.format(t.get_type(), t.get_value()), end=' ')
        print()

    def lex(self, input):
        regex = re.compile('function\s[a-zA-Z]+\d*|==|!=|\d+|[a-zA-Z]+\d*|[-+*/=;<>{}()]')
        t = regex.findall(input)

        for tok in t:
            for reg, typ in self.rules:
                if re.match(re.compile(reg), tok):
                    self.tokens.append(Token(typ, tok))
                    break
        self.print_tokens()
        return self.tokens


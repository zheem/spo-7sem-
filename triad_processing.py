from token import Token


class Triad:
    def __init__(self, tokens, fun):
        self.tokens = tokens
        self.stack = []
        self.triads = []
        self.value_table = []
        self.token_count = 0
        self.stop_list = []
        self.pn = []
        self.out = []
        self.function = fun

    def triad_op(self, fl=True):
        self.triad_transfer()

        self.triads_optimization()

        if fl:
            self.reduction()
            print_triads(self.triads)
        else:
            print_triads(self.triads)

        print('RBN after triad optimization:')
        self.triads_to_pm()
        print_tokens(self.out)

        for v in self.value_table:
            v[1] = v[1].get_value()
        if len(self.value_table[0]) > 1:
            pass
        if fl:
            return self.out, self.value_table
        else:
            return self.out


    def triads_to_pm(self):
        for i in range(len(self.triads)):
            #for j in range(1,3):
            if self.triads[i][3].get_type() == 'CONST':
                pass
            elif self.triads[i][3].get_type() == 'WHILE' or self.triads[i][3].get_type() == 'IF' or self.triads[i][3].get_type() == 'GO_F' or self.triads[i][3].get_type() == 'GO_A' or self.triads[i][3].get_type() == 'END':
                self.pn.append(self.triads[i][3])

            else:
                if not self.found_triad_link(self.triads[i]):

                    if self.triads[i][1].get_type() != 'TR':
                        self.pn.append(self.triads[i][1])
                    else:
                        self.pn += self.add_triad(self.triads[i][1])
                    if self.triads[i][2].get_type() != 'TR':
                        self.pn.append(self.triads[i][2])
                    else:
                        self.pn += self.add_triad(self.triads[i][2])
                    self.pn.append(self.triads[i][3])
        self.pn = [i for i in self.pn if i.get_type() != 'FUN' and i.get_value() != 'RETURN']
        self.change_transitions()

    def change_transitions(self):
        self.token_count = 0
        transitions = ''
        while self.token_count < len(self.pn):
            if self.pn[self.token_count].get_type() == 'WHILE':
                transitions = 'WHILE'
            elif self.pn[self.token_count].get_type() == 'IF':
                transitions = 'IF'

            if self.pn[self.token_count].get_type() == 'WHILE':
                self.token_count += 1
                self.out += self.while_transitions()
            elif self.pn[self.token_count].get_type() == 'IF':
                self.token_count += 1
                self.out += self.if_transitions()
            else:
                self.out.append(self.pn[self.token_count])
            self.token_count += 1
        pass

    def while_transitions(self):
        _out = []
        while self.pn[self.token_count].get_type() != 'GO_A':
            _out.append( self.pn[self.token_count])
            self.token_count += 1
        _out.append( self.pn[self.token_count])
        for o in _out:
            if o.get_type() == 'GO_F':
                o.set_value(len(self.out) + len(_out)-1)
        for o in _out:
            if o.get_type() == 'GO_A':
                o.set_value(len(self.out)-1)
        return _out

    def if_transitions(self):
        _out = []
        while self.pn[self.token_count].get_type() != 'GO_A':
            _out.append(self.pn[self.token_count])
            self.token_count += 1
        for o in _out:
            if o.get_type() == 'GO_F':
                o.set_value(len(self.out) + len(_out))
        _out.append(self.pn[self.token_count])
        self.token_count+=1
        while self.pn[self.token_count].get_type() != 'END' and self.token_count < len(self.pn):
            _out.append(self.pn[self.token_count])
            self.token_count += 1
        for o in _out:
            if o.get_type() == 'GO_A':
                o.set_value(len(self.out) + len(_out)-1)
        return _out

    def index_search(self, tr):
        for i in range(len(self.triads)):
            if self.triads[i][0] == tr:
                return i


    def add_triad(self, t, fl = True):
        ind = self.index_search(t.get_value())
        out = []
        t = self.triads[ind]
        if t[3].get_type() == 'CONST':

            out = [t[1]]
        else:
            if True:
                if t[1].get_type() != 'TR':
                    out.append(t[1])
                else:
                    out += self.add_triad(t[1])
                if t[2].get_type() != 'TR':
                    out.append(t[2])
                else:
                    out += self.add_triad(t[2])
                out.append(t[3])
        return out


    def triad_transfer(self):
        ending = -1
        while self.token_count < len(self.tokens):
            if self.token_count == ending:
                self.triads.append(['^' + str(len(self.triads)), Token('END', 'END'), Token('END', 'END'),
                                    Token('END', self.token_count-1)])

            if self.tokens[self.token_count].get_type() == 'VAR' or self.tokens[self.token_count].get_type() == 'DIGIT':
                self.stack.append(self.tokens[self.token_count])
            elif self.tokens[self.token_count].get_type() == 'ARI_OP' or self.tokens[self.token_count].get_type() == 'ASSIGN_OP':
                self.triad_making()
            elif self.tokens[self.token_count].get_type() == 'ARI_OP' or self.tokens[self.token_count].get_type() == 'LOG_OP':
                self.triad_making()
            elif self.tokens[self.token_count].get_type() == 'GO_F':
                self.triads.append(['^' + str(len(self.triads)),Token('GO_F','GO_F'), self.tokens[self.token_count], self.tokens[self.token_count]])
            elif self.tokens[self.token_count].get_type() == 'GO_A':
                self.triads.append(['^' + str(len(self.triads)), Token('GO_A','GO_A'), self.tokens[self.token_count], self.tokens[self.token_count]])
                ending = self.tokens[self.token_count].get_value()+1

            elif self.tokens[self.token_count].get_type() == 'IF':
                self.triads.append(['^' + str(len(self.triads)), Token('IF', 'IF'), self.tokens[self.token_count],
                                    self.tokens[self.token_count]])
            elif self.tokens[self.token_count].get_type() == 'WHILE':
                self.triads.append(['^' + str(len(self.triads)), Token('WHILE', 'WHILE'), self.tokens[self.token_count],
                                    self.tokens[self.token_count]])
            elif self.tokens[self.token_count].get_type() == 'RETURN':
                self.triads.append(['^' + str(len(self.triads)), self.stack.pop(), self.tokens[self.token_count],
                                    Token('RETURN', 'RETURN')])

            elif self.tokens[self.token_count].get_type() == 'F_NAME':
                list = []
                f_ind = self.search_fun_index(self.tokens[self.token_count].get_value())
                length = len(self.function[f_ind][1])
                for i in range(length):
                    list.append(self.stack.pop())
                list.reverse()
                self.triads.append(['^' + str(len(self.triads)), Token('FN_VALUE', list), self.tokens[self.token_count],Token('FUN','FUN')])
                self.stack.append(Token('TR', self.triads[-1][0]))
            self.token_count += 1
        if ending >= self.token_count:
            self.triads.append(['^' + str(len(self.triads)), Token('END', 'END'), Token('END', 'END'),Token('END', self.token_count - 1)])


    def triad_making(self):
        e2 = self.stack.pop()
        e1 = self.stack.pop()
        self.triads.append(['^' + str(len(self.triads)), e1, e2, self.tokens[self.token_count]])
        self.stack.append(Token('TR', self.triads[-1][0]))

    def triads_optimization(self):
        count = 0
        variability = True
        #variability_end = 0
        while count < len(self.triads):
            # print(count)
            if self.triads[count][3].get_type() == 'GO_F':
                variability = False
            if self.triads[count][3].get_type() == 'END':
                variability = True

            if not variability:
                operand2 = self.triads[count][2]
            else:
                operand2 = self.operand_processing(self.triads[count][2])

            if self.triads[count][3].get_type() == 'ASSIGN_OP':
                if not variability:
                    if not self.triads[count][1].get_value() in self.stop_list:
                        self.stop_list.append(self.triads[count][1].get_value())

                    count += 1
                    continue
                self.triads[count][2] = operand2
                if self.find_value(self.triads[count][1].get_value()) is None:
                    self.value_table.append([self.triads[count][1].get_value(), operand2])
                else:
                    ind = self.find_value(self.triads[count][1].get_value(), False)
                    self.value_table[ind][-1] = operand2
            elif self.triads[count][3].get_type() == 'ARI_OP':
                if not variability:
                    operand1 = self.triads[count][1]
                else:
                    operand1 = self.operand_processing(self.triads[count][1])
                if operand2.get_type() == 'DIGIT' and operand1.get_type() == 'DIGIT':
                    self.triads[count][1] = self.operation(operand1.get_value(), operand2.get_value(), self.triads[count][3].get_value())
                    self.triads[count][2] = Token('DIGIT', 0)
                    self.triads[count][3] = Token('CONST', 'C')
            count += 1



    def operand_processing(self, triad):
        if triad.get_type() == 'VAR':
            op = self.find_value(triad.get_value())
            if op is not None and triad.get_value() not in self.stop_list:
                return Token('DIGIT', op.get_value())
            else:
                return triad
        elif triad.get_type() == 'TR':
            t = self.triads[int(triad.get_value()[1:])]
            if t[3].get_type() == 'CONST':
                return t[1]
            return triad
        elif triad.get_type() == 'DIGIT':
            return triad
        else:
            return triad

    def reduction(self):
        count = 0
        while count < len(self.triads):
            if self.triads[count][3].get_type() == 'CONST':
                if not self.found_triad_link(self.triads[count], count):
                    del self.triads[count]
                    count -= 1
            elif self.triads[count][3].get_type() == 'ASSIGN_OP' and self.triads[count][2].get_type() == 'DIGIT':
                if self.triads[count][1].get_value() in self.stop_list:
                    count+=1
                    continue
                c = self.found_var(self.triads[count], 0, count, False)
                if c[0] and self.triads[c[1]][3].get_type() == 'ASSIGN_OP' and self.triads[c[1]][2].get_type() == 'DIGIT':
                    if not self.found_var(self.triads[count], c[1]+1, count):
                        del self.triads[c[1]]
                        count -= 1

                if not self.found_var(self.triads[count], count+1, len(self.triads)):
                    del self.triads[count]
                    count -= 1

            count += 1

    def found_var(self, t, count, fin, fl = True):
        for i in range(count, fin):
            if t[1].get_value() == self.triads[i][1].get_value() or t[1].get_value() == self.triads[i][2].get_value():
                if fl:
                    return True
                else:
                    return [True, i]
        if fl:
            return False
        else:
            return [False, 0]

    def found_triad_link(self, t, count = 0):
        for i in range(count, len(self.triads)):
            if t[0] == self.triads[i][1].get_value() or t[0] == self.triads[i][2].get_value():
                return True
        return False

    def find_value(self, name, fl=True):
        for i in range(len(self.value_table)):
            if name == self.value_table[i][0]:
                if fl:
                    return self.value_table[i][-1]
                else:
                    return i
        return None

    def print_value(self):
        print('Value table')
        i = 0
        while i < len(self.value_table):
            if self.value_table[i][1].get_type() == 'TR':
                del self.value_table[i]
            else:
                print(self.value_table[i][0], self.value_table[i][1].get_value())
                i+=1


    def operation(self, e1, e2, op):
        if op == '-':
            return Token('DIGIT', float(e1) - float(e2))
        if op == '+':
            return Token('DIGIT', float(e1) + float(e2))
        if op == '*':
            return Token('DIGIT', float(e1) * float(e2))
        if op == '/':
            return Token('DIGIT', round(float(e1) / float(e2), 3))
        if op == '==':
            return Token('BOOL', float(e1) == float(e2))
        if op == '!=':
            return Token('BOOL', float(e1) != float(e2))
        if op == '>':
            return Token('BOOL', float(e1) > float(e2))
        if op == '<':
            return Token('BOOL', float(e1) < float(e2))

    def search_fun_index(self, name):
        for i in range(len(self.function)):
            if self.function[i][0] == name:
                return i
        return -1

def print_triads(triads):
    print("\nTriads:")
    for t in triads:
        if t[3].get_type() == 'FUN':
            print(t[0], end=' ')
            print_tokens(t[1].get_value(), False)
            print(t[2].get_value(), t[3].get_value())
        elif t[3].get_type() != 'WHILE' and t[3].get_type() != 'IF' and t[3].get_type() != 'END':
            print(t[0], t[1].get_value(), t[2].get_value(), t[3].get_value())
    print()



def print_tokens(tokens, fl = True):
    for t in tokens:
        if t.get_type() == 'FN_VALUE':
            print_tokens(t.get_value(), False )
        else:
            print('''({}: '{}')'''.format(t.get_type(), t.get_value()), end=' ')
    if fl:
        print()

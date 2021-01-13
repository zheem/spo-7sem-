from token import Token

class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.pos = 0
        self.expressions = []
        self.fn_list = []

    def lang(self):
        flag = True
        while self.pos < len(self.tokens):
            flag, pos = self.expr(self.pos)
            if not flag:
                print('Error')
                break
        return flag

    def expr(self, num):
        expr, new_pos = self.assign_expr(num)
        expr_if, new_pos_if = self.if_expr(num)
        expr_while, new_pos_while = self.while_expr(num)
        expr_fn, new_pos_fn = self.function_expr(num)
        self.pos = new_pos_if + new_pos + new_pos_while + new_pos_fn
        return expr or expr_if or expr_while or expr_fn,  self.pos


    def if_expr(self, num):
        if not self.if_t(num):
            return False, 0
        if_expr, num = self.head(num+1)
        if_ex, num = self.body(num)
        if_el = True
        num+=1
        if self.else_t(num):
            if_el, num = self.body(num+1)
        return if_expr and if_ex and if_el, num+1

    def function_expr(self, num):
        if not (self.function_t(num) and self.op(num + 1)):
            return False, 0
        func_expr, num = self.function_head(num+2)
        if not func_expr:
            return False, 0
        else:
            f_exp, num = self.function_body(num+1)
            return f_exp, num

    def function_body(self, num):
        body = self.ob(num)
        num+=1
        r, _num = self.return_expr(num)
        if r:
            return r, _num + 1
        while num <= len(self.tokens) :
           if self.cb(num):
               return body, num
           num1 = num
           body, num = self.expr(num)
           if not body:
               body, num = self.return_expr(num1)
               if not body:
                    return False, 0
               else:
                   return True, num+1
        return body, num

    def return_expr(self,num):
        return self.return_oper(num) and self.value(num+1) and self.semicolon(num+2), num+3

    def function_head(self,num):
        i = num
        while self.var(i):
            i+=1
        if self.cp(i):
            return True, i
        else:
            return False, 0

    def while_expr(self, num):
        if not self.while_t(num):
            return False, 0
        while_expr, num = self.head(num+1)
        while_ex, num = self.body(num)
        return while_expr and while_ex, num + 1

    def body(self, num):
        body = self.ob(num)
        num+=1
        while num <= len(self.tokens) :
           if self.cb(num):
               return body, num
           body, num = self.expr(num)
           if not body:
               return False, 0
        return body, num

    def head(self, num):
        return self.op(num) and self.log_expr(num+1) and self.cp(num+4), num+5

    def log_expr(self, n):
        return self.value(n) and self.log_op(n+1) and self.value(n+2)

    def assign_expr(self, num):
        var = self.var(num)
        assign = self.assign(num + 1)
        if not (var and assign):
            return False, 0
        value_expr, new_pos = self.value_expr(num + 2)
        if var and assign and value_expr:
            return True,  2 + new_pos
        else:
            return False, 0

    def value_expr(self, n):
        op_c = 0
        cp_c = 0
        val2 = True
        while(not self.semicolon(n)):
            if self.cp(n):
                cp_c += 1
            if self.op(n):
                op_c += 1
            val2 = val2 and (self.value(n) or self.ari_oper(n) or self.cp(n) or self.op(n))
            n += 1
            if not val2:
                return False, 0
        if op_c != cp_c:
            return False, 0
        return val2, n-1

    def value(self, num):
        if num >= len(self.tokens):
            return False
        return self.var(num) or self.digit(num) or self.fun(num)

    def fun(self, num):
        if self.tokens[num].get_value() in self.fn_list and self.op(num+1):
            num = num + 2
            while self.value(num):
                num+=1
            if self.cp(num):
                return True
            else:
                return False
        else:
            return False

    def semicolon(self, num):
        if num >= len(self.tokens):
            return False
        return self.find_token(self.tokens[num].get_type(), 'SEMICOLON')

    def var(self, num):
        if num >= len(self.tokens):
            return False
        return self.find_token(self.tokens[num].get_type(), 'VAR')

    def assign(self, num):
        if num >= len(self.tokens):
            return False
        return self.find_token(self.tokens[num].get_type(), 'ASSIGN_OP')

    def digit(self, num):
        if num >= len(self.tokens):
            return False
        return self.find_token(self.tokens[num].get_type(), 'DIGIT')

    def ari_oper(self, num):
        if num >= len(self.tokens):
            return False
        return self.find_token(self.tokens[num].get_type(), 'ARI_OP')

    def return_oper(self, num):
        if num >= len(self.tokens):
            return False
        return self.find_token(self.tokens[num].get_type(), 'RETURN')

    def function_t(self, num):
        if num >= len(self.tokens):
            return False
        exp = self.find_token(self.tokens[num].get_type(), 'FN')
        if exp:
            self.fn_list.append(self.tokens[num].get_value()[len('function '):])
        return self.find_token(self.tokens[num].get_type(), 'FN')


    def op(self, num):
        if num >= len(self.tokens):
            return False
        return self.find_token(self.tokens[num].get_type(), 'OP')

    def cp(self, num):
        if num >= len(self.tokens):
            return False
        return self.find_token(self.tokens[num].get_type(), 'CP')

    def if_t(self, num):
        if num >= len(self.tokens):
            return False
        return self.find_token(self.tokens[num].get_type(), 'IF')

    def while_t(self, num):
        if num >= len(self.tokens):
            return False
        return self.find_token(self.tokens[num].get_type(), 'WHILE')

    def else_t(self, num):
        if num >= len(self.tokens):
            return False
        return self.find_token(self.tokens[num].get_type(), 'ELSE')

    def ob(self, num):
        if num >= len(self.tokens):
            return False
        return self.find_token(self.tokens[num].get_type(), 'OB')

    def cb(self, num):
        if num >= len(self.tokens):
            return False
        return self.find_token(self.tokens[num].get_type(), 'CB')

    def log_op(self, num):
        if num >= len(self.tokens):
            return False
        return self.find_token(self.tokens[num].get_type(), 'LOG_OP')

    def find_token(self, type, found_t):
        if type == found_t:
            #print('Найдено', type)
            return True
        else:
            #print('упс', type,'искали -', found_t)
            return False
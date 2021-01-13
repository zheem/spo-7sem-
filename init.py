import sys
from lexer import Lexer
from parser import Parser
from rpn import RPN
from stack_machine import StackMachine
from triad_processing import Triad
from thread_manager import ThreadManager
from thread import Thread


print('Lexer:')
tokens = Lexer().lex((open(sys.argv[1]).read()))

print('\nParser initialized...\nSyntax valid?', Parser(tokens).lang())

if Parser(tokens).lang():
    rpn = RPN(tokens)
    transfer, fun = rpn.transfer_PN()

    t, val = Triad(transfer, fun).triad_op()

    for i in range(len(fun)):
        print("\nFunctions triads processing:")
        triad = Triad(fun[i][-1], fun)
        fun[i][-1] = triad.triad_op(False)

    stack_machine_instance = StackMachine(t, val, fun)

    if sys.argv[1] == 'spec/threads.lang':
        print('Enable multi-threading? [Yes/No]')
        thread_flag = input()
        if thread_flag == 'Yes':
            main_th = Thread('init', stack_machine_instance)
            th_manager = ThreadManager([main_th])
            th_manager.run()
            pass
        else:
            print('\nStack machine\nValues table:')
            stack_machine_instance.runner()
    else: 
        print('\nStack machine\nValues table:')
        stack_machine_instance.runner()

    


   

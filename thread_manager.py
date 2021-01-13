from token import Token
from thread import Thread
from stack_machine import StackMachine


class ThreadManager:
    def __init__(self, queue):
        self.thread_queue = queue

    def add_thread(self, thread):
        self.thread_queue.append(thread)

    def run(self):
        fl = False
        print("Thread {} add".format(self.thread_queue[0].name))
        while len(self.thread_queue) > 0:
            for i in range(len(self.thread_queue)):
                if len(self.thread_queue) == 1 and self.thread_queue[0].data.token_count >= len(self.thread_queue[0].data.tokens):
                    print("Thread {} ended".format(self.thread_queue[0].name))
                    self.thread_queue.pop()
                    break
                if (len(self.thread_queue) > 2 and i == 0) or (fl and i == 0 and len(self.thread_queue) > 1):
                    continue
                print("Thread {} run".format(self.thread_queue[i].name))
                stat, d = self.thread_queue[i].data.runner(True, len(self.thread_queue))
                if stat == 'exit' and not (len(self.thread_queue) == 1 and i == 0):
                    print("Thread {} ended".format(self.thread_queue[i].name))
                    if len(self.thread_queue) > 1:
                        self.thread_queue[0].data.add_value(d)
                        fl = True
                    else:
                        pass
                    del self.thread_queue[i]
                    if i + 1 >= len(self.thread_queue):
                        break
                elif stat == 'wait':
                    self.thread_queue[i].status = stat
                    sm = StackMachine(d[1], d[2], d[3])
                    self.thread_queue.append(Thread(d[0].get_value(), sm))
                    print("Thread {} add".format(d[0].get_value()))
        print('\nValues table:')
        print(d)
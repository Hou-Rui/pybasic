import queue

from pybasic import global_table

@global_table.reflect('QUEUE')
def queue_queue():
    return queue.Queue()

@global_table.reflect('STACK')
def queue_stack():
    return queue.LifoQueue()

@global_table.reflect('PUSH')
def queue_push(q, x):
    q.put(x)
    return x

@global_table.reflect('POP')
def queue_pop(q):
    return q.get()
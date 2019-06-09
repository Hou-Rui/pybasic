from pybasic import global_table

@global_table.reflect('FRONT')
def deque_front(q):
    return q[0]

@global_table.reflect('BACK')
def deque_back(q):
    return q[-1]

@global_table.reflect('PUSHFRONT')
def deque_push_front(q, x):
    q.insert(0, x)
    return x

@global_table.reflect('PUSH')
def deque_push(q, x):
    q.append(x)
    return x

@global_table.reflect('POPFRONT')
def deque_pop_front(q: list):
    x = q[0]
    q = q[1:]
    return x

@global_table.reflect('POP')
def deque_pop(q):
    return q.pop()
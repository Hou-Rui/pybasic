from .symbol_table import global_table, table_stack
from .utils import BasicError


@global_table.register('<PLUS>')
def basic_plus(n):
    a, b = n[0].run(), n[1].run()
    if isinstance(a, str) or isinstance(b, str):
        a, b = str(a), str(b)
    return a + b

global_table.set('<MINUS>', lambda n: n[0].run() - n[1].run())
global_table.set('<TIMES>', lambda n: n[0].run() * n[1].run())
global_table.set('<DIVIDE>', lambda n: n[0].run() / n[1].run())
global_table.set('<EXACTDIV>', lambda n: n[0].run() // n[1].run())
global_table.set('<MOD>', lambda n: n[0].run() % n[1].run())
global_table.set('<EXP>', lambda n: n[0].run() ** n[1].run())
global_table.set('<ASSIGN>', lambda n: table_stack.top().set(n[0], n[1].run()))
global_table.set('<UMINUS>', lambda n: -n[0].run())
global_table.set('<GREATER_THAN>', lambda n: n[0].run() > n[1].run())
global_table.set('<LESS_THAN>', lambda n: n[0].run() < n[1].run())
global_table.set('<EQUAL_GREATER_THAN>', lambda n: n[0].run() >= n[1].run())
global_table.set('<EQUAL_LESS_THAN>', lambda n: n[0].run() <= n[1].run())
global_table.set('<NOT_EQUAL>', lambda n: n[0].run() != n[1].run())
global_table.set('<EQUAL>', lambda n: n[0].run() == n[1].run())
global_table.set('<AND>', lambda n: n[0].run() and n[1].run())
global_table.set('<OR>', lambda n: n[0].run() or n[1].run())
global_table.set('<NOT>', lambda n: not n[0].run())
global_table.set('<AS>', lambda n: n[1].run()(n[0].run()))

@global_table.register('<DIM_ARRAY>')
def basic_dim_array(n):
    id_name, type_name, size = n[0], n[1], n[2].run()
    py_type = global_table.get(type_name)
    array = [py_type() for _ in range(size)]
    global_table.set(id_name, array)

@global_table.register('<ASSIGN_ARRAY>')
def basic_assign_array(n):
    id_name, basic_count, exp = n[0], n[1].run(), n[2].run()
    py_list = global_table.get(id_name)
    py_count = basic_count - 1
    try:
        py_list[py_count] = exp
    except IndexError:
        raise BasicError('Index %d is out of range (maximum %d)' % (py_count, len(py_list)))

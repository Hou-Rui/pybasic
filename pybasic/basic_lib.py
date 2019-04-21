import math
import os
import platform
import random
import time

from .symbol_table import global_table, table_stack


# console I/O
@global_table.register('print')
def basic_print(n):
    for node in n:
        print(node.run())


@global_table.register('write')
def basic_write(n):
    for node in n:
        print(node.run(), end='')


@global_table.register('input')
def basic_input(n):
    return input()


# file I/O
global_table.reflect('open', open)
global_table.reflect('close', lambda f: f.close())


@global_table.register('fprint')
def basic_fprint(n):
    f = n[0].run()
    args = n[1:]
    for node in args:
        print(node.run(), file=f)


@global_table.register('fwrite')
def basic_fwrite(n):
    f = n[0].run()
    args = n[1:]
    for node in args:
        print(node.run(), end='', file=f)


@global_table.register('finput')
def basic_finput(n):
    f = n[0].run()
    line = f.readline()
    if not line:
        return None
    return line[:-1]


# math
global_table.reflect('abs', abs)
global_table.reflect('sqr', math.sqrt)
global_table.reflect('sin', math.sin)
global_table.reflect('cos', math.cos)
global_table.reflect('tan', math.tan)
global_table.reflect('exp', math.exp)
global_table.reflect('log', math.log)
global_table.reflect('rnd', random.random)

# strings
global_table.reflect('asc', ord)
global_table.reflect('chr$', chr)
global_table.reflect('len$', len)
global_table.reflect('space$', lambda x: x * ' ')
global_table.reflect('mid$', lambda s, n, m: s[n - 1:n + m - 1])
global_table.reflect('left$', lambda s, n: s[:n])
global_table.reflect('right$', lambda s, n: s[-n:])
global_table.reflect('lcase$', lambda s: s.lower())
global_table.reflect('ucase$', lambda s: s.upper())
global_table.reflect('trim$', lambda s: s.strip())

# system


# utilities
# FUNCTION CLS() ' clear the screen
@global_table.register('cls')
def basic_cls(n):
    if platform.system() == 'Windows':
        os.system('cls')
    else:
        os.system('clear')


# FUNCTION SLEEP(X) ' suspend for X milliseconds
global_table.reflect('sleep', time.sleep)


# FUNCTION SWAP(A ByRef, B ByRef) ' swap two variables
@global_table.register('swap')
def basic_swap(n):
    current_table = table_stack.top()
    value0, value1 = n[0].run(), n[1].run()
    current_table.set(n[0].value, value1)
    current_table.set(n[1].value, value0)

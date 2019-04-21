#!python3
import platform
import math
import os
from .utils import BasicError, Stack

class SymbolTable:
    def __init__(self, parent=None):
        self._table = {}
        self.parent = parent

    def get(self, id):
        id = id.upper()
        if id in self._table:
            return self._table[id]
        if self.parent is None:
            raise BasicError('undefined variable "%s"' % id)
        else:
            return self.parent.get(id)

    def set(self, id, value):
        self._table[id.upper()] = value

    def register(self, id):
        def decorator(func):
            self.set(id, func)
            return func
        return decorator
    
    def reflect(self, id, func=None):
        if func is not None:
            new_func = lambda n: func(*(x.run() for x in n))
            self.set(id, new_func)
        else:
            def decorator(func):
                new_func = lambda n: func(*(x.run() for x in n))
                self.set(id, new_func)
                return new_func
            return decorator

global_table = SymbolTable()
table_stack = Stack([global_table])

# Constants
global_table.set('Nothing', None)
global_table.set('True', True)
global_table.set('False', False)
global_table.set('Pi', 3.14159265)

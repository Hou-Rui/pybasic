#! python3
import runpy
import sys
from os import path
import traceback

from . import basic_lib
from . import basic_operators
from . import basic_types
from .symbol_table import SymbolTable, global_table, table_stack
from .utils import Stack, item_getter, BasicError

from itertools import count

# https://www.coder.work/article/1249259
def stack_size2a(size=2):
    """Get stack size for caller's frame.
    """
    frame = sys._getframe(size)

    for size in count(size):
        frame = frame.f_back
        if not frame:
            return size

class tracer(object):
    registry = {}
    def __init__(self, func):       # On @ decorator
        self.calls = 0              # Save func for later call
        self.func = func
        self.max_lvl = 0
        tracer.registry[func.__name__] = self

    def __call__(self, *args, **kwargs):  # On call to original func
        self.calls += 1
        if self.calls > self.max_lvl:
             self.max_lvl = self.calls
             # sys._debugmallocstats()
             # traceback.print_stack()
             # print(f'stack depth = {stack_size2a()}')
        # print(f'RUN {self.type} {self.value}', file=sys.stderr)
        r = self.func(*args, **kwargs)
        self.calls -= 1
        return r

    def __get__(self, instance, owner):   # On method fetch
        def wrapper(*args, **kwargs):     # Retain both inst
            return self(instance, *args, **kwargs) # Runs __call__
        return wrapper

class ASTControl:
    def __init__(self, msg, value=None):
        self.msg = msg
        self.value = value

    def __eq__(self, obj):
        return self.msg == obj.msg


class ASTNode:
    literals = ('number', 'string')

    def __init__(self, type='', value='', tree=[], parent=None):
        self.type = type
        self.value = value
        self.tree = tree[:]
        self.parent = parent
        self.block = None

    def __str__(self):
        return '<ASTNode type="%s", value="%s">' % (self.type, self.value)

    @classmethod
    def TrueNode(cls):
        return cls(type='number', value=True)

    @classmethod
    def BlockNode(cls):
        return cls(type='flag', value='<BLOCK>')

    @classmethod
    def NothingNode(cls):
        return cls(type='number', value=None)

    def add(self, node):
        self.tree.append(node)
        if isinstance(node, ASTNode):
            node.parent = self

    def add_group(self, nodes):
        for node in nodes:
            self.add(node)

    def negative(self):
        node = ASTNode(type='funcall', value='<NOT>')
        node.add(self)
        return node

    def show(self, layer=0, end=False):
        # layer - 1, layer 1 indent same as layer 0 (PROGRAM)
        pre = '|   ' * (layer - 1) + ('└── ' if end else '├── ')
        print(pre + str(self), file=sys.stderr)
        for node in self.tree:
            if isinstance(node, ASTNode) and node.tree:
                node.show(layer + 1, node is self.tree[-1])

    def run_flag(self):
        if self.value == '<PROGRAM>':
            for node in self.tree:
                node.run()

        elif self.value in ('<SUB>', '<FUNCTION>'):

            def func(n):
                local_table = SymbolTable(table_stack.top())
                # compute in caller's level
                for index, param in enumerate(self.tree[1]):
                    local_table.set(param, n[index].run())
                table_stack.push(local_table)
                # if len(table_stack) > 50:
                #    print(f"table_stack too deep {len(table_stack)}")
                block_node = self.tree[2]
                result = block_node.run()
                table_stack.pop()
                if isinstance(result, ASTControl) and result.msg == 'return':
                    return result.value

            table_stack.top().set(self.tree[0], func)

        elif self.value == '<BLOCK>':
            for node in self.tree:
                result = node.run()
                if isinstance(result, ASTControl):
                    return result

        elif self.value == '<SEQ>':
            for node in self.tree:
                result = node.run()
                if isinstance(result, ASTControl):
                    return result
                elif result is True:
                    return result
            return False

        elif self.value == '<IF>':
            if self.tree[0].run() is True:
                result = self.tree[1].run()
                if isinstance(result, ASTControl):
                    return result
                return True
            return False

        elif self.value == '<FOR>':
            loop_var_name = self.tree[0].value
            start = self.tree[1].run()
            get_end = lambda: self.tree[2].run()
            get_step = lambda: self.tree[3].run()
            table_stack.top().set(loop_var_name, start)
            while True:
                loop_var = table_stack.top().get(loop_var_name)
                result = self.tree[4].run()
                if isinstance(result, ASTControl):
                    if result.msg == 'break':
                        break
                    elif result.msg == 'continue':
                        continue
                    elif result.msg == 'return':
                        return result
                table_stack.top().set(loop_var_name, loop_var + get_step())
                if loop_var == get_end():
                    break

        elif self.value == '<DO>':
            while True:
                result = self.tree[1].run()
                if isinstance(result, ASTControl):
                    if result.msg == 'break':
                        break
                    elif result.msg == 'continue':
                        continue
                    elif result.msg == 'return':
                        return result
                if self.tree[0].run() is False:
                    break

        elif self.value == '<WHILE>':
            while self.tree[0].run() is True:
                result = self.tree[1].run()
                if isinstance(result, ASTControl):
                    if result.msg == 'break':
                        break
                    elif result.msg == 'continue':
                        continue
                    elif result.msg == 'return':
                        return result

        elif self.value == '<BREAK>':
            return ASTControl('break')

        elif self.value == '<CONTINUE>':
            return ASTControl('continue')

        elif self.value == '<RETURN>':
            return ASTControl('return', self.tree[0].run())

        elif self.value == '<END>':
            sys.exit(0)
            return ASTControl('end')

        elif self.value == '<RUN_PY>':
            file_name = self.tree[0]
            if path.isfile(file_name):
                runpy.run_path(file_name)

    @tracer
    def run(self):
        if self.type == 'flag':
            return self.run_flag()

        elif self.type == 'funcall':
            func = table_stack.top().get(self.value)
            if isinstance(func, list):
                getter = item_getter(func)
                return getter(self.tree)
            try:
                return func(self.tree)
            except IndexError:
                raise BasicError('Wrong number of arguments when calling %s' % self.value)

        elif self.type == 'id':
            return table_stack.top().get(self.value)

        elif self.type == 'array':
            return [n.run() for n in self.value]

        elif self.type in ASTNode.literals:
            return self.value


def build_ast():
    root = ASTNode(type='flag', value='<PROGRAM>')
    return root

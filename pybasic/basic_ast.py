#! python3
import runpy

from . import basic_lib
from . import basic_operators
from . import basic_types
from .symbol_table import SymbolTable, global_table, table_stack
from .utils import Stack, item_getter


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
        pre = '|   ' * (layer - 1) + ('└── ' if end else '├── ')
        print(pre + str(self))
        for node in self.tree:
            if isinstance(node, ASTNode) and node.tree:
                node.show(layer + 1, node is self.tree[-1])

    def run_flag(self):
        if self.value == '<PROGRAM>':
            for node in self.tree:
                node.run()

        elif self.value == '<FUNCTION>':

            def func(n):
                local_table = SymbolTable(table_stack.top())
                table_stack.push(local_table)
                for index, param in enumerate(self.tree[1]):
                    local_table.set(param, n[index].run())
                block_node = self.tree[2]
                result = block_node.run()
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

        elif self.value == '<RUN_PY>':
            runpy.run_path(self.tree[0])

    def run(self):
        if self.type == 'flag':
            return self.run_flag()

        elif self.type == 'funcall':
            func = table_stack.top().get(self.value)
            if isinstance(func, list):
                getter = item_getter(func)
                return getter(self.tree)
            return func(self.tree)

        elif self.type == 'id':
            return table_stack.top().get(self.value)

        elif self.type == 'array':
            return [n.run() for n in self.value]

        elif self.type in ASTNode.literals:
            return self.value


def build_ast():
    root = ASTNode(type='flag', value='<PROGRAM>')
    return root

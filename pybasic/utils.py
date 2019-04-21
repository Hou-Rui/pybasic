#! python3

class Stack:
    def __init__(self, items=[]):
        self.items = items
    def __len__(self):
        return len(self.items)
    def top(self):
        return self.items[-1]
    def push(self, x):
        self.items.append(x)
    def pop(self):
        return self.items.pop()

class RootStack(Stack):
    control_blocks = ('<WHILE>', '<DO>', '<FOR>')
    closure_blocks = ('<SUB>', '<FUNCTION>')
    def control_top(self):
        for item in reversed(self.items):
            if item.parent.value in RootStack.control_blocks:
                return item
        return None
    def closure_top(self):
        for item in reversed(self.items):
            if item.parent.value in RootStack.closure_blocks:
                return item
        return None

class BasicError(Exception):
    pass

def item_getter(x):
    def getter(args):
        result = x
        for layer in args:
            basic_count = layer.run()
            py_count = basic_count - 1
            try:
                result = result[py_count]
            except IndexError:
                raise BasicError('Index %d is out of range (maximum %d)' % (basic_count, len(result)))
        return result
    return getter

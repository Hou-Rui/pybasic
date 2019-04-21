#! python3
import readline
from os import path

import ply.yacc as yacc

from .basic_ast import ASTNode, build_ast
from .basic_lex import tokens
from .utils import BasicError, RootStack

# Abstract syntax tree.
ast = build_ast()
root_stack = RootStack([ast])

# Precedence specifier.
precedence = (
    ('left', 'COMMA'),
    ('left', 'AND', 'OR'),
    ('left', 'EQUALS', 'NOT_EQUAL', 'GREATER_THAN', 'LESS_THAN', 'EQUAL_GREATER_THAN', 'EQUAL_LESS_THAN'),
    ('left', 'AS'),
    ('left', 'PLUS', 'MINUS'),
    ('left', 'TIMES', 'DIVIDE', 'MOD'),
    ('left', 'EXP'),
    ('right', 'UMINUS', 'NOT'),
)

# Parsers.
def p_singleline_statement(p):
    '''
    statement : assignment
              | declaration
              | expression
              | funcall
              | control
              | return
              | defun_statement
    '''
    current_root = root_stack.top()
    p[0] = p[1]
    current_root.add(p[0])

def p_multiline_begin_statement(p):
    '''
    statement : block_begin
    '''
    current_root = root_stack.top()
    p[0] = p[1]
    current_root.add(p[0])
    root_stack.push(p[0].block)

def p_multiline_end_statement(p):
    '''
    statement : block_end
    '''
    root_stack.pop()
    p[0] = p[1]

def p_if_else_elseif(p):
    '''
    statement : if_block_begin
              | elseif_block_begin
              | else_statement
    '''
    p[0] = p[1]

def p_args_list(p):
    '''
    args_list : args_list COMMA expression
              | expression
    '''
    if len(p) == 2:
        p[0] = ASTNode(type='flag', value='<ARGS>', tree=[p[1]])
    else:
        p[0] = p[1]
        p[0].add(p[3])

def p_param_list(p):
    '''
    params_list : params_list COMMA ID
               | ID
    '''
    if len(p) == 2:
        p[0] = ASTNode(type='flag', value='<PARAMS>', tree=[p[1]])
    else:
        p[0] = p[1]
        p[0].add(p[3])

def p_defun(p):
    '''
    defun_statement : DEFUN ID LPAREN params_list RPAREN EQUALS expression
    '''
    p[0] = ASTNode(type='flag', value='<FUNCTION>')
    block_node = ASTNode.BlockNode()
    return_node = ASTNode(type='flag', value='<RETURN>')
    return_node.add(p[7])
    block_node.add(return_node)
    p[0].add_group([
        p[2], # function name
        p[4].tree[:], # params list
        block_node
    ])

def p_funcall(p):
    '''
    funcall : ID args_list
    '''
    args = p[2].tree[:]
    p[0] = ASTNode(type='funcall', value=p[1], tree=args)

def p_assignment(p):
    '''
    assignment : ID EQUALS expression
               | LET ID EQUALS expression
               | ID LPAREN expression RPAREN EQUALS expression
    '''
    if len(p) == 4:
        p[0] = ASTNode(type='funcall', value='<ASSIGN>', tree=[p[1], p[3]])
    elif len(p) == 5:
        p[0] = ASTNode(type='funcall', value='<ASSIGN>', tree=[p[2], p[4]])
    else:
        p[0] = ASTNode(type='funcall', value='<ASSIGN_ARRAY>', tree=[p[1], p[3], p[6]])

def p_declare(p):
    '''
    declaration : declare_array
    '''
    p[0] = p[1]

def p_declare_array(p):
    '''
    declare_array : DIM ID LPAREN expression RPAREN AS ID
    '''
    p[0] = ASTNode(type='funcall', value='<DIM_ARRAY>', tree=[p[2], p[7], p[4]])

def p_rel_expression(p):
    '''
    rel_expression : expression GREATER_THAN expression
                   | expression LESS_THAN expression
                   | expression EQUAL_GREATER_THAN expression
                   | expression EQUAL_LESS_THAN expression
                   | expression EQUALS expression
                   | expression NOT_EQUAL expression
                   | rel_expression AND rel_expression
                   | rel_expression OR rel_expression
                   | LPAREN rel_expression RPAREN
                   | NOT rel_expression
    '''
    if p[2] == '>':
        p[0] = ASTNode(type='funcall', value='<GREATER_THAN>', tree=[p[1], p[3]])
    elif p[2] == '<':
        p[0] = ASTNode(type='funcall', value='<LESS_THAN>', tree=[p[1], p[3]])
    elif p[2] == '>=':
        p[0] = ASTNode(type='funcall', value='<EQUAL_GREATER_THAN>', tree=[p[1], p[3]])
    elif p[2] == '<=':
        p[0] = ASTNode(type='funcall', value='<EQUAL_LESS_THAN>', tree=[p[1], p[3]])
    elif p[2] == '=':
        p[0] = ASTNode(type='funcall', value='<EQUAL>', tree=[p[1], p[3]])
    elif p[2] == '<>':
        p[0] = ASTNode(type='funcall', value='<NOT_EQUAL>', tree=[p[1], p[3]])
    elif p[2] == 'and':
        p[0] = ASTNode(type='funcall', value='<AND>', tree=[p[1], p[3]])
    elif p[2] == 'or':
        p[0] = ASTNode(type='funcall', value='<OR>', tree=[p[1], p[3]])
    elif p[1] == 'not':
        p[0] = ASTNode(type='funcall', value='<NOT>', tree=[p[2]])
    elif p[1] == '(':
            p[0] = p[2]

def p_expression_calc(p):
    '''
    expression : expression PLUS expression
               | expression MINUS expression
               | expression TIMES expression
               | expression DIVIDE expression
               | expression EXACTDIV expression
               | expression MOD expression
               | expression AS expression
               | expression EXP expression
               | MINUS expression %prec UMINUS
               | LPAREN expression RPAREN
    '''
    if len(p) == 4: # binary expression
        if p[2] == '+':
            p[0] = ASTNode(type='funcall', value='<PLUS>', tree=[p[1], p[3]])
        elif p[2] == '-':
            p[0] = ASTNode(type='funcall', value='<MINUS>', tree=[p[1], p[3]])
        elif p[2] == '*':
            p[0] = ASTNode(type='funcall', value='<TIMES>', tree=[p[1], p[3]])
        elif p[2] == '/':
            p[0] = ASTNode(type='funcall', value='<DIVIDE>', tree=[p[1], p[3]])
        elif p[2] == '\\':
            p[0] = ASTNode(type='funcall', value='<EXACTDIV>', tree=[p[1], p[3]])
        elif p[2] == 'MOD':
            p[0] = ASTNode(type='funcall', value='<MOD>', tree=[p[1], p[3]])
        elif p[2] == 'AS':
            p[0] = ASTNode(type='funcall', value='<AS>', tree=[p[1], p[3]])
        elif p[2] == '^':
            p[0] = ASTNode(type='funcall', value='<EXP>', tree=[p[1], p[3]])
        elif p[1] == '(':
            p[0] = p[2]
    elif len(p) == 3: # unary expression
        if p[1] == '-':
            p[0] = ASTNode(type='funcall', value='<UMINUS>', tree=[p[2]])

def p_inline_funcall(p):
    '''
    expression : ID LPAREN RPAREN
               | ID LPAREN args_list RPAREN
    '''
    if len(p) == 4:
        p[0] = ASTNode(type='funcall', value=p[1])
    else:
        args = p[3].tree[:]
        p[0] = ASTNode(type='funcall', value=p[1], tree=args)

def p_expression_number(p):
    '''
    expression : INTEGER
               | DECIMAL
    '''
    p[0] = ASTNode(type='number', value=p[1])

def p_expression_string(p):
    '''
    expression : STRING
    '''
    p[0] = ASTNode(type='string', value=p[1])

def p_expression_id(p):
    '''
    expression : ID
    '''
    p[0] = ASTNode(type='id', value=p[1])

def p_expression_array(p):
    '''
    expression : LBRACE args_list RBRACE
    '''
    elements = p[2].tree[:]
    p[0] = ASTNode(type='array', value=elements)

def p_block_begin(p):
    '''
    block_begin : while_block_begin
                | for_block_begin
                | do_block_begin
                | function_block_begin
    '''
    p[0] = p[1]

def p_if_block_begin(p):
    '''
    if_block_begin : IF rel_expression THEN
    '''
    current_root = root_stack.top()
    seq_node = ASTNode(type='flag', value='<SEQ>')
    current_root.add(seq_node)
    p[0] = ASTNode(type='flag', value='<IF>')
    p[0].add_group([
        p[2],
        ASTNode.BlockNode(),
    ])
    p[0].block = p[0].tree[1]
    seq_node.add(p[0])
    root_stack.push(p[0].block)

def p_else(p):
    '''
    else_statement : ELSE
    '''
    current_root = root_stack.top()
    if_node = current_root.parent
    if if_node.value != '<IF>':
        raise BasicError('ELSE without IF')
    seq_node = if_node.parent
    p[0] = ASTNode(type='flag', value='<IF>', parent=if_node)
    p[0].add_group([
        ASTNode.TrueNode(),
        ASTNode.BlockNode(),
    ])
    p[0].block = p[0].tree[1]
    seq_node.add(p[0])
    root_stack.pop()
    root_stack.push(p[0].block)

def p_elseif(p):
    '''
    elseif_block_begin : ELSEIF rel_expression THEN
    '''
    current_root = root_stack.top()
    if_node = current_root.parent
    if if_node.value != '<IF>':
        raise BasicError('ELSEIF without IF')
    seq_node = if_node.parent
    p[0] = ASTNode(type='flag', value='<IF>', parent=if_node)
    p[0].add_group([
        p[2],
        ASTNode.BlockNode(),
    ])
    p[0].block = p[0].tree[1]
    seq_node.add(p[0])
    root_stack.pop()
    root_stack.push(p[0].block)

def p_while_block_begin(p):
    '''
    while_block_begin : WHILE rel_expression
    '''
    p[0] = ASTNode(type='flag', value='<WHILE>')
    p[0].add_group([
        p[2], # judgement
        ASTNode.BlockNode()
    ])
    p[0].block = p[0].tree[1]

def p_do_block_begin(p):
    '''
    do_block_begin : DO
    '''
    p[0] = ASTNode(type='flag', value='<DO>')
    p[0].add_group([
        None, # to be filled when parsing LOOP
        ASTNode.BlockNode()
    ])
    p[0].block = p[0].tree[1]

def p_for_block_begin(p):
    '''
    for_block_begin : FOR ID EQUALS expression TO expression
                    | FOR ID EQUALS expression TO expression STEP expression
    '''
    p[0] = ASTNode(type='flag', value='<FOR>')
    p[0].add_group([
        ASTNode(type='id', value=p[2]), # loop variable
        p[4], # start
        p[6], # end
        ASTNode(type='number', value=1) if len(p) == 7 else p[8], # step
        ASTNode.BlockNode()
    ])
    p[0].block = p[0].tree[4]

def p_function_block_begin(p):
    '''
    function_block_begin : SUB ID LPAREN params_list RPAREN
                         | FUNCTION ID LPAREN params_list RPAREN
    '''
    p[0] = ASTNode(type='flag', value='<%s>' % p[1])
    block_node = ASTNode.BlockNode()
    p[0].add_group([
        p[2],
        p[4].tree[:],
        block_node
    ])
    p[0].block = p[0].tree[2]

def p_if_block_end(p):
    '''
    block_end : END IF
    '''
    current_root = root_stack.top()
    if current_root.parent.value != '<IF>':
        raise BasicError('END IF without IF')

def p_while_block_end(p):
    '''
    block_end : END WHILE
              | WEND
    '''
    current_root = root_stack.top()
    if current_root.parent.value != '<WHILE>':
        raise BasicError('END WHILE without WHILE')

def p_for_block_end(p):
    '''
    block_end : END FOR
              | NEXT ID
    '''
    current_root = root_stack.top()
    for_node = current_root.parent
    if for_node.value != '<FOR>':
        raise BasicError('END FOR without FOR')
    if p[1] == 'NEXT' and p[2] != for_node.tree[0].value:
        raise BasicError('Unmatched NEXT %s with %s' % p[2])

def p_do_block_end(p):
    '''
    block_end : LOOP
              | LOOP WHILE rel_expression
              | LOOP UNTIL rel_expression
    '''
    current_root = root_stack.top()
    do_node = current_root.parent
    if do_node.value != '<DO>':
        raise BasicError('LOOP without DO')
    if len(p) == 2:
        do_node.tree[0] = ASTNode.TrueNode()
    elif p[2] == 'WHILE':
        do_node.tree[0] = p[3]
    elif p[2] == 'UNTIL':
        do_node.tree[0] = p[3].negative()

def p_function_block_end(p):
    '''
    block_end : END SUB
              | END FUNCTION
    '''
    current_root = root_stack.top()
    func_node = current_root.parent
    if func_node.value != '<%s>' % p[2]:
        raise BasicError('END %s without %s' % (p[2], p[2]))

def p_return(p):
    '''
    return : RETURN
           | RETURN expression
    '''
    current_root = root_stack.closure_top()
    func_node = current_root.parent
    if len(p) == 2 and func_node.value not in ('<FUNCTION>', '<SUB>'):
        raise BasicError('RETURN without FUNCTION or SUB')
    if len(p) == 3 and func_node.value != '<FUNCTION>':
        raise BasicError('RETURN value without FUNCTION')
    p[0] = ASTNode(type='flag', value='<RETURN>')
    if len(p) == 2:
        p[0].add(ASTNode.NothingNode())
    else:
        p[0].add(p[2])

def p_control_exit(p):
    '''
    control : EXIT WHILE
            | EXIT DO
            | EXIT FOR
    '''
    current_root = root_stack.control_top()
    node = current_root.parent
    if node.value != '<%s>' % p[2]:
        raise BasicError('EXIT %s without %s' % (p[2], p[2]))
    p[0] = ASTNode(type='flag', value='<BREAK>')

def p_control_continue(p):
    '''
    control : CONTINUE WHILE
            | CONTINUE DO
            | CONTINUE FOR
    '''
    current_root = root_stack.control_top()
    node = current_root.parent
    if node.value != '<%s>' % p[2]:
        raise BasicError('CONTINUE %s without %s' % (p[2], p[2]))
    p[0] = ASTNode(type='flag', value='<CONTINUE>')

def p_use_statement(p):
    '''
    statement : USE ID
    '''
    py_module_name = '%s.py' % p[2]
    basic_module_name = '%s.bas' % p[2]
    if path.isfile(basic_module_name):
        module_file = open(basic_module_name)
        lines = module_file.readlines()
        module_file.close()
        for line in lines:
            parser.parse(line)
    elif path.isfile(py_module_name):
        current_root = root_stack.top()
        p[0] = ASTNode(type='flag', value='<RUN_PY>')
        p[0].add(py_module_name)
        current_root.add(p[0])
    else:
        raise BasicError('No such module: %s' % p[2])

# Error rule for syntax errors.
def p_error(p):
    # blank lines or errors
    if p is not None:
        raise BasicError('Syntax error on line %d' % p.lineno)

# Build the parser.
parser = yacc.yacc()

#! python3
import ply.lex as lex
from .utils import BasicError

# List of reserved words.
reserved_tuple = (
    'LET', 'DIM',
    'IF', 'THEN', 'ELSE', 'ELSEIF', 'END',
    'WHILE', 'DO', 'WEND', 'LOOP', 'UNTIL',
    'FOR', 'TO', 'STEP', 'NEXT',
    'EXIT', 'CONTINUE',
    'DEFUN', 'SUB', 'FUNCTION', 'RETURN',
    'AND', 'OR', 'NOT', 'MOD', 'AS',
    'USE',
)

reserved_words = {x : x for x in reserved_tuple}

# List of token names, including reserved words.
tokens = (
    'ID', 'INTEGER', 'DECIMAL', 'STRING',
    'EQUALS', 'PLUS', 'MINUS', 'TIMES', 'DIVIDE', 'EXACTDIV', 'EXP',
    'GREATER_THAN', 'LESS_THAN', 'EQUAL_GREATER_THAN', 'EQUAL_LESS_THAN', 'NOT_EQUAL',
    'LPAREN', 'RPAREN', 'LBRACE', 'RBRACE', 'COMMA',
)
tokens += reserved_tuple

# Characters to be ignored.
t_ignore = ' \t'
# Regular Expressions of tokens.
t_EQUALS = r'='
t_PLUS = r'\+'
t_MINUS = r'-'
t_TIMES = r'\*'
t_DIVIDE = r'/'
t_EXACTDIV = r'\\'
t_EXP = r'\^'
t_GREATER_THAN = r'\>'
t_LESS_THAN = r'\<'
t_EQUAL_GREATER_THAN = r'\>\='
t_EQUAL_LESS_THAN = r'\<\='
t_NOT_EQUAL = r'\<\>'
t_LPAREN = r'\('
t_RPAREN = r'\)'
t_LBRACE = r'\{'
t_RBRACE = r'\}'
t_COMMA = r'\,'

# Regular expression rules for some tokens with action codes.
def t_DECIMAL(t):
    r'[1-9]*[0-9]\.[0-9]*'
    t.value = float(t.value)
    return t
def t_INTEGER(t):
    r'\d+'
    t.value = int(t.value)
    return t
def t_STRING(t):
    r'\"(.*?)\"'
    t.value = t.value[1:-1]
    return t
def t_ID(t):
    r'[a-zA-Z_\$][a-zA-Z_\$0-9]*'
    t.value = t.value.upper()
    t.type = reserved_words.get(t.value.upper(), 'ID') # Check for reserved words
    return t
def t_COMMENT(t):
    r'\'.*'
    pass # Discard comments

# Track line numbers.
def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)
# Error handling rules.
def t_error(t):
    raise BasicError('Illegal character: "%s"' % t.value[0])

# Build the lexer.
lexer = lex.lex()

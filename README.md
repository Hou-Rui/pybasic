# pybasic

A structured BASIC interpreter written in Python.

```plain

usage: pybasic.py [-h] [-a] [-s AST_PATH] [program_name]

Execute pybasic programs, or start an REPL session.

positional arguments:

  program_name          The path of the source program to execute. If not
                        specified, an REPL session will be started.

optional arguments:
  -h, --help            show this help message and exit
  -a, --ast             Execute a binary abstract syntax tree file rather than
                        a source program. This will be ignored in REPL mode.
  -s AST_PATH, --save AST_PATH
                        Save the binary abstract syntax tree of the source
                        program to the given path. The source program will not
                        be executed. This will be ignored in REPL mode.
```

#### expressions

Supported expressions:

- `<expression>`: Math expressions. Support operators: `+`, `-`, `*`,
`/`, `\`(exact division), `MOD`
- `<rel_expression>`: Logic expressions. Support operators: `AND`,
`OR`, `NOT`, `=`(equals to), `<>`

Please notice `=` in `<rel_expression>` is different from `=` in assignment statement.

Literal values and function calls are also treated as `<expression>`. For example:

```basic
123                ' 123
123.5              ' 123.5
"123!"             ' "123!"
{1, 2, 3}          ' [1, 2, 3]
SQR(5)             ' 2.23606797749979
```

#### assignments

Use `LET <id> = <expression>` or simply `<id> = <expression>`.

Declarations are not required, for a variable are defined immediately before it is assigned for the first time. However, you can still use `DIM` to create an array filled with initial values. For example:

```basic
DIM A(5) AS INTEGER
PRINT A     ' [0, 0, 0, 0, 0]
```

#### control structures

Supported control structures:

- `WHILE <rel_expression> ... END WHILE / WEND`
- `DO ... LOOP`
- `DO ... LOOP WHILE / UNTIL <rel_expression>`
- `FOR <id> = <expression> TO <expression> ... NEXT <id> / END FOR`

Please notice that `GOTO` is not supported.

#### data types

Supported data types:

- `INTEGER` (mapped to Python type `int`)
- `DECIMAL` (mapped to Python type `float`)
- `STRING` (mapped to Python type `str`)

Please notice that pybasic does not actually store data types, which means the type of variables can be modified at runtime.

Use `AS` operator to do type conversions. For example:

```basic
2.5 AS INTEGER       ' 2
2.5 AS STRING        ' "2.5"
```

#### functions

Some inner functions are provided, like `SQR()` and etc.

Single-line functions can be defined with `DEFUN`. For example:

```basic
DEFUN F(x) = x * x
PRINT F(5)          ' 25
```

Multi-line functions can be defined with `SUB ... END SUB` or `FUNCTION ... END FUNCTION`.

Functions can be called directly by using the function name as an order. For example:

```basic
DEFUN PRTYES(s) = PRINT("yes! " + s)
SUB PRTYEAH(s)
    PRINT "yeah! " + s
END SUB
PRTYES "pybasic"           ' "yes! pybasic"
PRTYEAH "pybasic"          ' "yeah! pybasic"
```

#### Structures

Pybasic provides `STRUCT()` function to create a C-like structures. Once created, you may add any member to a structure or access a member using dot grammar. For example:

```basic
FUNCTION PERSON(NAME, AGE)
    THIS = STRUCT()
    THIS.NAME = NAME
    THIS.AGE = AGE
    RETURN THIS
END FUNCTION

JOHN = PERSON("John Smith", 30)
PRINT JOHN.NAME    ' "John Smith"
PRINT JOHN.AGE     ' 30

```

#### I/O

Unlike most BASIC dialects, pybasic provides `PRINT()` and `INPUT()` functions instead of statements. For example:

```basic
A = INPUT() AS INTEGER    ' input 17
PRINT "My age is " + A    ' "My age is 17"

```

#### modules

Use ```USE``` to import a Python module or another pybasic program. Pybasic will try finding a file ended with ```.bas``` or ```.py``` following the module's name in the current working directory. If no such file is finded, an error will be raised. For example:

```basic
' HELLO.bas
FUNCTION PRTHELLO(A)
    PRINT "Hello, " + A
END FUNCTION
```

```python
# MORNING.py
from pybasic import global_table

@global_table.reflect('PRTMORN')
def print_morning(a):
    print('Good morning, %s' % a)
```

```basic
' MAIN.bas
USE HELLO
USE MORNING

PRTHELLO "Jack" ' Hello, Jack
PRTMORN "Mary"  ' Good morning, Mary
```

Any code in the module will be executed. If the module is python-based, it will be executed at runtime; if it is pybasic-based, it will be compiled into the main program before being executed.

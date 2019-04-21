#!/usr/bin/env python3

import argparse
import pickle
import sys

from .basic_yacc import ast, parser, root_stack
from .utils import BasicError


def print_error(error):
    print('ERROR: %s' % error, file=sys.stderr)


# Read-evaluate-print-loop (REPL).
def parse_line(cnt, in_block=False):
    prompt = '> ' if in_block else 'In [%d]: ' % cnt
    while True:
        try: s = input(prompt)
        except (EOFError, KeyboardInterrupt):
            sys.exit(1)
        if s: break
    return parser.parse(s)

def repl():
    cnt = 1
    while True:
        try:
            result = parse_line(cnt)
            while len(root_stack) > 1:
                parse_line(cnt, in_block=True)
        except Exception as error:
            print_error(error)
            cnt += 1
            continue
        if result is not None:
            try:
                out = result.run()
                if out is not None:
                    print('Out [%d]: %s' % (cnt, out))
            except Exception as error:
                print_error(error)
            print('')
        cnt += 1

# Execute a text-based program.
def execute(program_name):
    f = open(program_name, 'r')
    lines = f.readlines()
    try:
        for line in lines:
            parser.parse(line)
        ast.run()
    except Exception as error:
        print_error(error)


# Save AST object with pickle.
def save_ast(input_name, output_name):
    with open(input_name, 'r') as input_file, open(output_name, 'wb') as output_file:
        lines = input_file.readlines()
        for line in lines:
            parser.parse(line)
        pickle.dump(ast, output_file)

# Execute a binary AST program.
def execute_ast(ast_file_name):
    with open(ast_file_name, 'rb') as input_file:
        new_ast = pickle.load(input_file)
    new_ast.run()


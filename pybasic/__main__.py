import argparse
import pickle
import sys

from .basic_yacc import ast, parser, root_stack
from .utils import BasicError
from .pybasic import *

# Main function.
def main():
    arg_parser = argparse.ArgumentParser(
        description='Execute pybasic programs, or start an REPL session.',
    )

    arg_parser.add_argument('program_name', nargs='?',
        help='The path of the source program to execute. '
        'If not specified, an REPL session will be started.')

    arg_parser.add_argument('-a', '--ast', action='store_true', dest='ast',
        help='Execute a binary abstract syntax tree file rather than a source program. '
        'This will be ignored in REPL mode. ')

    arg_parser.add_argument('-s', '--save', action='store', dest='ast_path',
        help='Save the binary abstract syntax tree of the source program to the given path. '
        'The source program will not be executed. '
        'This will be ignored in REPL mode. ')
    args = arg_parser.parse_args()
    if not args.program_name:
        repl()
    else:
        if args.ast_path:
            save_ast(args.program_name, args.ast_path)
            return
        if args.ast:
            execute_ast(args.program_name)
            return
        execute(args.program_name)


if __name__ == '__main__':
    main()
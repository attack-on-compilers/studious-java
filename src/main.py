#!/usr/bin/env python3

import ply.yacc as yacc
from lexer import *
import argparse
from dot import tree_gen, tree_reduce
from symbol_tac import generate_symbol_table
from symbol_table import *
from parse import *
from codegen import *


def getArgs():
    compiler = argparse.ArgumentParser()
    compiler.add_argument("-i", "--input", type=str, default=None, help="Input file")
    compiler.add_argument("-o", "--output", type=str, default="javao", help="Output file")
    compiler.add_argument("-a", "--all", action="store_true", help="Show Entire Parse Tree")
    compiler.add_argument("-v", "--verbose", action="store_true", help="Verbose Output")
    return compiler


if __name__ == "__main__":
    # lex.lex(debug=True)
    # yacc.yacc(debug=True)
    global args
    args = getArgs().parse_args()
    if args.verbose:
        print("Input file: {}".format(args.input))
        print("Output dot file: {}".format(args.output))
    if args.input == None:
        print("No input file specified")
        print("Use -h or --help for help")
    else:
        with open(str(args.input), "r+") as file:
            data = file.read()
            tree = yacc.parse(data)
            if args.output[-4:] == ".dot":
                args.output = args.output[:-4]
            if args.all:
                if args.verbose:
                    print("Generating Complete Parse Tree")
                tree_gen(tree, args.output)
            else:
                if args.verbose:
                    print("Generating AST")
                tree_gen(tree_reduce(tree), args.output)
        if args.verbose:
            print("Dot file generated: {}.dot".format(args.output))
        global_symbol_table, tac = generate_symbol_table(tree, args)
        if args.verbose:
            print("Symbol Table and TAC generated")

        gas = GAS()

        gas.tac_to_x86_mapping(tac)

        gas.tprint()

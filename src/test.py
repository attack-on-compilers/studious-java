import sys
import os
import lex
import ply.yacc as yacc
import argparse

from dot import generate_graph_from_ast, reduce_ast

tokens = lex.tokens
flag_for_error = 0

start = "compilation_unit"

def p_literal(p):
    """Literal : IntegerLiteral
               | FloatingPointLiteral
               | BooleanLiteral
               | CharacterLiteral
               | StringLiteral
               | NullLiteral"""
    p[0] = ("Literal",) + tuple(p[-len(p) + 1 :])

def p_Type(p):
    """Type : PrimitiveType
            | ReferenceType"""
    p[0] = ("Type",) + tuple(p[-len(p) + 1 :])

def p_PrimitiveType(p):
    """PrimitiveType : AlphaAnnotation NumericType
                     | AlphaAnnotation BOOLEAN"""
    p[0] = ("PrimitiveType",) + tuple(p[-len(p) + 1 :])

def p_AlphaAnnotation(p):
    """AlphaAnnotation : Annotation AlphaAnnotation
                       |"""
    p[0] = ("AlphaAnnotation",) + tuple(p[-len(p) + 1 :])

def p_NumericType(p):
    """NumericType : IntegralType
                   | FloatingPointType"""
    p[0] = ("NumericType",) + tuple(p[-len(p) + 1 :])

def p_IntegralType(p):
    """IntegralType : BYTE
                    | SHORT
                    | INT
                    | LONG
                    | CHAR"""
    p[0] = ("IntegralType",) + tuple(p[-len(p) + 1 :])

def p_FloatingPointType(p):
    """FloatingPointType : FLOAT
                         | DOUBLE"""
    p[0] = ("FloatingPointType",) + tuple(p[-len(p) + 1 :])

def p_ReferenceType(p):
    """ReferenceType : ClassOrInterfaceType
                     | TypeVariable
                     | ArrayType"""
    p[0] = ("ReferenceType",) + tuple(p[-len(p) + 1 :])

def p_ClassOrInterfaceType(p):
    """ClassOrInterfaceType : ClassType
                            | InterfaceType"""
    p[0] = ("ClassOrInterfaceType",) + tuple(p[-len(p) + 1 :])

def p_ClassType(p):
    """ClassType : ClassType DOT Identifier
                 | AlphaAnnotation Identifier"""
    p[0] = ("ClassType",) + tuple(p[-len(p) + 1 :])



def p_error(p):
    global flag_for_error
    flag_for_error = 1

    if p is not None:
        print("error at line no:  %s :: %s" % ((p.lineno), (p.value)))
        parser.errok()
    else:
        print("Unexpected end of input")


parser = yacc.yacc()


def getArgs():
    parser = argparse.ArgumentParser()
    parser.add_argument("input", type=str, default=None, help="Input file")
    parser.add_argument(
        "-o", "--output", type=str, default="AST", help="Output file"
    )
    parser.add_argument(
        "-t", "--trim", action="store_true", help="Trimmed ast"
    )
    return parser


if __name__ == "__main__":
    args = getArgs().parse_args()
    if args.input == None:
        print("No input file specified")
    else:
        with open(str(args.input), "r+") as file:
            data = file.read()
            tree = yacc.parse(data)
            if args.output[-4:] == ".dot":
                args.output = args.output[:-4]
            if args.trim:
                generate_graph_from_ast(reduce_ast(tree), args.output)
            else:
                generate_graph_from_ast(tree, args.output)

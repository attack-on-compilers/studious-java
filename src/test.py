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
    """ReferenceType : ClassType
                     | TypeVariable
                     | ArrayType"""
    p[0] = ("ReferenceType",) + tuple(p[-len(p) + 1 :])

def p_ClassType(p):
    """ClassType : AlphaAnnotation Identifier BetaTypeArguments
                 | ClassType DOT AlphaAnnotation Identifier BetaTypeArguments"""
    p[0] = ("ClassType",) + tuple(p[-len(p) + 1 :])

def p_BetaTypeArguments(p):
    """BetaTypeArguments : TypeArguments
                         |"""
    p[0] = ("BetaTypeArguments",) + tuple(p[-len(p) + 1 :])

def typeVariable(p):
    """TypeVariable : AlphaAnnotation Identifier"""
    p[0] = ("TypeVariable",) + tuple(p[-len(p) + 1 :])

def p_ArrayType(p):
    """ArrayType : PrimitiveType Dims
                 | ClassOrInterfaceType Dims
                 | TypeVariable Dims"""
    p[0] = ("ArrayType",) + tuple(p[-len(p) + 1 :])

def p_Dims(p):
    """Dims : AlphaAnnotation LBRACK RBRACK
            | AlphaAnnotation LBRACK RBRACK Dims"""
    p[0] = ("Dims",) + tuple(p[-len(p) + 1 :])

def p_TypeParameter(p):
    """ TypeParameter : AlphaTypeParameterModifier IDENTIFIER BetaTypeBound"""

def p_AlphaTypeParameterModifier(p):
    """AlphaTypeParameterModifier : TypeParameterModifier AlphaTypeParameterModifier
                                  |"""
    p[0] = ("AlphaTypeParameterModifier",) + tuple(p[-len(p) + 1 :])

def p_TypeParameterModifier(p):
    """TypeParameterModifier : Annotation"""
    p[0] = ("TypeParameterModifier",) + tuple(p[-len(p) + 1 :])

def p_BetaTypeBound(p):
    """BetaTypeBound : TypeBound
                     |"""
    p[0] = ("BetaTypeBound",) + tuple(p[-len(p) + 1 :])

def p_TypeBound(p):
    """TypeBound : EXTENDS TypeVariable
                 | EXTENDS ClassOrInterfaceType AlphaAdditionalBound"""
    p[0] = ("TypeBound",) + tuple(p[-len(p) + 1 :])

def p_AlphaAdditionalBound(p):
    """AlphaAdditionalBound : AdditionalBound AlphaAdditionalBound
                            |"""
    p[0] = ("AlphaAdditionalBound",) + tuple(p[-len(p) + 1 :])

def p_AdditionalBound(p):
    """AdditionalBound : AMPERSAND ClassType"""
    p[0] = ("AdditionalBound",) + tuple(p[-len(p) + 1 :])

def p_TypeArguments(p):
    """TypeArguments : LANGLE TypeArgumentList RANGLE"""
    p[0] = ("TypeArguments",) + tuple(p[-len(p) + 1 :])

def p_TypeArgumentList(p):
    """TypeArgumentList : TypeArgument AlphaCommaTypeArgument"""
    p[0] = ("TypeArgumentList",) + tuple(p[-len(p) + 1 :])

def p_AlphaCommaTypeArgument(p):
    """AlphaCommaTypeArgument : COMMA TypeArgument AlphaCommaTypeArgument
                              |"""
    p[0] = ("AlphaCommaTypeArgument",) + tuple(p[-len(p) + 1 :])

def p_TypeArgument(p):
    """TypeArgument : ReferenceType
                    | Wildcard"""
    p[0] = ("TypeArgument",) + tuple(p[-len(p) + 1 :])





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

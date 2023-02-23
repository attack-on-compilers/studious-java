import ply.yacc as yacc
import os
from lex import *
# import for unicode
import sys

# precedence = (
#     ('right', 'ASSIGNMENT'),
#     ('left', 'OR'),
#     ('left', 'AND'),
#     ('left', 'NOTEQUAL', 'EQUAL'),
#     ('left', 'GREATER', 'LESS', 'GREATEREQUAL', 'LESSEQUAL'),
#     ('left', 'ADDITION', 'SUBSTRACTION', 'CONCAT'),
#     ('left', 'MULTIPLICATION', 'DIVISION', 'MODULO'),
#     ('right','NEW', 'NOT','UMINUS'),
#     ('left', 'DOT')
# )

############
# program := package_decl imports_decl class_decl
############

def p_program(p):
    '''program : package_decl imports_decl'''
    p[0] = p[1] + p[2]

def p_package_decl(p):
    '''package_decl : PACKAGE IDENTIFIER iden_dot SEMICOLON
                    | empty'''
    if p[1] == 'package':
        p[0] = 'package ' + p[2] + ';\r'
    else:
        p[0] = ''

def p_iden_dot(p):
    '''iden_dot : DOT IDENTIFIER iden_dot
                | empty'''
    if p[1] == '.':
        p[0] = '.' + p[2] + p[3]
    else:
        p[0] = ''
    
def p_imports_decl(p):
    '''imports_decl : IMPORT import_static IDENTIFIER iden_dot import_star SEMICOLON imports_decl
                    | empty'''
    if p[1] == 'import':
        p[0] = 'import ' + str(p[2]) + p[3] + str(p[4]) + str(p[5]) + ';\r' + str(p[7])
    else: 
        p[0] = ''

def p_import_static(p):
    '''import_static : STATIC
                     | empty'''
    if p[1] == 'static':
        p[0] = 'static '
    else:
        p[0] = ''

def p_import_star(p):
    '''import_star : DOTSTAR
                   | empty'''
    if p[1] == '.*':
        p[0] = '.*'
    else:
        p[0] = ''

def p_empty(p):
    'empty : '

yacc.yacc()

if __name__ == "__main__":
    if len(sys.argv) > 1:
        filename = sys.argv[1]
        f = open(filename, 'r')
        data = f.read()
        f.close()
        result = yacc.parse(data)
        print(result)
    else:
        print("No input file given")
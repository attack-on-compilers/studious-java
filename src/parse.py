import ply.yacc as yacc
from lex import *
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
# program := package_decl imports_decl class_interface_decls
############


def p_program(p):
    """program : OrdinaryCompilationUnit"""
    p[0] = p[1]


def p_OrdinaryCompilationUnit(p):
    """OrdinaryCompilationUnit : BetaPackageDeclaration AlphaImportDeclaration AlphaTopLevelClassOrInterfaceDeclaration"""
    p[0] = p[1] + p[2] + p[3]


def p_BetaPackageDeclaration(p):
    """BetaPackageDeclaration : PACKAGE IDENTIFIER AlphaDotIdentifier SEMICOLON
    | empty"""
    if p[1] == "package":
        p[0] = "package " + p[2] + p[3] + ";\r"
    else:
        p[0] = ""


def p_AlphaDotIdentifier(p):
    """AlphaDotIdentifier : AlphaDotIdentifier DOT IDENTIFIER
    | empty"""
    if p[1]:
        p[0] = p[1] + p[2] + p[3]
    else:
        p[0] = ""


def p_AlphaImportDeclaration(p):
    """AlphaImportDeclaration : IMPORT BetaImportStatic IDENTIFIER AlphaDotIdentifier BetaImportStar SEMICOLON AlphaImportDeclaration
    | empty"""
    if p[1] == "import":
        p[0] = "import " + p[2] + p[3] + p[4] + p[5] + ";\r" + p[7]
    else:
        p[0] = ""


def p_BetaImportStatic(p):
    """BetaImportStatic : STATIC
    | empty"""
    if p[1] == "static":
        p[0] = "static "
    else:
        p[0] = ""


def p_BetaImportStar(p):
    """BetaImportStar : DOTSTAR
    | empty"""
    if p[1] == ".*":
        p[0] = ".*"
    else:
        p[0] = ""


######
# Class and Interface Declarations
######


def p_AlphaTopLevelClassOrInterfaceDeclaration(p):
    """AlphaTopLevelClassOrInterfaceDeclaration : TopLevelClassOrInterfaceDeclaration AlphaTopLevelClassOrInterfaceDeclaration
    | empty"""
    if p[1]:
        p[0] = p[1] + p[2]
    else:
        p[0] = ""


def p_TopLevelClassOrInterfaceDeclaration(p):
    """TopLevelClassOrInterfaceDeclaration : ClassDeclaration"""
    p[0] = p[1]
    #  """TopLevelClassOrInterfaceDeclaration : ClassDeclaration
    #     | InterfaceDeclaration
    #     | SEMICOLON"""


def p_ClassDeclaration(p):
    """ClassDeclaration : NormalClassDeclaration"""
    # ClassDeclaration        :   NormalClassDeclaration
    #                     |   EnumDeclaration
    #                     |   RecordDeclaration
    #                     ;
    p[0] = p[1]


def p_NormalClassDeclaration(p):
    """NormalClassDeclaration : AlphaClassModifier CLASS IDENTIFIER BetaTypeParameters BetaClassExtends BetaClassImplements BetaClassPermits"""  #    ClassBody"""
    p[0] = p[1] + "class " + p[3] + p[4]  # + p[5] + p[6] + p[7] + p[8]


def p_AlphaClassModifier(p):
    """AlphaClassModifier : ClassModifier AlphaClassModifier
    | empty"""
    if p[1]:
        p[0] = p[1] + p[2]
    else:
        p[0] = ""


def p_ClassModifier(p):
    """ClassModifier : PUBLIC
    | PROTECTED
    | PRIVATE
    | ABSTRACT
    | STATIC
    | FINAL
    | SEALED
    | NON_SEALED
    | STRICTFP"""
    p[0] = p[1] + " "


def p_BetaTypeParameters(p):
    """BetaTypeParameters : LESS TypeParameterList GREATER
    | empty"""
    if p[1] == "<":
        p[0] = "<" + p[2] + ">"
    else:
        p[0] = ""


def p_TypeParameterList(p):
    """TypeParameterList : TypeParameter AlphaCommaTypeParameter"""
    p[0] = p[1] + p[2]


def p_AlphaCommaTypeParameter(p):
    """AlphaCommaTypeParameter : COMMA TypeParameter AlphaCommaTypeParameter
    | empty"""
    if p[1] == ",":
        p[0] = ", " + p[2] + p[3]
    else:
        p[0] = ""


def p_TypeParameter(p):
    """TypeParameter : IDENTIFIER BetaTypeBound"""
    p[0] = p[1] + p[2]


def p_BetaTypeBound(p):
    """BetaTypeBound : EXTENDS TypeBound_1
    | empty"""
    if p[1] == "extends":
        p[0] = " extends " + p[2]
    else:
        p[0] = ""


def p_TypeBound_1(p):
    """TypeBound_1 : IDENTIFIER
    | ClassType AlphaAdditionalBound"""
    if p[1] == "IDENTIFIER":
        p[0] = p[1] + p[2]
    else:
        p[0] = p[1]


def p_AlphaAdditionalBound(p):
    """AlphaAdditionalBound : AMPERSAND ClassType AlphaAdditionalBound
    | empty"""
    if p[1] == "&":
        p[0] = " & " + p[2] + p[3]
    else:
        p[0] = ""


# def p_ClassOrInterfaceType(p):
#     """ClassOrInterfaceType : ClassType
#     | InterfaceType"""
#     p[0] = p[1]


# def p_InterfaceType(p):
#     """InterfaceType : ClassType"""
#     p[0] = p[1]


def p_ClassType(p):
    """ClassType : IDENTIFIER BetaTypeArguments
    | IDENTIFIER AlphaDotIdentifier BetaTypeArguments
    | ClassType DOT IDENTIFIER BetaTypeArguments"""
    if p[2] == ".":
        p[0] = p[1] + "." + p[3] + p[4]
    else:
        p[0] = p[1] + p[2]


def p_BetaTypeArguments(p):
    """BetaTypeArguments : TypeArguments BetaTypeArguments
    | empty"""
    if p[1]:
        p[0] = p[1] + p[2]
    else:
        p[0] = ""


def p_TypeArguments(p):
    """TypeArguments : LESS TypeArgumentList GREATER"""
    p[0] = "<" + p[2] + ">"


def p_TypeArgumentList(p):
    """TypeArgumentList : TypeArgument AlphaCommaTypeArgument"""
    p[0] = p[1] + p[2]


def p_AlphaCommaTypeArgument(p):
    """AlphaCommaTypeArgument : COMMA TypeArgument AlphaCommaTypeArgument
    | empty"""
    if p[1] == ",":
        p[0] = "," + p[2] + p[3]
    else:
        p[0] = ""


def p_TypeArgument(p):
    """TypeArgument : ReferenceType
    | Wildcard"""
    p[0] = p[1]


def p_ReferenceType(p):
    """ReferenceType : ClassType
    | TypeVariable
    | ArrayType"""
    p[0] = p[1]


def p_TypeVariable(p):
    """TypeVariable : IDENTIFIER"""
    p[0] = p[1]


def p_ArrayType(p):
    """ArrayType : PrimitiveType Dims
    | ClassType Dims
    | TypeVariable Dims"""
    p[0] = p[1] + p[2]


def p_PrimitiveType(p):
    """PrimitiveType : BOOLEAN
    | BYTE
    | SHORT
    | INT
    | LONG
    | CHAR
    | FLOAT
    | DOUBLE"""
    p[0] = p[1]


def p_Dims(p):
    """Dims : LEFT_BRACKET RIGHT_BRACKET Dims
    | LEFT_BRACKET RIGHT_BRACKET"""
    if p[3]:
        p[0] = "[]" + p[3]
    else:
        p[0] = "[]"


def p_Wildcard(p):
    """Wildcard : QUESTION BetaWildcardBounds"""
    p[0] = "?" + p[2]


def p_BetaWildcardBounds(p):
    """BetaWildcardBounds : EXTENDS ReferenceType
    | SUPER ReferenceType
    | empty"""
    if p[1] == "extends":
        p[0] = " extends " + p[2]
    elif p[1] == "super":
        p[0] = " super " + p[2]
    else:
        p[0] = ""


def p_BetaClassExtends(p):
    """BetaClassExtends : EXTENDS ClassType
    | empty"""
    if p[1] == "extends":
        p[0] = " extends " + p[2]
    else:
        p[0] = ""

def p_BetaClassImplements(p):
    """BetaClassImplements : IMPLEMENTS ClassTypeList
    | empty"""
    if p[1] == "implements":
        p[0] = " implements " + p[2]
    else:
        p[0] = ""

def p_ClassTypeList(p):
    """ClassTypeList : ClassType AlphaCommaClassType"""
    p[0] = p[1] + p[2]

def p_AlphaCommaClassType(p):
    """AlphaCommaClassType : COMMA ClassType AlphaCommaClassType
    | empty"""
    if p[1] == ",":
        p[0] = ", " + p[2] + p[3]
    else:
        p[0] = ""

def p_BetaClassPermits(p):
    """BetaClassPermits : PERMITS TypeName AlphaCommaTypeName
    | empty"""
    if p[1] == "permits":
        p[0] = " permits " + p[2]
    else:
        p[0] = ""

def p_AlphaCommaTypeName(p):
    """AlphaCommaTypeName : COMMA TypeName AlphaCommaTypeName
    | empty"""
    if p[1] == ",":
        p[0] = ", " + p[2] + p[3]
    else:
        p[0] = ""

def p_TypeName(p):
    """TypeName : IDENTIFIER
    | IDENTIFIER AlphaDotIdentifier"""
    if p[1]=="IDENTIFIER":
        p[0] = p[1] + "." + p[2]
    else:
        p[0] = p[1]

def p_empty(p):
    "empty :"
    p[0] = None


yacc.yacc(debug=True, debugfile="parser.out")

if __name__ == "__main__":
    if len(sys.argv) > 1:
        filename = sys.argv[1]
        f = open(filename, "r")
        data = f.read()
        f.close()
        result = yacc.parse(data)
        print(result)
    else:
        print("No input file given")

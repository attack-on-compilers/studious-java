import ply.yacc as yacc
from lex import *
import argparse
from dot import generate_graph_from_ast, reduce_ast


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

start = "program"


def p_program(p):
    """program : OrdinaryCompilationUnit"""
    p[0] = ("program",) + tuple(p[-len(p) + 1 :])


def p_OrdinaryCompilationUnit(p):
    """OrdinaryCompilationUnit : BetaPackageDeclaration AlphaImportDeclaration AlphaTopLevelClassOrInterfaceDeclaration"""
    p[0] = ("OrdinaryCompilationUnit",) + tuple(p[-len(p) + 1 :])


def p_BetaPackageDeclaration(p):
    """BetaPackageDeclaration : PACKAGE IDENTIFIER AlphaDotIdentifier SEMICOLON
    | empty"""
    p[0] = ("BetaPackageDeclaration",) + tuple(p[-len(p) + 1 :])


def p_AlphaDotIdentifier(p):
    """AlphaDotIdentifier : AlphaDotIdentifier DOT IDENTIFIER
    | empty"""
    p[0] = ("AlphaDotIdentifier",) + tuple(p[-len(p) + 1 :])


def p_AlphaImportDeclaration(p):
    """AlphaImportDeclaration : IMPORT BetaImportStatic IDENTIFIER AlphaDotIdentifier BetaImportStar SEMICOLON AlphaImportDeclaration
    | empty"""
    p[0] = ("AlphaImportDeclaration",) + tuple(p[-len(p) + 1 :])


def p_BetaImportStatic(p):
    """BetaImportStatic : STATIC
    | empty"""
    p[0] = ("BetaImportStatic",) + tuple(p[-len(p) + 1 :])


def p_BetaImportStar(p):
    """BetaImportStar : DOTSTAR
    | empty"""
    p[0] = ("BetaImportStar",) + tuple(p[-len(p) + 1 :])


######
# Class and Interface Declarations
######


def p_AlphaTopLevelClassOrInterfaceDeclaration(p):
    """AlphaTopLevelClassOrInterfaceDeclaration : TopLevelClassOrInterfaceDeclaration AlphaTopLevelClassOrInterfaceDeclaration
    | empty"""
    p[0] = ("AlphaTopLevelClassOrInterfaceDeclaration",) + tuple(p[-len(p) + 1 :])


def p_TopLevelClassOrInterfaceDeclaration(p):
    """TopLevelClassOrInterfaceDeclaration : ClassDeclaration
    | InterfaceDeclaration
    | SEMICOLON"""
    p[0] = ("TopLevelClassOrInterfaceDeclaration",) + tuple(p[-len(p) + 1 :])


def p_ClassDeclaration(p):
    """ClassDeclaration : NormalClassDeclaration"""
    # ClassDeclaration        :   NormalClassDeclaration
    #                     |   EnumDeclaration
    #                     |   RecordDeclaration
    #                     ;
    p[0] = ("ClassDeclaration",) + tuple(p[-len(p) + 1 :])


def p_NormalClassDeclaration(p):
    """NormalClassDeclaration : AlphaClassModifier CLASS IDENTIFIER BetaTypeParameters BetaClassExtends BetaClassImplements BetaClassPermits ClassBody"""  #    ClassBody"""
    p[0] = ("NormalClassDeclaration",) + tuple(p[-len(p) + 1 :])


def p_AlphaClassModifier(p):
    """AlphaClassModifier : ClassModifier AlphaClassModifier
    | empty"""
    p[0] = ("AlphaClassModifier",) + tuple(p[-len(p) + 1 :])


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
    p[0] = ("ClassModifier",) + tuple(p[-len(p) + 1 :])


def p_BetaTypeParameters(p):
    """BetaTypeParameters : LESS TypeParameterList GREATER
    | empty"""
    p[0] = ("BetaTypeParameters",) + tuple(p[-len(p) + 1 :])


def p_TypeParameterList(p):
    """TypeParameterList : TypeParameter AlphaCommaTypeParameter"""
    p[0] = ("TypeParameterList",) + tuple(p[-len(p) + 1 :])


def p_AlphaCommaTypeParameter(p):
    """AlphaCommaTypeParameter : COMMA TypeParameter AlphaCommaTypeParameter
    | empty"""
    p[0] = ("AlphaCommaTypeParameter",) + tuple(p[-len(p) + 1 :])


def p_TypeParameter(p):
    """TypeParameter : IDENTIFIER BetaTypeBound"""
    p[0] = ("TypeParameter",) + tuple(p[-len(p) + 1 :])


def p_BetaTypeBound(p):
    """BetaTypeBound : EXTENDS TypeBound1
    | empty"""
    p[0] = ("BetaTypeBound",) + tuple(p[-len(p) + 1 :])


def p_TypeBound1(p):
    """TypeBound1 : IDENTIFIER
    | ClassType AlphaAdditionalBound"""
    p[0] = ("TypeBound1",) + tuple(p[-len(p) + 1 :])


def p_AlphaAdditionalBound(p):
    """AlphaAdditionalBound : AMPERSAND ClassType AlphaAdditionalBound
    | empty"""
    p[0] = ("AlphaAdditionalBound",) + tuple(p[-len(p) + 1 :])


def p_ClassType(p):
    """ClassType : IDENTIFIER AlphaDotIdentifier BetaTypeArguments
    | ClassType DOT IDENTIFIER BetaTypeArguments"""
    p[0] = ("ClassType",) + tuple(p[-len(p) + 1 :])


def p_BetaTypeArguments(p):
    """BetaTypeArguments : TypeArguments
    | empty"""
    p[0] = ("BetaTypeArguments",) + tuple(p[-len(p) + 1 :])


def p_TypeArguments(p):
    """TypeArguments : LESS TypeArgumentList GREATER"""
    p[0] = ("TypeArguments",) + tuple(p[-len(p) + 1 :])


def p_TypeArgumentList(p):
    """TypeArgumentList : TypeArgument AlphaCommaTypeArgument"""
    p[0] = ("TypeArgumentList",) + tuple(p[-len(p) + 1 :])


def p_AlphaCommaTypeArgument(p):
    """AlphaCommaTypeArgument : COMMA TypeArgument AlphaCommaTypeArgument
    | empty"""
    p[0] = ("AlphaCommaTypeArgument",) + tuple(p[-len(p) + 1 :])


def p_TypeArgument(p):
    """TypeArgument : ReferenceType
    | Wildcard"""
    p[0] = ("TypeArgument",) + tuple(p[-len(p) + 1 :])


def p_Type(p):
    """Type : ReferenceType
    | PrimitiveType"""
    p[0] = ("Type",) + tuple(p[-len(p) + 1 :])


def p_ReferenceType(p):
    """ReferenceType : ClassType
    | TypeVariable
    | ArrayType"""
    p[0] = ("ReferenceType",) + tuple(p[-len(p) + 1 :])


def p_TypeVariable(p):
    """TypeVariable : IDENTIFIER"""
    p[0] = ("TypeVariable",) + tuple(p[-len(p) + 1 :])


def p_ArrayType(p):
    """ArrayType : PrimitiveType Dims
    | ClassType Dims
    | TypeVariable Dims"""
    p[0] = ("ArrayType",) + tuple(p[-len(p) + 1 :])


def p_PrimitiveType(p):
    """PrimitiveType : BOOLEAN
    | BYTE
    | SHORT
    | INT
    | LONG
    | CHAR
    | FLOAT
    | DOUBLE"""
    p[0] = ("PrimitiveType",) + tuple(p[-len(p) + 1 :])


def p_Dims(p):
    """Dims : LEFT_BRACKET RIGHT_BRACKET Dims
    | LEFT_BRACKET RIGHT_BRACKET"""
    p[0] = ("Dims",) + tuple(p[-len(p) + 1 :])


def p_Wildcard(p):
    """Wildcard : QUESTION BetaWildcardBounds"""
    p[0] = ("Wildcard",) + tuple(p[-len(p) + 1 :])


def p_BetaWildcardBounds(p):
    """BetaWildcardBounds : EXTENDS ReferenceType
    | SUPER ReferenceType
    | empty"""
    p[0] = ("BetaWildcardBounds",) + tuple(p[-len(p) + 1 :])


def p_BetaClassExtends(p):
    """BetaClassExtends : EXTENDS ClassType
    | empty"""
    p[0] = ("BetaClassExtends",) + tuple(p[-len(p) + 1 :])


def p_BetaClassImplements(p):
    """BetaClassImplements : IMPLEMENTS ClassTypeList
    | empty"""
    p[0] = ("BetaClassImplements",) + tuple(p[-len(p) + 1 :])


def p_ClassTypeList(p):
    """ClassTypeList : ClassType AlphaCommaClassType"""
    p[0] = ("ClassTypeList",) + tuple(p[-len(p) + 1 :])


def p_AlphaCommaClassType(p):
    """AlphaCommaClassType : COMMA ClassType AlphaCommaClassType
    | empty"""
    p[0] = ("AlphaCommaClassType",) + tuple(p[-len(p) + 1 :])


def p_BetaClassPermits(p):
    """BetaClassPermits : PERMITS IDENTIFIER AlphaDotIdentifier AlphaCommaTypeName
    | empty"""
    p[0] = ("BetaClassPermits",) + tuple(p[-len(p) + 1 :])


def p_AlphaCommaTypeName(p):
    """AlphaCommaTypeName : COMMA IDENTIFIER AlphaDotIdentifier AlphaCommaTypeName
    | empty"""
    p[0] = ("AlphaCommaTypeName",) + tuple(p[-len(p) + 1 :])


def p_empty(p):
    "empty :"
    p[0] = None


def p_ClassBody(p):
    """ClassBody : LEFT_BRACE AlphaClassBodyDeclaration RIGHT_BRACE"""
    p[0] = ("ClassBody",) + tuple(p[-len(p) + 1 :])


def p_AlphaClassBodyDeclaration(p):
    """AlphaClassBodyDeclaration : ClassBodyDeclaration AlphaClassBodyDeclaration
    | empty"""
    p[0] = ("AlphaClassBodyDeclaration",) + tuple(p[-len(p) + 1 :])


def p_ClassBodyDeclaration(p):
    """ClassBodyDeclaration : ClassMemberDeclaration
    | InstanceInitializer
    | StaticInitializer
    | ConstructorDeclaration"""
    p[0] = ("ClassBodyDeclaration",) + tuple(p[-len(p) + 1 :])

def p_ConstructorDeclaration(p):
    """ConstructorDeclaration : AlphaFieldModifier ConstructorDeclarator BetaThrows ConstructorBody"""
    p[0] = ("ConstructorDeclaration",) + tuple(p[-len(p) + 1 :])

def p_AlphaConstructorModifier(p):
    """AlphaConstructorModifier : ConstructorModifier AlphaConstructorModifier
    | empty"""
    p[0] = ("AlphaConstructorModifier",) + tuple(p[-len(p) + 1 :])

def p_ConstructorModifier(p):
    """ConstructorModifier : PUBLIC
    | PROTECTED
    | PRIVATE"""
    p[0] = ("ConstructorModifier",) + tuple(p[-len(p) + 1 :])

def p_ConstructorDeclarator(p):
    """ConstructorDeclarator : BetaTypeParameters IDENTIFIER LEFT_PAREN BetaRecieverParameterComma BetaFormalParameterList RIGHT_PAREN"""
    p[0] = ("ConstructorDeclarator",) + tuple(p[-len(p) + 1 :])

def p_BetaRecieverParameterComma(p):
    """BetaRecieverParameterComma : RecieverParameter COMMA
    | empty"""
    p[0] = ("BetaRecieverParameterComma",) + tuple(p[-len(p) + 1 :])

def p_ReceieverParameter(p):
    """RecieverParameter : Type BetaIdentifierDot THIS"""
    p[0] = ("RecieverParameter",) + tuple(p[-len(p) + 1 :])

def p_BetaIdentifierDot(p):
    """BetaIdentifierDot : IDENTIFIER DOT
    | empty"""
    p[0] = ("BetaIdentifierDot",) + tuple(p[-len(p) + 1 :])

def p_ConstructorBody(p):
    """ConstructorBody : LEFT_BRACE BetaExplicitConstructorInvocation BetaBlockStatements RIGHT_BRACE"""
    p[0] = ("ConstructorBody",) + tuple(p[-len(p) + 1 :])

def p_BetaExplicitConstructorInvocation(p):
    """BetaExplicitConstructorInvocation : ExplicitConstructorInvocation BetaBlockStatements
    | empty"""
    p[0] = ("BetaExplicitConstructorInvocation",) + tuple(p[-len(p) + 1 :])

def p_ExplicitConstructorInvocation(p):
    """ExplicitConstructorInvocation : BetaTypeArguments THIS LEFT_PAREN BetaArgumentList RIGHT_PAREN SEMICOLON
    | BetaTypeArguments SUPER LEFT_PAREN BetaArgumentList RIGHT_PAREN SEMICOLON
    | IDENTIFIER AlphaDotIdentifier DOT BetaTypeArguments SUPER LEFT_PAREN BetaArgumentList RIGHT_PAREN SEMICOLON
    | Primary DOT BetaTypeArguments SUPER LEFT_PAREN BetaArgumentList RIGHT_PAREN SEMICOLON"""
    p[0] = ("ExplicitConstructorInvocation",) + tuple(p[-len(p) + 1 :])

def p_BetaArgumentList(p):
    """BetaArgumentList : ArgumentList
    | empty"""
    p[0] = ("BetaArgumentList",) + tuple(p[-len(p) + 1 :])

def p_ArgumentList(p):
    """ArgumentList : TRANSITIVE"""
    p[0] = ("ArgumentList",) + tuple(p[-len(p) + 1 :])

def p_Primary(p):
    """Primary : TRANSITIVE"""
    p[0] = ("Primary",) + tuple(p[-len(p) + 1 :])




def  p_InstanceInitializer(p):
    """InstanceInitializer : Block"""
    p[0] = ("InstanceInitializer",) + tuple(p[-len(p) + 1 :])

def p_StaticInitializer(p):
    """StaticInitializer : STATIC Block"""
    p[0] = ("StaticInitializer",) + tuple(p[-len(p) + 1 :])

def p_ClassMemberDeclaration(p):
    """ClassMemberDeclaration : FieldDeclaration
    | MethodDeclaration
    | SEMICOLON"""
    # | ClassDeclaration        # (Never to be implemneted)
    # | InterfaceDeclaration    # (Never to be implemented)
    p[0] = ("ClassMemberDeclaration",) + tuple(p[-len(p) + 1 :])


def p_FieldDeclaration(p):
    """FieldDeclaration : AlphaFieldModifier Type VariableDeclaratorList SEMICOLON"""
    p[0] = ("FieldDeclaration",) + tuple(p[-len(p) + 1 :])


def p_AlphaFieldModifier(p):
    """AlphaFieldModifier : FieldModifier AlphaFieldModifier
    | empty"""
    p[0] = ("AlphaFieldModifier",) + tuple(p[-len(p) + 1 :])


def p_FieldModifier(p):
    """FieldModifier : PUBLIC
    | PROTECTED
    | PRIVATE
    | STATIC
    | FINAL
    | ABSTRACT
    | TRANSIENT
    | SYNCHRONIZED
    | NATIVE
    | STRICTFP
    | VOLATILE"""
    p[0] = ("FieldModifier",) + tuple(p[-len(p) + 1 :])


def p_VariableDeclaratorList(p):
    """VariableDeclaratorList : VariableDeclarator AlphaCommaVariableDeclarator"""
    p[0] = ("VariableDeclaratorList",) + tuple(p[-len(p) + 1 :])


def p_AlphaCommaVariableDeclarator(p):
    """AlphaCommaVariableDeclarator : COMMA VariableDeclarator AlphaCommaVariableDeclarator
    | empty"""
    p[0] = ("AlphaCommaVariableDeclarator",) + tuple(p[-len(p) + 1 :])


def p_VariableDeclarator(p):
    """VariableDeclarator : VariableDeclaratorId
    | VariableDeclaratorId ASSIGN VariableInitializer"""
    p[0] = ("VariableDeclarator",) + tuple(p[-len(p) + 1 :])


def p_VariableDeclaratorId(p):
    """VariableDeclaratorId : IDENTIFIER
    | IDENTIFIER Dims"""
    p[0] = ("VariableDeclaratorId",) + tuple(p[-len(p) + 1 :])


def p_VariableInitializer(p):
    """VariableInitializer : TRANSITIVE
    | ArrayInitializer"""
    p[0] = ("VariableInitializer",) + tuple(p[-len(p) + 1 :])


def p_ArrayInitializer(p):
    """ArrayInitializer : LEFT_BRACE VariableInitializerList RIGHT_BRACE
    | LEFT_BRACE VariableInitializerList COMMA RIGHT_BRACE"""
    p[0] = ("ArrayInitializer",) + tuple(p[-len(p) + 1 :])


def p_VariableInitializerList(p):
    """VariableInitializerList : VariableInitializer AlphaCommaVariableInitializer"""
    p[0] = ("VariableInitializerList",) + tuple(p[-len(p) + 1 :])


def p_AlphaCommaVariableInitializer(p):
    """AlphaCommaVariableInitializer : COMMA VariableInitializer AlphaCommaVariableInitializer
    | empty"""
    p[0] = ("AlphaCommaVariableInitializer",) + tuple(p[-len(p) + 1 :])


def p_MethodDeclaration(p):
    """MethodDeclaration : AlphaFieldModifier MethodHeader MethodBody"""
    p[0] = ("MethodDeclaration",) + tuple(p[-len(p) + 1 :])


def p_MethodHeader(p):
    """MethodHeader : Result MethodDeclarator BetaThrows
    | TypeParameters Result MethodDeclarator BetaThrows"""
    p[0] = ("MethodHeader",) + tuple(p[-len(p) + 1 :])


def p_BetaTypeParameters(p):
    """BetaTypeParameters : TypeParameters
    | empty"""
    p[0] = ("BetaTypeParameters",) + tuple(p[-len(p) + 1 :])


def p_TypeParameters(p):
    """TypeParameters : LESS TypeParameterList GREATER"""
    p[0] = ("TypeParameters",) + tuple(p[-len(p) + 1 :])


def p_Result(p):
    """Result : Type
    | VOID"""
    p[0] = ("Result",) + tuple(p[-len(p) + 1 :])


def p_MethodDeclarator(p):
    """MethodDeclarator : IDENTIFIER LEFT_PAREN BetaFormalParameterList RIGHT_PAREN"""
    p[0] = ("MethodDeclarator",) + tuple(p[-len(p) + 1 :])


def p_BetaFormalParameterList(p):
    """BetaFormalParameterList : FormalParameterList
    | empty"""
    p[0] = ("BetaFormalParameterList",) + tuple(p[-len(p) + 1 :])


def p_FormalParameterList(p):
    """FormalParameterList : FormalParameter AlphaCommaFormalParameter"""
    p[0] = ("FormalParameterList",) + tuple(p[-len(p) + 1 :])


def p_AlphaCommaFormalParameter(p):
    """AlphaCommaFormalParameter : COMMA FormalParameter AlphaCommaFormalParameter
    | empty"""
    p[0] = ("AlphaCommaFormalParameter",) + tuple(p[-len(p) + 1 :])


def p_FormalParameter(p):
    """FormalParameter : AlphaVariableModifier Type VariableDeclaratorId
    | VariableArityParameter"""
    p[0] = ("FormalParameter",) + tuple(p[-len(p) + 1 :])


def p_AlphaVariableModifier(p):
    """AlphaVariableModifier : VariableModifier AlphaVariableModifier
    | empty"""
    p[0] = ("AlphaVariableModifier",) + tuple(p[-len(p) + 1 :])


def p_VariableModifier(p):
    """VariableModifier : FINAL"""
    p[0] = ("VariableModifier",) + tuple(p[-len(p) + 1 :])


def p_VariableArityParameter(p):
    """VariableArityParameter : AlphaVariableModifier Type ELLIPSIS IDENTIFIER"""
    p[0] = ("VariableArityParameter",) + tuple(p[-len(p) + 1 :])


def p_BetaThrows(p):
    """BetaThrows : THROWS ClassTypeList
    | empty"""
    p[0] = ("BetaThrows",) + tuple(p[-len(p) + 1 :])


def p_MethodBody(p):
    """MethodBody : Block
    | SEMICOLON"""
    p[0] = ("MethodBody",) + tuple(p[-len(p) + 1 :])


def p_Block(p):
    """Block : LEFT_BRACE BetaBlockStatements RIGHT_BRACE"""
    p[0] = ("Block",) + tuple(p[-len(p) + 1 :])


def p_BetaBlockStatements(p):
    """BetaBlockStatements : empty"""
    p[0] = ("BetaBlockStatements",) + tuple(p[-len(p) + 1 :])


def p_error(p):
    print("Syntax error in input at line {} at token {}".format(p.lineno, p.value))


def p_InterfaceDeclaration(p):
    """InterfaceDeclaration : NormalInterfaceDeclaration"""
    p[0] = ("InterfaceDeclaration",) + tuple(p[-len(p) + 1 :])


def p_NormalInterfaceDeclaration(p):
    """NormalInterfaceDeclaration : AlphaClassModifier INTERFACE IDENTIFIER BetaTypeParameters BetaClassExtends BetaClassPermits InterfaceBody"""
    p[0] = ("NormalInterfaceDeclaration",) + tuple(p[-len(p) + 1 :])


def p_InterfaceBody(p):
    """InterfaceBody : LEFT_BRACE AlphaInterfaceMemberDeclaration RIGHT_BRACE"""
    p[0] = ("InterfaceBody",) + tuple(p[-len(p) + 1 :])


def p_AlphaInterfaceMemberDeclaration(p):
    """AlphaInterfaceMemberDeclaration : InterfaceMemberDeclaration AlphaInterfaceMemberDeclaration
    | empty"""
    p[0] = ("AlphaInterfaceMemberDeclaration",) + tuple(p[-len(p) + 1 :])


def p_InterfaceMemberDeclaration(p):
    """InterfaceMemberDeclaration : ConstantDeclaration
    | InterfaceMethodDeclaration
    | SEMICOLON"""
    # | InterfaceDeclaration
    # | ClassDeclaration"""
    p[0] = ("InterfaceMemberDeclaration",) + tuple(p[-len(p) + 1 :])


def p_InterfaceMethodDeclaration(p):
    """InterfaceMethodDeclaration : AlphaConstantModifier MethodHeader MethodBody"""
    p[0] = ("InterfaceMethodDeclaration",) + tuple(p[-len(p) + 1 :])


def p_ConstantDeclaration(p):
    """ConstantDeclaration : AlphaConstantModifier Type VariableDeclaratorList SEMICOLON"""
    p[0] = ("ConstantDeclaration",) + tuple(p[-len(p) + 1 :])


def p_AlphaConstantModifier(p):
    """AlphaConstantModifier : ConstantModifier AlphaConstantModifier
    | empty"""
    p[0] = ("AlphaConstantModifier",) + tuple(p[-len(p) + 1 :])


def p_ConstantModifier(p):
    """ConstantModifier : PUBLIC
    | STATIC
    | FINAL
    | ABSTRACT
    | DEFAULT
    | STRICTFP"""
    p[0] = ("ConstantModifier",) + tuple(p[-len(p) + 1 :])


yacc.yacc(debug=True, debugfile="parser.out")


def getArgs():
    parser = argparse.ArgumentParser()
    parser.add_argument("input", type=str, default=None, help="Input file")
    parser.add_argument("-o", "--output", type=str, default="AST", help="Output file")
    parser.add_argument("-t", "--trim", action="store_true", help="Trimmed ast")
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

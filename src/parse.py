import ply.yacc as yacc
from lex import *
import argparse
from dot import generate_graph_from_ast, reduce_ast


precedence = (
    ("right", "ASSIGN"),
    ("left", "LESS", "GREATER"),
    # ('left', 'AND'),
    # ('left', 'NOTEQUAL', 'EQUAL'),
    # ('left', 'GREATER', 'LESS', 'GREATEREQUAL', 'LESSEQUAL'),
    # ('left', 'ADDITION', 'SUBSTRACTION', 'CONCAT'),
    # ('left', 'MULTIPLICATION', 'DIVISION', 'MODULO'),
    # ('right','NEW', 'NOT','UMINUS'),
    ("left", "DOT"),
)

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
    | TRANSIENT
    | SYNCHRONIZED
    | NATIVE
    | VOLATILE
    | STRICTFP"""
    p[0] = ("ClassModifier",) + tuple(p[-len(p) + 1 :])


def p_BetaTypeParameters(p):
    """BetaTypeParameters : TypeParameters
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
    """BetaTypeBound : EXTENDS IDENTIFIER
    | EXTENDS ClassType AlphaAdditionalBound
    | empty"""
    p[0] = ("BetaTypeBound",) + tuple(p[-len(p) + 1 :])


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
    | IDENTIFIER
    | ArrayType"""
    p[0] = ("ReferenceType",) + tuple(p[-len(p) + 1 :])


def p_ArrayType(p):
    """ArrayType : PrimitiveType Dims
    | ClassType Dims
    | IDENTIFIER Dims"""
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
    """ConstructorDeclaration : AlphaClassModifier ConstructorDeclarator BetaThrows ConstructorBody"""
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


def p_InstanceInitializer(p):
    """InstanceInitializer : Block"""
    p[0] = ("InstanceInitializer",) + tuple(p[-len(p) + 1 :])


def p_StaticInitializer(p):
    """StaticInitializer : STATIC Block"""
    p[0] = ("StaticInitializer",) + tuple(p[-len(p) + 1 :])


def p_ClassMemberDeclaration(p):
    """ClassMemberDeclaration : FieldDeclaration
    | MethodDeclaration
    | SEMICOLON"""
    p[0] = ("ClassMemberDeclaration",) + tuple(p[-len(p) + 1 :])


def p_FieldDeclaration(p):
    """FieldDeclaration : AlphaClassModifier Result VariableDeclaratorList SEMICOLON"""
    p[0] = ("FieldDeclaration",) + tuple(p[-len(p) + 1 :])


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
    """VariableInitializer : Expression
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
    """MethodDeclaration : AlphaClassModifier MethodHeader MethodBody"""
    p[0] = ("MethodDeclaration",) + tuple(p[-len(p) + 1 :])


def p_MethodHeader(p):
    """MethodHeader : Result MethodDeclarator BetaThrows
    | TypeParameters Result MethodDeclarator BetaThrows"""
    p[0] = ("MethodHeader",) + tuple(p[-len(p) + 1 :])


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
    """FormalParameter : AlphaClassModifier Type VariableDeclaratorId
    | VariableArityParameter"""
    p[0] = ("FormalParameter",) + tuple(p[-len(p) + 1 :])


def p_VariableArityParameter(p):
    """VariableArityParameter : AlphaClassModifier Type ELLIPSIS IDENTIFIER"""
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
    """BetaBlockStatements : empty
    | BlockStatements"""
    p[0] = ("BetaBlockStatements",) + tuple(p[-len(p) + 1 :])


def p_BlockStatements(p):
    """BlockStatements : BlockStatement AlphaBlockStatement"""
    p[0] = ("BlockStatements",) + tuple(p[-len(p) + 1 :])


def p_AlphaBlockStatement(p):
    """AlphaBlockStatement : BlockStatement AlphaBlockStatement
    | empty"""
    p[0] = ("AlphaBlockStatement",) + tuple(p[-len(p) + 1 :])


# def p_BlockStatement(p):
#     """BlockStatement : LocalClassOrInterfaceDeclaration
#     | LocalVariableDeclarationStatement
#     | Statement"""
#     p[0] = p[1]


def p_LocalClassOrInterfaceDeclaration(p):
    """LocalClassOrInterfaceDeclaration : ClassDeclaration
    | NormalInterfaceDeclaration"""
    p[0] = ("LocalClassOrInterfaceDeclaration",) + tuple(p[-len(p) + 1 :])


def p_LocalVariableDeclarationStatement(p):
    """LocalVariableDeclarationStatement : LocalVariableDeclaration SEMICOLON"""
    p[0] = ("LocalVariableDeclarationStatement",) + tuple(p[-len(p) + 1 :])


def p_LocalVariableDeclaration(p):
    """LocalVariableDeclaration : AlphaClassModifier LocalVariableType VariableDeclaratorList"""
    p[0] = ("LocalVariableDeclaration",) + tuple(p[-len(p) + 1 :])


def p_LocalVariableType(p):
    """LocalVariableType : Type
    | VAR"""
    p[0] = ("LocalVariableType",) + tuple(p[-len(p) + 1 :])


def p_Statement(p):
    """Statement : StatementWithoutTrailingSubstatement
    | LabeledStatement
    | IfThenStatement
    | IfThenElseStatement
    | WhileStatement
    | ForStatement"""
    p[0] = ("Statement",) + tuple(p[-len(p) + 1 :])


def p_StatementNoShortIf(p):
    """StatementNoShortIf : StatementWithoutTrailingSubstatement
    | LabeledStatementNoShortIf
    | IfThenElseStatementNoShortIf
    | WhileStatementNoShortIf
    | ForStatementNoShortIf"""
    p[0] = ("StatementNoShortIf",) + tuple(p[-len(p) + 1 :])


def p_StatementWithoutTrailingSubstatement(p):
    """StatementWithoutTrailingSubstatement : Block
    | EmptyStatement
    | ExpressionStatement
    | AssertStatement
    | SwitchStatement
    | DoStatement
    | BreakStatement
    | ContinueStatement
    | ReturnStatement
    | SynchronizedStatement
    | ThrowStatement
    | TryStatement
    | YieldStatement"""
    p[0] = ("StatementWithoutTrailingSubstatement",) + tuple(p[-len(p) + 1 :])


def p_EmptyStatement(p):
    """EmptyStatement : SEMICOLON"""
    p[0] = ("EmptyStatement",) + tuple(p[-len(p) + 1 :])


def p_LabeledStatement(p):
    """LabeledStatement : IDENTIFIER COLON Statement"""
    p[0] = ("LabeledStatement",) + tuple(p[-len(p) + 1 :])


def p_LabeledStatementNoShortIf(p):
    """LabeledStatementNoShortIf : IDENTIFIER COLON StatementNoShortIf"""
    p[0] = ("LabeledStatementNoShortIf",) + tuple(p[-len(p) + 1 :])


def p_ExpressionStatement(p):
    """ExpressionStatement : StatementExpression SEMICOLON"""
    p[0] = ("ExpressionStatement",) + tuple(p[-len(p) + 1 :])


def p_StatementExpression(p):
    """StatementExpression : Assignment
    | PreIncrementExpression
    | PreDecrementExpression
    | PostIncrementExpression
    | PostDecrementExpression
    | MethodInvocation
    | ClassInstanceCreationExpression"""
    p[0] = ("StatementExpression",) + tuple(p[-len(p) + 1 :])


def p_IfThenStatement(p):
    """IfThenStatement : IF LEFT_PAREN Expression RIGHT_PAREN Statement"""
    p[0] = ("IfThenStatement",) + tuple(p[-len(p) + 1 :])


def p_IfThenElseStatement(p):
    """IfThenElseStatement : IF LEFT_PAREN Expression RIGHT_PAREN Statement ELSE Statement"""
    p[0] = ("IfThenElseStatement",) + tuple(p[-len(p) + 1 :])


def p_IfThenElseStatementNoShortIf(p):
    """IfThenElseStatementNoShortIf : IF LEFT_PAREN Expression RIGHT_PAREN StatementNoShortIf ELSE StatementNoShortIf"""
    p[0] = ("IfThenElseStatementNoShortIf",) + tuple(p[-len(p) + 1 :])


def p_AssertStatement(p):
    """AssertStatement : ASSERT Expression SEMICOLON
    | ASSERT Expression COLON Expression SEMICOLON"""
    p[0] = ("AssertStatement",) + tuple(p[-len(p) + 1 :])


def p_SwitchStatement(p):
    """SwitchStatement : SWITCH LEFT_PAREN Expression RIGHT_PAREN SwitchBlock"""
    p[0] = ("SwitchStatement",) + tuple(p[-len(p) + 1 :])


def p_SwitchBlock(p):
    """SwitchBlock : LEFT_BRACE SwitchRule AlphaSwitchRule RIGHT_BRACE
    | LEFT_BRACE AlphaSwitchBlockStatementGroup AlphaSwitchLabelColon RIGHT_BRACE"""
    p[0] = ("SwitchBlock",) + tuple(p[-len(p) + 1 :])


def p_AlphaSwitchRule(p):
    """AlphaSwitchRule : SwitchRule AlphaSwitchRule
    | empty"""
    p[0] = ("AlphaSwitchRule",) + tuple(p[-len(p) + 1 :])


def p_AlphaSwitchBlockStatementGroup(p):
    """AlphaSwitchBlockStatementGroup : SwitchBlockStatementGroup AlphaSwitchBlockStatementGroup
    | empty"""
    p[0] = ("AlphaSwitchBlockStatementGroup",) + tuple(p[-len(p) + 1 :])


def p_AlphaSwitchLabelColon(p):
    """AlphaSwitchLabelColon : SwitchLabel COLON AlphaSwitchLabelColon
    | empty"""
    p[0] = ("AlphaSwitchLabelColon",) + tuple(p[-len(p) + 1 :])


def p_SwitchRule(p):
    """SwitchRule : SwitchLabel ARROW Expression SEMICOLON
    | SwitchLabel ARROW Block
    | SwitchLabel ARROW ThrowStatement"""
    p[0] = ("SwitchRule",) + tuple(p[-len(p) + 1 :])


def p_SwitchBlockStatementGroup(p):
    """SwitchBlockStatementGroup : SwitchLabel COLON AlphaSwitchLabelColon BlockStatements"""
    p[0] = ("SwitchBlockStatementGroup",) + tuple(p[-len(p) + 1 :])


def p_SwitchLabel(p):
    """SwitchLabel : CASE CaseConstant AlphaCommaCaseConstant
    | DEFAULT COLON"""
    p[0] = ("SwitchLabel",) + tuple(p[-len(p) + 1 :])


def p_AlphaCommaCaseConstant(p):
    """AlphaCommaCaseConstant : COMMA CaseConstant AlphaCommaCaseConstant
    | empty"""
    p[0] = ("AlphaCommaCaseConstant",) + tuple(p[-len(p) + 1 :])


def p_CaseConstant(p):
    """CaseConstant : ConditionalExpression"""
    p[0] = ("CaseConstant",) + tuple(p[-len(p) + 1 :])


def p_WhileStatement(p):
    """WhileStatement : WHILE LEFT_PAREN Expression RIGHT_PAREN Statement"""
    p[0] = ("WhileStatement",) + tuple(p[-len(p) + 1 :])


def p_WhileStatementNoShortIf(p):
    """WhileStatementNoShortIf : WHILE LEFT_PAREN Expression RIGHT_PAREN StatementNoShortIf"""
    p[0] = ("WhileStatementNoShortIf",) + tuple(p[-len(p) + 1 :])


def p_DoStatement(p):
    """DoStatement : DO Statement WHILE LEFT_PAREN Expression RIGHT_PAREN SEMICOLON"""
    p[0] = ("DoStatement",) + tuple(p[-len(p) + 1 :])


def p_ForStatement(p):
    """ForStatement : BasicForStatement
    | EnhancedForStatement"""
    p[0] = ("ForStatement",) + tuple(p[-len(p) + 1 :])


def p_ForStatementNoShortIf(p):
    """ForStatementNoShortIf : BasicForStatementNoShortIf
    | EnhancedForStatementNoShortIf"""
    p[0] = ("ForStatementNoShortIf",) + tuple(p[-len(p) + 1 :])


def p_BasicForStatement(p):
    """BasicForStatement : FOR LEFT_PAREN BetaForInit SEMICOLON BetaExpression SEMICOLON BetaForUpdate RIGHT_PAREN Statement"""
    p[0] = ("BasicForStatement",) + tuple(p[-len(p) + 1 :])


def p_BetaForInit(p):
    """BetaForInit : ForInit
    | empty"""
    p[0] = ("BetaForInit",) + tuple(p[-len(p) + 1 :])


def p_BetaExpression(p):
    """BetaExpression : Expression
    | empty"""
    p[0] = ("BetaExpression",) + tuple(p[-len(p) + 1 :])


def p_BetaForUpdate(p):
    """BetaForUpdate : ForUpdate
    | empty"""
    p[0] = ("BetaForUpdate",) + tuple(p[-len(p) + 1 :])


def p_BasicForStatementNoShortIf(p):
    """BasicForStatementNoShortIf : FOR LEFT_PAREN BetaForInit SEMICOLON Expression SEMICOLON ForUpdate RIGHT_PAREN StatementNoShortIf"""
    p[0] = ("BasicForStatementNoShortIf",) + tuple(p[-len(p) + 1 :])


def p_ForInit(p):
    """ForInit : StatementExpressionList
    | LocalVariableDeclaration"""
    p[0] = ("ForInit",) + tuple(p[-len(p) + 1 :])


def p_ForUpdate(p):
    """ForUpdate : StatementExpressionList"""
    p[0] = ("ForUpdate",) + tuple(p[-len(p) + 1 :])


def p_StatementExpressionList(p):
    """StatementExpressionList : StatementExpression AlphaCommaStatementExpression"""
    p[0] = ("StatementExpressionList",) + tuple(p[-len(p) + 1 :])


def p_AlphaCommaStatementExpression(p):
    """AlphaCommaStatementExpression : COMMA StatementExpression AlphaCommaStatementExpression
    | empty"""
    p[0] = ("AlphaCommaStatementExpression",) + tuple(p[-len(p) + 1 :])


def p_EnhancedForStatement(p):
    """EnhancedForStatement : FOR LEFT_PAREN LocalVariableDeclaration COLON Expression RIGHT_PAREN Statement"""
    p[0] = ("EnhancedForStatement",) + tuple(p[-len(p) + 1 :])


def p_EnhancedForStatementNoShortIf(p):
    """EnhancedForStatementNoShortIf : FOR LEFT_PAREN LocalVariableDeclaration COLON Expression RIGHT_PAREN StatementNoShortIf"""
    p[0] = ("EnhancedForStatementNoShortIf",) + tuple(p[-len(p) + 1 :])


def p_BreakStatement(p):
    """BreakStatement : BREAK BetaIdentifier SEMICOLON"""
    p[0] = ("BreakStatement",) + tuple(p[-len(p) + 1 :])


def p_BetaIdentifier(p):
    """BetaIdentifier : IDENTIFIER
    | empty"""
    p[0] = ("BetaIdentifier",) + tuple(p[-len(p) + 1 :])


def p_YieldStatement(p):
    """YieldStatement : YIELD Expression SEMICOLON"""
    p[0] = ("YieldStatement",) + tuple(p[-len(p) + 1 :])


def p_ContinueStatement(p):
    """ContinueStatement : CONTINUE BetaIdentifier SEMICOLON"""
    p[0] = ("ContinueStatement",) + tuple(p[-len(p) + 1 :])


def p_ReturnStatement(p):
    """ReturnStatement : RETURN BetaExpression SEMICOLON"""
    p[0] = ("ReturnStatement",) + tuple(p[-len(p) + 1 :])


def p_ThrowStatement(p):
    """ThrowStatement : THROW Expression SEMICOLON"""
    p[0] = ("ThrowStatement",) + tuple(p[-len(p) + 1 :])


def p_SynchronizedStatement(p):
    """SynchronizedStatement : SYNCHRONIZED LEFT_PAREN Expression RIGHT_PAREN Block"""
    p[0] = ("SynchronizedStatement",) + tuple(p[-len(p) + 1 :])


def p_TryStatement(p):
    """TryStatement : TRY Block Catches
    | TRY Block BetaCatches Finally
    | TryWithResourcesStatement"""
    p[0] = ("TryStatement",) + tuple(p[-len(p) + 1 :])


def p_BetaCatches(p):
    """BetaCatches : Catches
    | empty"""
    p[0] = ("BetaCatches",) + tuple(p[-len(p) + 1 :])


def p_Catches(p):
    """Catches : CatchClause AlphaCatchClause"""
    p[0] = ("Catches",) + tuple(p[-len(p) + 1 :])


def p_AlphaCatchClause(p):
    """AlphaCatchClause : CatchClause AlphaCatchClause
    | empty"""
    p[0] = ("AlphaCatchClause",) + tuple(p[-len(p) + 1 :])


def p_CatchClause(p):
    """CatchClause : CATCH LEFT_PAREN CatchFormalParameter RIGHT_PAREN Block"""
    p[0] = ("CatchClause",) + tuple(p[-len(p) + 1 :])


def p_CatchFormalParameter(p):
    """CatchFormalParameter : AlphaClassModifier CatchType VariableDeclaratorId"""
    p[0] = ("CatchFormalParameter",) + tuple(p[-len(p) + 1 :])


def p_CatchType(p):
    """CatchType : Type AlphaPipeCatchType"""
    p[0] = ("CatchType",) + tuple(p[-len(p) + 1 :])


def p_AlphaPipeCatchType(p):
    """AlphaPipeCatchType : BAR CatchType AlphaPipeCatchType
    | empty"""
    p[0] = ("AlphaPipeCatchType",) + tuple(p[-len(p) + 1 :])


def p_Finally(p):
    """Finally : FINALLY Block"""
    p[0] = ("Finally",) + tuple(p[-len(p) + 1 :])


def p_TryWithResourcesStatement(p):
    """TryWithResourcesStatement : TRY ResourceSpecification Block Catches BetaFinally"""
    p[0] = ("TryWithResourcesStatement",) + tuple(p[-len(p) + 1 :])


def p_BetaFinally(p):
    """BetaFinally : Finally
    | empty"""
    p[0] = ("BetaFinally",) + tuple(p[-len(p) + 1 :])


def p_ResourceSpecification(p):
    """ResourceSpecification : LEFT_PAREN ResourceList BetaSemiColon RIGHT_PAREN"""
    p[0] = ("ResourceSpecification",) + tuple(p[-len(p) + 1 :])


def p_BetaSemiColon(p):
    """BetaSemiColon : SEMICOLON
    | empty"""
    p[0] = ("BetaSemiColon",) + tuple(p[-len(p) + 1 :])


def p_ResourceList(p):
    """ResourceList : Resource AlphaSemiColonResource"""
    p[0] = ("ResourceList",) + tuple(p[-len(p) + 1 :])


def p_AlphaSemiColonResource(p):
    """AlphaSemiColonResource : SEMICOLON Resource AlphaSemiColonResource
    | empty"""
    p[0] = ("AlphaSemiColonResource",) + tuple(p[-len(p) + 1 :])


def p_Resource(p):
    """Resource : LocalVariableDeclaration
    | VariableAccess"""
    p[0] = ("Resource",) + tuple(p[-len(p) + 1 :])


def p_Pattern(p):
    """Pattern : TypePattern"""
    p[0] = ("Pattern",) + tuple(p[-len(p) + 1 :])


def p_TypePattern(p):
    """TypePattern : LocalVariableDeclaration"""
    p[0] = ("TypePattern",) + tuple(p[-len(p) + 1 :])


# Productions from §15 (Blocks, Statements, and Patterns)


def p_VariableAccess(p):
    """VariableAccess : ExpressionName
    | FieldAccess"""
    p[0] = ("VariableAccess",) + tuple(p[-len(p) + 1 :])


# Productions from §15 (Expressions)


def p_Primary(p):
    """Primary : PrimaryNoNewArray
    | ArrayCreationExpression"""
    p[0] = ("Primary",) + tuple(p[-len(p) + 1 :])


def p_PrimaryNoNewArray(p):
    """PrimaryNoNewArray : Literal
    | ClassLiteral
    | THIS
    | IDENTIFIER AlphaDotIdentifier DOT THIS
    | LEFT_PAREN Expression RIGHT_PAREN
    | ClassInstanceCreationExpression
    | FieldAccess
    | ArrayAccess
    | MethodInvocation
    | MethodReference"""
    p[0] = ("PrimaryNoNewArray",) + tuple(p[-len(p) + 1 :])


def p_ClassLiteral(p):
    """ClassLiteral : IDENTIFIER AlphaDotIdentifier AlphaSquareBrackets DOT CLASS
    | Type AlphaSquareBrackets DOT CLASS
    | VOID DOT CLASS"""
    p[0] = ("ClassLiteral",) + tuple(p[-len(p) + 1 :])


def p_AlphaSquareBrackets(p):
    """AlphaSquareBrackets :
    | LEFT_BRACKET RIGHT_BRACKET AlphaSquareBrackets"""
    p[0] = ("AlphaSquareBrackets",) + tuple(p[-len(p) + 1 :])


def p_ClassInstanceCreationExpression(p):
    """ClassInstanceCreationExpression : UnqualifiedClassInstanceCreationExpression
    | ExpressionName DOT UnqualifiedClassInstanceCreationExpression
    | Primary DOT UnqualifiedClassInstanceCreationExpression"""
    p[0] = ("ClassInstanceCreationExpression",) + tuple(p[-len(p) + 1 :])


def p_UnqualifiedClassInstanceCreationExpression(p):
    """UnqualifiedClassInstanceCreationExpression : NEW BetaTypeArguments ClassOrInterfaceTypeToInstantiate LEFT_PAREN BetaArgumentList RIGHT_PAREN BetaClassBody
    | NEW BetaTypeArguments ClassOrInterfaceTypeToInstantiate LEFT_PAREN RIGHT_PAREN BetaClassBody"""
    p[0] = ("UnqualifiedClassInstanceCreationExpression",) + tuple(p[-len(p) + 1 :])


def p_ClassOrInterfaceTypeToInstantiate(p):
    """ClassOrInterfaceTypeToInstantiate : IDENTIFIER AlphaDotIdentifier BetaTypeArgumentsOrDiamond"""
    p[0] = ("ClassOrInterfaceTypeToInstantiate",) + tuple(p[-len(p) + 1 :])


def p_BetaTypeArgumentsOrDiamond(p):
    """BetaTypeArgumentsOrDiamond : TypeArgumentsOrDiamond
    | empty"""
    p[0] = ("BetaTypeArgumentsOrDiamond",) + tuple(p[-len(p) + 1 :])


def p_TypeArgumentsOrDiamond(p):
    """TypeArgumentsOrDiamond : TypeArguments
    | LESS GREATER"""
    p[0] = ("TypeArgumentsOrDiamond",) + tuple(p[-len(p) + 1 :])


def p_FieldAccess(p):
    """FieldAccess : Primary DOT IDENTIFIER
    | SUPER DOT IDENTIFIER
    | IDENTIFIER AlphaDotIdentifier DOT SUPER DOT IDENTIFIER"""
    p[0] = ("FieldAccess",) + tuple(p[-len(p) + 1 :])


def p_ArrayAccess(p):
    """ArrayAccess : ExpressionName LEFT_BRACKET Expression RIGHT_BRACKET
    | PrimaryNoNewArray LEFT_BRACKET Expression RIGHT_BRACKET"""
    p[0] = ("ArrayAccess",) + tuple(p[-len(p) + 1 :])


def p_MethodInvocation(p):
    """MethodInvocation : IDENTIFIER LEFT_PAREN BetaArgumentList RIGHT_PAREN
    | IDENTIFIER AlphaDotIdentifier DOT BetaTypeArguments IDENTIFIER LEFT_PAREN BetaArgumentList RIGHT_PAREN
    | ExpressionName DOT BetaTypeArguments IDENTIFIER LEFT_PAREN BetaArgumentList RIGHT_PAREN
    | Primary DOT BetaTypeArguments IDENTIFIER LEFT_PAREN BetaArgumentList RIGHT_PAREN
    | SUPER DOT BetaTypeArguments IDENTIFIER LEFT_PAREN BetaArgumentList RIGHT_PAREN
    | IDENTIFIER AlphaDotIdentifier DOT SUPER DOT BetaTypeArguments IDENTIFIER LEFT_PAREN BetaArgumentList RIGHT_PAREN"""
    p[0] = ("MethodInvocation",) + tuple(p[-len(p) + 1 :])


def p_ArgumentList(p):
    """ArgumentList : Expression AlphaCommaExpression"""
    p[0] = ("ArgumentList",) + tuple(p[-len(p) + 1 :])


def p_AlphaCommaExpression(p):
    """AlphaCommaExpression :
    | COMMA Expression AlphaCommaExpression"""
    p[0] = ("AlphaCommaExpression",) + tuple(p[-len(p) + 1 :])


def p_MethodReference(p):
    """MethodReference : ExpressionName COLON_COLON BetaTypeArguments IDENTIFIER
    | Primary COLON_COLON BetaTypeArguments IDENTIFIER
    | ReferenceType COLON_COLON BetaTypeArguments IDENTIFIER
    | SUPER COLON_COLON BetaTypeArguments IDENTIFIER
    | IDENTIFIER AlphaDotIdentifier DOT SUPER COLON_COLON BetaTypeArguments IDENTIFIER
    | ClassType COLON_COLON BetaTypeArguments NEW
    | ArrayType COLON_COLON NEW"""
    p[0] = ("MethodReference",) + tuple(p[-len(p) + 1 :])


def p_ArrayCreationExpression(p):
    """ArrayCreationExpression : NEW PrimitiveType DimExprs BetaDims
    | NEW ClassType DimExprs BetaDims
    | NEW PrimitiveType Dims ArrayInitializer
    | NEW ClassOrInterfaceTypeToInstantiate Dims ArrayInitializer"""
    p[0] = ("ArrayCreationExpression",) + tuple(p[-len(p) + 1 :])


def p_BetaDims(p):
    """BetaDims : Dims
    | empty"""
    p[0] = ("BetaDims",) + tuple(p[-len(p) + 1 :])


def p_DimExprs(p):
    """DimExprs : DimExpr AlphaDimExpr"""
    p[0] = ("DimExprs",) + tuple(p[-len(p) + 1 :])


def p_AlphaDimExpr(p):
    """AlphaDimExpr :
    | DimExpr AlphaDimExpr"""
    p[0] = ("AlphaDimExpr",) + tuple(p[-len(p) + 1 :])


def p_DimExpr(p):
    """DimExpr : RIGHT_BRACKET Expression LEFT_BRACKET"""
    p[0] = ("DimExpr",) + tuple(p[-len(p) + 1 :])


def p_Expression(p):
    """Expression : LambdaExpression
    | AssignmentExpression"""
    p[0] = ("Expression",) + tuple(p[-len(p) + 1 :])


def p_LambdaExpression(p):
    """LambdaExpression : LambdaParameters ARROW LambdaBody"""
    p[0] = ("LambdaExpression",) + tuple(p[-len(p) + 1 :])


def p_LambdaParameters(p):
    """LambdaParameters : LEFT_PAREN BetaLambdaParameterList RIGHT_PAREN
    | IDENTIFIER"""
    p[0] = ("LambdaParameters",) + tuple(p[-len(p) + 1 :])


def p_BetaLambdaParameterList(p):
    """BetaLambdaParameterList : LambdaParameterList
    | empty"""
    p[0] = ("BetaLambdaParameterList",) + tuple(p[-len(p) + 1 :])


def p_LambdaParameterList(p):
    """LambdaParameterList : LambdaParameter AlphaCommaLambdaParameter
    | IDENTIFIER AlphaCommaIdentifier"""
    p[0] = ("LambdaParameterList",) + tuple(p[-len(p) + 1 :])


def p_AlphaCommaLambdaParameter(p):
    """AlphaCommaLambdaParameter :
    | COMMA LambdaParameter AlphaCommaLambdaParameter"""
    p[0] = ("AlphaCommaLambdaParameter",) + tuple(p[-len(p) + 1 :])


def p_AlphaCommaIdentifier(p):
    """AlphaCommaIdentifier :
    | COMMA IDENTIFIER AlphaCommaIdentifier"""
    p[0] = ("AlphaCommaIdentifier",) + tuple(p[-len(p) + 1 :])


def p_LambdaParameter(p):
    """LambdaParameter : AlphaClassModifier LambdaParameterType VariableDeclaratorId
    | VariableArityParameter"""
    p[0] = ("LambdaParameter",) + tuple(p[-len(p) + 1 :])


def p_LambdaParameterType(p):
    """LambdaParameterType : Type
    | VAR"""
    p[0] = ("LambdaParameterType",) + tuple(p[-len(p) + 1 :])


def p_LambdaBody(p):
    """LambdaBody : Expression
    | Block"""
    p[0] = ("LambdaBody",) + tuple(p[-len(p) + 1 :])


def p_AssignmentExpression(p):
    """AssignmentExpression : ConditionalExpression
    | Assignment"""
    p[0] = ("AssignmentExpression",) + tuple(p[-len(p) + 1 :])


def p_Assignment(p):
    """Assignment : LeftHandSide AssignmentOperator Expression"""
    p[0] = ("Assignment",) + tuple(p[-len(p) + 1 :])


def p_LeftHandSide(p):
    """LeftHandSide : ExpressionName
    | FieldAccess
    | ArrayAccess"""
    p[0] = ("LeftHandSide",) + tuple(p[-len(p) + 1 :])


def p_AssignmentOperator(p):
    """AssignmentOperator : ASSIGN
    | STAR_ASSIGN
    | SLASH_ASSIGN
    | PERCENT_ASSIGN
    | PLUS_ASSIGN
    | MINUS_ASSIGN
    | LEFT_SHIFT_ASSIGN
    | RIGHT_SHIFT_ASSIGN
    | UNSIGNED_RIGHT_SHIFT_ASSIGN
    | AMPERSAND_ASSIGN
    | CARET_ASSIGN
    | BAR_ASSIGN"""
    p[0] = ("AssignmentOperator",) + tuple(p[-len(p) + 1 :])


def p_ConditionalExpression(p):
    """ConditionalExpression : ConditionalOrExpression
    | ConditionalOrExpression QUESTION Expression COLON ConditionalExpression
    | ConditionalOrExpression QUESTION Expression COLON LambdaExpression"""
    p[0] = ("ConditionalExpression",) + tuple(p[-len(p) + 1 :])


def p_ConditionalOrExpression(p):
    """ConditionalOrExpression : ConditionalAndExpression
    | ConditionalOrExpression BAR_BAR ConditionalAndExpression"""
    p[0] = ("ConditionalOrExpression",) + tuple(p[-len(p) + 1 :])


def p_ConditionalAndExpression(p):
    """ConditionalAndExpression : InclusiveOrExpression
    | ConditionalAndExpression AMPERSAND_AMPERSAND InclusiveOrExpression"""
    p[0] = ("ConditionalAndExpression",) + tuple(p[-len(p) + 1 :])


def p_InclusiveOrExpression(p):
    """InclusiveOrExpression : ExclusiveOrExpression
    | InclusiveOrExpression BAR ExclusiveOrExpression"""
    p[0] = ("InclusiveOrExpression",) + tuple(p[-len(p) + 1 :])


def p_ExclusiveOrExpression(p):
    """ExclusiveOrExpression : AndExpression
    | ExclusiveOrExpression CARET AndExpression"""
    p[0] = ("ExclusiveOrExpression",) + tuple(p[-len(p) + 1 :])


def p_AndExpression(p):
    """AndExpression : EqualityExpression
    | AndExpression AMPERSAND EqualityExpression"""
    p[0] = ("AndExpression",) + tuple(p[-len(p) + 1 :])


def p_EqualityExpression(p):
    """EqualityExpression : RelationalExpression
    | EqualityExpression EQUAL_EQUAL RelationalExpression
    | EqualityExpression EXCLAMATION_EQUAL RelationalExpression"""
    p[0] = ("EqualityExpression",) + tuple(p[-len(p) + 1 :])


def p_RelationalExpression(p):
    """RelationalExpression : ShiftExpression
    | RelationalExpression LESS ShiftExpression
    | RelationalExpression GREATER ShiftExpression
    | RelationalExpression LESS_EQUAL ShiftExpression
    | RelationalExpression GREATER_EQUAL ShiftExpression
    | InstanceofExpression"""
    p[0] = ("RelationalExpression",) + tuple(p[-len(p) + 1 :])


def p_InstanceofExpression(p):
    """InstanceofExpression : RelationalExpression INSTANCEOF ReferenceType
    | RelationalExpression INSTANCEOF Pattern"""
    p[0] = ("InstanceofExpression",) + tuple(p[-len(p) + 1 :])


def p_ShiftExpression(p):
    """ShiftExpression : AdditiveExpression
    | ShiftExpression LEFT_SHIFT AdditiveExpression
    | ShiftExpression RIGHT_SHIFT AdditiveExpression
    | ShiftExpression UNSIGNED_RIGHT_SHIFT AdditiveExpression"""
    p[0] = ("ShiftExpression",) + tuple(p[-len(p) + 1 :])


def p_AdditiveExpression(p):
    """AdditiveExpression : MultiplicativeExpression
    | AdditiveExpression PLUS MultiplicativeExpression
    | AdditiveExpression MINUS MultiplicativeExpression"""
    p[0] = ("AdditiveExpression",) + tuple(p[-len(p) + 1 :])


def p_MultiplicativeExpression(p):
    """MultiplicativeExpression : UnaryExpression
    | MultiplicativeExpression STAR UnaryExpression
    | MultiplicativeExpression SLASH UnaryExpression
    | MultiplicativeExpression PERCENT UnaryExpression"""
    p[0] = ("MultiplicativeExpression",) + tuple(p[-len(p) + 1 :])


def p_UnaryExpression(p):
    """UnaryExpression : PreIncrementExpression
    | PreDecrementExpression
    | PLUS UnaryExpression
    | MINUS UnaryExpression
    | UnaryExpressionNotPlusMinus"""
    p[0] = ("UnaryExpression",) + tuple(p[-len(p) + 1 :])


def p_PreIncrementExpression(p):
    """PreIncrementExpression : PLUS_PLUS UnaryExpression"""
    p[0] = ("PreIncrementExpression",) + tuple(p[-len(p) + 1 :])


def p_DecrementExpression(p):
    """PreDecrementExpression : MINUS_MINUS UnaryExpression"""
    p[0] = ("PreDecrementExpression",) + tuple(p[-len(p) + 1 :])


def p_UnaryExpressionNotPlusMinus(p):
    """UnaryExpressionNotPlusMinus : PostfixExpression
    | TILDE UnaryExpression
    | EXCLAMATION UnaryExpression
    | CastExpression
    | SwitchExpression"""
    p[0] = ("UnaryExpressionNotPlusMinus",) + tuple(p[-len(p) + 1 :])


def p_PostfixExpression(p):
    """PostfixExpression : Primary
    | ExpressionName
    | PostIncrementExpression
    | PostDecrementExpression"""
    p[0] = ("PostfixExpression",) + tuple(p[-len(p) + 1 :])


def p_PostIncrementExpression(p):
    """PostIncrementExpression : PostfixExpression PLUS_PLUS"""
    p[0] = ("PostIncrementExpression",) + tuple(p[-len(p) + 1 :])


def p_PostDecrementExpression(p):
    """PostDecrementExpression : PostfixExpression MINUS_MINUS"""
    p[0] = ("PostDecrementExpression",) + tuple(p[-len(p) + 1 :])


def p_CastExpression(p):
    """CastExpression : LEFT_PAREN PrimitiveType RIGHT_PAREN UnaryExpression
    | LEFT_PAREN ReferenceType AlphaAdditionalBound RIGHT_PAREN UnaryExpressionNotPlusMinus
    | LEFT_PAREN ReferenceType AlphaAdditionalBound RIGHT_PAREN LambdaExpression"""
    p[0] = ("CastExpression",) + tuple(p[-len(p) + 1 :])


def p_SwitchExpression(p):
    """SwitchExpression : SWITCH LEFT_PAREN Expression RIGHT_PAREN SwitchBlock"""
    p[0] = ("SwitchExpression",) + tuple(p[-len(p) + 1 :])


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


def p_BetaArgumentList(p):
    """BetaArgumentList : ArgumentList
    | empty"""
    p[0] = ("BetaArgumentList",) + tuple(p[-len(p) + 1 :])


def p_BetaClassBody(p):
    """BetaClassBody : ClassBody
    | empty"""
    p[0] = ("BetaClassBody",) + tuple(p[-len(p) + 1 :])


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


def p_ExpressionName(p):
    """ExpressionName : IDENTIFIER AlphaDotIdentifier"""
    p[0] = ("ExpressionName",) + tuple(p[-len(p) + 1 :])


def p_BlockStatement(p):
    """BlockStatement : LocalClassOrInterfaceDeclaration
    | LocalVariableDeclarationStatement
    | Statement"""
    p[0] = ("BlockStatement",) + tuple(p[-len(p) + 1 :])


def p_Literal(p):
    """Literal : INTEGER_LITERAL_OCTAL
    | INTEGER_LITERAL_HEXADEC
    | INTEGER_LITERAL_DEC
    | INTEGER_LITERAL_BINAR
    | FLOATING_POINT_LITERAL
    | BOOLEAN_LITERAL
    | CHARACTER_LITERAL
    | STRING_LITERAL
    | TEXT_BLOCK
    | NULL_LITERAL"""
    p[0] = ("Literal",) + tuple(p[-len(p) + 1 :])


def p_empty(p):
    "empty :"
    p[0] = None


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

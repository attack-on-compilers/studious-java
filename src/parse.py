#!/usr/bin/env python3

import ply.yacc as yacc
from lexer import *
import argparse
from dot import tree_gen, tree_reduce
from symTabGen import generate_symbol_table
from symbol_table import *

start = "Start"


def p_Start(p):
    """Start : CompilationUnit"""
    p[0] = ("Start",) + tuple(p[-len(p) + 1 :])


def p_CompilationUnit(p):
    """CompilationUnit : BetaPackageDeclaration BetaAlphaImportDeclaration BetaAlphaTypeDeclaration"""
    p[0] = ("CompilationUnit",) + tuple(p[-len(p) + 1 :])


def p_BetaPackageDeclaration(p):
    """BetaPackageDeclaration : PackageDeclaration
    | empty"""
    p[0] = ("BetaPackageDeclaration",) + tuple(p[-len(p) + 1 :])


def p_AlphaImportDeclaration(p):
    """AlphaImportDeclaration : ImportDeclaration
    | AlphaImportDeclaration ImportDeclaration"""
    p[0] = ("AlphaImportDeclaration",) + tuple(p[-len(p) + 1 :])


def p_AlphaTypeDeclaration(p):
    """AlphaTypeDeclaration : TypeDeclaration
    | AlphaTypeDeclaration TypeDeclaration"""
    p[0] = ("AlphaTypeDeclaration",) + tuple(p[-len(p) + 1 :])


def p_PackageDeclaration(p):
    """PackageDeclaration : PACKAGE Name SEMICOLON"""
    p[0] = ("PackageDeclaration",) + tuple(p[-len(p) + 1 :])


def p_ImportDeclaration(p):
    """ImportDeclaration : SingleTypeImportDeclaration
    | TypeImportOnDemandDeclaration"""
    p[0] = ("ImportDeclaration",) + tuple(p[-len(p) + 1 :])


def p_SingleTypeImportDeclaration(p):
    """SingleTypeImportDeclaration : IMPORT Name SEMICOLON"""
    p[0] = ("SingleTypeImportDeclaration",) + tuple(p[-len(p) + 1 :])


def p_TypeImportOnDemandDeclaration(p):
    """TypeImportOnDemandDeclaration : IMPORT Name DOT STAR SEMICOLON"""
    p[0] = ("TypeImportOnDemandDeclaration",) + tuple(p[-len(p) + 1 :])


def p_Name(p):
    """Name : IdentifierId
    | NameDotIdentifierId"""
    p[0] = ("Name",) + tuple(p[-len(p) + 1 :])


def p_IdentifierId(p):
    """IdentifierId : IDENTIFIER"""
    p[0] = ("IdentifierId",) + tuple(p[-len(p) + 1 :])


def p_NameDotIdentifierId(p):
    """NameDotIdentifierId : Name DOT IDENTIFIER"""
    p[0] = ("NameDotIdentifierId",) + tuple(p[-len(p) + 1 :])


def p_BetaAlphaImportDeclaration(p):
    """BetaAlphaImportDeclaration : AlphaImportDeclaration
    | empty"""
    p[0] = ("BetaAlphaImportDeclaration",) + tuple(p[-len(p) + 1 :])


def p_BetaAlphaTypeDeclaration(p):
    """BetaAlphaTypeDeclaration : AlphaTypeDeclaration
    | empty"""
    p[0] = ("BetaAlphaTypeDeclaration",) + tuple(p[-len(p) + 1 :])


def p_TypeDeclaration(p):
    """TypeDeclaration : ClassDeclaration
    | InterfaceDeclaration
    | SEMICOLON"""
    p[0] = ("TypeDeclaration",) + tuple(p[-len(p) + 1 :])


def p_AlphaModifier(p):
    """AlphaModifier : Modifier
    | AlphaModifier Modifier"""
    p[0] = ("AlphaModifier",) + tuple(p[-len(p) + 1 :])


def p_Modifier(p):
    """Modifier : PUBLIC
    | PROTECTED
    | PRIVATE
    | STATIC
    | ABSTRACT
    | FINAL
    | NATIVE
    | SYNCHRONIZED
    | TRANSIENT
    | VOLATILE
    | STRICTFP"""
    p[0] = ("Modifier",) + tuple(p[-len(p) + 1 :])


def p_ClassDeclaration(p):
    """ClassDeclaration : BetaAlphaModifier CLASS IDENTIFIER BetaSuper BetaAlphaInterface ClassBody"""
    p[0] = ("ClassDeclaration",) + tuple(p[-len(p) + 1 :])


def p_BetaAlphaInterface(p):
    """BetaAlphaInterface : AlphaInterface
    | empty"""
    p[0] = ("BetaAlphaInterface",) + tuple(p[-len(p) + 1 :])


def p_BetaAlphaModifier(p):
    """BetaAlphaModifier : AlphaModifier
    | empty"""
    p[0] = ("BetaAlphaModifier",) + tuple(p[-len(p) + 1 :])


def p_BetaSuper(p):
    """BetaSuper : Super
    | empty"""
    p[0] = ("BetaSuper",) + tuple(p[-len(p) + 1 :])


def p_Super(p):
    """Super : EXTENDS ClassType"""
    p[0] = ("Super",) + tuple(p[-len(p) + 1 :])


def p_AlphaInterface(p):
    """AlphaInterface : IMPLEMENTS InterfaceTypeList"""
    p[0] = ("AlphaInterface",) + tuple(p[-len(p) + 1 :])


def p_InterfaceTypeList(p):
    """InterfaceTypeList : InterfaceType
    | InterfaceTypeList COMMA InterfaceType"""
    p[0] = ("InterfaceTypeList",) + tuple(p[-len(p) + 1 :])


def p_ClassBody(p):
    """ClassBody : LEFT_BRACE BetaAlphaClassBodyDeclaration RIGHT_BRACE"""
    p[0] = ("ClassBody",) + tuple(p[-len(p) + 1 :])


def p_BetaAlphaClassBodyDeclaration(p):
    """BetaAlphaClassBodyDeclaration : AlphaClassBodyDeclaration
    | empty"""
    p[0] = ("BetaAlphaClassBodyDeclaration",) + tuple(p[-len(p) + 1 :])


def p_AlphaClassBodyDeclaration(p):
    """AlphaClassBodyDeclaration : ClassBodyDeclaration
    | AlphaClassBodyDeclaration ClassBodyDeclaration"""
    p[0] = ("AlphaClassBodyDeclaration",) + tuple(p[-len(p) + 1 :])


def p_ClassBodyDeclaration(p):
    """ClassBodyDeclaration : ClassMemberDeclaration
    | StaticInitializer
    | ConstructorDeclaration"""
    p[0] = ("ClassBodyDeclaration",) + tuple(p[-len(p) + 1 :])


def p_ClassMemberDeclaration(p):
    """ClassMemberDeclaration : FieldDeclaration
    | MethodDeclaration"""
    p[0] = ("ClassMemberDeclaration",) + tuple(p[-len(p) + 1 :])


def p_Type(p):
    """Type : PrimitiveType
    | ReferenceType"""
    p[0] = ("Type",) + tuple(p[-len(p) + 1 :])


def p_PrimitiveType(p):
    """PrimitiveType : NumericType
    | BOOLEAN"""
    p[0] = ("PrimitiveType",) + tuple(p[-len(p) + 1 :])


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
    | ArrayType"""
    p[0] = ("ReferenceType",) + tuple(p[-len(p) + 1 :])


def p_ClassOrInterfaceType(p):
    """ClassOrInterfaceType : Name"""
    p[0] = ("ClassOrInterfaceType",) + tuple(p[-len(p) + 1 :])


def p_ClassType(p):
    """ClassType : ClassOrInterfaceType"""
    p[0] = ("ClassType",) + tuple(p[-len(p) + 1 :])


def p_InterfaceType(p):
    """InterfaceType : ClassOrInterfaceType"""
    p[0] = ("InterfaceType",) + tuple(p[-len(p) + 1 :])


def p_InterfaceDeclaration(p):
    """InterfaceDeclaration : BetaAlphaModifier INTERFACE IDENTIFIER BetaExtendsAlphaInterface InterfaceBody"""
    p[0] = ("InterfaceDeclaration",) + tuple(p[-len(p) + 1 :])


def p_BetaExtendsAlphaInterface(p):
    """BetaExtendsAlphaInterface : ExtendsAlphaInterface
    | empty"""
    p[0] = ("BetaExtendsAlphaInterface",) + tuple(p[-len(p) + 1 :])


def p_ExtendsAlphaInterface(p):
    """ExtendsAlphaInterface : EXTENDS InterfaceType
    | ExtendsAlphaInterface COMMA InterfaceType"""
    p[0] = ("ExtendsAlphaInterface",) + tuple(p[-len(p) + 1 :])


def p_InterfaceBody(p):
    """InterfaceBody : LEFT_BRACE BetaAlphaInterfaceMemberDeclaration RIGHT_BRACE"""
    p[0] = ("InterfaceBody",) + tuple(p[-len(p) + 1 :])


def p_BetaAlphaInterfaceMemberDeclaration(p):
    """BetaAlphaInterfaceMemberDeclaration : AlphaInterfaceMemberDeclaration
    | empty"""
    p[0] = ("BetaAlphaInterfaceMemberDeclaration",) + tuple(p[-len(p) + 1 :])


def p_AlphaInterfaceMemberDeclaration(p):
    """AlphaInterfaceMemberDeclaration : InterfaceMemberDeclaration
    | AlphaInterfaceMemberDeclaration InterfaceMemberDeclaration"""
    p[0] = ("AlphaInterfaceMemberDeclaration",) + tuple(p[-len(p) + 1 :])


def p_InterfaceMemberDeclaration(p):
    """InterfaceMemberDeclaration : ConstantDeclaration
    | AbstractMethodDeclaration"""
    p[0] = ("InterfaceMemberDeclaration",) + tuple(p[-len(p) + 1 :])


def p_ConstantDeclaration(p):
    """ConstantDeclaration : FieldDeclaration"""
    p[0] = ("ConstantDeclaration",) + tuple(p[-len(p) + 1 :])


def p_ArrayType(p):
    """ArrayType : PrimitiveType LEFT_BRACKET RIGHT_BRACKET
    | Name LEFT_BRACKET RIGHT_BRACKET
    | ArrayType LEFT_BRACKET RIGHT_BRACKET"""
    p[0] = ("ArrayType",) + tuple(p[-len(p) + 1 :])


def p_AlphaVariableDeclarator(p):
    """AlphaVariableDeclarator : VariableDeclarator
    | AlphaVariableDeclarator COMMA VariableDeclarator"""
    p[0] = ("AlphaVariableDeclarator",) + tuple(p[-len(p) + 1 :])


def p_VariableDeclarator(p):
    """VariableDeclarator : VariableDeclaratorId
    | VariableDeclaratorId ASSIGN VariableInitializer"""
    p[0] = ("VariableDeclarator",) + tuple(p[-len(p) + 1 :])


def p_VariableDeclaratorId(p):
    """VariableDeclaratorId : IDENTIFIER
    | VariableDeclaratorId LEFT_BRACKET RIGHT_BRACKET"""
    p[0] = ("VariableDeclaratorId",) + tuple(p[-len(p) + 1 :])


def p_VariableInitializer(p):
    """VariableInitializer : Expression
    | ArrayInitializer"""
    p[0] = ("VariableInitializer",) + tuple(p[-len(p) + 1 :])


def p_FieldDeclaration(p):
    """FieldDeclaration : BetaAlphaModifier Type AlphaVariableDeclarator SEMICOLON"""
    p[0] = ("FieldDeclaration",) + tuple(p[-len(p) + 1 :])


def p_MethodDeclaration(p):
    """MethodDeclaration : MethodHeader MethodBody"""
    p[0] = ("MethodDeclaration",) + tuple(p[-len(p) + 1 :])


def p_MethodHeader(p):
    """MethodHeader : BetaAlphaModifier Type MethodDeclarator BetaAlphaThrow
    | BetaAlphaModifier VOID MethodDeclarator BetaAlphaThrow"""
    p[0] = ("MethodHeader",) + tuple(p[-len(p) + 1 :])


def p_BetaAlphaThrow(p):
    """BetaAlphaThrow : AlphaThrow
    | empty"""
    p[0] = ("BetaAlphaThrow",) + tuple(p[-len(p) + 1 :])


def p_MethodDeclarator(p):
    """MethodDeclarator : IDENTIFIER LEFT_PAREN BetaFormalParameterList RIGHT_PAREN
    | MethodDeclarator LEFT_BRACKET RIGHT_BRACKET"""
    p[0] = ("MethodDeclarator",) + tuple(p[-len(p) + 1 :])


def p_BetaFormalParameterList(p):
    """BetaFormalParameterList : FormalParameterList
    | empty"""
    p[0] = ("BetaFormalParameterList",) + tuple(p[-len(p) + 1 :])


def p_FormalParameterList(p):
    """FormalParameterList : FormalParameter
    | FormalParameterList COMMA FormalParameter"""
    p[0] = ("FormalParameterList",) + tuple(p[-len(p) + 1 :])


def p_FormalParameter(p):
    """FormalParameter : Type VariableDeclaratorId"""
    p[0] = ("FormalParameter",) + tuple(p[-len(p) + 1 :])


def p_AlphaThrow(p):
    """AlphaThrow : THROWS ClassTypeList"""
    p[0] = ("AlphaThrow",) + tuple(p[-len(p) + 1 :])


def p_ClassTypeList(p):
    """ClassTypeList : ClassType
    | ClassTypeList COMMA ClassType"""
    p[0] = ("ClassTypeList",) + tuple(p[-len(p) + 1 :])


def p_MethodBody(p):
    """MethodBody : Block
    | SEMICOLON"""
    p[0] = ("MethodBody",) + tuple(p[-len(p) + 1 :])


def p_StaticInitializer(p):
    """StaticInitializer : STATIC Block"""
    p[0] = ("StaticInitializer",) + tuple(p[-len(p) + 1 :])


def p_ConstructorDeclaration(p):
    """ConstructorDeclaration : BetaAlphaModifier ConstructorDeclarator BetaAlphaThrow ConstructorBody"""
    p[0] = ("ConstructorDeclaration",) + tuple(p[-len(p) + 1 :])


def p_ConstructorDeclarator(p):
    """ConstructorDeclarator : IdentifierId LEFT_PAREN BetaFormalParameterList RIGHT_PAREN"""
    p[0] = ("ConstructorDeclarator",) + tuple(p[-len(p) + 1 :])


def p_ConstructorBody(p):
    """ConstructorBody : LEFT_BRACE BetaExplicitConstructorInvocation BetaAlphaBlockStatement RIGHT_BRACE"""
    p[0] = ("ConstructorBody",) + tuple(p[-len(p) + 1 :])


def p_BetaAlphaBlockStatement(p):
    """BetaAlphaBlockStatement : AlphaBlockStatement
    | empty"""
    p[0] = ("BetaAlphaBlockStatement",) + tuple(p[-len(p) + 1 :])


def p_BetaExplicitConstructorInvocation(p):
    """BetaExplicitConstructorInvocation : ExplicitConstructorInvocation
    | empty"""
    p[0] = ("BetaExplicitConstructorInvocation",) + tuple(p[-len(p) + 1 :])


def p_ExplicitConstructorInvocation(p):
    """ExplicitConstructorInvocation : THIS LEFT_PAREN BetaArgumentList RIGHT_PAREN SEMICOLON
    | SUPER LEFT_PAREN BetaArgumentList RIGHT_PAREN SEMICOLON"""
    p[0] = ("ExplicitConstructorInvocation",) + tuple(p[-len(p) + 1 :])


def p_BetaArgumentList(p):
    """BetaArgumentList : ArgumentList
    | empty"""
    p[0] = ("BetaArgumentList",) + tuple(p[-len(p) + 1 :])


def p_AbstractMethodDeclaration(p):
    """AbstractMethodDeclaration : MethodHeader SEMICOLON"""
    p[0] = ("AbstractMethodDeclaration",) + tuple(p[-len(p) + 1 :])


def p_ArrayInitializer(p):
    """ArrayInitializer : LEFT_BRACE BetaAlphaVariableInitializer COMMA RIGHT_BRACE
    | LEFT_BRACE BetaAlphaVariableInitializer RIGHT_BRACE"""
    p[0] = ("ArrayInitializer",) + tuple(p[-len(p) + 1 :])


def p_BetaAlphaVariableInitializer(p):
    """BetaAlphaVariableInitializer : AlphaVariableInitializer
    | empty"""
    p[0] = ("BetaAlphaVariableInitializer",) + tuple(p[-len(p) + 1 :])


def p_AlphaVariableInitializer(p):
    """AlphaVariableInitializer : VariableInitializer
    | AlphaVariableInitializer COMMA VariableInitializer"""
    p[0] = ("AlphaVariableInitializer",) + tuple(p[-len(p) + 1 :])


def p_Block(p):
    """Block : LEFT_BRACE BetaAlphaBlockStatement RIGHT_BRACE"""
    p[0] = ("Block",) + tuple(p[-len(p) + 1 :])


def p_AlphaBlockStatement(p):
    """AlphaBlockStatement : BlockStatement
    | AlphaBlockStatement BlockStatement"""
    p[0] = ("AlphaBlockStatement",) + tuple(p[-len(p) + 1 :])


def p_BlockStatement(p):
    """BlockStatement : LocalVariableDeclarationStatement
    | Statement"""
    p[0] = ("BlockStatement",) + tuple(p[-len(p) + 1 :])


def p_LocalVariableDeclarationStatement(p):
    """LocalVariableDeclarationStatement : LocalVariableDeclaration SEMICOLON"""
    p[0] = ("LocalVariableDeclarationStatement",) + tuple(p[-len(p) + 1 :])


def p_LocalVariableDeclaration(p):
    """LocalVariableDeclaration : Type AlphaVariableDeclarator"""
    p[0] = ("LocalVariableDeclaration",) + tuple(p[-len(p) + 1 :])


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
    | SwitchStatement
    | DoStatement
    | BreakStatement
    | ContinueStatement
    | ReturnStatement
    | SynchronizedStatement
    | ThrowStatement
    | TryStatement"""
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
    """IfThenElseStatement : IF LEFT_PAREN Expression RIGHT_PAREN StatementNoShortIf ELSE Statement"""
    p[0] = ("IfThenElseStatement",) + tuple(p[-len(p) + 1 :])


def p_IfThenElseStatementNoShortIf(p):
    """IfThenElseStatementNoShortIf : IF LEFT_PAREN Expression RIGHT_PAREN StatementNoShortIf ELSE StatementNoShortIf"""
    p[0] = ("IfThenElseStatementNoShortIf",) + tuple(p[-len(p) + 1 :])


def p_SwitchStatement(p):
    """SwitchStatement : SWITCH LEFT_PAREN Expression RIGHT_PAREN SwitchBlock"""
    p[0] = ("SwitchStatement",) + tuple(p[-len(p) + 1 :])


def p_SwitchBlock(p):
    """SwitchBlock : LEFT_BRACE BetaAlphaSwitchBlockStatementGroup BetaAlphaSwitchLabel RIGHT_BRACE"""
    p[0] = ("SwitchBlock",) + tuple(p[-len(p) + 1 :])


def p_BetaAlphaSwitchBlockStatementGroup(p):
    """BetaAlphaSwitchBlockStatementGroup : AlphaSwitchBlockStatementGroup
    | empty"""
    p[0] = ("BetaAlphaSwitchBlockStatementGroup",) + tuple(p[-len(p) + 1 :])


def p_BetaAlphaSwitchLabel(p):
    """BetaAlphaSwitchLabel : AlphaSwitchLabel
    | empty"""
    p[0] = ("BetaAlphaSwitchLabel",) + tuple(p[-len(p) + 1 :])


def p_AlphaSwitchBlockStatementGroup(p):
    """AlphaSwitchBlockStatementGroup : SwitchBlockStatementGroup
    | AlphaSwitchBlockStatementGroup SwitchBlockStatementGroup"""
    p[0] = ("AlphaSwitchBlockStatementGroup",) + tuple(p[-len(p) + 1 :])


def p_SwitchBlockStatementGroup(p):
    """SwitchBlockStatementGroup : AlphaSwitchLabel AlphaBlockStatement"""
    p[0] = ("SwitchBlockStatementGroup",) + tuple(p[-len(p) + 1 :])


def p_AlphaSwitchLabel(p):
    """AlphaSwitchLabel : SwitchLabel
    | AlphaSwitchLabel SwitchLabel"""
    p[0] = ("AlphaSwitchLabel",) + tuple(p[-len(p) + 1 :])


def p_SwitchLabel(p):
    """SwitchLabel : CASE ConstantExpression COLON
    | DEFAULT COLON"""
    p[0] = ("SwitchLabel",) + tuple(p[-len(p) + 1 :])


def p_ForStatement(p):
    """ForStatement : FOR LEFT_PAREN BetaForInit SEMICOLON BetaExpression SEMICOLON BetaForUpdate RIGHT_PAREN Statement"""
    p[0] = ("ForStatement",) + tuple(p[-len(p) + 1 :])


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


def p_ForStatementNoShortIf(p):
    """ForStatementNoShortIf : FOR LEFT_PAREN BetaForInit SEMICOLON BetaExpression SEMICOLON BetaForUpdate RIGHT_PAREN StatementNoShortIf"""
    p[0] = ("ForStatementNoShortIf",) + tuple(p[-len(p) + 1 :])


def p_ForInit(p):
    """ForInit : StatementExpressionList
    | LocalVariableDeclaration"""
    p[0] = ("ForInit",) + tuple(p[-len(p) + 1 :])


def p_ForUpdate(p):
    """ForUpdate : StatementExpressionList"""
    p[0] = ("ForUpdate",) + tuple(p[-len(p) + 1 :])


def p_StatementExpressionList(p):
    """StatementExpressionList : StatementExpression
    | StatementExpressionList COMMA StatementExpression"""
    p[0] = ("StatementExpressionList",) + tuple(p[-len(p) + 1 :])


def p_BreakStatement(p):
    """BreakStatement : BREAK BetaIdentifier SEMICOLON"""
    p[0] = ("BreakStatement",) + tuple(p[-len(p) + 1 :])


def p_BetaIdentifier(p):
    """BetaIdentifier : IDENTIFIER
    | empty"""
    p[0] = ("BetaIdentifier",) + tuple(p[-len(p) + 1 :])


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
    | TRY Block BetaCatches Finally"""
    p[0] = ("TryStatement",) + tuple(p[-len(p) + 1 :])


def p_BetaCatches(p):
    """BetaCatches : Catches
    | empty"""
    p[0] = ("BetaCatches",) + tuple(p[-len(p) + 1 :])


def p_Catches(p):
    """Catches : CatchClause
    | Catches CatchClause"""
    p[0] = ("Catches",) + tuple(p[-len(p) + 1 :])


def p_CatchClause(p):
    """CatchClause : CATCH LEFT_PAREN FormalParameter RIGHT_PAREN Block"""
    p[0] = ("CatchClause",) + tuple(p[-len(p) + 1 :])


def p_Finally(p):
    """Finally : FINALLY Block"""
    p[0] = ("Finally",) + tuple(p[-len(p) + 1 :])


def p_Primary(p):
    """Primary : PrimaryNoNewArray
    | ArrayCreationExpression"""
    p[0] = ("Primary",) + tuple(p[-len(p) + 1 :])


def p_PrimaryNoNewArray(p):
    """PrimaryNoNewArray : Literal
    | THIS
    | LEFT_PAREN Expression RIGHT_PAREN
    | ClassInstanceCreationExpression
    | FieldAccess
    | MethodInvocation
    | ArrayAccess"""

    p[0] = ("PrimaryNoNewArray",) + tuple(p[-len(p) + 1 :])


def p_ClassInstanceCreationExpression(p):
    """ClassInstanceCreationExpression : NEW ClassType LEFT_PAREN BetaArgumentList RIGHT_PAREN"""
    p[0] = ("ClassInstanceCreationExpression",) + tuple(p[-len(p) + 1 :])


def p_ArgumentList(p):
    """ArgumentList : Expression
    | ArgumentList COMMA Expression"""
    p[0] = ("ArgumentList",) + tuple(p[-len(p) + 1 :])


def p_ArrayCreationExpression(p):
    """ArrayCreationExpression : NEW PrimitiveType BetaAlphaDimExpr AlphaDim
    | NEW ClassOrInterfaceType BetaAlphaDimExpr AlphaDim"""
    p[0] = ("ArrayCreationExpression",) + tuple(p[-len(p) + 1 :])


def p_BetaAlphaDimExpr(p):
    """BetaAlphaDimExpr : AlphaDimExpr
    | empty"""
    p[0] = ("BetaAlphaDimExpr",) + tuple(p[-len(p) + 1 :])


def p_AlphaDimExpr(p):
    """AlphaDimExpr : DimExpr
    | AlphaDimExpr DimExpr"""
    p[0] = ("AlphaDimExpr",) + tuple(p[-len(p) + 1 :])


def p_DimExpr(p):
    """DimExpr : LEFT_BRACKET Expression RIGHT_BRACKET"""
    p[0] = ("DimExpr",) + tuple(p[-len(p) + 1 :])


def p_AlphaDim(p):
    """AlphaDim : LEFT_BRACKET RIGHT_BRACKET
    | AlphaDim LEFT_BRACKET RIGHT_BRACKET"""
    p[0] = ("AlphaDim",) + tuple(p[-len(p) + 1 :])


def p_FieldAccess(p):
    """FieldAccess : Primary DOT IDENTIFIER
    | SUPER DOT IDENTIFIER"""
    p[0] = ("FieldAccess",) + tuple(p[-len(p) + 1 :])


def p_MethodInvocation(p):
    """MethodInvocation : Name LEFT_PAREN BetaArgumentList RIGHT_PAREN
    | Primary DOT IDENTIFIER LEFT_PAREN BetaArgumentList RIGHT_PAREN
    | SUPER DOT IDENTIFIER LEFT_PAREN BetaArgumentList RIGHT_PAREN"""
    p[0] = ("MethodInvocation",) + tuple(p[-len(p) + 1 :])


def p_ArrayAccess(p):
    """ArrayAccess : Name LEFT_BRACKET Expression RIGHT_BRACKET
    | PrimaryNoNewArray LEFT_BRACKET Expression RIGHT_BRACKET"""
    p[0] = ("ArrayAccess",) + tuple(p[-len(p) + 1 :])


def p_PostfixExpression(p):
    """PostfixExpression : Primary
    | Name
    | PostIncrementExpression
    | PostDecrementExpression"""
    p[0] = ("PostfixExpression",) + tuple(p[-len(p) + 1 :])


def p_PostIncrementExpression(p):
    """PostIncrementExpression : PostfixExpression PLUS_PLUS"""
    p[0] = ("PostIncrementExpression",) + tuple(p[-len(p) + 1 :])


def p_PostDecrementExpression(p):
    """PostDecrementExpression : PostfixExpression MINUS_MINUS"""
    p[0] = ("PostDecrementExpression",) + tuple(p[-len(p) + 1 :])


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


def p_PreDecrementExpression(p):
    """PreDecrementExpression : MINUS_MINUS UnaryExpression"""
    p[0] = ("PreDecrementExpression",) + tuple(p[-len(p) + 1 :])


def p_UnaryExpressionNotPlusMinus(p):
    """UnaryExpressionNotPlusMinus : PostfixExpression
    | TILDE UnaryExpression
    | EXCLAMATION UnaryExpression
    | CastExpression"""
    p[0] = ("UnaryExpressionNotPlusMinus",) + tuple(p[-len(p) + 1 :])


def p_CastExpression(p):
    """CastExpression : LEFT_PAREN PrimitiveType BetaAlphaDim RIGHT_PAREN UnaryExpression
    | LEFT_PAREN Expression RIGHT_PAREN UnaryExpressionNotPlusMinus
    | LEFT_PAREN Name AlphaDim RIGHT_PAREN UnaryExpressionNotPlusMinus"""
    p[0] = ("CastExpression",) + tuple(p[-len(p) + 1 :])

def p_BetaAlphaDim(p):
    """BetaAlphaDim : AlphaDim
    | empty"""
    p[0] = ("BetaAlphaDim",) + tuple(p[-len(p) + 1 :])


def p_MultiplicativeExpression(p):
    """MultiplicativeExpression : UnaryExpression
    | MultiplicativeExpression STAR UnaryExpression
    | MultiplicativeExpression SLASH UnaryExpression
    | MultiplicativeExpression PERCENT UnaryExpression"""
    p[0] = ("MultiplicativeExpression",) + tuple(p[-len(p) + 1 :])


def p_AdditiveExpression(p):
    """AdditiveExpression : MultiplicativeExpression
    | AdditiveExpression PLUS MultiplicativeExpression
    | AdditiveExpression MINUS MultiplicativeExpression"""
    p[0] = ("AdditiveExpression",) + tuple(p[-len(p) + 1 :])


def p_ShiftExpression(p):
    """ShiftExpression : AdditiveExpression
    | ShiftExpression LEFT_SHIFT AdditiveExpression
    | ShiftExpression RIGHT_SHIFT AdditiveExpression
    | ShiftExpression UNSIGNED_RIGHT_SHIFT AdditiveExpression"""
    p[0] = ("ShiftExpression",) + tuple(p[-len(p) + 1 :])


def p_RelationalExpression(p):
    """RelationalExpression : ShiftExpression
    | RelationalExpression LESS ShiftExpression
    | RelationalExpression GREATER ShiftExpression
    | RelationalExpression LESS_EQUAL ShiftExpression
    | RelationalExpression GREATER_EQUAL ShiftExpression
    | RelationalExpression INSTANCEOF ReferenceType"""
    p[0] = ("RelationalExpression",) + tuple(p[-len(p) + 1 :])


def p_EqualityExpression(p):
    """EqualityExpression : RelationalExpression
    | EqualityExpression EQUAL_EQUAL RelationalExpression
    | EqualityExpression EXCLAMATION_EQUAL RelationalExpression"""
    p[0] = ("EqualityExpression",) + tuple(p[-len(p) + 1 :])


def p_AndExpression(p):
    """AndExpression : EqualityExpression
    | AndExpression AMPERSAND EqualityExpression"""
    p[0] = ("AndExpression",) + tuple(p[-len(p) + 1 :])


def p_ExclusiveOrExpression(p):
    """ExclusiveOrExpression : AndExpression
    | ExclusiveOrExpression CARET AndExpression"""
    p[0] = ("ExclusiveOrExpression",) + tuple(p[-len(p) + 1 :])


def p_InclusiveOrExpression(p):
    """InclusiveOrExpression : ExclusiveOrExpression
    | InclusiveOrExpression BAR ExclusiveOrExpression"""
    p[0] = ("InclusiveOrExpression",) + tuple(p[-len(p) + 1 :])


def p_ConditionalAndExpression(p):
    """ConditionalAndExpression : InclusiveOrExpression
    | ConditionalAndExpression AMPERSAND_AMPERSAND InclusiveOrExpression"""
    p[0] = ("ConditionalAndExpression",) + tuple(p[-len(p) + 1 :])


def p_ConditionalOrExpression(p):
    """ConditionalOrExpression : ConditionalAndExpression
    | ConditionalOrExpression BAR_BAR ConditionalAndExpression"""
    p[0] = ("ConditionalOrExpression",) + tuple(p[-len(p) + 1 :])


def p_ConditionalExpression(p):
    """ConditionalExpression : ConditionalOrExpression
    | ConditionalOrExpression QUESTION Expression COLON ConditionalExpression"""
    p[0] = ("ConditionalExpression",) + tuple(p[-len(p) + 1 :])


def p_AssignmentExpression(p):
    """AssignmentExpression : ConditionalExpression
    | Assignment"""
    p[0] = ("AssignmentExpression",) + tuple(p[-len(p) + 1 :])


def p_Assignment(p):
    """Assignment : LeftHandSide AssignmentOperator AssignmentExpression"""
    p[0] = ("Assignment",) + tuple(p[-len(p) + 1 :])


def p_LeftHandSide(p):
    """LeftHandSide : Name
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


def p_Expression(p):
    """Expression : AssignmentExpression"""
    p[0] = ("Expression",) + tuple(p[-len(p) + 1 :])


def p_ConstantExpression(p):
    """ConstantExpression : Expression"""
    p[0] = ("ConstantExpression",) + tuple(p[-len(p) + 1 :])


def p_WhileStatement(p):
    """WhileStatement : WHILE LEFT_PAREN Expression RIGHT_PAREN Statement"""
    p[0] = ("WhileStatement",) + tuple(p[-len(p) + 1 :])


def p_WhileStatementNoShortIf(p):
    """WhileStatementNoShortIf : WHILE LEFT_PAREN Expression RIGHT_PAREN StatementNoShortIf"""
    p[0] = ("WhileStatementNoShortIf",) + tuple(p[-len(p) + 1 :])


def p_DoStatement(p):
    """DoStatement : DO Statement WHILE LEFT_PAREN Expression RIGHT_PAREN SEMICOLON"""
    p[0] = ("DoStatement",) + tuple(p[-len(p) + 1 :])


def p_Literal(p):
    """Literal : INTEGER_LITERAL_OCTAL
    | INTEGER_LITERAL_HEXADEC
    | INTEGER_LITERAL_DEC
    | INTEGER_LITERAL_BINAR
    | FLOATING_LITERAL_REDUCED_POINT
    | BOOLEAN_LITERAL
    | CHARACTER_LITERAL
    | STRING_LITERAL
    | TEXT_BLOCK
    | NULL_LITERAL"""
    p[0] = ("Literal",) + tuple(p[-len(p) + 1 :])


def p_empty(p):
    "empty :"
    p[0] = ("",)


def p_error(p):
    print("Syntax error in input at line {} at token {}".format(p.lineno, p.value))
    #raise Exception("Syntax error in input at line {} at token {}".format(p.lineno, p.value))


yacc.yacc(debug=False, debugfile="parser.out")


def getArgs():
    parser = argparse.ArgumentParser()
    parser.add_argument("-i", "--input", type=str, default=None, help="Input file")
    parser.add_argument("-o", "--output", type=str, default="ast", help="Output file")
    parser.add_argument("-a", "--all", action="store_true", help="Show Entire Parse Tree")
    parser.add_argument("-v", "--verbose", action="store_true", help="Verbose Output")
    return parser


if __name__ == "__main__":
    # lex.lex(debug=True)
    # yacc.yacc(debug=True)
    args = getArgs().parse_args()
    if args.verbose:
        print("Input file: {}".format(args.input))
        print("Output file: {}".format(args.output))
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
            print("Generating Symbol Table")
        global_symbol_table = generate_symbol_table(tree)
        if args.verbose:
            print("Symbol Table generated")


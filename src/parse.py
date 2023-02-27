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

start = "program"


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
    """TopLevelClassOrInterfaceDeclaration : ClassDeclaration
    | InterfaceDeclaration
    | SEMICOLON"""
    p[0] = p[1]


def p_ClassDeclaration(p):
    """ClassDeclaration : NormalClassDeclaration"""
    # ClassDeclaration        :   NormalClassDeclaration
    #                     |   EnumDeclaration
    #                     |   RecordDeclaration
    #                     ;
    p[0] = p[1]


def p_NormalClassDeclaration(p):
    """NormalClassDeclaration : AlphaClassModifier CLASS IDENTIFIER BetaTypeParameters BetaClassExtends BetaClassImplements BetaClassPermits ClassBody"""  #    ClassBody"""
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
    """ClassType : IDENTIFIER AlphaDotIdentifier BetaTypeArguments
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


def p_Type(p):
    """Type : ReferenceType
    | PrimitiveType"""
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
    """BetaClassPermits : PERMITS IDENTIFIER AlphaDotIdentifier AlphaCommaTypeName
    | empty"""
    if p[1] == "permits":
        p[0] = " permits " + p[2]
    else:
        p[0] = ""


def p_AlphaCommaTypeName(p):
    """AlphaCommaTypeName : COMMA IDENTIFIER AlphaDotIdentifier AlphaCommaTypeName
    | empty"""
    if p[1] == ",":
        p[0] = ", " + p[2] + p[3]
    else:
        p[0] = ""


def p_empty(p):
    "empty :"
    p[0] = None


def p_ClassBody(p):
    """ClassBody : LEFT_BRACE ClassBodyDeclaration RIGHT_BRACE"""
    p[0] = "{" + p[2] + "}"


def p_ClassBodyDeclaration(p):
    """ClassBodyDeclaration : ClassMemberDeclaration"""
    # | InstanceInitializer
    # | StaticInitializer
    # | ConstructorDeclaration"""
    p[0] = p[1]


def p_ClassMemberDeclaration(p):
    """ClassMemberDeclaration : FieldDeclaration
    | MethodDeclaration
    | SEMICOLON"""
    # | ClassDeclaration        # (Never to be implemneted)
    # | InterfaceDeclaration    # (Never to be implemneted)
    p[0] = p[1]


def p_FieldDeclaration(p):
    """FieldDeclaration : AlphaFieldModifier Type VariableDeclaratorList SEMICOLON"""
    p[0] = p[1] + " " + p[2] + " " + p[3] + ";"


def p_AlphaFieldModifier(p):
    """AlphaFieldModifier : FieldModifier AlphaFieldModifier
    | empty"""
    if p[1]:
        p[0] = p[1] + " " + p[2]
    else:
        p[0] = ""


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
    p[0] = p[1]


def p_VariableDeclaratorList(p):
    """VariableDeclaratorList : VariableDeclarator AlphaCommaVariableDeclarator"""
    p[0] = p[1] + p[2]


def p_AlphaCommaVariableDeclarator(p):
    """AlphaCommaVariableDeclarator : COMMA VariableDeclarator AlphaCommaVariableDeclarator
    | empty"""
    if p[1] == ",":
        p[0] = ", " + p[2] + p[3]
    else:
        p[0] = ""


def p_VariableDeclarator(p):
    """VariableDeclarator : VariableDeclaratorId
    | VariableDeclaratorId ASSIGN VariableInitializer"""
    if p[2] == "=":
        p[0] = p[1] + " = " + p[3]
    else:
        p[0] = p[1]


def p_VariableDeclaratorId(p):
    """VariableDeclaratorId : IDENTIFIER
    | IDENTIFIER Dims"""
    try:
        p[0] = p[1] + p[2]
    except IndexError:
        p[0] = p[1]


def p_VariableInitializer(p):
    """VariableInitializer : TRANSITIVE
    | ArrayInitializer"""
    p[0] = p[1]


def p_ArrayInitializer(p):
    """ArrayInitializer : LEFT_BRACE VariableInitializerList RIGHT_BRACE
    | LEFT_BRACE VariableInitializerList COMMA RIGHT_BRACE"""
    if p[3] == ",":
        p[0] = "{" + p[2] + ",}"
    else:
        p[0] = "{" + p[2] + "}"


def p_VariableInitializerList(p):
    """VariableInitializerList : VariableInitializer AlphaCommaVariableInitializer"""
    p[0] = p[1] + p[2]


def p_AlphaCommaVariableInitializer(p):
    """AlphaCommaVariableInitializer : COMMA VariableInitializer AlphaCommaVariableInitializer
    | empty"""
    if p[1] == ",":
        p[0] = ", " + p[2] + p[3]
    else:
        p[0] = ""


def p_MethodDeclaration(p):
    """MethodDeclaration : AlphaFieldModifier MethodHeader MethodBody"""
    p[0] = p[1] + p[2]



def p_MethodHeader(p):
    """MethodHeader : Result MethodDeclarator BetaThrows
    | TypeParameters Result MethodDeclarator BetaThrows"""


def p_TypeParameters(p):
    """TypeParameters : LESS TypeParameterList GREATER"""
    p[0] = "<" + p[2] + ">"


def p_Result(p):
    """Result : Type
    | VOID"""
    p[0] = p[1]


def p_MethodDeclarator(p):
    """MethodDeclarator : IDENTIFIER LEFT_PAREN FormalParameterList RIGHT_PAREN
    | IDENTIFIER LEFT_PAREN RIGHT_PAREN"""
    if p[3] == "(":
        p[0] = p[1] + "(" + p[3] + ")"
    else:
        p[0] = p[1] + "(" + p[3] + ")"


def p_FormalParameterList(p):
    """FormalParameterList : FormalParameter AlphaCommaFormalParameter"""
    p[0] = p[1] + p[2]


def p_AlphaCommaFormalParameter(p):
    """AlphaCommaFormalParameter : COMMA FormalParameter AlphaCommaFormalParameter
    | empty"""
    if p[1] == ",":
        p[0] = ", " + p[2] + p[3]
    else:
        p[0] = ""


def p_FormalParameter(p):
    """FormalParameter : AlphaVariableModifier Type VariableDeclaratorId VariableArityParameter"""
    p[0] = p[1] + " " + p[2] + " " + p[3] + p[4]


def p_AlphaVariableModifier(p):
    """AlphaVariableModifier : VariableModifier AlphaVariableModifier
    | empty"""
    if p[1]:
        p[0] = p[1] + " " + p[2]
    else:
        p[0] = ""


def p_VariableModifier(p):
    """VariableModifier : FINAL"""
    p[0] = p[1]


def p_VariableArityParameter(p):
    """VariableArityParameter : AlphaVariableModifier Type ELLIPSIS IDENTIFIER"""
    if p[1] == "...":
        p[0] = "..."
    else:
        p[0] = ""


def p_BetaThrows(p):
    """BetaThrows : THROWS ClassTypeList
    | empty"""
    if p[1] == "throws":
        p[0] = " throws " + p[2]
    else:
        p[0] = ""


def p_MethodBody(p):
    """MethodBody : Block
    | SEMICOLON"""
    p[0] = p[1]


def p_Block(p):
    """Block : LEFT_BRACE BetaBlockStatements RIGHT_BRACE"""
    p[0] = "{" + p[2] + "}"

def p_BetaBlockStatements(p):
    """BetaBlockStatements : empty
    | BlockStatements"""
    p[0] = p[1]

def p_BlockStatements(p):
    """BlockStatements : BlockStatement AlphaBlockStatement"""
    p[0] = p[1] + p[2]

def p_AlphaBlockStatement(p):
    """AlphaBlockStatement : BlockStatement AlphaBlockStatement
    | empty"""
    if p[1]:
        p[0] = p[1] + p[2]
    else:
        p[0] = ""

# def p_BlockStatement(p):
#     """BlockStatement : LocalClassOrInterfaceDeclaration
#     | LocalVariableDeclarationStatement
#     | Statement"""
#     p[0] = p[1]


def p_LocalClassOrInterfaceDeclaration(p):
    """LocalClassOrInterfaceDeclaration : ClassDeclaration
    | NormalInterfaceDeclaration"""
    p[0] = p[1]


def p_LocalVariableDeclarationStatement(p):
    """LocalVariableDeclarationStatement : LocalVariableDeclaration SEMICOLON"""
    p[0] = p[1] + ";"

def p_LocalVariableDeclaration(p):
    """LocalVariableDeclaration : AlphaVariableModifier LocalVariableType VariableDeclaratorList"""
    p[0] = p[1] + " " + p[2] + " " + p[3]


def p_localVariableType(p):
    """LocalVariableType : Type
    | VAR"""
    p[0] = p[1]

def p_Statement(p):
    """Statement : StatementWithoutTrailingSubstatement
    | LabeledStatement
    | IfThenStatement
    | IfThenElseStatement
    | WhileStatement
    | ForStatement"""
    p[0] = p[1]

def p_StatementNoShortIf(p):
    """StatementNoShortIf : StatementWithoutTrailingSubstatement
    | LabeledStatementNoShortIf
    | IfThenElseStatementNoShortIf
    | WhileStatementNoShortIf
    | ForStatementNoShortIf"""
    p[0] = p[1]    

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
    p[0] = p[1]

def p_EmptyStatement(p):
    """EmptyStatement : SEMICOLON"""
    p[0] = ";"

def p_LabeledStatement(p):
    """LabeledStatement : IDENTIFIER COLON Statement"""
    p[0] = p[1] + ":" + p[3]    

def p_LabeledStatementNoShortIf(p):
    """LabeledStatementNoShortIf : IDENTIFIER COLON StatementNoShortIf"""
    p[0] = p[1] + ":" + p[3]    

def p_ExpressionStatement(p):
    """ExpressionStatement : StatementExpression SEMICOLON"""
    p[0] = p[1] + ";"

def p_StatementExpression(p):
    """StatementExpression : Assignment
    | PreIncrementExpression
    | PreDecrementExpression
    | PostIncrementExpression
    | PostDecrementExpression
    | MethodInvocation
    | ClassInstanceCreationExpression"""
    p[0] = p[1]    

def p_IfThenStatement(p):
    """IfThenStatement : IF LEFT_PAREN Expression RIGHT_PAREN Statement"""
    p[0] = "if (" + p[3] + ")" + p[5]

def p_IfThenElseStatement(p):
    """IfThenElseStatement : IF LEFT_PAREN Expression RIGHT_PAREN Statement ELSE Statement"""
    p[0] = "if (" + p[3] + ")" + p[5] + "else" + p[7]

def p_IfThenElseStatementNoShortIf(p):
    """IfThenElseStatementNoShortIf : IF LEFT_PAREN Expression RIGHT_PAREN StatementNoShortIf ELSE StatementNoShortIf"""
    p[0] = "if (" + p[3] + ")" + p[5] + "else" + p[7]

def p_AssertStatement(p):
    """AssertStatement : ASSERT Expression SEMICOLON
    | ASSERT Expression COLON Expression SEMICOLON"""
    if p[3] == ":":
        p[0] = "assert " + p[2] + " : " + p[4] + ";"
    else:
        p[0] = "assert " + p[2] + ";"

def p_SwitchStatement(p):
    """SwitchStatement : SWITCH LEFT_PAREN Expression RIGHT_PAREN SwitchBlock"""
    p[0] = "switch (" + p[3] + ")" + p[5]

def p_SwitchBlock(p):
    """SwitchBlock : LEFT_BRACE SwitchBlockStatementGroup RIGHT_BRACE
    | LEFT_BRACE SwitchLabel RIGHT_BRACE"""
    p[0] = "{" + p[2] + "}"

def p_AlphaSwitchRule(p):
    """AlphaSwitchRule : SwitchRule AlphaSwitchRule
    | empty"""
    if p[1]:
        p[0] = p[1] + p[2]
    else:
        p[0] = ""

def p_AlphaSwitchBlockStatementGroup(p):
    """AlphaSwitchBlockStatementGroup : SwitchBlockStatementGroup AlphaSwitchBlockStatementGroup
    | empty"""
    if p[1]:
        p[0] = p[1] + p[2]
    else:
        p[0] = ""

def p_AlphaSwitchLabelColon(p):
    """AlphaSwitchLabelColon : SwitchLabel COLON AlphaSwitchLabelColon
    | empty"""
    if p[1]:
        p[0] = p[1] + p[2]
    else:
        p[0] = ""

def p_SwitchRule(p):
    """SwitchRule : SwitchLabel ARROW Expression SEMICOLON
    | SwitchLabel ARROW Block
    | SwitchLabel ARROW ThrowStatement"""
    if p[3] == "{":
        p[0] = p[1] + " -> " + p[3]
    elif p[3] == "throw":
        p[0] = p[1] + " -> " + p[3] + p[4] + ";"        
    else:
        p[0] = p[1] + " -> " + p[3] + ";"

def p_SwitchBlockStatementGroup(p):
    """SwitchBlockStatementGroup : SwitchLabel COLON AlphaSwitchLabelColon BlockStatements"""
    p[0] = p[1] + p[2]  


def p_SwitchLabel(p):
    """SwitchLabel : CASE ConstantExpression COLON
    | DEFAULT COLON"""
    if p[1] == "case":
        p[0] = "case " + p[2] + ":"
    else:
        p[0] = "default:"

def p_AlphaCommaCaseConstant(p):
    """AlphaCommaCaseConstant : COMMA CaseConstant AlphaCommaCaseConstant
    | empty"""
    if p[1]:
        p[0] = p[1] + p[2] + p[3]
    else:
        p[0] = ""

def p_CaseConstant(p):
    """CaseConstant : ConstantExpression"""
    p[0] = p[1]

def p_WhileStatement(p):
    """WhileStatement : WHILE LEFT_PAREN Expression RIGHT_PAREN Statement"""
    p[0] = "while (" + p[3] + ")" + p[5]

def p_WhileStatementNoShortIf(p):
    """WhileStatementNoShortIf : WHILE LEFT_PAREN Expression RIGHT_PAREN StatementNoShortIf"""
    p[0] = "while (" + p[3] + ")" + p[5]

def p_DoStatement(p):
    """DoStatement : DO Statement WHILE LEFT_PAREN Expression RIGHT_PAREN SEMICOLON"""
    p[0] = "do" + p[2] + "while (" + p[5] + ");"        

def p_ForStatement(p):
    """ForStatement : BasicForStatement
    | EnhancedForStatement"""
    p[0] = p[1]

def p_ForStatementNoShortIf(p):
    """ForStatementNoShortIf : BasicForStatementNoShortIf
    | EnhancedForStatementNoShortIf"""
    p[0] = p[1]

def p_BasicForStatement(p):
    """BasicForStatement : FOR LEFT_PAREN ForInit SEMICOLON Expression SEMICOLON ForUpdate RIGHT_PAREN Statement"""
    p[0] = "for (" + p[3] + ";" + p[5] + ";" + p[7] + ")" + p[9]

def p_BetaForInit(p):
    """BetaForInit : ForInit
    | empty"""
    p[0] = p[1]

def p_BetaExpression(p):
    """BetaExpression : Expression
    | empty"""
    p[0] = p[1]

def p_BetaForUpdate(p):
    """BetaForUpdate : ForUpdate
    | empty"""
    p[0] = p[1]

def p_BasicForStatementNoShortIf(p):
    """BasicForStatementNoShortIf : FOR LEFT_PAREN ForInit SEMICOLON Expression SEMICOLON ForUpdate RIGHT_PAREN StatementNoShortIf"""
    p[0] = "for (" + p[3] + ";" + p[5] + ";" + p[7] + ")" + p[9]

def p_ForInit(p):
    """ForInit : StatementExpressionList
    | LocalVariableDeclaration"""
    p[0] = p[1]

def p_ForUpdate(p):
    """ForUpdate : StatementExpressionList"""
    p[0] = p[1]

def p_StatementExpressionList(p):
    """StatementExpressionList : StatementExpression AlphaCommaStatementExpression"""
    p[0] = p[1] + p[2]

def p_AlphaCommaStatementExpression(p):
    """AlphaCommaStatementExpression : COMMA StatementExpression AlphaCommaStatementExpression
    | empty"""
    if p[1]:
        p[0] = p[1] + p[2] + p[3]
    else:
        p[0] = ""

def p_EnhancedForStatement(p):
    """EnhancedForStatement : FOR LEFT_PAREN VariableModifier Type IDENTIFIER COLON Expression RIGHT_PAREN Statement"""
    p[0] = "for (" + p[3] + p[4] + p[5] + ":" + p[7] + ")" + p[9]

def p_EnhancedForStatementNoShortIf(p):
    """EnhancedForStatementNoShortIf : FOR LEFT_PAREN VariableModifier Type IDENTIFIER COLON Expression RIGHT_PAREN StatementNoShortIf"""
    p[0] = "for (" + p[3] + p[4] + p[5] + ":" + p[7] + ")" + p[9]

def p_BreakStatement(p):
    """BreakStatement : BREAK BetaIdentifier SEMICOLON"""
    p[0] = "break" + p[2] + ";"

def p_BetaIdentifier(p):
        """BetaIdentifier : IDENTIFIER
        | empty"""
        p[0] = p[1]

def p_YieldStatement(p):
    """YieldStatement : YIELD Expression SEMICOLON
    | YIELD BetaExpression SEMICOLON"""
    p[0] = "yield " + p[2] + ";"

def p_ContinueStatement(p):
    """ContinueStatement : CONTINUE BetaIdentifier SEMICOLON"""
    p[0] = "continue" + p[2] + ";"

def p_ReturnStatement(p):
    """ReturnStatement : RETURN BetaExpression SEMICOLON"""
    p[0] = "return " + p[2] + ";"

def p_ThrowStatement(p):
    """ThrowStatement : THROW Expression SEMICOLON"""
    p[0] = "throw " + p[2] + ";"

def p_SynchronizedStatement(p):
    """SynchronizedStatement : SYNCHRONIZED LEFT_PAREN Expression RIGHT_PAREN Block"""
    p[0] = "synchronized (" + p[3] + ")" + p[5]

def p_TryStatement(p):
    """TryStatement : TRY Block Catches"""
    p[0] = "try" + p[2] + p[3]

def p_BetaCatches(p):
    """BetaCatches : Catches
    | empty"""
    p[0] = p[1]


def p_Catches(p):
    """Catches : CatchClause AlphaCatchClause"""
    p[0] = p[1] + p[2]

def p_AlphaCatchClause(p):
    """AlphaCatchClause : CatchClause AlphaCatchClause
    | empty"""
    if p[1]:
        p[0] = p[1] + p[2]
    else:
        p[0] = ""

def p_CatchClause(p):
    """CatchClause : CATCH LEFT_PAREN FormalParameter RIGHT_PAREN Block"""
    p[0] = "catch (" + p[3] + ")" + p[5]

def p_CatchFormalParameter(p):
    """CatchFormalParameter : CatchType IDENTIFIER"""
    p[0] = p[1] + p[2]

def p_CatchType(p):
    """CatchType : Type"""
    p[0] = p[1] 

def p_AlphaPipeCatchType(p):
    """AlphaPipeCatchType : BAR CatchType AlphaPipeCatchType
    | empty"""
    if p[1]:
        p[0] = p[1] + p[2] + p[3]
    else:
        p[0] = ""

def p_Finally(p):
    """Finally : FINALLY Block"""
    p[0] = "finally" + p[2]

def p_TryWithResourcesStatement(p):
    """TryWithResourcesStatement : TRY ResourceSpecification Block Catches BetaFinally"""
    p[0] = "try" + p[2] + p[3] + p[4] + p[5]

def p_BetaFinally(p):
    """BetaFinally : Finally
    | empty"""
    p[0] = p[1]

def p_ResourceSpecification(p):
    """ResourceSpecification : LEFT_PAREN ResourceList BetaSemiColon RIGHT_PAREN"""
    p[0] = "(" + p[2] + ";)"

def p_BetaSemiColon(p):
    """BetaSemiColon : SEMICOLON
    | empty"""
    p[0] = p[1]

def p_ResourceList(p):
    """ResourceList : Resource AlphaSemiColonResource"""
    p[0] = p[1] + p[2]

def p_AlphaSemiColonResource(p):
    """AlphaSemiColonResource : SEMICOLON Resource AlphaSemiColonResource
    | empty"""
    if p[1]:
        p[0] = p[1] + p[2] + p[3]
    else:
        p[0] = ""

def p_Resource(p):
    """Resource : LocalVariableDeclaration
    | VariableAccess"""
    p[0] = p[1]

def p_Pattern(p):
    """Pattern : TypePattern"""
    p[0] = p[1]

def p_TypePattern(p):
    """TypePattern : LocalVariableDeclaration"""
    p[0] = p[1]   


# Productions from §15 (Blocks, Statements, and Patterns) 

def p_VaraibleAccess(p):
    """VariableAccess : ExpressionName
    | FieldAccess"""
    p[0] = p[1]
        
# Productions from §15 (Expressions) 

def p_Primary(p):
    """Primary : PrimaryNoNewArray
    | ArrayCreationExpression"""
    p[0] = p[1]

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
    if p[1] == "this":
        p[0] = "this"
    elif p[1] == "(":
        p[0] = "(" + p[2] + ")"
    elif p[1] == "new":
        p[0] = p[1] + p[2]
    else:
        p[0] = p[1]

def p_ClassLiteral(p):
    """ClassLiteral : IDENTIFIER AlphaDotIdentifier AlphaSquareBrackets DOT CLASS
    | Type AlphaSquareBrackets DOT CLASS
    | VOID DOT CLASS"""
    if p[1] == "void":
        p[0] = "void.class"
    elif p[1] == "boolean":
        p[0] = "boolean.class"
    else:
        p[0] = p[1] + p[2] + ".class"

def p_AlphaSquareBrackets(p):
    """AlphaSquareBrackets : 
    | LEFT_BRACKET RIGHT_BRACKET AlphaSquareBrackets"""
    if len(p) == 2:
        p[0] = ""
    else:
        p[0] = "[]" + p[3]        

def p_ClassInstanceCreationExpression(p):
    """ClassInstanceCreationExpression : UnqualifiedClassInstanceCreationExpression
    | ExpressionName DOT UnqualifiedClassInstanceCreationExpression
    | Primary DOT UnqualifiedClassInstanceCreationExpression"""
    if len(p) == 2:
        p[0] = p[1]
    elif len(p) == 4:
        p[0] = p[1] + "." + p[3]

def p_UnqualifiedClassInstanceCreationExpression(p):
    """UnqualifiedClassInstanceCreationExpression : NEW BetaTypeArguments ClassOrInterfaceTypeToInstantiate LEFT_PAREN BetaArgumentList RIGHT_PAREN BetaClassBody
    | NEW BetaTypeArguments ClassOrInterfaceTypeToInstantiate LEFT_PAREN RIGHT_PAREN BetaClassBody"""
    if len(p) == 7:
        p[0] = "new " + p[2] + p[3] + "(" + p[5] + ")" + p[6]
    else:
        p[0] = "new " + p[2] + p[3] + "()" + p[6]

def p_ClassOrInterfaceTypeToInstantiate(p):
    """ClassOrInterfaceTypeToInstantiate : IDENTIFIER AlphaDotIdentifier BetaTypeArgumentsOrDiamond"""
    p[0] = p[1] + p[2] + p[3] 


def p_BetaTypeArgumentsOrDiamond(p):
    """BetaTypeArgumentsOrDiamond : TypeArgumentsOrDiamond
    | empty"""
    p[0] = p[1]    

def p_TypeArgumentsOrDiamond(p):
    """TypeArgumentsOrDiamond : TypeArguments
    | LESS GREATER"""
    if len(p) == 2:
        p[0] = p[1]
    else:
        p[0] = "<>"

def p_FieldAccess(p):
    """FieldAccess : Primary DOT IDENTIFIER
    | SUPER DOT IDENTIFIER
    | IDENTIFIER AlphaDotIdentifier DOT SUPER DOT IDENTIFIER"""
    if len(p) == 4:
        p[0] = p[1] + "." + p[3]
    else:
        p[0] = p[1] + "." + p[3] + "." + p[5]

def p_ArrayAccess(p):
    """ArrayAccess : ExpressionName LEFT_BRACKET Expression RIGHT_BRACKET
    | PrimaryNoNewArray LEFT_BRACKET Expression RIGHT_BRACKET"""
    if len(p) == 5:
        p[0] = p[1] + "[" + p[3] + "]"
    else:
        p[0] = p[1] + "[" + p[3] + "]"          

def p_MethodInvocation(p):
    """MethodInvocation : IDENTIFIER LEFT_PAREN BetaArgumentList RIGHT_PAREN
    | IDENTIFIER AlphaDotIdentifier DOT BetaTypeArguments IDENTIFIER LEFT_PAREN BetaArgumentList RIGHT_PAREN
    | ExpressionName DOT BetaTypeArguments IDENTIFIER LEFT_PAREN BetaArgumentList RIGHT_PAREN
    | Primary DOT BetaTypeArguments IDENTIFIER LEFT_PAREN BetaArgumentList RIGHT_PAREN
    | SUPER DOT BetaTypeArguments IDENTIFIER LEFT_PAREN BetaArgumentList RIGHT_PAREN
    | IDENTIFIER AlphaDotIdentifier DOT SUPER DOT BetaTypeArguments IDENTIFIER LEFT_PAREN BetaArgumentList RIGHT_PAREN"""
    if len(p) == 5:
        p[0] = p[1] + "(" + p[3] + ")"
    else:
        p[0] = p[1] + "." + p[3] + p[4] + "(" + p[6] + ")"

def p_ArgumentList(p):
    """ArgumentList : Expression AlphaCommaExpression"""
    p[0] = p[1] + p[2]

def p_AlphaCommaExpression(p):
    """AlphaCommaExpression : 
    | COMMA Expression AlphaCommaExpression"""
    if len(p) == 2:
        p[0] = ""
    else:
        p[0] = "," + p[2] + p[3]

def p_MethodReference(p):
    """MethodReference : ExpressionName COLON_COLON BetaTypeArguments IDENTIFIER
    | Primary COLON_COLON BetaTypeArguments IDENTIFIER
    | ReferenceType COLON_COLON BetaTypeArguments IDENTIFIER
    | SUPER COLON_COLON BetaTypeArguments IDENTIFIER
    | IDENTIFIER AlphaDotIdentifier DOT SUPER COLON_COLON BetaTypeArguments IDENTIFIER
    | ClassType COLON_COLON BetaTypeArguments NEW
    | ArrayType COLON_COLON NEW"""
    if len(p) == 5:
        p[0] = p[1] + "::" + p[3] + p[4]
    elif len(p) == 4:
        p[0] = p[1] + "::" + p[3]
    else:
        p[0] = p[1] + "::new"

def p_ArrayCreationExpression(p):
    """ArrayCreationExpression : NEW PrimitiveType DimExprs BetaDims
    | NEW ClassType DimExprs BetaDims
    | NEW PrimitiveType Dims ArrayInitializer
    | NEW ClassOrInterfaceTypeToInstantiate Dims ArrayInitializer"""
    if len(p) == 4:
        p[0] = "new " + p[2] + p[3] + p[4]
    else:
        p[0] = "new " + p[2] + p[3] + p[4]

def p_BetaDims(p):
    """BetaDims : Dims
    | empty"""
    p[0] = p[1]

def p_DimExprs(p):
    """DimExprs : DimExpr AlphaDimExpr"""
    p[0] = p[1] + p[2]

def p_AlphaDimExpr(p):
    """AlphaDimExpr : 
    | DimExpr AlphaDimExpr"""
    if len(p) == 2:
        p[0] = ""
    else:
        p[0] = p[1] + p[2]                    

def p_DimExpr(p):
    """DimExpr : RIGHT_BRACKET Expression LEFT_BRACKET"""
    p[0] = "[" + p[2] + "]"

def p_Expression(p):
    """Expression : LambdaExpression
    | AssignmentExpression"""
    p[0] = p[1]

def p_LambdaExpression(p):
    """LambdaExpression : LambdaParameters ARROW LambdaBody"""  
    p[0] = p[1] + "->" + p[3]

def p_LambdaParameters(p):
    """LambdaParameters : LEFT_PAREN BetaLambdaParameterList RIGHT_PAREN
    | IDENTIFIER"""
    if len(p) == 2:
        p[0] = p[1]
    else:
        p[0] = "(" + p[2] + ")"

def p_BetaLambdaParameterList(p):
    """BetaLambdaParameterList : LambdaParameterList
    | empty"""
    p[0] = p[1]

def p_LambdaParameterList(p):
    """LambdaParameterList : LambdaParameter AlphaCommaLambdaParameter
    | IDENTIFIER AlphaCommaIdentifier"""
    if len(p) == 3:
        p[0] = p[1] + p[2]
    else:
        p[0] = p[1] + p[2]

def p_AlphaCommaLambdaParameter(p):
    """AlphaCommaLambdaParameter : 
    | COMMA LambdaParameter AlphaCommaLambdaParameter"""
    if len(p) == 2:
        p[0] = ""
    else:
        p[0] = "," + p[2] + p[3]

def p_AlphaCommaIdentifier(p):
    """AlphaCommaIdentifier : 
    | COMMA IDENTIFIER AlphaCommaIdentifier"""
    if len(p) == 2:
        p[0] = ""
    else:
        p[0] = "," + p[2] + p[3]

def p_LambdaParameter(p):
    """LambdaParameter : AlphaVariableModifier LambdaParameterType VariableDeclaratorId
    | VariableArityParameter"""
    p[0] = p[1] + p[2] + p[3]    

def p_LambdaParameterType(p):
    """LambdaParameterType : Type
    | VAR"""
    p[0] = p[1]     

def p_LambdaBody(p):
    """LambdaBody : Expression
    | Block"""
    p[0] = p[1]

def p_AssignmentExpression(p):
    """AssignmentExpression : ConditionalExpression
    | Assignment"""
    p[0] = p[1]

def p_Assignment(p):
    """Assignment : LeftHandSide AssignmentOperator Expression"""
    p[0] = p[1] + p[2] + p[3]

def p_LeftHandSide(p):
    """LeftHandSide : ExpressionName
    | FieldAccess
    | ArrayAccess"""
    p[0] = p[1]

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
    p[0] = p[1]    

def p_ConditionalExpression(p):
    """ConditionalExpression : ConditionalOrExpression
    | ConditionalOrExpression QUESTION Expression COLON ConditionalExpression
    | ConditionalOrExpression QUESTION Expression COLON LambdaExpression"""
    if len(p) == 2:
        p[0] = p[1]
    else:
        p[0] = p[1] + "?" + p[3] + ":" + p[5]  
def p_ConditionalOrExpression(p):
    """ConditionalOrExpression : ConditionalAndExpression
    | ConditionalOrExpression BAR_BAR ConditionalAndExpression"""
    if len(p) == 2:
        p[0] = p[1]
    else:
        p[0] = p[1] + "||" + p[3]

def p_ConditionalAndExpression(p):
    """ConditionalAndExpression : InclusiveOrExpression
    | ConditionalAndExpression AMPERSAND_AMPERSAND InclusiveOrExpression"""
    if len(p) == 2:
        p[0] = p[1]
    else:
        p[0] = p[1] + "&&" + p[3]

def p_InclusiveOrExpression(p):
    """InclusiveOrExpression : ExclusiveOrExpression
    | InclusiveOrExpression BAR ExclusiveOrExpression"""
    if len(p) == 2:
        p[0] = p[1]
    else:
        p[0] = p[1] + "|" + p[3]     

def p_ExclusiveOrExpression(p):
    """ExclusiveOrExpression : AndExpression
    | ExclusiveOrExpression CARET AndExpression"""
    if len(p) == 2:
        p[0] = p[1]
    else:
        p[0] = p[1] + "^" + p[3]      

def p_AndExpression(p):
    """AndExpression : EqualityExpression
    | AndExpression AMPERSAND EqualityExpression"""
    if len(p) == 2:
        p[0] = p[1]
    else:
        p[0] = p[1] + "&" + p[3]

def p_EqualityExpression(p):
    """EqualityExpression : RelationalExpression
    | EqualityExpression EQUAL_EQUAL RelationalExpression
    | EqualityExpression EXCLAMATION_EQUAL RelationalExpression"""
    if len(p) == 2:
        p[0] = p[1]
    else:
        p[0] = p[1] + p[2] + p[3]        

def p_RelationalExpression(p):
    """RelationalExpression : ShiftExpression
    | RelationalExpression LESS ShiftExpression
    | RelationalExpression GREATER ShiftExpression
    | RelationalExpression LESS_EQUAL ShiftExpression
    | RelationalExpression GREATER_EQUAL ShiftExpression
    | InstanceofExpression"""
    if len(p) == 2:
        p[0] = p[1]
    else:
        p[0] = p[1] + p[2] + p[3]

def p_InstanceofExpression(p):
    """InstanceofExpression : RelationalExpression INSTANCEOF ReferenceType"""
    p[0] = p[1] + "instanceof" + p[3]

def p_ShiftExpression(p):
    """ShiftExpression : AdditiveExpression
    | ShiftExpression LEFT_SHIFT AdditiveExpression
    | ShiftExpression RIGHT_SHIFT AdditiveExpression
    | ShiftExpression UNSIGNED_RIGHT_SHIFT AdditiveExpression"""
    if len(p) == 2:
        p[0] = p[1]
    else:
        p[0] = p[1] + p[2] + p[3]  

def p_AdditiveExpression(p):
    """AdditiveExpression : MultiplicativeExpression
    | AdditiveExpression PLUS MultiplicativeExpression
    | AdditiveExpression MINUS MultiplicativeExpression"""
    if len(p) == 2:
        p[0] = p[1]
    else:
        p[0] = p[1] + p[2] + p[3]       

def p_MultiplicativeExpression(p):
    """MultiplicativeExpression : UnaryExpression
    | MultiplicativeExpression STAR UnaryExpression
    | MultiplicativeExpression SLASH UnaryExpression
    | MultiplicativeExpression PERCENT UnaryExpression"""
    if len(p) == 2:
        p[0] = p[1]
    else:
        p[0] = p[1] + p[2] + p[3]    

def p_UnaryExpression(p):
    """UnaryExpression : PreIncrementExpression
    | PreDecrementExpression
    | PLUS UnaryExpression
    | MINUS UnaryExpression
    | UnaryExpressionNotPlusMinus"""
    if len(p) == 2:
        p[0] = p[1]
    else:
        p[0] = p[1] + p[2]     

def p_PreIncrementExpression(p):
    """PreIncrementExpression : PLUS_PLUS UnaryExpression"""
    p[0] = p[1] + p[2]

def p_DecrementExpression(p):
    """PreDecrementExpression : MINUS_MINUS UnaryExpression"""
    p[0] = p[1] + p[2]             

def p_UnaryExpressionNotPlusMinus(p):
    """UnaryExpressionNotPlusMinus : PostfixExpression
    | TILDE UnaryExpression
    | EXCLAMATION UnaryExpression
    | CastExpression
    | SwitchExpression"""
    if len(p) == 2:
        p[0] = p[1]
    else:
        p[0] = p[1] + p[2] + p[3]


def p_PostfixExpression(p):
    """PostfixExpression : Primary
    | ExpressionName
    | PostIncrementExpression
    | PostDecrementExpression"""
    p[0] = p[1]

def p_PostIncrementExpression(p):
    """PostIncrementExpression : PostfixExpression PLUS_PLUS"""
    p[0] = p[1] + p[2]


def p_PostDecrementExpression(p):
    """PostDecrementExpression : PostfixExpression MINUS_MINUS"""
    p[0] = p[1] + p[2]

def p_CastExpression(p):
    """CastExpression : LEFT_PAREN PrimitiveType RIGHT_PAREN UnaryExpression  
    | LEFT_PAREN ReferenceType AlphaAdditionalBound RIGHT_PAREN UnaryExpressionNotPlusMinus
    | LEFT_PAREN ReferenceType AlphaAdditionalBound RIGHT_PAREN LambdaExpression"""
    if len(p) == 5:
        p[0] = p[1] + p[2] + p[3] + p[4]
    else:
        p[0] = p[1] + p[2] + p[3] + p[4] + p[5] 

def p_SwitchExpression(p):
    """SwitchExpression : SWITCH LEFT_PAREN Expression RIGHT_PAREN SwitchBlock"""
    p[0] = p[1] + p[2] + p[3] + p[4] + p[5]

def p_ConstantExpression(p):
    """ConstantExpression : Expression"""
    p[0] = p[1]

def p_error(p):
    print("Syntax error in input!")


def p_InterfaceDeclaration(p):
    """InterfaceDeclaration : NormalInterfaceDeclaration"""
    p[0] = p[1]


def p_NormalInterfaceDeclaration(p):
    """NormalInterfaceDeclaration : AlphaClassModifier INTERFACE IDENTIFIER BetaTypeParameters BetaClassExtends BetaClassPermits InterfaceBody"""
    p[0] = "interface " + p[2] + p[3] + p[4] + p[5] + p[6] + p[7]


def p_InterfaceBody(p):
    """InterfaceBody : LEFT_BRACE AlphaInterfaceMemberDeclaration RIGHT_BRACE"""
    p[0] = "{" + p[2] + "}"


def p_AlphaInterfaceMemberDeclaration(p):
    """AlphaInterfaceMemberDeclaration : InterfaceMemberDeclaration AlphaInterfaceMemberDeclaration
    | empty"""
    if p[1]:
        p[0] = p[1] + p[2]
    else:
        p[0] = ""


def p_InterfaceMemberDeclaration(p):
    """InterfaceMemberDeclaration : ConstantDeclaration
    | InterfaceMethodDeclaration
    | SEMICOLON"""
    p[0] = p[1]


def p_InterfaceMethodDeclaration(p):
    """InterfaceMethodDeclaration : AlphaConstantModifier MethodHeader MethodBody"""
    p[0] = p[1] + p[2] + p[3] + "(" + p[5] + ")" + p[7] + p[8] + ";"


def p_ConstantDeclaration(p):
    """ConstantDeclaration : AlphaConstantModifier Type VariableDeclaratorList SEMICOLON"""
    p[0] = p[1] + p[2] + p[3] + ";"


def p_BetaArgumentList(p):
    """BetaArgumentList : ArgumentList
    | empty"""
    p[0] = p[1]

def p_BetaClassBody(p):
    """BetaClassBody : ClassBody
    | empty"""
    p[0] = p[1]




def p_AlphaConstantModifier(p):
    """AlphaConstantModifier : ConstantModifier AlphaConstantModifier
    | empty"""
    if p[1]:
        p[0] = p[1] + p[2]
    else:
        p[0] = ""


def p_ConstantModifier(p):
    """ConstantModifier : PUBLIC
    | STATIC
    | FINAL
    | ABSTRACT
    | DEFAULT
    | STRICTFP"""
    p[0] = p[1]


def p_ExpressionName(p):
    """ExpressionName : IDENTIFIER AlphaDotIdentifier"""
    p[0] = p[1]

def p_BlockStatement(p):
    """BlockStatement : LocalClassOrInterfaceDeclaration
    | LocalVariableDeclarationStatement
    | Statement"""
    p[0] = p[1]




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
    p[0] = p[1]

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

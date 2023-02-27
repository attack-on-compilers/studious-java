parser grammar Java8Parser;

options {
    tokenVocab=Java8Lexer;
}

/************Productions from §3 (Lexical Structure)************/

literal
	:	IntegerLiteral
	|	FloatingPointLiteral
	|	BooleanLiteral
	|	CharacterLiteral
	|	StringLiteral
	|	NullLiteral
	;

/************Productions from §4 (Types, Values, and Variables)************/

type0
	:	primitiveType
	|	referenceType
	;

primitiveType
	:	annotation* numericType
	|	annotation* 'boolean'
	;

numericType
	:	integralType
	|	floatingPointType
	;

integralType
	:	'byte'
	|	'short'
	|	'int'
	|	'long'
	|	'char'
	;

floatingPointType
	:	'float'
	|	'double'
	;

referenceType
	:	classOrInterfaceType
	|	typeVariable
	|	arrayType
	;

classOrInterfaceType
	:	( annotation* Identifier typeArguments? )
		( '.' annotation* Identifier typeArguments? )*
	;

classType
	:	annotation* Identifier typeArguments?
	|	classOrInterfaceType '.' annotation* Identifier typeArguments?
	;

interfaceType
	:	classType
	;

typeVariable
	:	annotation* Identifier
	;

arrayType
	:	primitiveType dims
	|	classOrInterfaceType dims
	|	typeVariable dims
	;

dims
	:	annotation* '[' ']' (annotation* '[' ']')*
	;

typeParameter
	:	typeParameterModifier* Identifier typeBound?
	;

typeParameterModifier
	:	annotation
	;

typeBound
	:	'extends' typeVariable
	|	'extends' classOrInterfaceType additionalBound*
	;

additionalBound
	:	'&' interfaceType
	;

typeArguments
	:	'<' typeArgumentList '>'
	;

typeArgumentList
	:	typeArgument (',' typeArgument)*
	;

typeArgument
	:	referenceType
	|	wildcard
	;

wildcard
	:	annotation* '?' wildcardBounds?
	;

wildcardBounds
	:	'extends' referenceType
	|	'super' referenceType
	;


/************Productions from §6 (Names)************/

typeName
	:	Identifier
	|	packageOrTypeName '.' Identifier
	;

packageOrTypeName
	:	Identifier
	|	packageOrTypeName '.' Identifier
	;

expressionName
	:	Identifier
	|	ambiguousName '.' Identifier
	;

methodName
	:	Identifier
	;

packageName
	:	Identifier
	|	packageName '.' Identifier
	;

ambiguousName
	:	Identifier
	|	ambiguousName '.' Identifier
	;


/*************Productions from §7 (Packages)*************/

compilationUnit
	:	packageDeclaration? importDeclaration* typeDeclaration* EOF
	;

packageDeclaration
	:	packageModifier* 'package' Identifier ( '.' Identifier )* ';'
	;

packageModifier
	:	annotation
	;

importDeclaration
	:	singleTypeImportDeclaration
	|	typeImportOnDemandDeclaration
	|	singleStaticImportDeclaration
	|	staticImportOnDemandDeclaration
	;

singleTypeImportDeclaration
	:	'import' typeName ';'
	;

typeImportOnDemandDeclaration
	:	'import' packageOrTypeName '.' '*' ';'
	;

singleStaticImportDeclaration
	:	'import' 'static' typeName '.' Identifier ';'
	;

staticImportOnDemandDeclaration
	:	'import' 'static' typeName '.' '*' ';'
	;

typeDeclaration
	:	classDeclaration
	|	interfaceDeclaration
	|	';'
	;


/*************Productions from §8 (Classes)*************/

classDeclaration
	:	normalClassDeclaration
	|	enumDeclaration
	;

normalClassDeclaration
	:	classModifier* 'class' Identifier typeParameters? superclass? superinterfaces? classBody
	;

classModifier
	:	annotation
	|	'public'
	|	'protected'
	|	'private'
	|	'abstract'
	|	'static'
	|	'final'
	|	'strictfp'
	;

typeParameters
	:	'<' typeParameterList '>'
	;

typeParameterList
	:	typeParameter (',' typeParameter)*
	;

superclass
	:	'extends' classType
	;

superinterfaces
	:	'implements' interfaceTypeList
	;

interfaceTypeList
	:	interfaceType (',' interfaceType)*
	;

classBody
	:	'{' classBodyDeclaration* '}'
	;

classBodyDeclaration
	:	classMemberDeclaration
	|	instanceInitializer
	|	staticInitializer
	|	constructorDeclaration
	;

classMemberDeclaration
	:	fieldDeclaration
	|	methodDeclaration
	|	classDeclaration
	|	interfaceDeclaration
	|	';'
	;

fieldDeclaration
	:	fieldModifier* unannType variableDeclaratorList ';'
	;

fieldModifier
	:	annotation
	|	'public'
	|	'protected'
	|	'private'
	|	'static'
	|	'final'
	|	'transient'
	|	'volatile'
	;

variableDeclaratorList
	:	variableDeclarator (',' variableDeclarator)*
	;

variableDeclarator
	:	variableDeclaratorId ('=' variableInitializer)?
	;

variableDeclaratorId
	:	Identifier dims?
	;

variableInitializer
	:	expression
	|	arrayInitializer
	;

unannType
	:	unannPrimitiveType
	|	unannReferenceType
	;

unannPrimitiveType
	:	numericType
	|	'boolean'
	;

unannReferenceType
	:	unannClassOrInterfaceType
	|	unannTypeVariable
	|	unannArrayType
	;

unannClassOrInterfaceType
	:	( Identifier typeArguments? ) ( '.' annotation* Identifier typeArguments? )*
	;

unannClassType
	:	Identifier typeArguments?
	|	unannClassOrInterfaceType '.' annotation* Identifier typeArguments?
	;

unannInterfaceType
	:	unannClassType
	;

unannTypeVariable
	:	Identifier
	;

unannArrayType
	:	unannPrimitiveType dims
	|	unannClassOrInterfaceType dims
	|	unannTypeVariable dims
	;

methodDeclaration
	:	methodModifier* methodHeader methodBody
	;

methodModifier
	:	annotation
	|	'public'
	|	'protected'
	|	'private'
	|	'abstract'
	|	'static'
	|	'final'
	|	'synchronized'
	|	'native'
	|	'strictfp'
	;

methodHeader
	:	result methodDeclarator throws0?
	|	typeParameters annotation* result methodDeclarator throws0?
	;

result
	:	unannType
	|	'void'
	;

methodDeclarator
	:	Identifier '(' formalParameterList? ')' dims?
	;

formalParameterList
	:	receiverParameter
	|	formalParameters ',' lastFormalParameter
	|	lastFormalParameter
	;

formalParameters
	:	formalParameter (',' formalParameter)*
	|	receiverParameter (',' formalParameter)*
	;

formalParameter
	:	variableModifier* unannType variableDeclaratorId
	;

variableModifier
	:	annotation
	|	'final'
	;

lastFormalParameter
	:	variableModifier* unannType annotation* '...' variableDeclaratorId
	|	formalParameter
	;

receiverParameter
	:	annotation* unannType (Identifier '.')? 'this'
	;

throws0
	:	'throws' exceptionTypeList
	;

exceptionTypeList
	:	exceptionType (',' exceptionType)*
	;

exceptionType
	:	classType
	|	typeVariable
	;

methodBody
	:	block
	|	';'
	;

instanceInitializer
	:	block
	;

staticInitializer
	:	'static' block
	;

constructorDeclaration
	:	constructorModifier* constructorDeclarator throws0? constructorBody
	;

constructorModifier
	:	annotation
	|	'public'
	|	'protected'
	|	'private'
	;

constructorDeclarator
	:	typeParameters? simpleTypeName '(' formalParameterList? ')'
	;

simpleTypeName
	:	Identifier
	;

constructorBody
	:	'{' explicitConstructorInvocation? blockStatements? '}'
	;

explicitConstructorInvocation
	:	typeArguments? 'this' '(' argumentList? ')' ';'
	|	typeArguments? 'super' '(' argumentList? ')' ';'
	|	expressionName '.' typeArguments? 'super' '(' argumentList? ')' ';'
	|	primary '.' typeArguments? 'super' '(' argumentList? ')' ';'
	;

enumDeclaration
	:	classModifier* 'enum' Identifier superinterfaces? enumBody
	;

enumBody
	:	'{' enumConstantList? ','? enumBodyDeclarations? '}'
	;

enumConstantList
	:	enumConstant (',' enumConstant)*
	;

enumConstant
	:	enumConstantModifier* Identifier ('(' argumentList? ')')? classBody?
	;

enumConstantModifier
	:	annotation
	;

enumBodyDeclarations
	:	';' classBodyDeclaration*
	;


/*******************Productions from §9 (Interfaces)*******************/

interfaceDeclaration
	:	normalInterfaceDeclaration
	|	annotationTypeDeclaration
	;

normalInterfaceDeclaration
	:	interfaceModifier* 'interface' Identifier typeParameters? extendsInterfaces? interfaceBody
	;

interfaceModifier
	:	annotation
	|	'public'
	|	'protected'
	|	'private'
	|	'abstract'
	|	'static'
	|	'strictfp'
	;

extendsInterfaces
	:	'extends' interfaceTypeList
	;

interfaceBody
	:	'{' interfaceMemberDeclaration* '}'
	;

interfaceMemberDeclaration
	:	constantDeclaration
	|	interfaceMethodDeclaration
	|	classDeclaration
	|	interfaceDeclaration
	|	';'
	;

constantDeclaration
	:	constantModifier* unannType variableDeclaratorList ';'
	;

constantModifier
	:	annotation
	|	'public'
	|	'static'
	|	'final'
	;

interfaceMethodDeclaration
	:	interfaceMethodModifier* methodHeader methodBody
	;

interfaceMethodModifier
	:	annotation
	|	'public'
	|	'abstract'
	|	'default'
	|	'static'
	|	'strictfp'
	;

annotationTypeDeclaration
	:	interfaceModifier* '@' 'interface' Identifier annotationTypeBody
	;

annotationTypeBody
	:	'{' annotationTypeMemberDeclaration* '}'
	;

annotationTypeMemberDeclaration
	:	annotationTypeElementDeclaration
	|	constantDeclaration
	|	classDeclaration
	|	interfaceDeclaration
	|	';'
	;

annotationTypeElementDeclaration
	:	annotationTypeElementModifier* unannType Identifier '(' ')' dims? defaultValue? ';'
	;

annotationTypeElementModifier
	:	annotation
	|	'public'
	|	'abstract'
	;

defaultValue
	:	'default' elementValue
	;

annotation
	:	normalAnnotation
	|	markerAnnotation
	|	singleElementAnnotation
	;

normalAnnotation
	:	'@' typeName '(' elementValuePairList? ')'
	;

elementValuePairList
	:	elementValuePair (',' elementValuePair)*
	;

elementValuePair
	:	Identifier '=' elementValue
	;

elementValue
	:	conditionalExpression
	|	elementValueArrayInitializer
	|	annotation
	;

elementValueArrayInitializer
	:	'{' elementValueList? ','? '}'
	;

elementValueList
	:	elementValue (',' elementValue)*
	;

markerAnnotation
	:	'@' typeName
	;

singleElementAnnotation
	:	'@' typeName '(' elementValue ')'
	;


/*******************Productions from §10 (Arrays)*******************/

arrayInitializer
	:	'{' variableInitializerList? ','? '}'
	;

variableInitializerList
	:	variableInitializer (',' variableInitializer)*
	;


/*******************Productions from §14 (Blocks and Statements)*******************/

block
	:	'{' blockStatements? '}'
	;

blockStatements
	:	blockStatement blockStatement*
	;

blockStatement
	:	localVariableDeclarationStatement
	|	classDeclaration
	|	statement
	;

localVariableDeclarationStatement
	:	localVariableDeclaration ';'
	;

localVariableDeclaration
	:	variableModifier* unannType variableDeclaratorList
	;

statement
	:	statementWithoutTrailingSubstatement
	|	labeledStatement
	|	ifThenStatement
	|	ifThenElseStatement
	|	whileStatement
	|	forStatement
	;

statementNoShortIf
	:	statementWithoutTrailingSubstatement
	|	labeledStatementNoShortIf
	|	ifThenElseStatementNoShortIf
	|	whileStatementNoShortIf
	|	forStatementNoShortIf
	;

statementWithoutTrailingSubstatement
	:	block
	|	emptyStatement
	|	expressionStatement
	|	assertStatement
	|	switchStatement
	|	doStatement
	|	breakStatement
	|	continueStatement
	|	returnStatement
	|	synchronizedStatement
	|	throwStatement
	|	tryStatement
	;

emptyStatement
	:	';'
	;

labeledStatement
	:	Identifier ':' statement
	;

labeledStatementNoShortIf
	:	Identifier ':' statementNoShortIf
	;

expressionStatement
	:	statementExpression ';'
	;

statementExpression
	:	assignment
	|	preIncrementExpression
	|	preDecrementExpression
	|	postIncrementExpression
	|	postDecrementExpression
	|	methodInvocation
	|	classInstanceCreationExpression
	;

ifThenStatement
	:	'if' '(' expression ')' statement
	;

ifThenElseStatement
	:	'if' '(' expression ')' statementNoShortIf 'else' statement
	;

ifThenElseStatementNoShortIf
	:	'if' '(' expression ')' statementNoShortIf 'else' statementNoShortIf
	;

assertStatement
	:	'assert' expression ';'
	|	'assert' expression ':' expression ';'
	;

switchStatement
	:	'switch' '(' expression ')' switchBlock
	;

switchBlock
	:	'{' switchBlockStatementGroup* switchLabel* '}'
	;

switchBlockStatementGroup
	:	switchLabels blockStatements
	;

switchLabels
	:	switchLabel switchLabel*
	;

switchLabel
	:	'case' constantExpression ':'
	|	'case' enumConstantName ':'
	|	'default' ':'
	;

enumConstantName
	:	Identifier
	;

whileStatement
	:	'while' '(' expression ')' statement
	;

whileStatementNoShortIf
	:	'while' '(' expression ')' statementNoShortIf
	;

doStatement
	:	'do' statement 'while' '(' expression ')' ';'
	;

forStatement
	:	basicForStatement
	|	enhancedForStatement
	;

forStatementNoShortIf
	:	basicForStatementNoShortIf
	|	enhancedForStatementNoShortIf
	;

basicForStatement
	:	'for' '(' forInit? ';' expression? ';' forUpdate? ')' statement
	;

basicForStatementNoShortIf
	:	'for' '(' forInit? ';' expression? ';' forUpdate? ')' statementNoShortIf
	;

forInit
	:	statementExpressionList
	|	localVariableDeclaration
	;

forUpdate
	:	statementExpressionList
	;

statementExpressionList
	:	statementExpression (',' statementExpression)*
	;

enhancedForStatement
	:	'for' '(' variableModifier* unannType variableDeclaratorId ':' expression ')' statement
	;

enhancedForStatementNoShortIf
	:	'for' '(' variableModifier* unannType variableDeclaratorId ':' expression ')' statementNoShortIf
	;

breakStatement
	:	'break' Identifier? ';'
	;

continueStatement
	:	'continue' Identifier? ';'
	;

returnStatement
	:	'return' expression? ';'
	;

throwStatement
	:	'throw' expression ';'
	;

synchronizedStatement
	:	'synchronized' '(' expression ')' block
	;

tryStatement
	:	'try' block catches
	|	'try' block catches? finally0
	|	tryWithResourcesStatement
	;

catches
	:	catchClause catchClause*
	;

catchClause
	:	'catch' '(' catchFormalParameter ')' block
	;

catchFormalParameter
	:	variableModifier* catchType variableDeclaratorId
	;

catchType
	:	unannClassType ('|' classType)*
	;

finally0
	:	'finally' block
	;

tryWithResourcesStatement
	:	'try' resourceSpecification block catches? finally0?
	;

resourceSpecification
	:	'(' resourceList ';'? ')'
	;

resourceList
	:	resource (';' resource)*
	;

resource
	:	variableModifier* unannType variableDeclaratorId '=' expression
	;


/*******************Productions from §15 (Expressions)*******************/

primary
	:	( primaryNoNewArray0 | arrayCreationExpression ) ( primaryNoNewArray1 )*
	;

primaryNoNewArray
	:	literal
	|	typeName ('[' ']')* '.' 'class'
	|	'void' '.' 'class'
	|	'this'
	|	typeName '.' 'this'
	|	'(' expression ')'
	|	classInstanceCreationExpression
	|	fieldAccess
	|	arrayAccess
	|	methodInvocation
	|	methodReference
	;

primaryNoNewArray2
	:	literal
	|	typeName ('[' ']')* '.' 'class'
	|	'void' '.' 'class'
	|	'this'
	|	typeName '.' 'this'
	|	'(' expression ')'
	|	classInstanceCreationExpression
	|	fieldAccess
	|	methodInvocation
	|	methodReference
	;

primaryNoNewArray1
	:	classInstanceCreationExpression0
	|	fieldAccess0
	|	arrayAccess0
	|	methodInvocation0
	|	methodReference0
	;

primaryNoNewArray3
	:	classInstanceCreationExpression0
	|	fieldAccess0
	|	methodInvocation0
	|	methodReference0
	;

primaryNoNewArray0
	:	literal
	|	typeName ('[' ']')* '.' 'class'
	|	unannPrimitiveType ('[' ']')* '.' 'class'
	|	'void' '.' 'class'
	|	'this'
	|	typeName '.' 'this'
	|	'(' expression ')'
	|	classInstanceCreationExpression1
	|	fieldAccess1
	|	arrayAccess1
	|	methodInvocation1
	|	methodReference1
	;

primaryNoNewArray4
	:	literal
	|	typeName ('[' ']')* '.' 'class'
	|	unannPrimitiveType ('[' ']')* '.' 'class'
	|	'void' '.' 'class'
	|	'this'
	|	typeName '.' 'this'
	|	'(' expression ')'
	|	classInstanceCreationExpression1
	|	fieldAccess1
	|	methodInvocation1
	|	methodReference1
	;

classInstanceCreationExpression
	:	unqualifiedClassInstanceCreationExpression
	|	expressionName '.' unqualifiedClassInstanceCreationExpression
	|	primary '.' unqualifiedClassInstanceCreationExpression
	;

unqualifiedClassInstanceCreationExpression
    :   'new' typeArguments? classOrInterfaceTypeToInstantiate '(' argumentList? ')' classBody?
    ;

classOrInterfaceTypeToInstantiate
    :   annotation* Identifier ('.' annotation* Identifier)* typeArgumentsOrDiamond?
    ;

classInstanceCreationExpression0
	:	'.' 'new' typeArguments? annotation* Identifier typeArgumentsOrDiamond? '(' argumentList? ')' classBody?
	;

classInstanceCreationExpression1
	:	'new' typeArguments? annotation* Identifier ('.' annotation* Identifier)* typeArgumentsOrDiamond? '(' argumentList? ')' classBody?
	|	expressionName '.' 'new' typeArguments? annotation* Identifier typeArgumentsOrDiamond? '(' argumentList? ')' classBody?
	;

typeArgumentsOrDiamond
	:	typeArguments
	|	'<' '>'
	;

fieldAccess
	:	primary '.' Identifier
	|	'super' '.' Identifier
	|	typeName '.' 'super' '.' Identifier
	;

fieldAccess0
	:	'.' Identifier
	;

fieldAccess1
	:	'super' '.' Identifier
	|	typeName '.' 'super' '.' Identifier
	;

arrayAccess
	:	( expressionName '[' expression ']' |	primaryNoNewArray2 '[' expression ']' )	( '[' expression ']' )*
	;

arrayAccess0
	:	( primaryNoNewArray3 '[' expression ']' ) ( '[' expression ']' )*
	;

arrayAccess1
	:	( expressionName '[' expression ']' |	primaryNoNewArray4 '[' expression ']' ) ( '[' expression ']' )*
	;

methodInvocation
	:	methodName '(' argumentList? ')'
	|	typeName '.' typeArguments? Identifier '(' argumentList? ')'
	|	expressionName '.' typeArguments? Identifier '(' argumentList? ')'
	|	primary '.' typeArguments? Identifier '(' argumentList? ')'
	|	'super' '.' typeArguments? Identifier '(' argumentList? ')'
	|	typeName '.' 'super' '.' typeArguments? Identifier '(' argumentList? ')'
	;

methodInvocation0
	:	'.' typeArguments? Identifier '(' argumentList? ')'
	;

methodInvocation1
	:	methodName '(' argumentList? ')'
	|	typeName '.' typeArguments? Identifier '(' argumentList? ')'
	|	expressionName '.' typeArguments? Identifier '(' argumentList? ')'
	|	'super' '.' typeArguments? Identifier '(' argumentList? ')'
	|	typeName '.' 'super' '.' typeArguments? Identifier '(' argumentList? ')'
	;

argumentList
	:	expression (',' expression)*
	;

methodReference
	:	expressionName '::' typeArguments? Identifier
	|	referenceType '::' typeArguments? Identifier
	|	primary '::' typeArguments? Identifier
	|	'super' '::' typeArguments? Identifier
	|	typeName '.' 'super' '::' typeArguments? Identifier
	|	classType '::' typeArguments? 'new'
	|	arrayType '::' 'new'
	;

methodReference0
	:	'::' typeArguments? Identifier
	;

methodReference1
	:	expressionName '::' typeArguments? Identifier
	|	referenceType '::' typeArguments? Identifier
	|	'super' '::' typeArguments? Identifier
	|	typeName '.' 'super' '::' typeArguments? Identifier
	|	classType '::' typeArguments? 'new'
	|	arrayType '::' 'new'
	;

arrayCreationExpression
	:	'new' primitiveType dimExprs dims?
	|	'new' classOrInterfaceType dimExprs dims?
	|	'new' primitiveType dims arrayInitializer
	|	'new' classOrInterfaceType dims arrayInitializer
	;

dimExprs
	:	dimExpr dimExpr*
	;

dimExpr
	:	annotation* '[' expression ']'
	;

expression
	:	lambdaExpression
	|	assignmentExpression
	;

lambdaExpression
	:	lambdaParameters '->' lambdaBody
	;

lambdaParameters
	:	Identifier
	|	'(' formalParameterList? ')'
	|	'(' inferredFormalParameterList ')'
	;

inferredFormalParameterList
	:	Identifier (',' Identifier)*
	;

lambdaBody
	:	expression
	|	block
	;

assignmentExpression
	:	conditionalExpression
	|	assignment
	;

assignment
	:	leftHandSide assignmentOperator expression
	;

leftHandSide
	:	expressionName
	|	fieldAccess
	|	arrayAccess
	;

assignmentOperator
	:	'='
	|	'*='
	|	'/='
	|	'%='
	|	'+='
	|	'-='
	|	'<<='
	|	'>>='
	|	'>>>='
	|	'&='
	|	'^='
	|	'|='
	;

conditionalExpression
	:	conditionalOrExpression
	|	conditionalOrExpression '?' expression ':' conditionalExpression
    |   conditionalOrExpression '?' expression ':' lambdaExpression
	;

conditionalOrExpression
	:	conditionalAndExpression
	|	conditionalOrExpression '||' conditionalAndExpression
	;

conditionalAndExpression
	:	inclusiveOrExpression
	|	conditionalAndExpression '&&' inclusiveOrExpression
	;

inclusiveOrExpression
	:	exclusiveOrExpression
	|	inclusiveOrExpression '|' exclusiveOrExpression
	;

exclusiveOrExpression
	:	andExpression
	|	exclusiveOrExpression '^' andExpression
	;

andExpression
	:	equalityExpression
	|	andExpression '&' equalityExpression
	;

equalityExpression
	:	relationalExpression
	|	equalityExpression '==' relationalExpression
	|	equalityExpression '!=' relationalExpression
	;

relationalExpression
	:	shiftExpression
	|	relationalExpression '<' shiftExpression
	|	relationalExpression '>' shiftExpression
	|	relationalExpression '<=' shiftExpression
	|	relationalExpression '>=' shiftExpression
	|	relationalExpression 'instanceof' referenceType
	;

shiftExpression
	:	additiveExpression
	|	shiftExpression '<' '<' additiveExpression
	|	shiftExpression '>' '>' additiveExpression
	|	shiftExpression '>' '>' '>' additiveExpression
	;

additiveExpression
	:	multiplicativeExpression
	|	additiveExpression '+' multiplicativeExpression
	|	additiveExpression '-' multiplicativeExpression
	;

multiplicativeExpression
	:	unaryExpression
	|	multiplicativeExpression '*' unaryExpression
	|	multiplicativeExpression '/' unaryExpression
	|	multiplicativeExpression '%' unaryExpression
	;

unaryExpression
	:	preIncrementExpression
	|	preDecrementExpression
	|	'+' unaryExpression
	|	'-' unaryExpression
	|	unaryExpressionNotPlusMinus
	;

preIncrementExpression
	:	'++' unaryExpression
	;

preDecrementExpression
	:	'--' unaryExpression
	;

unaryExpressionNotPlusMinus
	:	postfixExpression
	|	'~' unaryExpression
	|	'!' unaryExpression
	|	castExpression
	;

postfixExpression
	:	( primary | expressionName ) ( '++' | '--' )*
	;

postIncrementExpression
	:	postfixExpression '++'
	;

postDecrementExpression
	:	postfixExpression '--'
	;

castExpression
	:	'(' primitiveType ')' unaryExpression
	|	'(' referenceType additionalBound* ')' unaryExpressionNotPlusMinus
	|	'(' referenceType additionalBound* ')' lambdaExpression
	;

constantExpression
	:	expression
	;
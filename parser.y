%{
    #include <stdio.h>
    #include <stdlib.h>
    #include <bits/stdc++.h>
    #include <vector>

    using namespace std;
    extern int yylex();
    extern int yyparse();
    extern FILE* yyin;

    void yyerror(const char* s);

    int line = 0;

    #define YYDEBUG 1

%}
%output "parser.tab.c"
%glr-parser
%define parse.error verbose
%union {
	char* tokenname;
}

%token<tokenname>    TYPEIDENTIFIER
/* %token<tokenname>    IDENTIFIER */
/* %token<tokenname>    UNQUALIFIEDMETHODIDENTIFIER */
%token<tokenname>    LITERAL


%token<tokenname>    EXCLAMATION
%token<tokenname>    NOTEQUALS
%token<tokenname>    PERCENT
%token<tokenname>    PERCENTEQUALS
%token<tokenname>    AND
%token<tokenname>    ANDAND
%token<tokenname>    ANDEQUALS
%token<tokenname>    OPENPAREN
%token<tokenname>    CLOSEPAREN
%token<tokenname>    STAR
%token<tokenname>    STAREQUALS
%token<tokenname>    PLUS
%token<tokenname>    PLUSPLUS
%token<tokenname>    PLUSEQUALS
%token<tokenname>    COMMA
%token<tokenname>    MINUS
%token<tokenname>    MINUSMINUS
%token<tokenname>    MINUSEQUALS
%token<tokenname>    ARROW
%token<tokenname>    PERIOD
%token<tokenname>    THREEDOTS
%token<tokenname>    SLASH
%token<tokenname>    SLASHEQUALS
%token<tokenname>    COLON
%token<tokenname>    COLONCOLON
%token<tokenname>    SEMICOLON
%token<tokenname>    OPENANGLE
%token<tokenname>    LESSLESS
%token<tokenname>    LESSLESSEQUALS
%token<tokenname>    LESSEQUALS
%token<tokenname>    EQUALS
%token<tokenname>    EQUALSEQUALS
%token<tokenname>    CLOSEANGLE
%token<tokenname>    GREATEREQUALS
%token<tokenname>    GREATERGREATER
%token<tokenname>    GREATERGREATEREQUALS
%token<tokenname>    GREATERGREATERGREATER
%token<tokenname>    GREATERGREATERGREATEREQUALS
%token<tokenname>    QUESTION
%token<tokenname>    AT
%token<tokenname>    OPENBOX
%token<tokenname>    CLOSEBOX
%token<tokenname>    CARET
%token<tokenname>    CARETEQUALS
%token<tokenname>    ABSTRACT
%token<tokenname>    ASSERT
%token<tokenname>    BOOLEAN
%token<tokenname>    BREAK
%token<tokenname>    BYTE
%token<tokenname>    CASE
%token<tokenname>    CATCH
%token<tokenname>    CHAR
%token<tokenname>    CLASS
%token<tokenname>    CONTINUE
%token<tokenname>    DEFAULT
%token<tokenname>    DO
%token<tokenname>    DOUBLE
%token<tokenname>    ELSE
%token<tokenname>    ENUM
%token<tokenname>    EXPORTS
%token<tokenname>    EXTENDS
%token<tokenname>    FINAL
%token<tokenname>    FINALLY
%token<tokenname>    FLOAT
%token<tokenname>    FOR
%token<tokenname>    IF
%token<tokenname>    IMPLEMENTS
%token<tokenname>    IMPORT
%token<tokenname>    INSTANCEOF
%token<tokenname>    INT
%token<tokenname>    INTERFACE
%token<tokenname>    LONG
%token<tokenname>    MODULE
%token<tokenname>    NATIVE
%token<tokenname>    NEW
%token<tokenname>    NONSEALED
%token<tokenname>    OPEN
%token<tokenname>    OPENS
%token<tokenname>    PACKAGE
%token<tokenname>    PERMITS
%token<tokenname>    PRIVATE
%token<tokenname>    PROTECTED
%token<tokenname>    PROVIDES
%token<tokenname>    PUBLIC
%token<tokenname>    RECORD
%token<tokenname>    REQUIRES
%token<tokenname>    RETURN
%token<tokenname>    SEALED
%token<tokenname>    SHORT
%token<tokenname>    STATIC
%token<tokenname>    STRICTFP
%token<tokenname>    SUPER
%token<tokenname>    SWITCH
%token<tokenname>    SYNCHRONIZED
%token<tokenname>    THIS
%token<tokenname>    THROW
%token<tokenname>    THROWS
%token<tokenname>    TO
%token<tokenname>    TRANSIENT
%token<tokenname>    TRANSITIVE
%token<tokenname>    TRY
%token<tokenname>    USES
%token<tokenname>    VAR
%token<tokenname>    VOID
%token<tokenname>    VOLATILE
%token<tokenname>    WHILE
%token<tokenname>    WITH
%token<tokenname>    YIELD
%token<tokenname>    OPENBRACE
%token<tokenname>    PIPE
%token<tokenname>    PIPEEQUALS
%token<tokenname>    PIPEPIPE
%token<tokenname>    CLOSEBRACE
%token<tokenname>    TILDE

%start CompilationUnit

%%

// {NonTerminal}
// AlphaNonTeminal

// [NonTerminal]
// BetaNonTerminal

/* Productions from §3 (Lexical Structure) */

UnqualifiedMethodIdentifier : TYPEIDENTIFIER
                        |   PERMITS
                        |   RECORD
                        |   SEALED
                        |   VAR
                        ;
Identifier              :   TYPEIDENTIFIER
                        |   PERMITS
                        |   RECORD
                        |   SEALED
                        |   VAR
                        |   YIELD
                        ;



/* Productions from §4 (Types, Values, and Variables) */

Type                    :   PrimitiveType
                        |   ReferenceType
                        ;
PrimitiveType           :   AlphaAnnotation NumericType
                        |   AlphaAnnotation BOOLEAN
                        ;
AlphaAnnotation         :   /* Epsilon */
                        |   Annotation AlphaAnnotation
                        ;
NumericType             :   IntegralType
                        |   FloatingPointType
                        ;
IntegralType            :   BYTE
                        |   SHORT
                        |   INT
                        |   LONG
                        |   CHAR
                        ;
FloatingPointType       :   FLOAT 
                        |   DOUBLE
                        ;
ReferenceType           :   ClassOrInterfaceType
                        |   TypeVariable
                        |   ArrayType
                        ;
ClassOrInterfaceType    :   ClassType
                        |   InterfaceType
                        ;
ClassType               :   AlphaAnnotation TYPEIDENTIFIER BetaTypeArguments
                        |   PackageName PERIOD AlphaAnnotation TYPEIDENTIFIER BetaTypeArguments
                        |   ClassOrInterfaceType PERIOD AlphaAnnotation TYPEIDENTIFIER BetaTypeArguments
                        ;
BetaTypeArguments       :   /* Epsilon */
                        |   TypeArguments
                        ;
InterfaceType           :   ClassType
                        ;
TypeVariable            :   AlphaAnnotation TYPEIDENTIFIER
                        ;
ArrayType               :   PrimitiveType Dims
                        |   ClassOrInterfaceType Dims
                        |   TypeVariable Dims
                        ;
Dims                    :   AlphaAnnotation OPENBOX CLOSEBOX Dims
                        |   AlphaAnnotation OPENBOX CLOSEBOX
                        ;
TypeParameter           :   AlphaTypeParameterModifier TYPEIDENTIFIER BetaTypeBound
                        ;
AlphaTypeParameterModifier:   /* Epsilon */
                        |   TypeParameterModifier AlphaTypeParameterModifier
                        ;
BetaTypeBound           :   /* Epsilon */
                        |   TypeBound
                        ;
TypeParameterModifier   :   Annotation
                        ;
TypeBound               :   EXTENDS TypeVariable
                        |   EXTENDS ClassOrInterfaceType AlphaAdditionalBound
                        ;
AlphaAdditionalBound    :   /* Epsilon */
                        |   AdditionalBound AlphaAdditionalBound
                        ;
AdditionalBound         :   AND InterfaceType
                        ;
TypeArguments           :   OPENANGLE TypeArgumentList CLOSEANGLE
                        ;
TypeArgumentList        :   TypeArgument AlphaCommaTypeArgument
                        ;
AlphaCommaTypeArgument  :   /* Epsilon */
                        |   COMMA TypeArgument AlphaCommaTypeArgument
                        ;
TypeArgument            :   ReferenceType
                        |   Wildcard
                        ;
Wildcard                :   AlphaAnnotation QUESTION BetaWildcardBounds
                        ;
BetaWildcardBounds      :   /* Epsilon */
                        |   WildcardBounds
                        ;
WildcardBounds          :   EXTENDS ReferenceType
                        |   SUPER ReferenceType
                        ;



/* Productions from §6 (Names) */

ModuleName              :   Identifier
                        |   ModuleName PERIOD Identifier
                        ;
PackageName             :   Identifier
                        |   PackageName PERIOD Identifier
                        ;
TypeName                :   TYPEIDENTIFIER
                        |   PackageOrTypeName PERIOD TYPEIDENTIFIER
                        ;
ExpressionName          :   Identifier 
                        |   AmbiguousName PERIOD Identifier
                        ;
MethodName              :   UnqualifiedMethodIdentifier 
                        ;
PackageOrTypeName       :   Identifier
                        |   PackageOrTypeName PERIOD Identifier
                        ;
AmbiguousName           :   Identifier 
                        |   AmbiguousName PERIOD Identifier
                        ;



/* Productions from §7 (Packages and Modules) */

CompilationUnit         :   OrdinaryCompilationUnit
                        |   ModularCompilationUnit
                        ;
OrdinaryCompilationUnit :   BetaPackageDeclaration AlphaImportDeclaration AlphaTopLevelClassOrInterfaceDeclaration
                        ;
BetaPackageDeclaration  :   /* Epsilon */ 
                        |   PackageDeclaration
                        ;
AlphaImportDeclaration  :   /* Epsilon */
                        |   ImportDeclaration AlphaImportDeclaration
                        ;
AlphaTopLevelClassOrInterfaceDeclaration:   /* Epsilon */
                        |   TopLevelClassOrInterfaceDeclaration AlphaTopLevelClassOrInterfaceDeclaration
                        ;
ModularCompilationUnit  :   AlphaImportDeclaration ModuleDeclaration
                        ;
PackageDeclaration      :   AlphaPackageModifier PACKAGE Identifier AlphaDotIdentifier SEMICOLON
                        ;
AlphaPackageModifier    :   /* Epsilon */ 
                        |   PackageModifier AlphaPackageModifier
                        ;
AlphaDotIdentifier      :   /* Epsilon */ 
                        |   PERIOD Identifier AlphaDotIdentifier
                        ;
                        ;
PackageModifier         :   Annotation
                        ;
ImportDeclaration       :   SingleTypeImportDeclaration
                        |   TypeImportOnDemandDeclaration
                        |   SingleStaticImportDeclaration
                        |   StaticImportOnDemandDeclaration
                        ;
SingleTypeImportDeclaration:   IMPORT TypeName SEMICOLON
                        ;
TypeImportOnDemandDeclaration:   IMPORT PackageOrTypeName PERIOD STAR SEMICOLON 
                        ;
SingleStaticImportDeclaration:   IMPORT STATIC TypeName PERIOD Identifier SEMICOLON
                        ;
StaticImportOnDemandDeclaration:   IMPORT STATIC TypeName PERIOD STAR SEMICOLON 
                        ;
TopLevelClassOrInterfaceDeclaration:   ClassDeclaration 
                        |   InterfaceDeclaration
                        |  SEMICOLON
                        ;
ModuleDeclaration       :   AlphaAnnotation BetaOpen MODULE Identifier AlphaDotIdentifier OPENBRACE AlphaModuleDirective CLOSEBRACE
                        ;
BetaOpen                :   /* Epsilon */
                        |   OPEN
                        ;
AlphaModuleDirective    :   /* Epsilon */
                        |   ModuleDirective AlphaModuleDirective
                        ;
ModuleDirective         :   REQUIRES AlphaRequiresModifier ModuleName SEMICOLON
                        |   EXPORTS PackageName BetaToModuleNameAlphaCommaModuleName SEMICOLON
                        |   OPENS PackageName BetaToModuleNameAlphaCommaModuleName SEMICOLON
                        |   USES TypeName SEMICOLON
                        |   PROVIDES TypeName WITH TypeName AlphaCommaTypeName SEMICOLON
                        ;
AlphaRequiresModifier   :   /* Epsilon */ 
                        |   RequiresModifier AlphaRequiresModifier
                        ;
BetaToModuleNameAlphaCommaModuleName        :   /* Epsilon */ 
                        |   TO ModuleName AlphaCommaModuleName
                        ;
AlphaCommaModuleName    :   /* Epsilon */ 
                        |   COMMA ModuleName AlphaCommaModuleName
                        ;
AlphaCommaTypeName      :   /* Epsilon */ 
                        |   COMMA TypeName AlphaCommaTypeName
                        ;
RequiresModifier        :   TRANSITIVE 
                        |   STATIC
                        ;



/* Productions from §8 (Classes) */

ClassDeclaration        :   NormalClassDeclaration 
                        |   EnumDeclaration
                        |   RecordDeclaration
                        ;
NormalClassDeclaration  :   AlphaClassModifier CLASS TYPEIDENTIFIER BetaTypeParameters BetaClassExtends BetaClassImplements BetaClassPermits ClassBody
                        ;
AlphaClassModifier      :   /* Epsilon */ 
                        |   ClassModifier AlphaClassModifier
                        ;
BetaTypeParameters      :   /* Epsilon */ 
                        |   TypeParameters
                        ;
BetaClassExtends        :   /* Epsilon */ 
                        |   ClassExtends
                        ;
BetaClassImplements     :   /* Epsilon */ 
                        |   ClassImplements
                        ;
BetaClassPermits        :   /* Epsilon */
                        |   ClassPermits
                        ;
ClassModifier           :   Annotation 
                        |   PUBLIC 
                        |   PROTECTED 
                        |   PRIVATE 
                        |   ABSTRACT 
                        |   STATIC 
                        |   FINAL 
                        |   SEALED 
                        |   NONSEALED 
                        |   STRICTFP
                        ;
TypeParameters          :   OPENANGLE TypeParameterList CLOSEANGLE
                        ;
TypeParameterList       :   TypeParameter AlphaCommaTypeParameter
                        ;
AlphaCommaTypeParameter :   /* Epsilon */ 
                        |   COMMA TypeParameter AlphaCommaTypeParameter
                        ;
ClassExtends            :   EXTENDS ClassType
                        ;
ClassImplements         :   IMPLEMENTS InterfaceTypeList
                        ;
InterfaceTypeList       :   InterfaceType AlphaCommaInterfaceType
                        ;
AlphaCommaInterfaceType :   /* Epsilon */ 
                        |   COMMA InterfaceType AlphaCommaInterfaceType
                        ;
ClassPermits            :   PERMITS TypeName AlphaCommaTypeName
                        ;
ClassBody               :   OPENBRACE AlphaClassBodyDeclaration CLOSEBRACE
                        ;
AlphaClassBodyDeclaration : /* Epsilon */
                        |   ClassBodyDeclaration AlphaClassBodyDeclaration
                        ;
ClassBodyDeclaration    :   ClassMemberDeclaration 
                        |   InstanceInitializer 
                        |   StaticInitializer 
                        |   ConstructorDeclaration
                        ;
ClassMemberDeclaration  :   FieldDeclaration 
                        |   MethodDeclaration 
                        |   ClassDeclaration 
                        |   InterfaceDeclaration
                        |   SEMICOLON
                        ;
FieldDeclaration        :   AlphaFieldModifier UnannType VariableDeclaratorList SEMICOLON
                        ;
AlphaFieldModifier      :   /* Epsilon */ 
                        |   FieldModifier AlphaFieldModifier
                        ;
FieldModifier           :   Annotation 
                        |   PUBLIC 
                        |   PROTECTED 
                        |   PRIVATE 
                        |   STATIC 
                        |   FINAL 
                        |   TRANSIENT 
                        |   VOLATILE
                        ;
VariableDeclaratorList  :   VariableDeclarator AlphaCommaVariableDeclarator
                        ;
AlphaCommaVariableDeclarator : /* Epsilon */ 
                        |   COMMA VariableDeclarator AlphaCommaVariableDeclarator
                        ;
VariableDeclarator      :   VariableDeclaratorId BetaEqualVariableInitializer
                        ;
BetaEqualVariableInitializer : /* Epsilon */ 
                        |   EQUALS VariableInitializer
                        ;
VariableDeclaratorId    :   Identifier BetaDims
                        ;
BetaDims                :   /* Epsilon */
                        |   Dims
                        ;
VariableInitializer     :   Expression
                        |   ArrayInitializer
                        ;
UnannType               :   UnannPrimitiveType 
                        |   UnannReferenceType
                        ;
UnannPrimitiveType      :   NumericType 
                        |   BOOLEAN
                        ;
UnannReferenceType      :   UnannClassOrInterfaceType 
                        |   UnannTypeVariable 
                        |   UnannArrayType
                        ;
UnannClassOrInterfaceType :   UnannClassType 
                        |   UnannInterfaceType
                        ;
UnannClassType          :   TYPEIDENTIFIER BetaTypeArguments
                        |   PackageName PERIOD AlphaAnnotation TYPEIDENTIFIER BetaTypeArguments
                        |   UnannClassOrInterfaceType PERIOD AlphaAnnotation TYPEIDENTIFIER BetaTypeArguments
                        ;
UnannInterfaceType      :   UnannClassType
                        ;
UnannTypeVariable       :   TYPEIDENTIFIER
                        ;
UnannArrayType          :   UnannPrimitiveType Dims 
                        |   UnannClassOrInterfaceType Dims 
                        |   UnannTypeVariable Dims
                        ;
MethodDeclaration       :   AlphaMethodModifier MethodHeader MethodBody
                        ;
AlphaMethodModifier     :   /* Epsilon */ 
                        |   MethodModifier AlphaMethodModifier
                        ;
MethodModifier          :   Annotation 
                        |   PUBLIC 
                        |   PROTECTED 
                        |   PRIVATE 
                        |   ABSTRACT 
                        |   STATIC 
                        |   FINAL 
                        |   SYNCHRONIZED 
                        |   NATIVE 
                        |   STRICTFP
                        ;
MethodHeader            :   Result MethodDeclarator BetaThrows
                        |   TypeParameters AlphaAnnotation Result MethodDeclarator BetaThrows
                        ;
BetaThrows              :   /* Epsilon */
                        |   Throws
                        ;
Result                  :   UnannType 
                        |   VOID
                        ;
MethodDeclarator        :   Identifier OPENPAREN BetaRecieverParameterComma BetaFormalParameterList CLOSEPAREN BetaDims
                        ;
BetaRecieverParameterComma : /* Epsilon */
                        |   RecieverParameter COMMA
                        ;
BetaFormalParameterList :   /* Epsilon */ 
                        |   FormalParameterList
                        ;
RecieverParameter       :   AlphaAnnotation UnannType BetaIdentifierDot THIS
                        ;
BetaIdentifierDot       :   /* Epsilon */ 
                        |   Identifier PERIOD
                        ;
FormalParameterList     :   FormalParameter AlphaCommaFormalParameter
                        ;
AlphaCommaFormalParameter : /* Epsilon */ 
                        |   COMMA FormalParameter AlphaCommaFormalParameter
                        ;
FormalParameter         :   AlphaVariableModifier UnannType VariableDeclaratorId VariableArityParameter
                        ;
AlphaVariableModifier   :   /* Epsilon */ 
                        |   VariableModifier AlphaVariableModifier
                        ;
VariableArityParameter  :   AlphaVariableModifier UnannType AlphaAnnotation THREEDOTS Identifier
                        ;
VariableModifier        :   Annotation 
                        |   FINAL
                        ;
Throws                  :   THROWS ExceptionTypeList 
                        ;
ExceptionTypeList       :   ExceptionType AlphaCommaExceptionType 
                        ;
AlphaCommaExceptionType :   /* Epsilon */ 
                        |   COMMA ExceptionType AlphaCommaExceptionType
                        ;
ExceptionType           :   ClassType 
                        |   TypeVariable
                        ;
MethodBody              :   Block 
                        |   SEMICOLON
                        ;
InstanceInitializer     :   Block 
                        ;
StaticInitializer       :   STATIC Block 
                        ;
ConstructorDeclaration  :   AlphaConstructorModifier ConstructorDeclarator BetaThrows ConstructorBody
                        ;
AlphaConstructorModifier : /* Epsilon */ 
                        |   ConstructorModifier AlphaConstructorModifier
                        ;
ConstructorModifier     :   Annotation 
                        |   PUBLIC 
                        |   PROTECTED 
                        |   PRIVATE
                        ;
ConstructorDeclarator   :   BetaTypeParameters SimpleTypeName OPENPAREN BetaRecieverParameterComma BetaFormalParameterList CLOSEPAREN
                        ;
SimpleTypeName          :   TYPEIDENTIFIER
                        ;
ConstructorBody         :   OPENBRACE BetaExplicitConstructorInvocation BetaBlockStatements CLOSEBRACE 
                        ;
BetaExplicitConstructorInvocation : /* Epsilon */ 
                        |   ExplicitConstructorInvocation
                        ;
BetaBlockStatements     :   /* Epsilon */ 
                        |   BlockStatements
                        ;
ExplicitConstructorInvocation :   BetaTypeArguments THIS OPENPAREN BetaArgumentList CLOSEPAREN SEMICOLON
                        |   BetaTypeArguments SUPER OPENPAREN BetaArgumentList CLOSEPAREN SEMICOLON
                        |   ExpressionName PERIOD BetaTypeArguments SUPER OPENPAREN BetaArgumentList CLOSEPAREN SEMICOLON
                        |   Primary PERIOD BetaTypeArguments SUPER OPENPAREN BetaArgumentList CLOSEPAREN SEMICOLON
                        ;
BetaArgumentList        :   /* Epsilon */ 
                        |   ArgumentList
                        ;
EnumDeclaration         :   AlphaClassModifier ENUM TYPEIDENTIFIER BetaClassImplements EnumBody
                        ;
EnumBody                :   OPENBRACE BetaEnumConstantList BetaComma BetaEnumBodyDeclarations CLOSEBRACE
                        ;
BetaEnumConstantList    :   /* Epsilon */
                        |   EnumConstantList
                        ;
BetaComma               :   /* Epsilon */ 
                        |   COMMA
                        ;
BetaEnumBodyDeclarations : /* Epsilon */ 
                        |   EnumBodyDeclarations
                        ;
EnumConstantList        :   EnumConstant AlphaCommaEnumConstant
                        ;
AlphaCommaEnumConstant  :   /* Epsilon */ 
                        |   COMMA EnumConstant AlphaCommaEnumConstant
                        ;
EnumConstant            :   AlphaEnumConstantModifier Identifier BetaBracketBetaArgumentListBracket BetaClassBody 
                        ;
AlphaEnumConstantModifier : /* Epsilon */ 
                        |   EnumConstantModifier AlphaEnumConstantModifier
                        ;
BetaBracketBetaArgumentListBracket : /* Epsilon */ 
                        |   OPENPAREN BetaArgumentList CLOSEPAREN
                        ;
BetaClassBody           : /* Epsilon */ 
                        |   ClassBody
                        ;
EnumConstantModifier    :   Annotation 
                        ;
EnumBodyDeclarations    :   SEMICOLON AlphaClassBodyDeclaration
                        ;
RecordDeclaration       :   AlphaClassModifier RECORD TYPEIDENTIFIER BetaTypeParameters RecordHeader BetaClassImplements RecordBody
                        ;
RecordHeader            :   OPENPAREN BetaRecordComponentList CLOSEPAREN 
                        ;
BetaRecordComponentList :   /* Epsilon */ 
                        |   RecordComponentList
                        ;
RecordComponentList     :   RecordComponent AlphaCommaRecordComponent 
                        ;
AlphaCommaRecordComponent : /* Epsilon */ 
                        |   COMMA RecordComponent AlphaCommaRecordComponent
                        ;
RecordComponent         :   AlphaRecordComponentModifier UnannType Identifier VariableArityRecordComponent
                        ;
AlphaRecordComponentModifier : /* Epsilon */ 
                        |   RecordComponentModifier AlphaRecordComponentModifier
                        ;
VariableArityRecordComponent : AlphaRecordComponentModifier UnannType AlphaAnnotation THREEDOTS Identifier
                        ;
RecordComponentModifier :   Annotation 
                        ;
RecordBody              :   OPENBRACE AlphaRecordBodyDeclaration CLOSEBRACE 
                        ;
AlphaRecordBodyDeclaration : /* Epsilon */ 
                        |   RecordBodyDeclaration AlphaRecordBodyDeclaration
                        ;
RecordBodyDeclaration   :   ClassBodyDeclaration 
                        |   CompactConstructorDeclaration
                        ;
CompactConstructorDeclaration :   AlphaConstructorModifier SimpleTypeName ConstructorBody
                        ;



/* Productions from §9 (Interfaces) */

InterfaceDeclaration    :   NormalInterfaceDeclaration 
                        |   AnnotationInterfaceDeclaration
                        ;
NormalInterfaceDeclaration :   AlphaInterfaceModifier INTERFACE TYPEIDENTIFIER BetaTypeParameters BetaInterfaceExtends BetaInterfacePermits InterfaceBody
                        ;
AlphaInterfaceModifier  :   /* Epsilon */ 
                        |   InterfaceModifier AlphaInterfaceModifier
                        ;
BetaInterfaceExtends    :   /* Epsilon */ 
                        |   InterfaceExtends
                        ;
BetaInterfacePermits    :   /* Epsilon */ 
                        |   InterfacePermits
                        ;
InterfaceModifier       :   Annotation 
                        |   PUBLIC 
                        |   PROTECTED 
                        |   PRIVATE
                        |   ABSTRACT 
                        |   STATIC 
                        |   SEALED 
                        |   NONSEALED 
                        |   STRICTFP
                        ;
InterfaceExtends        :   EXTENDS InterfaceTypeList 
                        ;
InterfacePermits        :   PERMITS TypeName AlphaCommaTypeName 
                        ;
InterfaceBody           :   OPENBRACE AlphaInterfaceMemberDeclaration CLOSEBRACE 
                        ;
AlphaInterfaceMemberDeclaration : /* Epsilon */ 
                        |   InterfaceMemberDeclaration AlphaInterfaceMemberDeclaration
                        ;
InterfaceMemberDeclaration :   ConstantDeclaration 
                        |   InterfaceMethodDeclaration 
                        |   ClassDeclaration 
                        |   InterfaceDeclaration
                        |   SEMICOLON
                        ;
ConstantDeclaration     :   AlphaConstantModifier UnannType VariableDeclaratorList SEMICOLON 
                        ;
AlphaConstantModifier   :   /* Epsilon */ 
                        |   ConstantModifier AlphaConstantModifier
                        ;
ConstantModifier        :   Annotation 
                        |   PUBLIC 
                        |   STATIC 
                        |   FINAL
                        ;
InterfaceMethodDeclaration :   AlphaInterfaceMethodModifier MethodHeader MethodBody
                        ;
AlphaInterfaceMethodModifier : /* Epsilon */ 
                        |   InterfaceMethodModifier AlphaInterfaceMethodModifier
                        ;
InterfaceMethodModifier :   Annotation 
                        |   PUBLIC 
                        |   PRIVATE 
                        |   ABSTRACT 
                        |   DEFAULT 
                        |   STATIC 
                        |   STRICTFP
                        ;
AnnotationInterfaceDeclaration :   AlphaInterfaceModifier AT INTERFACE TYPEIDENTIFIER AnnotationInterfaceBody
                        ;
AnnotationInterfaceBody :   OPENBRACE AlphaAnnotationInterfaceMemberDeclaration CLOSEBRACE
                        ;
AlphaAnnotationInterfaceMemberDeclaration : /* Epsilon */ 
                        |   AnnotationInterfaceMemberDeclaration AlphaAnnotationInterfaceMemberDeclaration
                        ;
AnnotationInterfaceMemberDeclaration :   AnnotationInterfaceElementDeclaration 
                        |   ConstantDeclaration 
                        |   ClassDeclaration 
                        |   InterfaceDeclaration
                        |   SEMICOLON
                        ;
AnnotationInterfaceElementDeclaration :   AlphaAnnotationInterfaceElementModifier UnannType Identifier OPENPAREN CLOSEPAREN BetaDims BetaDefaultValue SEMICOLON
                        ;
AlphaAnnotationInterfaceElementModifier : /* Epsilon */ 
                        |   AnnotationInterfaceElementModifier AlphaAnnotationInterfaceElementModifier
                        ;
BetaDefaultValue        :   /* Epsilon */ 
                        |   DefaultValue
                        ;
AnnotationInterfaceElementModifier :   Annotation 
                        |   PUBLIC 
                        |   ABSTRACT
                        ;
DefaultValue            :   DEFAULT ElementValue 
                        ;
Annotation              :   NormalAnnotation 
                        |   MarkerAnnotation 
                        |   SingleElementAnnotation
                        ;
NormalAnnotation        :   AT TypeName OPENPAREN BetaElementValuePairList CLOSEPAREN 
                        ;
BetaElementValuePairList :   /* Epsilon */ 
                        |   ElementValuePairList
                        ;
ElementValuePairList    :   ElementValuePair AlphaCommaElementValuePair 
                        ;
AlphaCommaElementValuePair : /* Epsilon */ 
                        |   COMMA ElementValuePair AlphaCommaElementValuePair
                        ;
ElementValuePair        :   Identifier EQUALS ElementValue 
                        ;
ElementValue            :   ConditionalExpression 
                        |   ElementValueArrayInitializer 
                        |   Annotation
                        ;
ElementValueArrayInitializer :   OPENBRACE BetaElementValueList BetaComma CLOSEBRACE
                        ;
BetaElementValueList    :   /* Epsilon */ 
                        |   ElementValueList
                        ;
ElementValueList        :   ElementValue AlphaCommaElementValue 
                        ;
AlphaCommaElementValue  :   /* Epsilon */ 
                        |   COMMA ElementValue AlphaCommaElementValue
                        ;
MarkerAnnotation        :   AT TypeName 
                        ;
SingleElementAnnotation :   AT TypeName OPENPAREN ElementValue CLOSEPAREN 
                        ;



/* Productions from §10 (Arrays) */

ArrayInitializer        :   OPENBRACE BetaVariableInitializerList BetaComma CLOSEBRACE
                        ;
BetaVariableInitializerList : /* Epsilon */ 
                        |   VariableInitializerList
                        ;
VariableInitializerList :   VariableInitializer AlphaCommaVariableInitializer 
                        ;
AlphaCommaVariableInitializer : /* Epsilon */ 
                        |   COMMA VariableInitializer AlphaCommaVariableInitializer
                        ;



/* Productions from §14 (Blocks, Statements, and Patterns) */

Block                   :   OPENBRACE BetaBlockStatements CLOSEBRACE
                        ;
BlockStatements         :   BlockStatement AlphaBlockStatement 
                        ;
AlphaBlockStatement     :   /* Epsilon */
                        |   BlockStatement AlphaBlockStatement
                        ;
BlockStatement          :   LocalClassOrInterfaceDeclaration 
                        |   LocalVariableDeclarationStatement 
                        |   Statement
                        ;
LocalClassOrInterfaceDeclaration :   ClassDeclaration 
                        |   NormalInterfaceDeclaration
                        ;
LocalVariableDeclarationStatement :   LocalVariableDeclaration SEMICOLON 
                        ;
LocalVariableDeclaration :   AlphaVariableModifier LocalVariableType VariableDeclaratorList 
                        ;
LocalVariableType       :   UnannType 
                        |   VAR
                        ;
Statement               :   StatementWithoutTrailingSubstatement 
                        |   LabeledStatement 
                        |   IfThenStatement 
                        |   IfThenElseStatement 
                        |   WhileStatement 
                        |   ForStatement
                        ;
StatementNoShortIf      :   StatementWithoutTrailingSubstatement 
                        |   LabeledStatementNoShortIf 
                        |   IfThenElseStatementNoShortIf 
                        |   WhileStatementNoShortIf 
                        |   ForStatementNoShortIf
                        ;
StatementWithoutTrailingSubstatement :   Block 
                        |   EmptyStatement 
                        |   ExpressionStatement 
                        |   AssertStatement 
                        |   SwitchStatement 
                        |   DoStatement 
                        |   BreakStatement 
                        |   ContinueStatement 
                        |   ReturnStatement 
                        |   SynchronizedStatement 
                        |   ThrowStatement 
                        |   TryStatement 
                        |   YieldStatement
                        ;
EmptyStatement          :   SEMICOLON 
                        ;
LabeledStatement        :   Identifier COLON Statement 
                        ;
LabeledStatementNoShortIf :   Identifier COLON StatementNoShortIf 
                        ;
ExpressionStatement     :   StatementExpression SEMICOLON 
                        ;
StatementExpression     :   Assignment 
                        |   PreIncrementExpression 
                        |   PreDecrementExpression 
                        |   PostIncrementExpression 
                        |   PostDecrementExpression 
                        |   MethodInvocation 
                        |   ClassInstanceCreationExpression
                        ;
IfThenStatement         :   IF OPENPAREN Expression CLOSEPAREN Statement 
                        ;
IfThenElseStatement     :   IF OPENPAREN Expression CLOSEPAREN StatementNoShortIf ELSE Statement 
                        ;
IfThenElseStatementNoShortIf :   IF OPENPAREN Expression CLOSEPAREN StatementNoShortIf ELSE StatementNoShortIf
                        ;
AssertStatement         :   ASSERT Expression SEMICOLON 
                        |   ASSERT Expression COLON Expression SEMICOLON
                        ;
SwitchStatement         :   SWITCH OPENPAREN Expression CLOSEPAREN SwitchBlock 
                        ;
SwitchBlock             :   OPENBRACE SwitchRule AlphaSwitchRule CLOSEBRACE
                        |   OPENBRACE AlphaSwitchBlockStatementGroup AlphaSwitchLabelColon CLOSEBRACE
                        ;
AlphaSwitchRule         :   /* Epsilon */
                        |   SwitchRule AlphaSwitchRule
                        ;
AlphaSwitchBlockStatementGroup :   /* Epsilon */
                        |   SwitchBlockStatementGroup AlphaSwitchBlockStatementGroup
                        ;
AlphaSwitchLabelColon   :   /* Epsilon */ 
                        |   SwitchLabel COLON AlphaSwitchLabelColon
                        ;
SwitchRule              :   SwitchLabel ARROW Expression SEMICOLON 
                        |   SwitchLabel ARROW Block 
                        |   SwitchLabel ARROW ThrowStatement
                        ;
SwitchBlockStatementGroup :   SwitchLabel COLON AlphaSwitchLabelColon BlockStatements 
                        ;
SwitchLabel             :   CASE CaseConstant AlphaCommaCaseConstant
                        |   DEFAULT
                        ;
AlphaCommaCaseConstant  :   /* Epsilon */ 
                        |   COMMA CaseConstant AlphaCommaCaseConstant
                        ;
CaseConstant            :   ConditionalExpression 
                        ;
WhileStatement          :   WHILE OPENPAREN Expression CLOSEPAREN Statement
                        ;
WhileStatementNoShortIf :   WHILE OPENPAREN Expression CLOSEPAREN StatementNoShortIf 
                        ;
DoStatement             :   DO Statement WHILE OPENPAREN Expression CLOSEPAREN SEMICOLON 
                        ;
ForStatement            :   BasicForStatement 
                        |   EnhancedForStatement
                        ;
ForStatementNoShortIf   :   BasicForStatementNoShortIf 
                        |   EnhancedForStatementNoShortIf
                        ;
BasicForStatement       :   FOR OPENPAREN BetaForInit SEMICOLON BetaExpression SEMICOLON BetaForUpdate CLOSEPAREN Statement 
                        ;
BetaForInit             :   /* Epsilon */ 
                        |   ForInit
                        ;
BetaExpression          :   /* Epsilon */ 
                        |   Expression
                        ;
BetaForUpdate           :   /* Epsilon */ 
                        |   ForUpdate
                        ;
BasicForStatementNoShortIf :   FOR OPENPAREN BetaForInit SEMICOLON BetaExpression SEMICOLON BetaForUpdate CLOSEPAREN StatementNoShortIf 
                        ;
ForInit                 :   StatementExpressionList 
                        |   LocalVariableDeclaration
                        ;
ForUpdate               :   StatementExpressionList 
                        ;
StatementExpressionList :   StatementExpression AlphaCommaStatementExpression 
                        ;
AlphaCommaStatementExpression :   /* Epsilon */ 
                        |   COMMA StatementExpression AlphaCommaStatementExpression
                        ;
EnhancedForStatement    :   FOR OPENPAREN LocalVariableDeclaration COLON Expression CLOSEPAREN Statement 
                        ;
EnhancedForStatementNoShortIf :   FOR OPENPAREN LocalVariableDeclaration COLON Expression CLOSEPAREN StatementNoShortIf 
                        ;
BreakStatement          :   BREAK BetaIdentifier SEMICOLON 
                        ;
BetaIdentifier          :   /* Epsilon */ 
                        |   Identifier
                        ;
YieldStatement          :   YIELD Expression SEMICOLON 
                        ;
ContinueStatement       :   CONTINUE BetaIdentifier SEMICOLON 
                        ;
ReturnStatement         :   RETURN BetaExpression SEMICOLON 
                        ;
ThrowStatement          :   THROW Expression SEMICOLON 
                        ;
SynchronizedStatement   :   SYNCHRONIZED OPENPAREN Expression CLOSEPAREN Block 
                        ;
TryStatement            :   TRY Block Catches 
                        |   TRY Block BetaCatches Finally
                        |   TryWithResourcesStatement
                        ;
BetaCatches             :   /* Epsilon */ 
                        |   Catches
                        ;
Catches                 :   CatchClause AlphaCatchClause 
                        ;
AlphaCatchClause        :   /* Epsilon */ 
                        |   CatchClause AlphaCatchClause
                        ;
CatchClause             :   CATCH OPENPAREN CatchFormalParameter CLOSEPAREN Block 
                        ;
CatchFormalParameter    :   AlphaVariableModifier CatchType VariableDeclaratorId 
                        ;
CatchType               :   UnannClassType AlphaPipeCatchType
                        ;
AlphaPipeCatchType        :   /* Epsilon */ 
                        |   PIPE CatchType AlphaPipeCatchType
                        ;
Finally                 :   FINALLY Block 
                        ;
TryWithResourcesStatement :   TRY ResourceSpecification Block BetaCatches BetaFinally 
                        ;
BetaFinally             :   /* Epsilon */ 
                        |   Finally
                        ;
ResourceSpecification   :   OPENPAREN ResourceList BetaSemiColon CLOSEPAREN 
                        ;
BetaSemiColon           :   /* Epsilon */ 
                        |   SEMICOLON
                        ;
ResourceList            :   Resource AlphaSemiColonResource 
                        ;
AlphaSemiColonResource  :   /* Epsilon */ 
                        |   SEMICOLON Resource AlphaSemiColonResource
                        ;
Resource                :   LocalVariableDeclaration 
                        |   VariableAccess
                        ;
Pattern                 :   TypePattern
                        ;
TypePattern             :  LocalVariableDeclaration
                        ;



/* Productions from §15 (Blocks, Statements, and Patterns) */

VariableAccess          :   ExpressionName 
                        |   FieldAccess
                        ;



/* Productions from §15 (Expressions) */

Primary                 :   PrimaryNoNewArray
                        |   ArrayCreationExpression
                        ;
PrimaryNoNewArray       :   LITERAL 
                        |   ClassLiteral
                        |   THIS
                        |   TypeName PERIOD THIS
                        |   OPENPAREN Expression CLOSEPAREN
                        |   ClassInstanceCreationExpression
                        |   FieldAccess
                        |   ArrayAccess
                        |   MethodInvocation
                        |   MethodReference
                        ;
ClassLiteral            :   TypeName AlphaSquareBrackets PERIOD CLASS
                        |   NumericType AlphaSquareBrackets PERIOD CLASS
                        |   BOOLEAN AlphaSquareBrackets PERIOD CLASS
                        |   VOID PERIOD CLASS
                        ;
AlphaSquareBrackets     :   /* Epsilon */ 
                        |   OPENBOX CLOSEBOX AlphaSquareBrackets
                        ;
ClassInstanceCreationExpression :   UnqualifiedClassInstanceCreationExpression
                        |   ExpressionName PERIOD UnqualifiedClassInstanceCreationExpression
                        |   Primary PERIOD UnqualifiedClassInstanceCreationExpression
                        ;
UnqualifiedClassInstanceCreationExpression :   NEW BetaTypeArguments ClassOrInterfaceTypeToInstantiate OPENPAREN BetaArgumentList CLOSEPAREN BetaClassBody
                        ;
ClassOrInterfaceTypeToInstantiate :   AlphaAnnotation Identifier AlphaDotAlphaAnnotationIdentifier BetaTypeArgumentsOrDiamond
                        ;
AlphaDotAlphaAnnotationIdentifier :   /* Epsilon */ 
                        |   PERIOD AlphaAnnotation Identifier AlphaDotAlphaAnnotationIdentifier
                        ;
BetaTypeArgumentsOrDiamond :   /* Epsilon */ 
                        |   TypeArgumentsOrDiamond
                        ;
TypeArgumentsOrDiamond  :   TypeArguments
                        |   OPENANGLE CLOSEANGLE
                        ;
FieldAccess             :   Primary PERIOD Identifier 
                        |   SUPER PERIOD Identifier
                        |   TypeName PERIOD SUPER PERIOD Identifier
                        ;
ArrayAccess             :   ExpressionName OPENBOX Expression CLOSEBOX 
                        |   PrimaryNoNewArray OPENBOX Expression CLOSEBOX
                        ;
MethodInvocation        :   MethodName OPENPAREN BetaArgumentList CLOSEPAREN 
                        |   TypeName PERIOD BetaTypeArguments Identifier OPENPAREN BetaArgumentList CLOSEPAREN 
                        |   ExpressionName PERIOD BetaTypeArguments Identifier OPENPAREN BetaArgumentList CLOSEPAREN 
                        |   Primary PERIOD BetaTypeArguments Identifier OPENPAREN BetaArgumentList CLOSEPAREN 
                        |   SUPER PERIOD BetaTypeArguments Identifier OPENPAREN BetaArgumentList CLOSEPAREN 
                        |   TypeName PERIOD SUPER PERIOD BetaTypeArguments Identifier OPENPAREN BetaArgumentList CLOSEPAREN 
                        ;
ArgumentList            :   Expression AlphaCommaExpression
                        ;
AlphaCommaExpression    :   /* Epsilon */ 
                        |   COMMA Expression AlphaCommaExpression
                        ;
MethodReference         :   ExpressionName COLONCOLON BetaTypeArguments Identifier 
                        |   Primary COLONCOLON BetaTypeArguments Identifier 
                        |   ReferenceType COLONCOLON BetaTypeArguments Identifier 
                        |   SUPER COLONCOLON BetaTypeArguments Identifier 
                        |   TypeName PERIOD SUPER COLONCOLON BetaTypeArguments Identifier 
                        |   ClassType COLONCOLON BetaTypeArguments NEW
                        |   ArrayType COLONCOLON NEW
                        ;
ArrayCreationExpression :   NEW PrimitiveType DimExprs BetaDims
                        |   NEW ClassOrInterfaceType DimExprs BetaDims
                        |   NEW PrimitiveType Dims ArrayInitializer
                        |   NEW ClassOrInterfaceTypeToInstantiate Dims ArrayInitializer
                        ;
DimExprs                :   DimExpr AlphaDimExpr
                        ;
AlphaDimExpr            :   /* Epsilon */
                        |   DimExpr AlphaDimExpr
                        ;
DimExpr                 :   AlphaAnnotation OPENBOX Expression CLOSEBOX 
                        ;
Expression              :   LambdaExpression
                        |   AssignmentExpression
                        ;
LambdaExpression        :   LambdaParameters ARROW LambdaBody 
                        ;
LambdaParameters        :   OPENPAREN BetaLambdaParameterList CLOSEPAREN 
                        |   Identifier
                        ;
BetaLambdaParameterList :   /* Epsilon */ 
                        |   LambdaParameterList
                        ;
LambdaParameterList     :   LambdaParameter AlphaCommaLambdaParameter 
                        |   Identifier AlphaCommaIdentifier
                        ;
AlphaCommaLambdaParameter :   /* Epsilon */ 
                        |   COMMA LambdaParameter AlphaCommaLambdaParameter
                        ;
AlphaCommaIdentifier    :   /* Epsilon */ 
                        |   COMMA Identifier AlphaCommaIdentifier
                        ;
LambdaParameter         :   AlphaVariableModifier LambdaParameterType VariableDeclaratorId
                        |   VariableArityParameter
                        ;
LambdaParameterType     :   UnannType
                        |   VAR
                        ;
LambdaBody              :   Expression 
                        |   Block
                        ;
AssignmentExpression    :   ConditionalExpression
                        |   Assignment
                        ;
Assignment              :   LeftHandSide AssignmentOperator Expression
                        ;
LeftHandSide            :   ExpressionName 
                        |   FieldAccess
                        |   ArrayAccess
                        ;
AssignmentOperator      :   EQUALS 
                        |   STAREQUALS
                        |   SLASHEQUALS
                        |   PERCENTEQUALS
                        |   PLUSEQUALS
                        |   MINUSEQUALS
                        |   LESSLESSEQUALS
                        |   GREATERGREATEREQUALS
                        |   GREATERGREATERGREATEREQUALS
                        |   ANDEQUALS
                        |   CARETEQUALS
                        |   PIPEEQUALS
                        ;
ConditionalExpression   :   ConditionalOrExpression 
                        |   ConditionalOrExpression QUESTION Expression COLON ConditionalExpression
                        |   ConditionalOrExpression QUESTION Expression COLON LambdaExpression
                        ;
ConditionalOrExpression :   ConditionalAndExpression
                        |   ConditionalOrExpression PIPEPIPE ConditionalAndExpression
                        ;
ConditionalAndExpression :   InclusiveOrExpression 
                        |   ConditionalAndExpression ANDAND InclusiveOrExpression
                        ;
InclusiveOrExpression   :   ExclusiveOrExpression 
                        |   InclusiveOrExpression PIPE ExclusiveOrExpression
                        ;
ExclusiveOrExpression   :   AndExpression 
                        |   ExclusiveOrExpression CARET AndExpression
                        ;
AndExpression           :   EqualityExpression 
                        |   AndExpression AND EqualityExpression
                        ;
EqualityExpression      :   RelationalExpression 
                        |   EqualityExpression EQUALSEQUALS RelationalExpression
                        |   EqualityExpression NOTEQUALS RelationalExpression
                        ;
RelationalExpression    :   ShiftExpression 
                        |   RelationalExpression OPENANGLE ShiftExpression
                        |   RelationalExpression CLOSEANGLE ShiftExpression
                        |   RelationalExpression LESSEQUALS ShiftExpression
                        |   RelationalExpression GREATEREQUALS ShiftExpression
                        |   InstanceofExpression
                        ;
InstanceofExpression    :   RelationalExpression INSTANCEOF ReferenceType
                        |   RelationalExpression INSTANCEOF Pattern
                        ;
ShiftExpression         :   AdditiveExpression 
                        |   ShiftExpression LESSLESS AdditiveExpression
                        |   ShiftExpression GREATERGREATER AdditiveExpression
                        |   ShiftExpression GREATERGREATERGREATER AdditiveExpression
                        ;
AdditiveExpression      :   MultiplicativeExpression 
                        |   AdditiveExpression PLUS MultiplicativeExpression
                        |   AdditiveExpression MINUS MultiplicativeExpression
                        ;
MultiplicativeExpression :   UnaryExpression 
                        |   MultiplicativeExpression STAR UnaryExpression
                        |   MultiplicativeExpression SLASH UnaryExpression
                        |   MultiplicativeExpression PERCENT UnaryExpression
                        ;
UnaryExpression         :   PreIncrementExpression 
                        |   PreDecrementExpression
                        |   PLUS UnaryExpression
                        |   MINUS UnaryExpression
                        |   UnaryExpressionNotPlusMinus
                        ;
PreIncrementExpression  :   PLUSPLUS UnaryExpression
                        ;
PreDecrementExpression  :   MINUSMINUS UnaryExpression 
                        ;
UnaryExpressionNotPlusMinus :   PostfixExpression 
                        |   TILDE UnaryExpression
                        |   EXCLAMATION UnaryExpression
                        |   CastExpression
                        |   SwitchExpression
                        ;
PostfixExpression       :   Primary 
                        |   ExpressionName
                        |   PostIncrementExpression
                        |   PostDecrementExpression
                        ;
PostIncrementExpression :   PostfixExpression PLUSPLUS 
                        ;
PostDecrementExpression :   PostfixExpression MINUSMINUS 
                        ;
CastExpression          :   OPENPAREN PrimitiveType CLOSEPAREN UnaryExpression 
                        |   OPENPAREN ReferenceType AlphaAdditionalBound CLOSEPAREN UnaryExpressionNotPlusMinus
                        |   OPENPAREN ReferenceType AlphaAdditionalBound CLOSEPAREN LambdaExpression
                        ;
SwitchExpression        :   SWITCH OPENPAREN Expression CLOSEPAREN SwitchBlock
                        ;
ConstantExpression      :   Expression
                        ;


%%

int main()
{
	do
    {
		yyparse();
	}   while(!feof(yyin));
	return 0;
}
void yyerror(const char* s)
{
	fprintf(stderr, "Parse error at line number %d at token: %s::::%s", line, s, yylval);
    return;
	/* exit(1); */
}
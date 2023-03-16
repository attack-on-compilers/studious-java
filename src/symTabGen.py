from symbol_table import *
from pprint import pprint as pprint
from ast import literal_eval

static_init_count = 0
previous_block_count = 0
block_count = 0

def generate_symbol_table(tree):
    global symbol_table
    symbol_table = RootSymbolTable()
    # pprint(tree) 
        
    traverse_tree(tree)
    symbol_table.tprint()
    return

def traverse_tree(tree):
    global symbol_table
    global static_init_count
    global previous_block_count
    global block_count
    

    
    print((tree), '\n')

    print(len(tree))
    if tree[0] == "Assignment":
        
        print('\n', tree[1], '\n')
       
        left = get_expression_Type(tree[1])
        print("Succesfully printing left type", left)
        operator = tree[2][1]
        print('\n', tree[3], '\n')
       
        right = get_expression_Type(tree[3])
        print("Succesfully printing right type", right)

    
    if tree[0] == "AdditiveExpression" and len(tree) ==4:
        print('\n', tree[1], '\n')
       
        left = get_expression_Type(tree[1])
        print("Succesfully printing left type", left)
        operator = tree[2]
        print('\n', tree[3], '\n')
       
        right = get_expression_Type(tree[3])
        print("Succesfully printing right type", right)  

    if tree[0] == "UnaryExpressionNotPlusMinus" and len(tree) ==3:
        
        operator = tree[1]
        print('\n', tree[1], '\n')
       
        right = get_expression_Type(tree[2])
        print("Succesfully printing right type", right)  

    if tree[0] == "PreIncrementExpression" or tree[0] == "PreDecrementExpression":

        operator = tree[1]
        print('\n', tree[1], '\n')
       
        right = get_expression_Type(tree[2])
        print("Succesfully printing right type", right)


    if tree[0] == "PostIncrementExpression" or tree[0] == "PostDecrementExpression":

        operator = tree[2]
        print('\n', tree[2], '\n')
       
        left = get_expression_Type(tree[1])
        print("Succesfully printing left type", left)

    # if tree[0] == "BlockStatement" and len(tree) ==1:
    #     print('\n', tree[1], '\n')
       
    #     left = get_expression_Type(tree[1])
    #     print("Succesfully printing left type", left)
    #     operator = tree[2]
    #     print('\n', tree[3], '\n')
       
    #     right = get_expression_Type(tree[3])
    #     print("Succesfully printing right type", right)       

    if tree[0] == "MethodDeclaration":
        
        if tree[1][2] == "void":
            methodheader_type = tree[1][2]
        else:
            methodheader_type = get_expression_Type(tree[1][2])
        print("Succesfully printing method header type", methodheader_type)

        ##yet to do
        
        # methodbodyreturn_type = get_expression_Type(tree[2][1][2])     ##case semicolon left
        # print("Succesfully printing final return type", methodbodyreturn_type)

    # We perform a depth first traversal of the tree
    match tree[0]:

        case "BetaAlphaTypeDeclaration":
            initial_Traverse(tree)
            traverse_tree(tree[1])

        case "":
            return
        
        case "PackageDeclaration":
            packageName = get_Name(tree[2])
            symbol_table.add_symbol(PackageSymbol(packageName))
        
        case "SingleTypeImportDeclaration":
            importName = get_Name(tree[2])
            symbol_table.add_symbol(ImportSymbol(importName))

        case "TypeImportOnDemandDeclaration":
            importName = get_Name(tree[2]) + ".*"
            symbol_table.add_symbol(ImportSymbol(importName))
        
        case "ClassDeclaration":
            static_init_count = 0
            className = tree[3]
            symbol_table.enter_scope(className)
            traverse_tree(tree[6])
            symbol_table.exit_scope()

        case "MethodDeclaration":
            methodName = get_Name(tree[1][3])
            methodParams = []
            if len(tree[1][3]) == 5:
                methodParams = get_Parameters(tree[1][3][3])
            methodSignature = methodName + "(" 
            for i in methodParams:
                methodSignature += i[0] + ","
            methodSignature += ")"
            symbol_table.enter_scope(methodSignature)
            for i in methodParams:
                fieldModifiers = []
                fieldType = i[0]
                dims = 0
                if fieldType[-1] == "]":
                    dims = fieldType.count("[")
                    fieldType = fieldType[:fieldType.find("[")]
                symbol_table.add_symbol(VariableSymbol(i[1], fieldType, [], dims))
            traverse_tree(tree[2])
            symbol_table.exit_scope()

        case "StaticInitializer":
            static_init_count += 1
            static_init_name = "<static_init_" + str(static_init_count) + ">"
            symbol_table.add_symbol(MethodSymbol(static_init_name, "void", symbol_table.current, [], []))
            symbol_table.enter_scope(static_init_name)
            traverse_tree(tree[2])
            symbol_table.exit_scope()

        case "ConstructorDeclaration":
            constructorName = get_Name(tree[2][1])
            constructorParams = get_Parameters(tree[2][3])
            constructorSignature = constructorName + "("
            for i in constructorParams:
                constructorSignature += i[0] + ","
            constructorSignature += ")"
            symbol_table.enter_scope(constructorSignature)
            for i in constructorParams:
                fieldModifiers = []
                fieldType = i[0]
                dims = 0
                if fieldType[-1] == "]":
                    dims = fieldType.count("[")
                    fieldType = fieldType[:fieldType.find("[")]
                symbol_table.add_symbol(VariableSymbol(i[1], fieldType, [], dims))
            traverse_tree(tree[4])
            symbol_table.exit_scope()


        case "InterfaceDeclaration":
            interfaceName = tree[3]
            symbol_table.enter_scope(interfaceName)
            traverse_tree(tree[5])
            symbol_table.exit_scope()

        case "AbstractMethodDeclaration":
            methodName = get_Name(tree[1][3])
            methodParams = []
            if len(tree[1][3]) == 5:
                methodParams = get_Parameters(tree[1][3][3])
            methodSignature = methodName + "(" 
            for i in methodParams:
                methodSignature += i[0] + ","
            methodSignature += ")"
            symbol_table.enter_scope(methodSignature)
            for i in methodParams:
                fieldModifiers = []
                fieldType = i[0]
                dims = 0
                if fieldType[-1] == "]":
                    dims = fieldType.count("[")
                    fieldType = fieldType[:fieldType.find("[")]
                symbol_table.add_symbol(VariableSymbol(i[1], fieldType, [], dims))
            symbol_table.exit_scope()

        case "LocalVariableDeclaration":
            fieldType = get_Type(tree[1])
            dims = 0
            if fieldType[-1] == "]":
                dims = fieldType.count("[")
                fieldType = fieldType[:fieldType.find("[")]
            fieldVariables = get_Variables(tree[2])
            for i in fieldVariables:
                symbol_table.add_symbol(VariableSymbol(i, fieldType, [], dims))

        case "StatementWithoutTrailingSubstatement":
            match tree[1][0]:
                case "Block":
                    block_count += 1
                    previous_block_count = block_count
                    symbol_table.add_symbol(BlockSymbol("block"+str(block_count), symbol_table.current))
                    symbol_table.enter_scope("block"+str(block_count))
                    block_count = 0
                    traverse_tree(tree[1])
                    symbol_table.exit_scope()
                    block_count = previous_block_count
                case _:
                    traverse_tree(tree[1])
            
        case _:
            if type(tree) == tuple:
                for i in range(1, len(tree)):
                    traverse_tree(tree[i])

def initial_Traverse(tree):
    # A separate traversal to get the class body declarations and interface body declarations
    global symbol_table

    
        
    match tree[0]:

        case "":
            return
        
        case "BetaAlphaTypeDeclaration":
            initial_initial_Traverse(tree)
            initial_Traverse(tree[1])
        
        case "ClassDeclaration":
            className = tree[3]
            symbol_table.enter_scope(className)
            initial_Traverse(tree[6])
            symbol_table.exit_scope()

        case "InterfaceDeclaration":
            interfaceName = tree[3]
            symbol_table.enter_scope(interfaceName)
            initial_Traverse(tree[5])
            symbol_table.exit_scope()

        case "FieldDeclaration":
            fieldModifiers = get_Modifiers(tree[1])
            fieldType = get_Type(tree[2])
            dims = 0
            if fieldType[-1] == "]":
                dims = fieldType.count("[")
                fieldType = fieldType[:fieldType.find("[")]
            fieldVariables = get_Variables(tree[3])
            for i in fieldVariables:
                symbol_table.add_symbol(VariableSymbol(i, fieldType, fieldModifiers, dims))
            

        case "MethodDeclaration":
            methodModifiers = get_Modifiers(tree[1][1])
            if tree[1][2] == "void":
                methodReturnType = "void"
            else:
                methodReturnType = get_Type(tree[1][2])
            methodName = get_Name(tree[1][3])
            methodParams = []
            if len(tree[1][3]) == 5:
                methodParams = get_Parameters(tree[1][3][3])
            methodThrows = get_Exceptions(tree[1][4])
            methodSignature = methodName + "(" 
            for i in methodParams:
                methodSignature += i[0] + ","
            methodSignature += ")"
            symbol_table.add_symbol(MethodSymbol(methodSignature, methodReturnType, symbol_table.current, methodModifiers, methodThrows))

        case "StaticInitializer":
            return

        case "ConstructorDeclaration":
            constructorModifiers = get_Modifiers(tree[1])
            constructorName = get_Name(tree[2][1])
            constructorParams = get_Parameters(tree[2][3])
            constructorThrows = get_Exceptions(tree[3])
            constructorSignature = constructorName + "("
            for i in constructorParams:
                constructorSignature += i[0] + ","
            constructorSignature += ")"
            symbol_table.add_symbol(MethodSymbol(constructorSignature, None, symbol_table.current, constructorModifiers, constructorThrows))

        case "AbstractMethodDeclaration":
            methodModifiers = get_Modifiers(tree[1][1])
            if tree[1][2] == "void":
                methodReturnType = "void"
            else:
                methodReturnType = get_Type(tree[1][2])
            methodName = get_Name(tree[1][3])
            methodParams = []
            if len(tree[1][3]) == 5:
                methodParams = get_Parameters(tree[1][3][3])
            methodThrows = get_Exceptions(tree[1][4])
            methodSignature = methodName + "(" 
            for i in methodParams:
                methodSignature += i[0] + ","
            methodSignature += ")"
            symbol_table.add_symbol(MethodSymbol(methodSignature, methodReturnType, symbol_table.current, methodModifiers, methodThrows))
        
        case _:
            if type(tree) == tuple:
                for i in range(1, len(tree)):
                    initial_Traverse(tree[i])

def initial_initial_Traverse(tree):
    # A separate traversal to get the class names and interface names
    global symbol_table
    match tree[0]:

        case "":
            return
        
        case "ClassDeclaration":
            className = tree[3]
            classModifiers = get_Modifiers(tree[1])
            classParent = get_Parent(tree[4])
            classInterfaces = get_Interfaces(tree[5])
            symbol_table.add_symbol(ClassSymbol(className, symbol_table.current, classModifiers, classParent, classInterfaces))

        case "InterfaceDeclaration":
            interfaceName = tree[3]
            interfaceModifiers = get_Modifiers(tree[1])
            interfaceInterfaces = get_Interfaces(tree[4])
            symbol_table.add_symbol(InterfaceSymbol(interfaceName, symbol_table.current, interfaceModifiers, interfaceInterfaces))

        case _:
            if type(tree) == tuple:
                for i in range(1, len(tree)):
                    initial_initial_Traverse(tree[i])
        
        


def get_Name(tree):
    match tree[0]:
        case "Name":
            return get_Name(tree[1])
        case "IdentifierId":
            return tree[1]
        case "NameDotIdentifierId":
            return get_Name(tree[1]) + "." + tree[3]
        case "InterfaceType":
            return get_Name(tree[1])
        case "ClassOrInterfaceType":
            return get_Name(tree[1])
        case "ClassType":
            return get_Name(tree[1])
        case "VariableDeclaratorId":
            match len(tree):
                case 2:
                    return tree[1]
                case 4:
                    return tree[1] + "[]"
        case "MethodDeclarator":
            if len(tree) == 5:
                return tree[1]
            else:
                return get_Name(tree[1])
        
def get_Type(tree):
    match tree[0]:
        case "Type":
            return get_Type(tree[1])
        case "PrimitiveType":
            match tree[1]:
                case "boolean":
                    return "boolean"
            return get_Type(tree[1])
        case "NumericType":
            return get_Type(tree[1])
        case "IntegralType":
            return tree[1]
        case "FloatingPointType":
            return tree[1]
        case "ReferenceType":
            return get_Type(tree[1])
        case "ClassOrInterfaceType":
            return get_Name(tree[1])
        case "ArrayType":
            match tree[1][0]:
                case "Name":
                    return get_Name(tree[1]) + "[]"
            return get_Type(tree[1]) + "[]"

        
def get_Modifiers(tree):
    match tree[0]:
        case "BetaAlphaModifier":
            return get_Modifiers(tree[1])
        case "":
            return []
        case "AlphaModifier":
            if len(tree) == 2:
                return get_Modifiers(tree[1])
            else:
                return get_Modifiers(tree[1]) + get_Modifiers(tree[2])
        case "Modifier":
            return [tree[1]]

def get_Parent(tree):
    match tree[0]:
        case "BetaSuper":
            return get_Parent(tree[1])
        case "Super":
            return get_Name(tree[2])
        
def get_Interfaces(tree):
    match tree[0]:
        case "BetaAlphaInterface":
            return get_Interfaces(tree[1])
        case "AlphaInterface":
            return get_Interfaces(tree[2])
        case "InterfaceTypeList":
            if len(tree) == 2:
                return get_Interfaces(tree[1])
            else:
                return get_Interfaces(tree[1]) + get_Interfaces(tree[3])
        case "InterfaceType":
            return [get_Name(tree[1])]
        case "BetaExtendsAlphaInterface":
            if tree[1] == "":
                return []
            else:
                return get_Interfaces(tree[1])
        case "ExtendsAlphaInterface":
            if len(tree) == 2:
                return get_Interfaces(tree[1])
            else:
                return get_Interfaces(tree[1]) + get_Interfaces(tree[3])


def get_Exceptions(tree):
    match tree[0]:
        case "BetaAlphaThrow":
            if tree[1] == "":
                return []
            else:
                return get_Exceptions(tree[1])
        case "AlphaThrow":
            return get_Exceptions(tree[2])
        case "ClassTypeList":
            if len(tree) == 2:
                return [get_Name(tree[1])]
            else:
                return get_Exceptions(tree[1]) + [get_Name(tree[3])]
        case _:
            return []
        
def get_Variables(tree):
    match tree[0]:
        case "AlphaVariableDeclarator":
            if len(tree) == 2:
                return get_Variables(tree[1])
            else:
                return get_Variables(tree[1]) + get_Variables(tree[3])
        case "VariableDeclarator":
            if len(tree) == 2:
                return [get_Name(tree[1])]
            else:
                # traverse_tree(tree)
                # Need to add traverse logic for VariableDeclaratorId : VariableDeclaratorId ASSIGN Expression
                return [get_Name(tree[1])]

def get_Parameters(tree):
    match tree[0]:
        case "BetaFormalParameterList":
            if tree[1] == "":
                return []
            else:
                return get_Parameters(tree[1])
        case "FormalParameterList":
            if len(tree) == 2:
                return get_Parameters(tree[1])
            else:
                return get_Parameters(tree[1]) + get_Parameters(tree[3])
        case "FormalParameter":
            parameterType = get_Type(tree[1])
            parameterName = get_Name(tree[2])
            return [[parameterType, parameterName]]
        case _:
            return []


def type_check(left, op, right):
    # print("inside type check", left)
    # left_type = get_expression_Type(get_Name(left[1]))
    # print("inside type check", right)
    # right_type = get_expression_Type(get_Terminal(right[1]))
    # check if left and right types are the same
    # if left_type != right_type or left_type == False or right_type == False:
    #     print(f"Type Error: Incompatible types")
    #     #raise Exception
    #     return False
    
    # if both types are compatible and operator is supported, return True
    return True

def string_to_type(expression):

    try:
         literal_type = literal_eval(expression)
         return type(literal_type).__name__ 
    except:
        return type(expression).__name__

###yet to complete
def get_expression_Type(expression):
    print("This is", expression[0])

    match expression[0]:
        case "LeftHandSide":
            return get_expression_Type(expression[1])
        case "FieldAccess":
            pass

        case "ArrayAccess":
            pass

        case "Name":  
            return get_expression_Type(expression[1])
        case "IdentifierId":
            #print("inside identifier", expression[0])
            return symbol_table.get_symbol(expression[1]).data_type 
            # symbol = symbol_table.get_symbol(expression)
            # print('hiiii', symbol)
            # if symbol is None:
            #     print(f"Type Error: Symbol {expression} not found in symbol table")
            #     return None
            # else:
            #     return symbol.data_type
        case "AssignmentExpression":
            return get_expression_Type(expression[1])
        case "ConditionalExpression":
            return get_expression_Type(expression[1])
        case "ConditionalOrExpression":
            return get_expression_Type(expression[1])
        case "ConditionalAndExpression":
            return get_expression_Type(expression[1])
        case "InclusiveOrExpression":
            return get_expression_Type(expression[1])
        case "ExclusiveOrExpression":
            return get_expression_Type(expression[1])
        case "AndExpression":
            return get_expression_Type(expression[1])
        case "EqualityExpression":
            return get_expression_Type(expression[1])
        case "RelationalExpression":
            return get_expression_Type(expression[1])
        case "ShiftExpression":
            return get_expression_Type(expression[1])
        case "AdditiveExpression":
            return get_expression_Type(expression[1])
        case "MultiplicativeExpression":
            return get_expression_Type(expression[1])
        case "UnaryExpression":
            return get_expression_Type(expression[1])
        case "PreIncrementExpression":
            return get_expression_Type(expression[2])
        case "PreDecrementExpression":
            return get_expression_Type(expression[2])
        case "UnaryExpressionNotPlusMinus":
            if(len(expression) == 3):
                return get_expression_Type(expression[2])
            else:                                                             
                return get_expression_Type(expression[1])
        case "PostfixExpression":
            return get_expression_Type(expression[1])
        case "PostIncrementExpression":
            return get_expression_Type(expression[1])
        case "PostDecrementExpression":
            return get_expression_Type(expression[1])
        case "CastExpression":
            return get_expression_Type(expression[1])
        case "Primary":
            return get_expression_Type(expression[1])
        case "PrimaryNoNewArray":
            return get_expression_Type(expression[1])
        case "PrimaryArrayCreationExpression":
            return get_expression_Type(expression[1])
        case "Literal":
            return string_to_type(expression[1])
            
        case "THIS":
            pass
        case "LEFT_PAREN Expression RIGHT_PAREN":
            pass
        case "ClassInstanceCreationExpression":
            pass
        case "FieldAccess":
            pass
        case "MethodInvocation":
            pass
        case "ArrayAccess":
            pass
        case "Type":
            return get_Type(expression[1])
        case "BetaAlphaBlockStatement":
            return get_expression_Type(expression[1])
        case "AlphaBlockStatement":
            return get_expression_Type(expression[2])
        case "BlockStatement":
            return get_expression_Type(expression[1])
        case "LocalVariableDeclarationStatement":
            pass
        case "Statement":
            return get_expression_Type(expression[1])
        case "StatementWithoutTrailingSubstatement":
            return get_expression_Type(expression[1])
        case "ReturnStatement":
            return get_expression_Type(expression[2])
        case "BetaExpression":
            return get_expression_Type(expression[1])
        case "Expression":
            return get_expression_Type(expression[1])
        # case "TILDE":
        #     return get_expression_Type(expression[1])   
        # case "EXCLAMATION":
        #     return get_expression_Type(expression[1]) 
    

    


    #print("\n yooooooo", get_Type(expression))

    if isinstance(expression, str):
        symbol = symbol_table.get_symbol(expression)
        print('hiiii', symbol)
        if symbol is None:
            print(f"Type Error: Symbol {expression} not found in symbol table")
            return None
        else:
            return symbol.data_type


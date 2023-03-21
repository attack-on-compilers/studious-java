from symbol_table import *
from pprint import pprint as pprint
from tac import TAC
from lexer import *
from utils import *

static_init_count = 0
previous_block_count = 0
block_count = 0

global symbol_table
symbol_table = RootSymbolTable()

global tac
tac = TAC()


def generate_symbol_table(tree):
    # pprint(tree)

    traverse_tree(tree)
    symbol_table.tprint()
    tac.tprint()
    return


def traverse_tree(tree):
    global static_init_count
    global previous_block_count
    global block_count

    if tree[0] == "Assignment":
        left = get_expression_Type(tree[1])
        operator = tree[2][1]
        right = get_expression_Type(tree[3])

        binop_type_check(left, operator, right, tree[0])

    if tree[0] == "AdditiveExpression" and len(tree) == 4:
        left = get_expression_Type(tree[1])
        operator = tree[2]
        right = get_expression_Type(tree[3])

        binop_type_check(left, operator, right, tree[0])

    if tree[0] == "MultiplicativeExpression" and len(tree) == 4:
        left = get_expression_Type(tree[1])
        operator = tree[2]
        right = get_expression_Type(tree[3])

        binop_type_check(left, operator, right, tree[0])

    if tree[0] == "UnaryExpressionNotPlusMinus" and len(tree) == 3:
        operator = tree[1]
        right = get_expression_Type(tree[2])

        unop_type_check(operator, right, tree[0])

    if tree[0] == "PreIncrementExpression" or tree[0] == "PreDecrementExpression":
        operator = tree[1]
        right = get_expression_Type(tree[2])

        unop_type_check(operator, right, tree[0])

    if tree[0] == "PostIncrementExpression" or tree[0] == "PostDecrementExpression":
        operator = tree[2]
        left = get_expression_Type(tree[1])

        unop_type_check(operator, left, tree[0])

    if tree[0] == "ReturnStatement":
        methodreturn_type = get_expression_Type(tree[2])
        methodheader_type = symbol_table.get_method_symbol()

        method_type_check(methodreturn_type, methodheader_type)

    if tree[0] == "MethodInvocation":
        method_check(tree)
    
    # if tree[0] == "ClassInstanceCreationExpression":
        
    #     print("kokki")
    #     methodInvocationName = get_expression_Type(tree[2])

    #     print("gyggy", methodInvocationName)


    if tree[0] == "ShiftExpression" and len(tree) == 4:
        operator = tree[2]
        left = get_expression_Type(tree[1])
        right = get_expression_Type(tree[3])

        binop_type_check(left, operator, right, tree[0])

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
            tac.add_label(className)
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
            method_sym_name = symbol_table.get_symbol_name(methodName)
            tac.add_label(method_sym_name)
            symbol_table.enter_scope(methodName)
            for i in methodParams:
                fieldModifiers = []
                fieldType = i[0]
                dims = 0
                if fieldType[-1] == "]":
                    dims = fieldType.count("[")
                    fieldType = fieldType[: fieldType.find("[")]
                symbol_table.add_symbol(VariableSymbol(i[1], fieldType, VariableScope.PARAMETER, dims))
                tac.add_param(symbol_table.get_symbol_name(i[1]))
            traverse_tree(tree[2][1][2])
            symbol_table.exit_scope()

        case "StaticInitializer":
            static_init_count += 1
            static_init_name = "<static_init_" + str(static_init_count) + ">"
            symbol_table.add_symbol(MethodSymbol(static_init_name, static_init_name, [], "void", symbol_table.current, [], []))
            symbol_table.enter_scope(static_init_name)
            traverse_tree(tree[2][2])
            symbol_table.exit_scope()

        case "ConstructorDeclaration":
            constructorName = get_Name(tree[2][1])
            constructorParams = get_Parameters(tree[2][3])
            constructorSignature = constructorName + "("
            for i in constructorParams:
                constructorSignature += i[0] + ","
            constructorSignature += ")"
            symbol_table.enter_scope(constructorName)
            for i in constructorParams:
                fieldModifiers = []
                fieldType = i[0]
                dims = 0
                if fieldType[-1] == "]":
                    dims = fieldType.count("[")
                    fieldType = fieldType[: fieldType.find("[")]
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
                    fieldType = fieldType[: fieldType.find("[")]
                symbol_table.add_symbol(VariableSymbol(i[1], fieldType, [], dims))
            symbol_table.exit_scope()

        case "LocalVariableDeclaration":
            fieldType = get_Type(tree[1])
            dims = 0
            if fieldType[-1] == "]":
                dims = fieldType.count("[")
                fieldType = fieldType[: fieldType.find("[")]
            fieldVariables = get_Variables(tree[2])
            for i in fieldVariables:
                newi = i
                if i[-1] == "]":
                    dims = i.count("[")
                    newi = i[: i.find("[")]
                symbol_table.add_symbol(VariableSymbol(newi, fieldType, [], dims))
            post_type_check(tree)

        case "Block":
            block_count += 1
            previous_block_count = block_count
            symbol_table.add_symbol(BlockSymbol("block" + str(block_count), symbol_table.current))
            symbol_table.enter_scope("block" + str(block_count))
            traverse_tree(tree[2])
            symbol_table.exit_scope()

        case "ForStatement":
            block_count += 1
            previous_block_count = block_count
            symbol_table.add_symbol(BlockSymbol("block" + str(block_count), symbol_table.current))
            symbol_table.enter_scope("block" + str(block_count))
            traverse_tree(tree[3])
            traverse_tree(tree[5])
            traverse_tree(tree[7])
            if tree[9][1][0] == "StatementWithoutTrailingSubstatement" and tree[9][1][1][0] == "Block":
                traverse_tree(tree[9][1][1][2])
            else:
                traverse_tree(tree[9])
            symbol_table.exit_scope()

        case "ForStatementNoShortIf":
            block_count += 1
            previous_block_count = block_count
            symbol_table.add_symbol(BlockSymbol("block" + str(block_count), symbol_table.current))
            symbol_table.enter_scope("block" + str(block_count))
            traverse_tree(tree[3])
            traverse_tree(tree[5])
            traverse_tree(tree[7])
            if tree[9][1][0] == "StatementWithoutTrailingSubstatement" and tree[9][1][1][0] == "Block":
                traverse_tree(tree[9][1][1][2])
            else:
                traverse_tree(tree[9])
            symbol_table.exit_scope()

        case "SwitchBlock":
            block_count += 1
            previous_block_count = block_count
            symbol_table.add_symbol(BlockSymbol("switch_block" + str(block_count), symbol_table.current))
            symbol_table.enter_scope("switch_block" + str(block_count))
            traverse_tree(tree[2])
            traverse_tree(tree[3])
            symbol_table.exit_scope()
        case _:
            if type(tree) == tuple:
                for i in range(1, len(tree)):
                    traverse_tree(tree[i])


def initial_Traverse(tree):
    # A separate traversal to get the class body declarations and interface body declarations

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
                fieldType = fieldType[: fieldType.find("[")]
            fieldVariables = get_Variables(tree[3])
            for i in fieldVariables:
                newi = i
                if i[-1] == "]":
                    dims = i.count("[")
                    newi = i[: i.find("[")]
                symbol_table.add_symbol(VariableSymbol(newi, fieldType, fieldModifiers, dims))

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
            methodParamTypes = []
            for i in methodParams:
                methodSignature += i[0] + ","
                methodParamTypes.append(i[0])
            methodSignature += ")"
            symbol_table.add_symbol(
                MethodSymbol(
                    methodName,
                    methodSignature,
                    methodParamTypes,
                    methodReturnType,
                    symbol_table.current,
                    methodModifiers,
                    methodThrows,
                )
            )

        case "StaticInitializer":
            return

        case "ConstructorDeclaration":
            constructorModifiers = get_Modifiers(tree[1])
            constructorName = get_Name(tree[2][1])
            constructorParams = get_Parameters(tree[2][3])
            constructorThrows = get_Exceptions(tree[3])
            constructorSignature = constructorName + "("
            constructorParamTypes = []
            for i in constructorParams:
                constructorSignature += i[0] + ","
                constructorParamTypes.append(i[0])
            constructorSignature += ")"
            symbol_table.add_symbol(
                MethodSymbol(
                    constructorName,
                    constructorSignature,
                    constructorParamTypes,
                    None,
                    symbol_table.current,
                    constructorModifiers,
                    constructorThrows,
                )
            )

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
            symbol_table.add_symbol(
                MethodSymbol(
                    methodName,
                    methodSignature,
                    methodParams,
                    methodReturnType,
                    symbol_table.current,
                    methodModifiers,
                    methodThrows,
                )
            )

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


def post_type_check(expression):
    match expression[0]:
        case "LocalVariableDeclaration":
            temp = expression[2]
            if len(temp) == 4:
                post_type_check(temp[3])
                post_type_check(temp[1])
            else:
                post_type_check(temp[1])
        case "VariableDeclarator":
            if len(expression) == 2:
                pass
            else:
                left = get_expression_Type(expression[1])
                right = get_expression_Type(expression[3])
                binop_type_check(left, "=", right, expression)

        case "VariableInitializer":
            get_expression_Type(expression[1])

        case "AlphaVariableDeclarator":
            if len(expression) == 2:
                post_type_check(expression[1])
            else:
                post_type_check(expression[1])
                post_type_check(expression[3])

        case _:
            pass

def method_check(expression):
    if len(expression) == 5:
            methodInvocationName = get_Name(expression[1])

            if methodInvocationName == "System.out.println":
                pass
            else:
                methodcalledtype = symbol_table.get_symbol_name(methodInvocationName)
                methodInvocationParams = []
                newtree = expression[3]
                if newtree[1] == "":
                    methodInvocationParams = []
                else:
                    newtree = newtree[1]
                    while len(newtree) == 4:
                        methodInvocationParams.append(get_expression_Type(newtree[3]))
                        newtree = newtree[1]
                    methodInvocationParams.append(get_expression_Type(newtree[1]))
                    methodInvocationParams.reverse()
                arr = methodcalledtype.params
                if len(methodInvocationParams) != len(arr):
                    raise Exception("Error: Method Invocation Parameters don't match the method declaration")
                else:
                    for i in range(len(methodInvocationParams)):
                        big_method(methodInvocationParams[i], arr[i])

    elif len(expression) == 7:
        pass

###yet to complete
def get_expression_Type(expression):
    match expression[0]:
        case "LeftHandSide":
            return get_expression_Type(expression[1])
        case "FieldAccess":
            pass

        case "ArrayAccess":
            t = get_expression_Type(expression[3])
            if t != "int":
                raise Exception("Array index must be of type int")
            if expression[1][0] == "Name":
                return symbol_table.get_symbol(get_Name(expression[1])).data_type
            else:
                return get_expression_Type(expression[1])

        case "ArrayCreationExpression":
            return get_Type(expression[2])

        case "ClassInstanceCreationExpression":
            return get_expression_Type(expression[2])

        case "Name":
            return get_expression_Type(expression[1])
        case "IdentifierId":
            return symbol_table.get_symbol(expression[1]).data_type
        case "Expression":
            return get_expression_Type(expression[1])
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
            if len(expression) == 2:
                return get_expression_Type(expression[1])
            else:
                t1 = get_expression_Type(expression[1])
                t2 = get_expression_Type(expression[3])
                return big(t1, t2)
        case "MultiplicativeExpression":
            if len(expression) == 2:
                return get_expression_Type(expression[1])
            else:
                t1 = get_expression_Type(expression[1])
                t2 = get_expression_Type(expression[3])
                return big(t1, t2)
        case "UnaryExpression":
            if len(expression) == 3:
                return get_expression_Type(expression[2])
            else:
                return get_expression_Type(expression[1])
        case "PreIncrementExpression":
            return get_expression_Type(expression[2])
        case "PreDecrementExpression":
            return get_expression_Type(expression[2])
        case "UnaryExpressionNotPlusMinus":
            if len(expression) == 3:
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
            if len(expression) == 4:
                return get_expression_Type(expression[2])
            else:
                return get_expression_Type(expression[1])
        case "ArrayCreationExpression":
            pass
        case "Literal":
            return string_to_type(expression[1])
        case "ClassType":
            return get_expression_Type(expression[1])
        case "ClassOrInterfaceType":
            return get_Name(expression[1])
        case "BetaArgumentList":
            pass
        case "ArgumentList":
            if len(expression) == 4:
                return get_expression_Type(expression[4])
            else:
                return get_expression_Type(expression[1])
        case "FieldAccess":
            pass
        case "MethodInvocation":
            method_check(expression)
            if len(expression) == 5:
                methodInvocationName = get_Name(expression[1])
                if methodInvocationName == "System.out.println":
                    pass
                else:
                    return symbol_table.get_symbol_name(methodInvocationName).return_type
            elif len(expression) == 7:
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
            return get_expression_Type(expression[1])
        case "Statement":
            return get_expression_Type(expression[1])
        case "StatementWithoutTrailingSubstatement":
            return get_expression_Type(expression[1])
        case "ExpressionStatement":
            return get_expression_Type(expression[1])
        case "StatementExpression":
            return get_expression_Type(expression[1])
        case "ReturnStatement":
            return get_expression_Type(expression[2])
        case "BetaExpression":
            return get_expression_Type(expression[1])
        case "Expression":
            return get_expression_Type(expression[1])
        case "VariableInitializer":
            return get_expression_Type(expression[1])
        case "VariableDeclarator":
            return get_expression_Type(expression[1])
        case "VariableDeclaratorId":
            if len(expression) == 2:
                return symbol_table.get_symbol(expression[1]).data_type
            else:
                return get_expression_Type(expression[1])
        case "VariableDeclaratorInitializer":
            return get_expression_Type(expression[1])
        case "Block":
            return get_expression_Type(expression[2])
        case "BetaAlphaBlockStatement":
            return get_expression_Type(expression[1])
        # case "AlphaBlockStatement":
        #     return get_expression_Type(expression[1])
        # case "BlockStatement":
        #     return get_expression_Type(expression[1])

        ##case need to add logic for variabledeclator
        # case "FormalParameterList":
        #     if len(expression) == 4:
        #         return get_expression_Type(expression[3])
        #     else:
        #         return get_expression_Type(expression[1])
        # case "FormalParameter":
        #     return get_expression_Type(expression[1])
        case _:
            pass

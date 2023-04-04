from pprint import pprint
from symbol_table import *
from lexer import *
from utils import *
from tac import *

static_init_count = 0
previous_block_count = 0
block_count = 0

global symbol_table
symbol_table = RootSymbolTable()

global tac
tac = TAC()

offset = [0]


def generate_symbol_table(tree, args):
    if args.verbose:
        print("Generating Symbol Table")

    traverse_tree(tree)
    if args.verbose:
        print("Symbol Table:")
        symbol_table.tprint()
    with open("{}.csv".format(args.output), mode="w") as sys.stdout:
        symbol_table.tprint()
    sys.stdout = sys.__stdout__
    print("Symbol Table generated: {}.csv".format(args.output))

    symbol_table.fprint(args.output)

    global block_count
    block_count = 0
    print("Generating TAC")
    generate_tac(tree)
    if args.verbose:
        print("TAC:")
        tac.tprint()

    with open("{}.txt".format(args.output), mode="w") as sys.stdout:
        tac.tprint()
    sys.stdout = sys.__stdout__
    print("TAC generated: {}.txt".format(args.output))


def traverse_tree(tree):
    global static_init_count
    global previous_block_count
    global block_count
    global offset

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

    if tree[0] == "ClassInstanceCreationExpression":
        constructor_check(tree)

    if tree[0] == "ShiftExpression" and len(tree) == 4:
        operator = tree[2]
        left = get_expression_Type(tree[1])
        right = get_expression_Type(tree[3])

        binop_type_check(left, operator, right, tree[0])

    if tree[0] == "RelationalExpression" and len(tree) == 4 and tree[2] != "instanceof":
        operator = tree[2]
        left = get_expression_Type(tree[1])
        right = get_expression_Type(tree[3])
        binop_type_check(left, operator, right, tree[0])

    if tree[0] == "EqualityExpression" and len(tree) == 4:
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
            traverse_tree(tree[6])
            symbol_table.exit_scope()

        case "MethodDeclaration":
            methodName = get_Name(tree[1][3])
            methodParams = []
            if len(tree[1][3]) == 5:
                methodParams = get_Parameters(tree[1][3][3])
            methodSignature = methodName + "("
            for i in methodParams:
                methodSignature += i[0].split("[")[0] + ","
            methodSignature += ")"
            method_sym_name = symbol_table.get_symbol_name(methodName)
            symbol_table.enter_scope(methodName)
            offset = offset + [0]
            symbol_table.add_symbol(VariableSymbol("this", symbol_table.current.parent.name[:-13], 8, 0, [], 0, []))
            offset[-1] = offset[-1] + 8
            for i in methodParams:
                fieldModifiers = []
                fieldType = i[0]
                dims = 0
                if fieldType[-1] == "]":
                    dims = fieldType.count("[")
                    fieldType = fieldType[: fieldType.find("[")]
                newdims = dims + i[1].count("[")
                if i[1][-1] == "]":
                    # if dims == 0:
                    #     dims = i[1].count("[")
                    i[1] = i[1][: i[1].find("[")]
                symbol_table.add_symbol(
                    VariableSymbol(i[1], fieldType, get_TypeSize(fieldType), offset[-1], [VariableScope.PARAMETER], newdims, [])
                )
                offset[-1] = offset[-1] + get_TypeSize(fieldType)
            traverse_tree(tree[2][1][2])
            symbol_table.exit_scope()
            offset.pop()

        case "StaticInitializer":
            static_init_count += 1
            static_init_name = "<static_init_" + str(static_init_count) + ">"
            symbol_table.add_symbol(MethodSymbol(static_init_name, static_init_name, [], "void", symbol_table.current, [], []))
            symbol_table.enter_scope(static_init_name)
            offset = offset + [0]
            traverse_tree(tree[2][2])
            symbol_table.exit_scope()
            offset.pop()

        case "ConstructorDeclaration":
            constructorName = get_Name(tree[2][1])
            constructorParams = get_Parameters(tree[2][3])
            constructorSignature = constructorName + "("
            for i in constructorParams:
                constructorSignature += i[0] + ","
            constructorSignature += ")"
            symbol_table.enter_scope(constructorName)
            offset = offset + [0]
            symbol_table.add_symbol(VariableSymbol("this", symbol_table.current.parent.name[:-13], 8, 0, [], 0, []))
            offset[-1] = offset[-1] + 8
            for i in constructorParams:
                fieldModifiers = []
                fieldType = i[0]
                dims = 0
                if fieldType[-1] == "]":
                    dims = fieldType.count("[")
                    fieldType = fieldType[: fieldType.find("[")]
                newdims = dims + i[1].count("[")
                if i[1][-1] == "]":
                    # if dims == 0:
                    #     dims = i[1].count("[")
                    i[1] = i[1][: i[1].find("[")]
                symbol_table.add_symbol(VariableSymbol(i[1], fieldType, get_TypeSize(fieldType), offset[-1], [VariableScope.PARAMETER], newdims, []))
                offset[-1] = offset[-1] + get_TypeSize(fieldType)
            traverse_tree(tree[4])
            symbol_table.exit_scope()
            offset.pop()

        case "InterfaceDeclaration":
            interfaceName = tree[3]
            symbol_table.enter_scope(interfaceName)
            offset = offset + [0]
            traverse_tree(tree[5])
            symbol_table.exit_scope()
            offset.pop()

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
            offset = offset + [0]
            for i in methodParams:
                fieldModifiers = []
                fieldType = i[0]
                dims = 0
                if fieldType[-1] == "]":
                    dims = fieldType.count("[")
                    fieldType = fieldType[: fieldType.find("[")]
                symbol_table.add_symbol(VariableSymbol(i[1], fieldType, get_TypeSize(fieldType), offset[-1], [], dims, []))
                offset[-1] = offset[-1] + get_TypeSize(fieldType)
            symbol_table.exit_scope()
            offset.pop()

        case "LocalVariableDeclaration":
            fieldType = get_Type(tree[1])
            dims = 0
            if fieldType[-1] == "]":
                dims = fieldType.count("[")
                fieldType = fieldType[: fieldType.find("[")]
            typeSize = get_TypeSize(fieldType)
            fieldVariables = get_Variables(tree[2])
            variablesizes = get_NumberOfElements(tree[2])
            arraydimensions = get_ArrayDimensions(tree[2])
            # print("AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA",arraydimensions)
            count = 0
            for i in fieldVariables:
                newi = i
                tempdims = dims + i.count("[")
                if i[-1] == "]":
                    # if dims == 0:
                    newi = i[: i.find("[")]
                symbol_table.add_symbol(VariableSymbol(newi, fieldType, typeSize * variablesizes[count], offset[-1], [], tempdims, arraydimensions[count]))
                offset[-1] = offset[-1] + typeSize * variablesizes[count]
                count += 1
            post_type_check(tree)
            normalTypes = ["int", "char", "boolean", "float", "double", "long", "short", "byte", "String"]
            if fieldType not in normalTypes:
                for i in symbol_table.root.get_symbol(fieldType).symbol_table.symbols.values():
                    if not i.name.startswith("this."):
                        if i.symbol_type == "variable" and "private" not in i.scope:
                            # print("YOYOYOYO",symbol_table.current)
                            for j in fieldVariables:
                                newj = j
                                if j[-1] == "]":
                                    newj = j[: j.find("[")]
                                symbol_table.add_symbol(VariableSymbol(newj + "." + i.name, i.data_type, 0, 0, i.scope, i.dims, i.dimArr))
                        # elif i.symbol_type == "method":
                        #     print("YOYOYOYO",symbol_table.current)
                        #     for j in fieldVariables:
                        #         newj = j
                        #         if j[-1] == "]":
                        #             newj = j[: j.find("[")]
                        #         symbol_table.add_symbol(MethodSymbol(j+"."+i.name, i.signature, i.params, i.return_type, "_DUMMY_", i.scope, i.throws))
                        # print("TTTTTtemp", i)

        case "Block":
            block_count += 1
            previous_block_count = block_count
            symbol_table.add_symbol(BlockSymbol("block" + str(block_count), symbol_table.current))
            symbol_table.enter_scope("block" + str(block_count))
            offset = offset + [0]
            traverse_tree(tree[2])
            symbol_table.exit_scope()
            offset.pop()

        case "ForStatement":
            block_count += 1
            previous_block_count = block_count
            symbol_table.add_symbol(BlockSymbol("block" + str(block_count), symbol_table.current))
            symbol_table.enter_scope("block" + str(block_count))
            offset = offset + [0]
            traverse_tree(tree[3])
            traverse_tree(tree[5])
            traverse_tree(tree[7])
            if tree[9][1][0] == "StatementWithoutTrailingSubstatement" and tree[9][1][1][0] == "Block":
                traverse_tree(tree[9][1][1][2])
            else:
                traverse_tree(tree[9])
            symbol_table.exit_scope()
            offset.pop()

        case "ForStatementNoShortIf":
            block_count += 1
            previous_block_count = block_count
            symbol_table.add_symbol(BlockSymbol("block" + str(block_count), symbol_table.current))
            symbol_table.enter_scope("block" + str(block_count))
            offset = offset + [0]
            traverse_tree(tree[3])
            traverse_tree(tree[5])
            traverse_tree(tree[7])
            if tree[9][1][0] == "StatementWithoutTrailingSubstatement" and tree[9][1][1][0] == "Block":
                traverse_tree(tree[9][1][1][2])
            else:
                traverse_tree(tree[9])
            symbol_table.exit_scope()
            offset.pop()

        case "SwitchBlock":
            block_count += 1
            previous_block_count = block_count
            symbol_table.add_symbol(BlockSymbol("switch_block" + str(block_count), symbol_table.current))
            symbol_table.enter_scope("switch_block" + str(block_count))
            offset = offset + [0]
            traverse_tree(tree[2])
            traverse_tree(tree[3])
            symbol_table.exit_scope()
            offset.pop()
        case _:
            if type(tree) == tuple:
                for i in range(1, len(tree)):
                    traverse_tree(tree[i])


def initial_Traverse(tree):
    global offset
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
            offset = offset + [0]
            symbol_table.add_symbol(VariableSymbol("this", className, 8, 0, [], 0, []))
            offset[-1] = offset[-1] + 8
            initial_Traverse(tree[6])
            symbol_table.exit_scope()
            offset.pop()

        case "InterfaceDeclaration":
            interfaceName = tree[3]
            symbol_table.enter_scope(interfaceName)
            initial_Traverse(tree[5])
            symbol_table.exit_scope()

        case "FieldDeclaration":
            # print("AAAAAAAAAAAAAAA", tree)
            fieldModifiers = get_Modifiers(tree[1])
            fieldType = get_Type(tree[2])
            dims = 0
            if fieldType[-1] == "]":
                dims = fieldType.count("[")
                fieldType = fieldType[: fieldType.find("[")]
            typeSize = get_TypeSize(fieldType)
            fieldVariables = get_Variables(tree[3])
            variablesizes = get_NumberOfElements(tree[3])
            arraydimensions = get_ArrayDimensions(tree[3])
            # print("BAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA", fieldVariables, variablesizes, arraydimensions, tree[2])
            count = 0
            for i in fieldVariables:
                newi = i
                tempdims = dims + i.count("[")
                if i[-1] == "]":
                    newi = i[: i.find("[")]
                symbol_table.add_symbol(
                    VariableSymbol(newi, fieldType, typeSize * variablesizes[count], offset[-1], fieldModifiers, tempdims, arraydimensions[count])
                )
                symbol_table.add_symbol(VariableSymbol("this." + newi, fieldType, 0, 0, fieldModifiers, dims, arraydimensions[count]))
                offset[-1] = offset[-1] + typeSize * variablesizes[count]
                count += 1
            symbol_table.current.parent.get_symbol(symbol_table.current.name.split(" ")[0]).size = offset[-1]
            post_type_check(tree)
            normalTypes = ["int", "char", "boolean", "float", "double", "long", "short", "byte", "String"]
            if fieldType not in normalTypes:
                for i in symbol_table.root.get_symbol(fieldType).symbol_table.symbols.values():
                    if not i.name.startswith("this."):
                        if i.symbol_type == "variable" and "private" not in i.scope:
                            # print("YOYOYOYO",symbol_table.current)
                            for j in fieldVariables:
                                newj = j
                                if j[-1] == "]":
                                    newj = j[: j.find("[")]
                                symbol_table.add_symbol(VariableSymbol(j + "." + i.name, i.data_type, 0, 0, i.scope, i.dims, i.dimArr))

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
                methodSignature += i[0].split("[")[0] + ","
                methodParamTypes.append(i[0].split("[")[0])
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
                constructorSignature += i[0].split("[")[0] + ","
                constructorParamTypes.append(i[0].split("[")[0])
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
            symbol_table.add_symbol(ClassSymbol(className, symbol_table.current, 0, classModifiers, classParent, classInterfaces))

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
        case "FieldDeclaration":
            post_type_check(expression[3])
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

        if (
            methodInvocationName == "System.out.println"
            or methodInvocationName == "println"
            or methodInvocationName == "System.out.print"
            or methodInvocationName == "print"
        ):
            pass
        else:
            methodcalledtype = symbol_table.get_symbol(methodInvocationName)
            methodInvocationParams = []
            newtree = expression[3]
            # print("AAAAAAAAAAAAA", newtree[1])
            if newtree[1][0] == "":
                methodInvocationParams = []
                # print("BBBBBBBAAAAAAAAAAAAA", methodInvocationName)
            else:
                newtree = newtree[1]
                while len(newtree) == 4:
                    methodInvocationParams.append(get_expression_Type(newtree[3]))
                    newtree = newtree[1]
                methodInvocationParams.append(get_expression_Type(newtree[1]))
                methodInvocationParams.reverse()
            arr = methodcalledtype.params
            if len(methodInvocationParams) != len(arr):
                raise Exception(
                    "Error: Method Invocation Parameters of {} don't match the method declaration".format(methodInvocationName)
                )
            else:
                for i in range(len(methodInvocationParams)):
                    big_method(methodInvocationParams[i], arr[i])

    elif len(expression) == 7:
        pass


def constructor_check(expression):
    pass

    # methodInvocationName = get_expression_Type(expression[2])
    # methodcalledtype = symbol_table.get_symbol_name(methodInvocationName)
    # methodInvocationParams = []
    # newtree = expression[4]
    # if newtree[1] == "":
    #     methodInvocationParams = []
    # else:
    #     newtree = newtree[1]
    #     while len(newtree) == 4:
    #         methodInvocationParams.append(get_expression_Type(newtree[3]))
    #         newtree = newtree[1]
    #         methodInvocationParams.append(get_expression_Type(newtree[1]))
    #         methodInvocationParams.reverse()
    #     arr = methodcalledtype.params
    #     if len(methodInvocationParams) != len(arr):
    #         raise Exception("Error: Invocation parameters don't match the declaration")
    #     else:
    #         for i in range(len(methodInvocationParams)):
    #             big_method(methodInvocationParams[i], arr[i])


def get_expression_Type(expression):
    # print("YYYYYYYYYYYY", expression[0])
    match expression[0]:
        case "LeftHandSide":
            return get_expression_Type(expression[1])
        case "FieldAccess":
            # print("AAAAAAAAAAAAAAAAAA",expression)
            return symbol_table.get_symbol(get_Name(expression)).data_type
        case "NameDotIdentifierId":
            return symbol_table.get_symbol(get_Name(expression)).data_type

        case "ArrayAccess":
            t = get_expression_Type(expression[3])
            if t != "int":
                raise Exception("Array index must be of type int instead recieved {}".format(t))
            if expression[1][0] == "Name":
                return symbol_table.get_symbol(get_Name(expression[1])).data_type
            else:
                return get_expression_Type(expression[1])

        case "ArrayCreationExpression":
            return get_Type(expression[2])

        case "ClassInstanceCreationExpression":
            constructor_check(expression)
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
            if len(expression) == 4:
                operator = expression[2]
                left = get_expression_Type(expression[1])
                right = get_expression_Type(expression[3])
                binop_type_check(left, operator, right, expression[0])
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
            operator = expression[1]
            right = get_expression_Type(expression[2])
            unop_type_check(operator, right, expression[0])
            return get_expression_Type(expression[2])
        case "PreDecrementExpression":
            operator = expression[1]
            right = get_expression_Type(expression[2])
            unop_type_check(operator, right, expression[0])
            return get_expression_Type(expression[2])
        case "UnaryExpressionNotPlusMinus":
            if len(expression) == 3:
                operator = expression[1]
                right = get_expression_Type(expression[2])
                unop_type_check(operator, right, expression[0])
                return get_expression_Type(expression[2])
            else:
                return get_expression_Type(expression[1])
        case "PostfixExpression":
            return get_expression_Type(expression[1])
        case "PostIncrementExpression":
            operator = expression[2]
            left = get_expression_Type(expression[1])
            unop_type_check(operator, left, expression[0])
            return get_expression_Type(expression[1])
        case "PostDecrementExpression":
            return get_expression_Type(expression[1])
        case "CastExpression":
            return get_Type(expression[2])
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
        case "MethodInvocation":
            method_check(expression)
            if len(expression) == 5:
                methodInvocationName = get_Name(expression[1])
                if methodInvocationName == "System.out.println":
                    pass
                else:
                    return symbol_table.get_symbol(methodInvocationName).return_type
            elif len(expression) == 7:
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
        case "ArrayInitializer":
            return get_expression_Type(expression[2])
        case "BetaAlphaVariableInitializer":
            return get_expression_Type(expression[1])
        case "AlphaVariableInitializer":
            if len(expression) == 2:
                return get_expression_Type(expression[1])
            else:
                t1 = get_expression_Type(expression[1])
                t2 = get_expression_Type(expression[3])
                return big(t1, t2)

        case _:
            pass


def generate_tac(tree, begin="", end=""):
    global block_count
    global tac
    match tree[0]:
        case "VariableDeclarator":
            if symbol_table.get_symbol(get_Name(tree[1]).split("[")[0]).dims > 0 or symbol_table.get_symbol(get_Name(tree[1]).split("[")[0]).data_type not in ["int", "float", "boolean", "char", "short", "long", "double", "byte"]:
                size = 8
            else:
                size = get_TypeSize(symbol_table.get_symbol(get_Name(tree[1]).split("[")[0]).data_type)
            tac.alloc_stack(size)
            if len(tree) == 4:
                # print("#"*100, symbol_table.current.name)
                right = generate_tac(tree[3])
                left = symbol_table.get_symbol_name(get_Name(tree[1]).split("[")[0])
                tac.add3("=", right, left)
                return
        case "VariableInitializer":
            return generate_tac(tree[1])
        case "Expression":
            return generate_tac(tree[1])
        case "ArrayInitializer":
            pass # Removed from basic feature
        case "AssignmentExpression":
            return generate_tac(tree[1])
        case "Assignment":
            if symbol_table.get_symbol(get_Name(tree[1])).dims > 0:
                name = get_Name(tree[1])
                dimensions = symbol_table.get_symbol(name).dimArr
                indices = get_Indices(tree[1])
                sym_type = symbol_table.get_symbol(name).data_type
                size = get_TypeSize(sym_type)
                y = tac.new_temp()
                tac.add3("=", 0, y)
                x = tac.new_temp()
                for i in range(len(dimensions)):
                    for j in range(i+1, len(dimensions)):
                        tac.add("*", indices[i], dimensions[j], x)
                        tac.add("+", x, y, y)
                tac.add("*", y, size, y)
                tac.add("+", symbol_table.get_symbol_name(name), y, y)
                right = generate_tac(tree[3])
                tac.add3(tree[2][1], right, "("+y+")")
                # print("XXXXXXXXXXXXXXXXXXX",name,dimensions,indices,symbol_table.get_symbol(name).data_type,size)
                return y
            elif "." in get_Name(tree[1]):
                # Non array access case (field access)
                base, comp = get_Name(tree[1]).split(".")
                sym = symbol_table.get_symbol(base)
                offset = sym.offset
                stype = sym.data_type
                symtable = symbol_table.root.get_symbol(stype)
                offset += symtable.symbol_table.symbols[comp].offset
                right = generate_tac(tree[3])
                left = symbol_table.get_symbol_name(get_Name(tree[1])).split(".")[0] + f"({offset})"
                tac.add3(tree[2][1], right, left)
                return left
            else:
                # Non array field access
                left = symbol_table.get_symbol_name(get_Name(tree[1]))
                right = generate_tac(tree[3])
                tac.add3(tree[2][1], right, left)
                return left
        case "ConditionalExpression":
            if len(tree) == 2:
                return generate_tac(tree[1])
            else:
                pass
                # raise Exception("Conditional Expression not supported")
        case "ConditionalOrExpression":
            if len(tree) == 2:
                return generate_tac(tree[1])
            else:
                out = tac.new_temp()
                left = generate_tac(tree[1])
                right = generate_tac(tree[3])
                tac.add("||", left, right, out)
                return out
        case "ConditionalAndExpression":
            if len(tree) == 2:
                return generate_tac(tree[1])
            else:
                out = tac.new_temp()
                left = generate_tac(tree[1])
                right = generate_tac(tree[3])
                tac.add("&&", left, right, out)
                return out
        case "InclusiveOrExpression":
            if len(tree) == 2:
                return generate_tac(tree[1])
            else:
                out = tac.new_temp()
                left = generate_tac(tree[1])
                right = generate_tac(tree[3])
                tac.add("|", left, right, out)
                return out
        case "ExclusiveOrExpression":
            if len(tree) == 2:
                return generate_tac(tree[1])
            else:
                out = tac.new_temp()
                left = generate_tac(tree[1])
                right = generate_tac(tree[3])
                tac.add("^", left, right, out)
                return out
        case "AndExpression":
            if len(tree) == 2:
                return generate_tac(tree[1])
            else:
                out = tac.new_temp()
                left = generate_tac(tree[1])
                right = generate_tac(tree[3])
                tac.add("&", left, right, out)
                return out
        case "EqualityExpression":
            if len(tree) == 2:
                return generate_tac(tree[1])
            else:
                out = tac.new_temp()
                left = generate_tac(tree[1])
                right = generate_tac(tree[3])
                tac.add(tree[2], left, right, out)
                return out
        case "RelationalExpression":
            if len(tree) == 2:
                return generate_tac(tree[1])
            else:
                out = tac.new_temp()
                left = generate_tac(tree[1])
                right = generate_tac(tree[3])
                tac.add(tree[2], left, right, out)
                if tree[2] == "instanceof":
                    raise Exception("instanceof not supported")
                return out
        case "ShiftExpression":
            if len(tree) == 2:
                return generate_tac(tree[1])
            else:
                out = tac.new_temp()
                left = generate_tac(tree[1])
                right = generate_tac(tree[3])
                tac.add(tree[2], left, right, out)
                return out
        case "AdditiveExpression":
            if len(tree) == 2:
                return generate_tac(tree[1])
            else:
                out = tac.new_temp()
                left = generate_tac(tree[1])
                right = generate_tac(tree[3])
                tac.add(tree[2], left, right, out)
                return out
        case "MultiplicativeExpression":
            if len(tree) == 2:
                return generate_tac(tree[1])
            else:
                out = tac.new_temp()
                left = generate_tac(tree[1])
                right = generate_tac(tree[3])
                tac.add(tree[2], left, right, out)
                return out
        case "UnaryExpression":
            if len(tree) == 2:
                return generate_tac(tree[1])
            else:
                out = tac.new_temp()
                right = generate_tac(tree[2])
                tac.add3(tree[1], right, out)
                return out
        case "PreIncrementExpression":
            out = tac.new_temp()
            right = generate_tac(tree[2])
            tac.add("+", right, "1", right)
            tac.add3("=", right, out)
            return out
        case "PreDecrementExpression":
            out = tac.new_temp()
            right = generate_tac(tree[2])
            tac.add("-", right, "1", right)
            tac.add3("=", right, out)
            return out
        case "UnaryExpressionNotPlusMinus":
            if len(tree) == 2:
                return generate_tac(tree[1])
            else:
                out = tac.new_temp()
                right = generate_tac(tree[2])
                tac.add3(tree[1], right, out)
                return out
        case "PostfixExpression":
            return generate_tac(tree[1])
        case "Primary":
            return generate_tac(tree[1])
        case "PrimaryNoNewArray":
            if len(tree) == 4:
                return generate_tac(tree[2])
            return generate_tac(tree[1])
        case "Literal":
            return tree[1]
        case "ClassInstanceCreationExpression":
            out = tac.new_temp()
            args = get_Argument_list(tree[4])
            classname = get_Name(tree[2])
            sym = symbol_table.root.get_symbol(classname)
            tac.alloc_mem(sym.size, out)
            try: 
                argtype = sym.symbol_table.symbols[classname].params
                if args is not None:
                    args.reverse()
                    argtype.reverse()
                    for i in range(len(args)):
                        tac.push_param(args[i], get_TypeSize(argtype[i]))
                tac.push_param(out)
                tac.add_call(f"{classname}_{classname}", "__")
            except Exception as e:
                pass
            return out
        case "FieldAccess":
            try:
                sym = symbol_table.get_symbol(get_Name(tree[1][1]))
                var += "." + tree[3]
                return var 
            except Exception as e:
                pass
        case "ArrayAccess":
            name = get_Name(tree[1])
            dimensions = symbol_table.get_symbol(name).dimArr
            indices = get_Indices(tree)
            sym_type = symbol_table.get_symbol(name).data_type
            size = get_TypeSize(sym_type)
            y = tac.new_temp()
            tac.add3("=", 0, y)
            x = tac.new_temp()
            for i in range(len(dimensions)):
                for j in range(i+1, len(dimensions)):
                    tac.add("*", indices[i], dimensions[j], x)
                    tac.add("+", x, y, y)
            tac.add("*", y, size, y)
            tac.add("+", symbol_table.get_symbol_name(name), y, y)
            print("MEOWMEOWMEOWMEOWMEOW", name, dimensions, indices, sym_type, size)
            # var = generate_tac(tree[1])
            # index = generate_tac(tree[3])
            # out = tac.new_temp()
            # tac.add("[]", y, index, out)
            return y
        case "MethodInvocation":
            if len(tree) == 5:
                funcname = symbol_table.get_symbol_name(get_Name(tree[1]))
                out = tac.new_temp()
                args = get_Argument_list(tree[3])
                sym = symbol_table.get_symbol(get_Name(tree[1]))
                try:
                    argtype = sym.params
                    if args is not None:
                        args.reverse()
                        argtype.reverse()
                        for i in range(len(args)):
                            tac.push_param(args[i], get_TypeSize(argtype[i]))
                    tac.push_param("this")
                    tac.add_call(funcname, out)
                except Exception as e:
                    # print("#"*10,e)
                    pass
                return out
            if len(tree) == 7:
                funcname = symbol_table.get_symbol_name(get_Name(tree[1]))
                funcname += "." + get_Name(tree[3])
                out = tac.new_temp()
                args = get_Argument_list(tree[5])
                sym = symbol_table.get_symbol(get_Name(tree[1]))
                try:
                    argtype = sym.params
                    if args is not None:
                        args.reverse()
                        argtype.reverse()
                        for i in range(len(args)):
                            tac.push_param(args[i], get_TypeSize(argtype[i]))
                    tac.push_param("this")
                    tac.add_call(funcname, out)
                except Exception as e:
                    # print(e)
                    pass
                return out
        case "ArrayCreationExpression":
            x = tac.new_temp()
            nelem = get_NumberOfElements(tree)
            sym_type = get_Type(tree[2])
            size = get_TypeSize(sym_type)
            tac.alloc_mem(size*get_NumberOfElements(tree), x)
            return x
        case "CastExpression":
            if tree[2][0] != "PrimitiveType":
                raise Exception("CastExpression only supported with PrimitiveType, recieved {}".format(tree[2][0]))
            ctype = get_Type(tree[2])
            out = tac.new_temp()
            right = generate_tac(tree[5])
            tac.add3("cast_to_" + ctype, right, out)
            return out
        case "Name":
            try:
                gname = get_Name(tree[1])
                if "." in gname:
                    base, comp = gname.split(".")
                    sym = symbol_table.get_symbol(base)
                    offset = sym.offset
                    stype = sym.data_type
                    symtable = symbol_table.root.get_symbol(stype)
                    offset += symtable.symbol_table.symbols[comp].offset
                    left = symbol_table.get_symbol_name(get_Name(tree[1])).split(".")[0] + f"({offset})"
                    return left
                return symbol_table.get_symbol_name(gname)
            except:
                return
        case "PostIncrementExpression":
            out = tac.new_temp()
            right = generate_tac(tree[1])
            tac.add3("=", right, out)
            tac.add("+", right, "1", right)
            return out
        case "PostDecrementExpression":
            out = tac.new_temp()
            right = generate_tac(tree[1])
            tac.add3("=", right, out)
            tac.add("-", right, "1", right)
            return out
        # case "Statement":
        #     if len(tree) == 2:
        #         return generate_tac(tree[1])
        case "ExpressionStatement":
            return generate_tac(tree[1])
        case "SwitchStatement":
            raise Exception("SwitchStatement not supported")
        case "StatementWithoutTrailingSubstatement":
            if tree[1][0] == "Block":
                return generate_tac(tree[1])
            return generate_tac(tree[1])
        case "ConstantExpression":
            return generate_tac(tree[1])
        case "DoStatement":
            begin_label = tac.gen_label()
            end_label = tac.gen_label()
            tac.add_label(begin_label)
            generate_tac(tree[2], begin=begin_label, end=end_label)
            cond = generate_tac(tree[5])
            tac.cond_jump(cond, begin_label)
            tac.add_label(end_label)
        case "IfThenElseStatementNoShortIf":
            cond = generate_tac(tree[3])
            notcond = tac.new_temp()
            tac.add3("!", cond, notcond)
            else_label = tac.gen_label()
            tac.cond_jump(notcond, else_label)
            generate_tac(tree[5])
            tac.add_label(else_label)
        case "WhileStatementNoShortIf":
            begin_label = tac.gen_label()
            end_label = tac.gen_label()
            tac.add_label(begin_label)
            cond = generate_tac(tree[3])
            out = tac.new_temp()
            tac.add3("!", cond, out)
            tac.cond_jump(out, end_label)
            generate_tac(tree[5], begin=begin_label, end=end_label)
            tac.jump(begin_label)
            tac.add_label(end_label)
        case "ForStatementNoShortIf":
            generate_tac(tree[3])
            begin_label = tac.gen_label()
            end_label = tac.gen_label()
            tac.add_label(begin_label)
            cond = generate_tac(tree[5])
            out = tac.new_temp()
            tac.add3("!", cond, out)
            tac.cond_jump(out, end_label)
            generate_tac(tree[7], begin=begin_label, end=end_label)
            generate_tac(tree[9])
            tac.jump(begin_label)
            tac.add_label(end_label)
        case "IfThenStatement":
            cond = generate_tac(tree[3])
            end_label = tac.gen_label()
            notcond = tac.new_temp()
            tac.add3("!", cond, notcond)
            tac.cond_jump(notcond, end_label)
            generate_tac(tree[5])
            tac.add_label(end_label)
        case "IfThenElseStatement":
            cond = generate_tac(tree[3])
            then_label = tac.gen_label()
            else_label = tac.gen_label()
            end_label = tac.gen_label()
            tac.cond_jump(cond, then_label)
            tac.jump(else_label)
            tac.add_label(then_label)
            generate_tac(tree[5], begin=then_label, end=end_label)
            tac.jump(end_label)
            tac.add_label(else_label)
            generate_tac(tree[7], begin=else_label, end=end_label)
            tac.jump(end_label)
            tac.add_label(end_label)
        case "WhileStatement":
            begin_label = tac.gen_label()
            end_label = tac.gen_label()
            tac.add_label(begin_label)
            cond = generate_tac(tree[3])
            notcond = tac.new_temp()
            tac.add3("!", cond, notcond)
            tac.cond_jump(notcond, end_label)
            generate_tac(tree[5], begin=begin_label, end=end_label)
            tac.jump(begin_label)
            tac.add_label(end_label)
        case "ForStatement":
            block_count += 1
            symbol_table.enter_scope("block" + str(block_count))
            generate_tac(tree[3])
            begin_label = tac.gen_label()
            end_label = tac.gen_label()
            tac.add_label(begin_label)
            cond = generate_tac(tree[5])
            out = tac.new_temp()
            tac.add3("!", cond, out)
            tac.cond_jump(out, end_label)
            generate_tac(tree[7], begin=begin_label, end=end_label)
            print(symbol_table.current.name)
            try:
                generate_tac(tree[9][1][1][1])
            except:
                pass
            tac.jump(begin_label)
            tac.add_label(end_label)
            symbol_table.exit_scope()
        case "ForStatementNoShortIf":
            block_count += 1
            symbol_table.enter_scope("block" + str(block_count))
            generate_tac(tree[3])
            begin_label = tac.gen_label()
            end_label = tac.gen_label()
            tac.add_label(begin_label)
            cond = generate_tac(tree[5])
            out = tac.new_temp()
            tac.add3("!", cond, out)
            tac.cond_jump(out, end_label)
            generate_tac(tree[7], begin=begin_label, end=end_label)
            try:
                generate_tac(tree[9][1][1][1])
            except:
                pass
            tac.jump(begin_label)
            tac.add_label(end_label)
            if tree[9][1][0] == "StatementWithoutTrailingSubstatement" and tree[9][1][1][0] == "Block":
                generate_tac(tree[9][1][1][2])
            else:
                generate_tac(tree[9])
            symbol_table.exit_scope()
        case "StatementNoShortIf":
            return generate_tac(tree[1])
        case "BreakStatement":
            tac.jump(end)
        case "ContinueStatement":
            tac.jump(begin)
        case "ReturnStatement":
            if len(tree) == 4:
                out = generate_tac(tree[2])
                tac.add_return(out)
        case "BetaExpression":
            return generate_tac(tree[1])
        case "ClassDeclaration":
            className = tree[3]
            symbol_table.enter_scope(className)
            tac.add_label(className)
            generate_tac(tree[6])
            symbol_table.exit_scope()
        case "MethodDeclaration":
            methodName = get_Name(tree[1][3])
            methodParams = []
            if len(tree[1][3]) == 5:
                methodParams = get_Parameters(tree[1][3][3])
            method_sym_name = symbol_table.get_symbol_name(methodName)
            tac.add_label(method_sym_name)
            symbol_table.enter_scope(methodName)
            for i in methodParams:
                tac.pop_param(symbol_table.get_symbol_name(i[1].split("[")[0]))
            generate_tac(tree[2][1][2])
            symbol_table.exit_scope()
        case "ConstructorDeclaration":
            constructorName = get_Name(tree[2][1])
            constructorParams = get_Parameters(tree[2][3])
            tac.add_label(symbol_table.get_symbol_name(constructorName))
            symbol_table.enter_scope(constructorName)
            for i in constructorParams:
                tac.pop_param(symbol_table.get_symbol_name(i[1]))
            generate_tac(tree[4])
            symbol_table.exit_scope()
        case "Block":
            block_count += 1
            previous_block_count = block_count
            symbol_table.enter_scope("block" + str(block_count))
            generate_tac(tree[2])
            symbol_table.exit_scope()
        case _:
            if type(tree) == tuple:
                for i in range(1, len(tree)):
                    generate_tac(tree[i])


def get_Argument_list(tree):
    match tree[0]:
        case "BetaArgumentList":
            return get_Argument_list(tree[1])
        case "empty":
            return []
        case "ArgumentList":
            if len(tree) == 2:
                out = generate_tac(tree[1])
                return [out]
            else:
                return get_Argument_list(tree[1]) + [generate_tac(tree[3])]


def get_TypeSize(type):
    if type == "int":
        return 4
    elif type == "boolean":
        return 1
    elif type == "char":
        return 1
    elif type == "byte":
        return 1
    elif type == "short":
        return 2
    elif type == "long":
        return 8
    elif type == "float":
        return 4
    elif type == "double":
        return 8
    elif type == "String":
        return 8
    else:
        return symbol_table.root.get_symbol(type).size
    
def get_ArrayDimensions(tree):
    # print("YOOOOOOOOO",tree[0])
    match tree[0]:
        case "AlphaVariableDeclarator":
            if len(tree) == 2:
                return [get_ArrayDimensions(tree[1])]
            else:
                return get_ArrayDimensions(tree[1]) + [get_ArrayDimensions(tree[3])]
        case "VariableDeclarator":
            if len(tree) == 2:
                if len(tree[1]) == 2:
                    return []
                else:
                    return []
            else:
                return get_ArrayDimensions(tree[3])
        case "VariableInitializer":
            return get_ArrayDimensions(tree[1])
        case "Expression":
            return get_ArrayDimensions(tree[1])
        case "ArrayCreationExpression":
            return get_ArrayDimensions(tree[3]) + get_ArrayDimensions(tree[4])
        case "BetaAlphaDim":
            if tree[1][0] == "":
                return []
            else:
                return get_ArrayDimensions(tree[1])
        case "AlphaDim":
            if len(tree) == 4:
                return get_ArrayDimensions(tree[1]) + [1]
            else:
                return [1]
        case "AlphaDimExpr":
            # print("BLABLABLA",tree)
            if len(tree) == 3:
                return get_ArrayDimensions(tree[1]) + [get_LiteralValue2(tree[2])]
            else:
                return [get_LiteralValue2(tree[1])]
        case "DimExpr":
            return get_ArrayDimensions(tree[2])
        case "Literal":
            return []
        case "ArrayInitializer":
            return get_ArrayDimensions(tree[2])
        case "BetaAlphaVariableInitializer":
            if tree[1] == "":
                return 0
            else:
                return get_ArrayDimensions(tree[1])
        case "AlphaVariableInitializer":
            if len(tree) == 2:
                return get_ArrayDimensions(tree[1])
            else:
                return get_ArrayDimensions(tree[1]) + get_ArrayDimensions(tree[3])
        case _:
            if len(tree) == 2:
                return get_ArrayDimensions(tree[1])
            else:
                return []

def get_LiteralValue2(tree):
    # print("NOOOOOOOOO",tree[0])
    match tree[0]:
        case "DimExpr":
            return get_LiteralValue2(tree[2])
        case "Literal":
            return int(tree[1])
        case "IdentifierId":
            return symbol_table.get_symbol_name(tree[1])
        case _:
            if len(tree) == 2:
                return get_LiteralValue2(tree[1])
            else:
                return 1
            
def get_Indices(tree):
    match tree[0]:
        case "LeftHandSide":
            return get_Indices(tree[1])
        case "ArrayAccess":
            return get_Indices(tree[1]) + [get_LiteralValue2(tree[3])]
        case "Name":
            return []
        case "PrimaryNoNewArray":
            return get_Indices(tree[1])
